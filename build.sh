#!/bin/bash

version=$(cat sendmail.py | grep "VERSION = " | sed 's/.*\"\(.*\)\".*/\1/g')
rm -rf build/sendmail-$version &&
mkdir -p build/sendmail-$version &&
cp sendmail.py install.sh build/sendmail-$version &&
tar -zcvf build/sendmail-$version.tar.gz -C build sendmail-$version