# sendmail
This is a tool for sending mail on linux.

# Usage
```bash
usage: sendmail [-h] [--config CONFIG] -t TO [-c CC] [--bcc BCC] -s SUBJECT [-a ATTACHMENT] [--from FROM_ADDRESS] [--noescape] [--host HOST] [--user USER] [--pass PASSWORD] [-v] [content]

Send mail by SMTP.

positional arguments:
  content               The content of mail

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       The config path, default is config.ini
  -t TO, --to TO        To address of mail
  -c CC, --cc CC        Cc address of mail
  --bcc BCC             Bcc address of mail
  -s SUBJECT, --subject SUBJECT
                        The subject of mail
  -a ATTACHMENT, --attachment ATTACHMENT
                        Add attachment to mail
  --from FROM_ADDRESS   From address of mail, default is mail.user
  --noescape            Don't escape content to html
  --host HOST           The host of mail
  --user USER           The username of mail
  --pass PASSWORD       The password of mail
  -v, --version         Print sendmail version
```

# Examples
```bash
sendmail -t xxxx@163.com -s "Test title" "Test content"

sendmail -t xxxx@163.com -t xxxx@gmail.com -s "Test title" "Test content"

sendmail -t xxxx@163.com -c xxxx@gmail.com "Test title" "Test content"

sendmail -t xxxx@163.com -s "Test title" -a file1 -a file2 "Test content"

ps aux | sendmail -t xxxx@163.com -s "Test title"

sendmail --config another_config.ini -t xxxx@163.com -s "Test title" "Test content"

sendmail --host smtp.xxx.com --user xxxx@163.com --pass xxxx -t xxxx@163.com -s "Test title" "Test content"
```

# Install
This tool is built with Python3, so you need to install `Python3.x` first.
```bash
tar -zxvf sendmail-1.0.0.tar.gz
cd sendmail-1.0.0
sudo ./install.sh
sudo vim /usr/local/sendmail/config.ini
```

## config.ini
This file stores your mail configuration.  
**Example:**
```conf
[mail]
host=smtp.163.com
user=xxxx@163.com
pass=xxxxxxx
```

# Uninstall
```bash
sudo ./install.sh -r
```
