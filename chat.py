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
import json
import messages_dao
import conversation_dao

REDIS_URL = os.environ['REDISCLOUD_URL']
REDIS_CHAN = 'chat'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)


clients = {}

@app.route('/')
def hello():
    return render_template('index.html')

@sockets.route('/broadcast')
def broadcast(ws):
    while ws.socket is not None:
        gevent.sleep(0.1)
        message = ws.receive()
        print message
        if message:
            message_json = json.loads(message)
            if 'uid' in message_json:
                clients[message_json['uid']] = ws
                print "registering client"
                break
    while ws.socket is not None:
        #sleeps
        gevent.sleep(0.1)
        message = ws.receive()
        print message
        if message:
            print "inserting message"
            message_json = json.loads(message)
            if ('content' in message_json and
                'conversation_id' in message_json and
                'sender_id' in message_json):
                    affected_users = executeSendMessage(message_json)
                    for user in affected_users:
                        try:
                            if user in clients:
                                clients[user].send(message)
                        except Exception:
                            print Exception
                            del clients[user]

def executeSendMessage(message):
    messages_dao.addMessageToConversation(message["content"], 
                                          message["conversation_id"],
                                          message["sender_id"])
    return conversation_dao.getUsersOptedInToConversation(message["conversation_id"])

@sockets.route('/update')
def update(ws):
    while ws.socket is not None:
        gevent.sleep(0.1)
        message = ws.receive()
        if message:
            message_json = json.loads(message)
            result = translateAndFetch(message_json)
            print ",".join(result)
            ws.send('{"results": ["' + '","'.join( result) + '"]}')


def translateAndFetch(request):
    methodName = request["method"]
    arguments = request["arguments"]
    print request
    if methodName == "getMessagesInConversation":
        return getMessagesInConversation(arguments[0])
    if methodName == "getConversationsInGroup":
        return getConversationsInGroup(arguments[0],arguments[1])



def getMessagesInConversation(conversation_id):
    messageIds = messages_dao.getMessagesInConversation(conversation_id)
    messages = []
    for messageId in messageIds:
        messages.extend(messages_dao.getMessageTextById(messageId))
    return messages

def getConversationsInGroup(group_id, user_id):
    conversation_ids = conversation_dao.getConversationsInGroup(group_id)
    opted_in = getUserOptedInConversationsForGroup(user_id, group_id)
    conversation_map = []
    for id in conversation_ids:
        conversation_map.append({"conversation_id" : id, "opted_in" : opted_in in conversation_ids})
    return messages



