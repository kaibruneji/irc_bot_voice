#! /usr/bin/env python
# -*- coding: utf-8 -*-

#-------Import modules---------------------

import socket
import sys
import time
import requests
import settings
import sqlite3
import random

#-------Functions---------------------------

# Function shortening of ic.send.  
def send(mes):
  return irc.send(bytes(mes,'utf-8'))          

#-------Connect server----------------------

network = settings.settings('network')
port = settings.settings('port')
irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
channel = settings.settings('channel')
botName = settings.settings('botName')
masterName = settings.settings('masterName')

#-------Connect to IRC-server----------------

irc.connect ((network, port))
print (irc.recv(2048).decode("UTF-8"))
send('NICK '+botName+'\r\n')
send('USER '+botName+' '+botName+' '+botName+' :Python IRC\r\n')
send('JOIN '+channel+' \r\n')
send('NickServ IDENTIFY '+settings.settings('password')+'\r\n')
send('MODE '+botName+' +x')

#-------Global_variables--------------------
   
name = ''
message = ''
num_users = 0
botOnOff = False

dict_name_question = {}
dict_voice_quest = settings.settings('dict_voice_quest')

#-------Major_while-------------------------

while True:
    try:
        data = irc.recv(2048).decode("UTF-8")
    except:
        continue
    # Ping-pong.
    if data.find('PING') != -1:
        send('PONG'+data.split()[1]+'\r\n')
    
    # Make variables Name, Message, IP from user message.
    if data.find('PRIVMSG') != -1:
        name = data.split('!',1)[0][1:]
        message = data.split('PRIVMSG',1)[1].split(':',1)[1].strip().lower()
    try:
        ip_user=data.split('@',1)[1].split(' ',1)[0]
    except:
        print('no name')

    #-----------GET num_users and give voice----------
    
    if 'PRIVMSG ' in data and ':!defender off' in data and name == masterName:
        botOnOff = False

    elif 'PRIVMSG ' in data and ':!defender on' in data and name == masterName:
        botOnOff = True

    if botOnOff == True:
        if ' QUIT :' in data or ' PART '+channel+' :' \
           in data and 'PRIVMSG' not in data or 'PRIVMSG '+channel+' :!NAMES\r\n' in \
           data and name == masterName:
            send('NAMES '+channel+'\r\n')    
           
        if botName+' = '+channel+' :' in data and 'PRIVMSG' not in data:
            num_users = len(data.split(channel+' :')[1].split(' \r\n')[0].split(' '))
            num_users += 1
            num_users_str = str(num_users)        
            send('MODE '+channel+' +l '+num_users_str+'\r\n')        
            print('I GOT USER NUM_LIST+1 : '+num_users_str+'\r\n')
                
        if ' JOIN :'+channel in data and 'PRIVMSG' not in data:
            name_join = data.split('!')[0].split(':')[1]
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            name_join_find = (name_join,)
            c.execute('SELECT role FROM stocks WHERE name=?', name_join_find)
            in_name_table = c.fetchone()
            voice_table_for_work = 'voice'
            voice_table_for_work_2 = (voice_table_for_work,)
            send('NAMES '+channel+'\r\n')
            if in_name_table == None:
                question_voice = random.choice(list(dict_voice_quest))
                send('PRIVMSG '+name_join+' :'+question_voice+'\r\n')
                dict_name_question[name_join] = dict_voice_quest[question_voice]
            elif in_name_table == voice_table_for_work_2:
                send('MODE '+channel+' +v '+name_join+'\r\n')
                
        if 'PRIVMSG '+botName+' :' and name in dict_name_question and \
           message == dict_name_question[name]:        
            name_in_table = (name,)
            conn = sqlite3.connect('users.db')
            c = conn.cursor()        
            c.execute('SELECT * FROM stocks WHERE name=?', name_in_table)            
            if c.fetchone() == None:
                send('MODE '+channel+' +v '+name+'\r\n')
                send('PRIVMSG '+name+' :Ответ правильный! Теперь у вас при заходе \
на канал с этого ника будет автоматически давать +v (голос)\r\n')
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                purchse_users_db = [(name, 'voice')]
                c.executemany('INSERT INTO stocks VALUES (?,?)', purchse_users_db)
                conn.commit()
                conn.close
            
    # Out command.  
    if data.find('PRIVMSG '+channel+' :!defender quit') != -1 and name == masterName:
        send('PRIVMSG '+channel+' :Хорошо, всем счастливо оставаться!\r\n')
        send('QUIT\r\n')
        sys.exit()

        #------------Printing---------------      

    print(data)
