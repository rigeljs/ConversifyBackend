# -*- coding: utf-8 -*-

"""
Chat Server
===========

This simple application uses WebSockets to run a primitive chat server.
"""

import os
import logging
import redis
import gevent
from flask import Flask, render_template
from flask_sockets import Sockets

REDIS_URL = os.environ['REDISCLOUD_URL']
REDIS_CHAN = 'chat'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)


clients = []
@app.route('/')
def hello():
    return render_template('index.html')

@sockets.route('/broadcast')
def broadcast(ws):
    clients.append(ws)
    #chats.register(ws)
    while ws.socket is not None:
        #sleeps
        gevent.sleep(0.1)
        message = ws.receive()
        print message
        if message:
            app.logger.info(u'Inserting message: {}')
            redis.publish(REDIS_CHAN, message)
            for client in clients:
                try:
                    client.send(message)
                except Exception:
                    print Exception
                    clients.remove(client)


@sockets.route('/intimate')
def intimate(ws):
	while ws.socket is not None:
		gevent.sleep(0.1)
		message = ws.receive()
		if message:
			ws.send(message)