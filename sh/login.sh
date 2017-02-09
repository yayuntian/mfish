#!/usr/bin/expect 
set timeout 30 
spawn ssh -l root 192.168.10.125
expect "password:" 
send "123456\r" 
interact 
