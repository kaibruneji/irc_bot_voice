network = 'irc.tambov.ru'
port = 7770
channel = '#magi'
botName = 'defender'
masterName = 'Кай'
password = '077777'

def settings(x):
    if x == 'network':
        return network
    elif x == 'port':
        return port
    elif x == 'botName':
        return botName
    elif x == 'masterName':
        return masterName
    elif x == 'password':
        return password   
    elif x == 'channel':
        return channel
    
