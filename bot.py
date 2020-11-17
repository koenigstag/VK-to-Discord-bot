# -*- coding: utf-8 -*
import urllib.request
import json
import re
import time
import datetime
#import codecs
import sys, os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

import config

# инициализируемся
bot = commands.Bot(command_prefix='!', help_command=None)

@bot.event
async def on_ready():
    print('------')
    print('Logged in')
    print('------')

# принудительно выключаем программу

@bot.command()
async def halt(msg):
    if msg.author == bot.get_user(469850108440084492):
        sys.exit()
    
@bot.command()
async def start(message):
    # парсим /start и подписываем новые ид на раздачу новостей
    
    await message.author.send(vk_bot_config.start_greeting)

    print(str(message.channel.id) + " !start")

    if not message.channel.id in chat_ids:
        # если исполнившего команду нет в списке - записываем
        # в файл и добпаляем в массив
        with open(os.getcwd() + '/vkbot/disc_channels', 'a') as ids:
                ids.write(str(message.channel.id) + ",")
        chat_ids.append(message.channel.id)

        print("chat_ids = " + chat_ids)
    




print('\n------')
print('\n vk_group =  https://vk.com/club' + str(config.vk_group_id))
print('check delay - ' + str(config.check_delay) + ' sec')
print('\n------')

chat_ids = []
disc_channels = open(os.getcwd() + '/vkbot/disc_channels', 'r')
ids_arr = disc_channels.read().split(',')
print("\ndiscord_chat_ids:")
for i in ids_arr:
    if len(i) > 1:
        chat_ids.append(int(i))
        #channel = bot.get_channel(i)
        #print('name - ' + channel.name + ', id - ' + i)
        print(' id - ' + i)
disc_channels.close()
print('\n------')
pool = ThreadPool(4)

# получаем пост с заданым сдвигом
def get_post(offset=1):
    posts_offset = offset
    
    cooked = []
    a = urllib.request.urlopen('https://api.vk.com/method/wall.get?owner_id=-' + str(config.vk_group_id) + '&filter=owner&count=1&offset=' + str(posts_offset) + '&access_token=' + str(config.access_token) + '&v=' + str(config.vkapi_version))
    out = a.read().decode('utf-8')
    print('--')
    print('\n https://api.vk.com/method/wall.get?owner_id=-' + str(config.vk_group_id) + '&filter=owner&count=1&offset=' + str(posts_offset) + '&access_token=' + str(config.access_token) + '&v=' + str(config.vkapi_version) + ' \n')
    print('\n--')
    
    json_data = json.loads(out)
    
    # получаем сырой текст
    text = json_data['response']['items'][0]["text"]
    #id_from_id = str(json_data['response']['items'][0]["from_id"])
    
    # убираем html требуху
    text = text.replace('<br>', '\n')
    text = text.replace('&amp', '&')
    text = text.replace('&quot', '"')
    text = text.replace('&apos', "'")
    text = text.replace('&gt', '>')
    text = text.replace('&lt', '<')

    # если встречается ссылка на профиль
    profile_to_replace = re.findall(r'\[(.*?)\]', text)
    profile_link = re.findall(r'\[(.*?)\|', text)
    profile_name = re.findall(r'\|(.*?)\]', text)
    profiles = []

    # заменаем ссылку на профиль в тексте
    try:
        for i in range(len(profile_link)):
            profiles.append(profile_name[i] + " (@" + profile_link[i] + ")")
        counter = 0
        for i in profile_to_replace:
            text = text.replace("[" + i + "]", profiles[counter])
            counter += 1
    except:
        pass

    #text += u"\n\nКомментарии: http://vk.com/wall" + id_from_id
    cooked.append(text)
    cooked.append(json_data['response']['items'][0]["date"])
    cooked.append(json_data['response']['items'][0]["id"])

    # на случай встречи с медиафайлами (пока что реализованы фото и тамб к видео)
    try:
        media = json_data['response']['items'][0]["attachments"]

        media_arr = []
        for media in attachments:
            if "photo" in media:
                media_arr.append(media["photo"]["sizes"][(len(media["photo"]["sizes"]) - 1)]["url"])
                # TODO "attachments": [ {"type":"photo","photo":{"sizes":[{"height":max,"url":"...\/...","type":"x","width":max}, {snd image}]
            #if "video" in media:
                #media_arr.append("http://vk.com/video" + media["video"]["owner_id"] + "_" + media["video"]["vid"])
            #if "doc" in media:
                #media_arr.append(media["doc"]["url"])
        cooked.append(media_arr)
    except:
        pass
    # cooked [text, timestamp, post_id, media_arr]
    return cooked
    
    
    
    
    
    
    
    
    
    
# проверяем новые посты
async def checker():
    await bot.wait_until_ready()
    
    if len(chat_ids) < 1:
        return
    
    with open(os.getcwd() + '/vkbot/last_post_id', 'r') as t:
        last_post_id = int(t.read())

    while not bot.is_closed():
        #print('\nchecking... ' + str(datetime.now()) + '__' + str(time.time()))
        
        #last_posts = 1
        #is_pinned = 1
        
        # берем закреп пост (потенциальный)
        pinned_post = get_post(0)
        # берем первый пост
        fst_post = get_post(1)
        
        # определяем есть закреп или нет
        #print('if pinned_id = ' + str(pinned_post[2]) + ' <= fst_id = ' + str(fst_post[2]))
        # если ид поста в закрепе старее чем ид первого поста
        if pinned_post[2] <= fst_post[2]:
            # установка для стены с закрепом
            is_pinned = 1
            # is_pinned = (если нет закрепа = 0)(если есть закреп = 1)

            #print('has_pinned')
        else:
            # установка для стены без закрепа
            is_pinned = 0
            # is_pinned = (если нет закрепа = 0)(если есть закреп = 1)
        last_posts = is_pinned


        end = False
        
        # проверяем новые новости по таймстампу и получаем количество новых
        while not end:
            # если есть закреп то проверяем 1-й пост, если нет то 0-й
            post = get_post(last_posts)
            
            # проверка на ласт пост (сверка с таймстампом в файле)
            #print('post = ' + str(post[2]) + '  >  last_post_id = ' + str(last_post_id))
            # если время в посте новее чем время в файле
            if post[2] > last_post_id:
                # если пост новее таймстампа
                #print('found +1 new post')
                
                last_posts += 1
                # ищем еще новые посты...
            else:
                # если таймстамп старше поста
                #print('found old post')
                # то это последний отправленный пост (время публикации которого запомнили в файле)
                
                # берем вторую границу 0-й или 1-й пост

                last = get_post(is_pinned)
                
                last_post_id = last[2]
                # запоминаем время 0-го или 1-го поста
                with open(os.getcwd() + '/vkbot/last_post_id', 'w') as t:
                    t.write(str(last_post_id))
                # завершаем цикл поиска новых постов
                end = True
        
        # выводим сообщение о найденых новых постах


        if last_posts > is_pinned:
            print('\nfound ' + str(last_posts - is_pinned) + ' new posts!')
            print('time: ' + str(datetime.now()) + '__' + str(time.time()) + '\n')
        
        # определяем условие отправки найденых постов
        # last_posts = 1+ если нет закрепа
        # last_posts = 2+ если есть закреп
        #print('is_pinned = ' + str(is_pinned))
        #print('last_posts = ' + str(last_posts))
        if last_posts > is_pinned:
        # рассылаем каждому нужное кол-во новых постов
            cprint('sending...\n', 'green')
            text_to_send = []
            timestamps = []
            post_ids = []
            
            # от 0 до [найденых постов -1(только если есть закреп)]
            for post_cur in range(last_posts - is_pinned):
                # берем пост (всего постов -1 -курсор(от 0 до [найденых постов -1(только если есть закреп)])
                post = get_post(last_posts - 1 - post_cur)
                # заполняем массив текста для поэтапной отправки
                text_to_send.append(post[0])
                timestamps.append(post[1])
                post_ids.append(post[2])
                
                # если в массиве поста есть фото
                photo_to_send = []
                if len(post) > 3:
                    for i in post[3]:
                        photo_to_send.append(i)
            
            # собственно попытка отправки
            try:
                # для всех каналов (ид которых взяты из файла ids)
                for ids_cur in range(len(chat_ids)):
                    # задаем переменную канала
                    channel = bot.get_channel(chat_ids[ids_cur])
                    
                    #print('trying to send. channel name - ' + str(channel.name) + ', channel_id - ' + str(chat_ids[ids_cur]))
                    # для каждого текста в масиве текстов
                    for text_cur in range(len(text_to_send)):
                        embedVar = discord.Embed(title="", description=str("[Посмотреть на стене](https://vk.com/club" + config.vk_group_id + "?w=wall-" + config.vk_group_id + "_" + str(post_ids[text_cur]) + ")" + "\n\n" + text_to_send[text_cur]), color=0x00ff00)
                        embedVar.timestamp = datetime.fromtimestamp(timestamps[text_cur])
                        
                        if str(text_to_send[text_cur]) != '':
                            await channel.send(embed=embedVar)
                            
                        if photo_to_send:
                            for i in photo_to_send:
                                embedVar = discord.Embed(title="", description=str("[Посмотреть на стене](https://vk.com/club" + config.vk_group_id + "?w=wall-" + config.vk_group_id + "_" + str(post_ids[text_cur]) + ")" + "\n\n"), color=0x00ff00)
                                embedVar.timestamp = datetime.fromtimestamp(timestamps[text_cur])
                                embedVar.set_image(url=str(i))
                                await channel.send(embed=embedVar)
                                #await channel.send(str(i))
                                #yield from client.send_file(client.get_channel(str(id_)), str(i))
                
                print('      ')
                for text_cur in range(len(text_to_send)):
                    if str(text_to_send[text_cur]) != '':
                        pass
                        #cprint('text was sent -' + str(text_to_send[text_cur]) + '~', 'green')
                    else:
                        pass
                
                cprint('sent...', 'green')
            except:
                cprint('\nException while sending...\n', 'red')
        
        #print('------')
        
        # спим 1 минут
        await asyncio.sleep(config.check_delay)       
        
bot.loop.create_task(checker())
bot.run(config.bot_token)
