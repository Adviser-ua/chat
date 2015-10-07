# coding=UTF-8
# script create by Konstantyn Davidenko
# mail: kostya_ya@it-transit.com
#

"""
start local developer server
"""

from chat import app

ip = '0.0.0.0'
port = 80
app.run(ip, port)