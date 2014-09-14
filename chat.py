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
import group_dao

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
                'time_updated' in message_json and
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
                                          message["time_updated"],
                                          message["conversation_id"],
                                          message["sender_id"])
    return conversation_dao.getUsersOptedInToConversation(message["conversation_id"])

@sockets.route('/update')
def update(ws):
    while ws.socket is not None:
        gevent.sleep(0.1)
        message = ws.receive()
        if message:
            print "got into the condition"
            message_json = json.loads(message)
            result = translateAndFetch(message_json)
            print result
            ws.send('{"results": ["' + '","'.join(result) + '"]}')


def translateAndFetch(request):
    methodName = request["method"]
    arguments = request["arguments"]
    print "got into the translate method"
    print methodName
    if methodName == "getMessagesInConversation":
        return getMessagesInConversation(arguments[0])
    if methodName == "getConversationsInGroup":
        return getConversationsInGroup(arguments[0],arguments[1])
    if methodName == "getGroupsForUser":
        return getGroupsForUser(arguments[0])
    if methodName == "getUsersInGroup":
        return getUsersInGroup(arguments[0])
    if methodName == "optOutOfConversation":
        return optOutOfConversation(arguments[0], arguments[1])
    if methodName == "optInToConversation":
        return optInToConversation(arguments[0], arguments[1])
    if methodName == "getApproversForMessage":
        return getApproversForMessage(arguments[0])
    if methodName == "getDisapproversForMessage":
        return getDisapproversForMessage(arguments[0])
    if methodName == "addUserToGroup":
        return addUserToGroup(arguments[0], arguments[1])
    if methodName == "removeUserFromGroup":
        return removeUserFromGroup(arguments[0], arguments[1])

def getMessagesInConversation(conversation_id):
    messageIds = messages_dao.getMessagesInConversation(conversation_id)
    messages = []
    for messageId in messageIds:
        messages.extend(messages_dao.getMessageTextById(messageId))
    return messages

def getConversationsInGroup(group_id, user_id):
    conversation_ids = conversation_dao.getConversationsInGroup(group_id)
    opted_in = conversation_dao.getUserOptedInConversationsForGroup(user_id, group_id)
    conversation_map = []
    for id in conversation_ids:
        conversation_map.append(str({"conversation_id" : id, "opted_in" : opted_in in conversation_ids}))
    return conversation_map

def getGroupsForUser(user_id):
    return [str(x) for x in group_dao.getGroupsForUser(user_id)]

def getUsersInGroup(group_id):
    return group_dao.getUsersInGroup(group_id)

def optOutOfConversation(user_id, conversation_id):
    try:
        conversation_dao.userOptOutOfConversation(user_id, conversation_id)
        return ["success"]
    except:
        return ["failure"]

def optInToConversation(user_id, conversation_id):
    try:
        conversation_dao.userOptInToConversation(user_id, conversation_id)
        return ["success"]
    except:
        return ["failure"]

def getApproversForMessage(message_id):
    return [str(x) for x in messages_dao.usersWhoApproveMessage(message_id)]

def getDisapproversForMessage(message_id):
    return [str(x) for x in messages_dao.usersWhoDisapproveMessage(message_id)]

def addUserToGroup(user_id, group_id):
    try:
        group_dao.addUserToGroup(user_id, group_id)
        return ["success"]
    except:
        return ["failure"]

def removeUserFromGroup(user_id, group_id):
    try:
        group_dao.removeUserFromGroup(user_id, group_id)
        return  ["success"]
    except:
        return ["failure"]