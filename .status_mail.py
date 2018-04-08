#!/usr/bin/env python

'''
Script to gather system statistics then send to an email address
Author: GaDayas
Version: 0.1  12 October 2017
'''

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import time

from plumbum import local
from plumbum.cmd import cat, tail, head, uptime, cut, df, who
from plumbum import colors


time = time.strftime("%H:%M:%S %A %d %b %Y")
up = local["uptime"] | cut["-c", "-28"]
who = local["who"] | cut["-c", "-38"]
mem = cat["/proc/meminfo"] | head[-3]
space = df["-h"] | cut["-c", "-37"]
chain = cat["/var/log/auth.log"] | tail[-5] | cut["-c", "-65"]

fromaddr = "yoursendingaddress@gmail.com"
toaddr = "yourrecievingemailaddress@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "DAILY UPDATE: " + str(time)

body = "Time / Date: " + str(time) + "\nMACHINE STATISTICS:\n\n" \
        + "UPTIME:\n" + str(up()) + "\n" \
        + "LOGGED ON USERS:\n" + str(who()) + "\n" \
        + "MEMORY:" "\n" + str(mem()) + '\n'       \
        + "DRIVE SPACE:\n" + str(space()) + "\n"  \
        + "AUTH-LOG:\n" + str(chain())

msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "sendingemailpassword")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
