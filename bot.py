# -*- coding: utf-8 -*-
import os
import telebot
import feedparser
import time
import re
from datetime import date
import datetime
import json
import requests
from conf.settings import TELEGRAM_TOKEN

#Token = "719662445:AAHyzcK5zE7pGcJjQfwBMnIlK35e506_TBk"
#Token = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['info'])
def info(session):
    #markdown = "*bold text* _italic text_ [text](URL)"
    #bot.send_message(session, markdown, parse_mode: 'Markdown')
    bot.reply_to(session, u"Olá {}! Bem-vindo ao bot! 🧙‍♂️".format(session.chat.first_name))

@bot.message_handler(commands=['t','test'])
def test(session):
    url = "http://9gagrss.com/feed"
    rss_d = feedparser.parse(url)
    rss_d.entries[0]['link']
    bot.reply_to(session, text=(rss_d.entries[0]['link']))

@bot.message_handler(commands=['9gag', '9g'])
def blog(session):
    url = "http://9gagrss.com/feed"
    rss_d = feedparser.parse(url)
    rss_d.entries[0]['link']
    bot.reply_to(session, text=(rss_d.entries[0]['link']))

@bot.message_handler(commands=['ahnegao'])
def blog(session):
    url = "https://www.ahnegao.com.br/feed"
    rss_d = feedparser.parse(url)
    rss_d.entries[0]['link']
    bot.reply_to(session, text=(rss_d.entries[0]['link']))

@bot.message_handler(commands=['blog','3c'])
def blog(session):
    url = "https://3cplusnow.com/feed"
    rss_d = feedparser.parse(url)
    rss_d.entries[0]['link']
    bot.reply_to(session, text=(rss_d.entries[0]['link']))

@bot.message_handler(commands=['dolar', 'Dolar'])
def dolar(session):
    r = requests.get('https://economia.awesomeapi.com.br/all/USD')
    data = r.json()
    data = data['USD']
    bot.reply_to(session, "💵 Nome: {} \n🔄 Valor em R$: {} \n⏱ Ultima atualização: {}".format(data['name'],data['bid'],data['create_date']))

@bot.message_handler(commands=['bitcoin','Bitcoin'])
def bitcoin(session):
    r = requests.get('https://economia.awesomeapi.com.br/all/BTC-BRL')
    data = r.json()
    data = data['BTC']
    bot.reply_to(session, "📊 Nome: {} \n🔄 Valor em R$: {} \n⏱ Ultima atualização: {}".format(data['name'],data['bid'],data['create_date']))

#wellcome message


@bot.message_handler(func=lambda m: True)
def reply(session):

    hoje = datetime.datetime.today()
    semana = hoje.strftime("%w")
    track = re.findall("^rastrear", session.text)

    if re.findall("windows",session.text.lower()):
        bot.reply_to(session, "https://tenor.com/IAlp.gif")

    elif re.findall("^rastrear", session.text.lower()):
        if not re.findall(r"...........br", session.text.lower()):
            bot.reply_to(session, "😥 Desculpe! \nSó consigo localizar encomendas do Brasil")
            return
        tmp = re.findall(r"...........br", session.text.lower())
        r = requests.get("https://api.linketrack.com/track/json?user=teste&token=1abcd00b2731640e886fb41a8a9671ad1434c599dbaa0a0de9a5aa619f29a83f&codigo={}".format(tmp[0]))
        data = r.json()
        events = data['eventos']
        events.reverse()
        count = data['quantidade']
        txtmsg = "Segundo o site Linketrack \n\n🔎 Código: {}\n📦 Serviço: {}\n".format(data['codigo'],data['servico'])
        for event in events:
            txtmsg = txtmsg + "\n\n📅 Data: {}\n🕰 Hora: {}\n🧭 Local: {}\n🏷 Status: {}".format(event['data'], event['hora'], event['local'], event['status'])
        bot.send_message(session.chat.id, txtmsg)

    elif re.findall("servlet",session.text.lower()):
        bot.reply_to(session, "https://media.giphy.com/media/3o7TKMEJrkqKFWea5i/giphy.gif")

    elif re.findall("vacilao",session.text.lower()):
        bot.reply_to(session, "Meu pé na tua mão 🙆‍♂️")

    elif re.findall("boa tarde",session.text.lower()):
        bot.reply_to(session, "Boa tarde pra você também {}!".format(session.chat.first_name))

    elif re.findall("bom dia",session.text.lower()):
        bot.reply_to(session, "Bom dia pra você também {}!".format(session.chat.first_name))

    elif re.findall("boa noite",session.text.lower()):
        bot.reply_to(session, "Boa noite pra você também {}!".format(session.chat.first_name))

    elif re.findall("hoje",session.text.lower()):
        if semana == 5:
            bot.reply_to(session, "Hoje é sexta feira carai! https://www.youtube.com/watch?v=052UiCa7xa8")

bot.polling()
