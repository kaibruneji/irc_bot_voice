import json

network = 'irc.tambov.ru'
port = 7770
channel = '#magi'
botName = 'defender'
masterName = 'Кай'

#----input_password-----
with open('code.json', 'r') as code_json:
    code=code_json.read()

obj = json.loads(code)

password = str(obj['password'])

dict_voice_quest = {
  'Как называется звезда нашей солнечной системы?':'солнце',
  'Как называется естественный спутник планеты Земля?':'луна',
  'Сколько будет от десяти отнять четыре и потом прибавить два\
?(Напишите буквами)':'восемь',
  'Сколько у собаки лап?(напишите буквами)':'четыре',
  'Какой запрещающий цвет загорается на светофоре?':'красный',
  'Сколько будет к шести прибавить два и разделить полученное на \
четыре(напишите буквами)':'два',
  'Как называется нос у слона?':'хобот',
  'Какой цвет у снега?':'белый',
  'Что твёрже: алмаз или мел?':'алмаз',
  'Сколько пальцев у человека на одной руке?(напишите буквами)':'пять',
  'Как называется наша планета?':'земля',
  'У кошки четыре ноги а позади у неё длинный...(что?)':'хвост',
  'Из какого вещества состоит алмаз и графит?':'углерод',
  'В комнате есть: стены, потолок и...?(по чему ходят)':'пол'
  }

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
    elif x == 'dict_voice_quest':
        return dict_voice_quest
