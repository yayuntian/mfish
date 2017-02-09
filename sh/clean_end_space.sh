#!/bin/sh

find ./ -name *.c| xargs sed -i 's/ *$//'
find ./ -name *.h| xargs sed -i 's/ *$//'
