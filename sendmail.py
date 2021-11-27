#!/usr/bin/env python3

import argparse
import configparser
import os.path
import smtplib
import sys
import platform
import html
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if platform.system() != "Windows":
    import fcntl

VERSION = "1.0.0"

mail_config = {}


def read_content_from_stdin(args):
    if platform.system() == "Windows":
        return

    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)
    try:
        content_from_stdin = sys.stdin.read()
        args.content = content_from_stdin
    except TypeError:
        # No content from stdin, ignore it.
        pass


def process_args(args):
    if len(args.to) == 0:
        raise Exception("To address can't be empty.")

    if args.from_address is None:
        args.from_address = mail_config["user"]

    read_content_from_stdin(args)

    if not args.noescape:
        args.content = escape_html(args)


def escape_html(args):
    return html.escape(args.content).replace("\n", "<br>").replace(" ", "&nbsp;")


def create_message(args):
    message = MIMEMultipart()
    message["Subject"] = Header(args.subject, "utf-8")
    message["From"] = args.from_address
    message["To"] = ", ".join(args.to)
    add_header_cc(args, message)

    message.attach(MIMEText(args.content, "html", "utf-8"))
    add_attachments(args, message)
    return message


def add_header_cc(args, message):
    if args.cc is not None and len(args.cc) != 0:
        message["Cc"] = ", ".join(args.cc)


def send(args):
    send_mail(args, create_message(args))


def send_mail(args, message):
    smtp = smtplib.SMTP_SSL(mail_config["host"])
    smtp.login(mail_config["user"], mail_config["pass"])
    smtp.sendmail(mail_config["user"], get_to_addrs(args), message.as_string())
    smtp.quit()


def add_attachments(args, message):
    if args.attachment is None:
        return
    for attachment in args.attachment:
        if not os.path.exists(attachment):
            raise Exception("No such file " + attachment)
        if not os.path.isfile(attachment):
            raise Exception(attachment + " is not a file")
        with open(attachment, "rb") as file:
            part = MIMEApplication(file.read())
            part.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment))
        message.attach(part)


def get_to_addrs(args):
    addrs = args.to
    if args.cc is not None:
        addrs += args.cc
    if args.bcc is not None:
        addrs += args.bcc
    return addrs


def parse_args():
    parser = argparse.ArgumentParser(prog="sendmail", description="Send mail by SMTP.")
    parser.add_argument("--config", help="The config path, default is /usr/local/sendmail/config.ini",
                        default="/usr/local/sendmail/config.ini")
    parser.add_argument("-t", "--to", action="append", help="To address of mail", required=True)
    parser.add_argument("-c", "--cc", action="append", help="Cc address of mail")
    parser.add_argument("--bcc", action="append", help="Bcc address of mail")
    parser.add_argument("-s", "--subject", help="The subject of mail", required=True)
    parser.add_argument("-a", "--attachment", action="append", help="Add attachment to mail")
    parser.add_argument("--from", dest="from_address", help="From address of mail, default is mail.user")
    parser.add_argument("--noescape", action="store_true", help="Don't escape content to html")
    parser.add_argument("--host", help="The host of mail")
    parser.add_argument("--user", help="The username of mail")
    parser.add_argument("--pass", dest="password", help="The password of mail")
    parser.add_argument("-v", "--version", action="store_true", help="Print sendmail version")
    parser.add_argument("content", nargs="?", default="No content", help="The content of mail")
    return parser.parse_args()


def parse_config(path):
    global mail_config

    if os.path.exists(path):
        config = configparser.ConfigParser()
        config.read(path, encoding="utf-8")

        if "mail" in config.sections():
            mail_config = config["mail"]
    else:
        raise Exception("Config path not found " + path)

    if args.host is not None:
        mail_config["host"] = args.host
    if args.user is not None:
        mail_config["user"] = args.user
    if args.password is not None:
        mail_config["pass"] = args.password

    if not mail_config.get("host"):
        raise Exception("Please configure mail.host")

    if not mail_config.get("user"):
        raise Exception("Please configure mail.user")

    if not mail_config.get("pass"):
        raise Exception("Please configure mail.pass")


def show_version():
    if len(sys.argv) > 1 and (sys.argv[1] == "-v" or sys.argv[1] == "--version"):
        print("sendmail v" + VERSION)
        exit(0)


if __name__ == '__main__':
    show_version()

    try:
        args = parse_args()
        parse_config(args.config)
        process_args(args)
        send(args)
    except Exception as e:
        print(e)
        exit(1)
