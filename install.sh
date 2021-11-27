#!/bin/bash

INSTALL_PATH="/usr/local/sendmail"
BIN_PATH="/usr/local/bin/sendmail"

uninstall() {
  rm -rf $INSTALL_PATH
  rm -rf $BIN_PATH
}

install() {
  mkdir -p $INSTALL_PATH &&
  echo -e "[mail]\nhost=\nuser=\npass=" > $INSTALL_PATH/config.ini &&
  cp sendmail.py $INSTALL_PATH &&
  chmod +x $INSTALL_PATH/sendmail.py &&
  rm -rf $BIN_PATH &&
  ln -s $INSTALL_PATH/sendmail.py $BIN_PATH

  if [ $? != 0 ]; then
      uninstall
  fi
}

while getopts ':r' OPT; do
    case $OPT in
        r)
            uninstall;exit 0;;
        ?)
            echo "Usage: $(basename $0) [-r]";exit 0;
    esac
done

shift $((OPTIND - 1))

install