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
import user_dao
import sys, traceback

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
                    (message_to_send, affected_users) = executeSendMessage(message_json)
                    print message_to_send
                    print affected_users
                    print clients
                    for user in affected_users:
                        try:
                            if user in clients:
                                print "user found: " + str(user)
                                print message_to_send
                                clients[user].send(message)
                        except Exception:
                            print Exception
                            del clients[user]

def executeSendMessage(message):
    mid = messages_dao.addMessageToConversation(message["content"], 
                                                message["time_updated"],
                                                message["conversation_id"],
                                                message["sender_id"])
    message = messages_dao.getMessageById(mid)[0]
    message_to_return = json.JSONEncoder().encode({"message_id": message[0], "conversation_id": message[1], "group_id": message[2],\
                             "sender_id": message[3], "content": message[4], "time_updated": message[5]})
    return (message_to_return, conversation_dao.getUsersOptedInToConversation(str(message[1])))

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
            ws.send('{"methodName": "' + message_json["method"] + '", "results": ["' + '","'.join(result) + '"]}')


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
    if methodName == "authenticateUser":
        return authenticateUser(arguments[0], arguments[1])
    if methodName == "addUser":
        return addUser(arguments[0],arguments[1],arguments[2],arguments[3],arguments[4])
    if methodName == "createConversation":
        return createConversation(arguments[0], arguments[1], arguments[2])
    if methodName == "getUserConversationsForGroup":
        return getUserConversationsForGroup(arguments[0], arguments[1])
    if methodName == "updateUser":
        return updateUser(arguments[0],arguments[1],arguments[2],arguments[3],arguments[4],arguments[5])
    if methodName == "getUserMessages":
        return getUserMessages(arguments[0])

def getMessagesInConversation(conversation_id):
    try:
        messageInfo = messages_dao.getMessagesInConversation(conversation_id)
        messages = []
        for info in messageInfo:
            print info
            print getApproversForMessage(str(info[0]))
            messageDict = {"message_id" : info[0], "user_id" : info[1], "message_text" : info[3], \
            "time_updated" : info[4], "approval_count" : len(getApproversForMessage(str(info[0]))) }
            messages.append(str(messageDict))

        messages.insert(0, "success")
        return messages
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def getConversationsInGroup(group_id, user_id):
    try:
        conversation_ids = conversation_dao.getConversationsInGroup(group_id)
        opted_in = conversation_dao.getUserOptedInConversationsForGroup(user_id, group_id)
        conversation_map = []
        for id in conversation_ids:
            conversation_map.append(str({"conversation_id" : id, "opted_in" : opted_in in conversation_ids}))
        conversation_map.insert(0,"success")
        return conversation_map
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def getGroupsForUser(user_id):
    try:
        groups = [str(x) for x in group_dao.getGroupsForUser(user_id)]
        groups.insert(0, "success")
        return groups
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def getUsersInGroup(group_id):
    try:
        users = group_dao.getUsersInGroup(group_id)
        users.insert(0, "success")
        return users
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def optOutOfConversation(user_id, conversation_id):
    try:
        conversation_dao.userOptOutOfConversation(user_id, conversation_id)
        return ["success"]
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def optInToConversation(user_id, conversation_id):
    try:
        conversation_dao.userOptInToConversation(user_id, conversation_id)
        return ["success"]
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def getApproversForMessage(message_id):
    try:
        result = [str(x) for x in messages_dao.usersWhoApproveMessage(message_id)]
        result.insert(0, "success")
        return result
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def getDisapproversForMessage(message_id):
    try:
        result = [str(x) for x in messages_dao.usersWhoDisapproveMessage(message_id)]
        result.insert(0, "success")
        return result
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def addUserToGroup(user_id, group_id):
    try:
        group_dao.addUserToGroup(user_id, group_id)
        return ["success"]
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def removeUserFromGroup(user_id, group_id):
    try:
        group_dao.removeUserFromGroup(user_id, group_id)
        return  ["success"]
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def addUser(user_name, user_email, user_phone, device_id, timestamp):
    try:
        user_id = user_dao.addUser(user_name, user_phone, user_email, device_id, timestamp)
        return ["success", str(user_id)]
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def authenticateUser(user_id, device_id):
    try: 
        if user_dao.authenticateUser(user_id, device_id) > 0:
            return ["success", "true"]
        else:
            return ["success", "false"]
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def createConversation(group_id, topic_name, is_announcement):
    try:
        cid = conversation_dao.addConversationForGroup(group_id, topic_name)
        user_ids = group_dao.getUsersInGroup(group_id)
        admin_ids = group_dao.getAdminForGroup(group_id)
        for user_id in user_ids:
            if is_announcement:
                if user_id in admin_ids:
                    conversation_dao.addUserToConversation(user_id, cid, True)
                else:
                    conversation_dao.addUserToConversation(user_id, cid, False)
            else:
                conversation_dao.addUserToConversation(user_id, cid, True)
        return ["success", str(cid)]
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def getUserConversationsForGroup(user_id, group_id):
    try:
        rows = conversation_dao.getUserConversationsForGroup(user_id, group_id)
        messages = []
        for row in rows:
            message = {"conversation_id": str(row[0]), "topic_name": row[1], "is_open": row[2], "is_opted_in": row[3], "can_write": row[4]}
            messages.append(str(message))
        messages.insert(0, "success")
        return messages
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def updateUser(user_id, user_name, user_email, user_phone, device_id, timestamp):
    try:
        user_dao.updateUser(user_id, user_name, user_email, user_phone, device_id, timestamp)
        return ["success"]
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

def getUserMessages(user_id):
    try:
        messageInfo = messages_dao.getMessagesForUser(user_id)
        messages = []
        for info in messageInfo:
            print info
            print getApproversForMessage(str(info[0]))
            messageDict = {"message_id" : info[0], "conversation_id": info[2], "message_text" : info[3], \
            "time_updated" : info[4], "approval_count" : len(getApproversForMessage(str(info[0]))) }
            messages.append(str(messageDict))

        messages.insert(0, "success")
        return messages
    except:
        traceback.print_exc(file=sys.stdout)
        return ["failure"]

