# -*- coding: utf-8 -*-
import os
import telebot
import feedparser
import time
import re
from datetime import date
from datetime import datetime
from time import sleep
import datetime
import json
import requests
from conf.settings import TELEGRAM_TOKEN
from conf.settings import CHAT_ID
from conf.settings import WHEATHER_TOKEN
from conf.settings import TRACK_TOKEN
from flask import Flask, request

bot = telebot.TeleBot(TELEGRAM_TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['info'])
def info(session):
    bot.reply_to(session, u"Olá {}! \n"
    "Bot na *versão BETA* para testes de algumas funcionalidades. Caso precise de "
    "alguma ajuda você pode usar */comandos* para saber o que tanto posso fazer. "
    "Alguns comandos não precisam de barra para funcionar como o rastrear. para usá-lo "
    "basta digitar rastrear seguido do codigo de rastreio de sua encomenda\n"
    "Para condições climaticas basta digitar clima seguido de sua cidade e estado."
    "\n \nCriado por: *Peterson Medeiros*"
    .format(session.from_user.first_name, session.chat.title), parse_mode='MARKDOWN')

@bot.message_handler(commands=['comandos','Comandos'])
def commands(session):
    bot.send_message(CHAT_ID, "/info - Obtem informações sobre o Bot.\n/9g - Meme aleatório do 9gag.\n/AhNegao - Meme aleatório do Ah Negão.\n"
    "/3c - Noticias do site da 3c Plus.\n"
    "/dolar - Cotação atual do Dolar.\n"
    "/bitcoin - Cotação atual do Bitcoin.\n"
    "/joke - Charada Aleatória.\n"
    "\n🔍 *Rastrear uma encomenda*: Escreva rastrear seguido do código de rastreamento. Exemplo: *rastrear PL059497789BR*\n"
    "\n🌦 *Informações climaticas*: Escreva clima seguido da cidade e sigla do estado. Exemplo *Clima Guarapuava PR*", parse_mode='MARKDOWN')

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
    sleep(10)

@bot.message_handler(commands=['ahnegao', 'AhNegao'])
def blog(session):
    url = "https://www.ahnegao.com.br/feed"
    rss_d = feedparser.parse(url)
    rss_d.entries[0]['link']
    bot.reply_to(session, text=(rss_d.entries[0]['link']))
    sleep(10)

@bot.message_handler(commands=['blog','3c'])
def blog(session):
    url = "https://3cplusnow.com/feed"
    rss_d = feedparser.parse(url)
    rss_d.entries[0]['link']
    bot.reply_to(session, text=(rss_d.entries[0]['link']))
    sleep(10)

@bot.message_handler(commands=['dolar', 'Dolar'])
def dolar(session):
    r = requests.get('https://economia.awesomeapi.com.br/all/USD')
    data = r.json()
    data = data['USD']
    bot.reply_to(session, "💵 Nome: {} \n🔄 Valor em R$: {} \n⏱ Ultima atualização: {}"
    .format(data['name'],data['bid'],data['create_date']))
    sleep(10)

@bot.message_handler(commands=['bitcoin','Bitcoin'])
def bitcoin(session):
    r = requests.get('https://economia.awesomeapi.com.br/all/BTC-BRL')
    data = r.json()
    data = data['BTC']
    bot.reply_to(session, "📊 Nome: {} \n🔄 Valor em R$: {} \n⏱ Ultima atualização: {}"
    .format(data['name'],data['bid'],data['create_date']))
    sleep(10)

@bot.message_handler(commands=['joke', 'piada'])
def dolar(session):
    url = 'https://us-central1-kivson.cloudfunctions.net/charada-aleatoria'
    headers = {'accept': 'application/json'}
    r = requests.post(url, headers=headers)
    data = r.json()
    bot.reply_to(session, "Charada Aleatória: \n \n{} \n\nResposta: {}"
    .format(data['pergunta'],data['resposta']))
    sleep(10)

@bot.message_handler(content_types = ['new_chat_members'])
def wellcome_message(session):
    bot.send_message(CHAT_ID, "Bem vindo *{}*! \nEu sou o Mandachuva aqui! Se precisar de minha ajuda digite /info 😉"
    .format(session.new_chat_member.first_name), parse_mode='MARKDOWN')
    sleep(10)


@bot.message_handler(commands=['corona'])
def corona(session):
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php?country=brazil"

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "9202259c1dmsh5a204e93ff9f9c4p19d5cfjsn75e520c8ab51"
    }
    r = requests.get(url, headers=headers)
    data = r.json()

    print("Resultado: {}".format(data))
    auxs = data['latest_stat_by_country']

    for aux in auxs:
        bot.reply_to(session, "⚠ Casos de Corona vírus (COVID-19) no Brasil:\n"
        "\n"
       "Total de casos: {}\n"
       "Total de mortes: {}\n"
       "Casos ativos: {}\n"
       "Casos criticos: {}\n"
       "Casos recuperados: {}\n"
       "Novos casos recentes: {}\n"
       .format(aux['total_cases'],aux['total_deaths'], aux['active_cases'], aux['serious_critical'], aux['total_recovered'], aux['new_cases']))
    sleep(10)

@bot.message_handler(func=lambda m: True)
def reply(session):
    hoje = datetime.datetime.today()
    semana = hoje.strftime("%w")

    if re.findall("windows",session.text.lower()):
        bot.reply_to(session, "https://tenor.com/IAlp.gif")

    elif re.findall("^rastrear", session.text.lower()):
        bot.send_chat_action(CHAT_ID, 'typing')
        if not re.findall(r"...........br", session.text.lower()):
            bot.reply_to(session, "😥 Desculpe! \nSó consigo localizar encomendas do Brasil")
            return
        tmp = re.findall(r"...........br", session.text.lower())
        r = requests.get("https://api.linketrack.com/track/json?user=teste&token={}&codigo={}".format(TRACK_TOKEN, tmp[0]))
        data = r.json()
        events = data['eventos']
        events.reverse()
        txtmsg = "Segundo o site Linketrack \n\n🔎 Código: {}\n📦 Serviço: {}\n".format(data['codigo'],data['servico'])
        for event in events:
            txtmsg = txtmsg + "\n\n📅 Data: {}\n🕰 Hora: {}\n🧭 Local: {}\n🏷 Status: {}".format(event['data'], event['hora'], event['local'], event['status'])
        bot.send_message(CHAT_ID, txtmsg)
        sleep(10)

    elif re.findall("^clima", session.text.lower()):
        msg = ""
        bot.send_chat_action(CHAT_ID, 'typing')
        search = session.text
        if not re.findall("^[Cc]lima\s+?([-\wÀ-ú ']+?)\s+?([a-zA-Z]{2})$", search):
            bot.send_message(CHAT_ID,"⚠ Desculpe, não consegui entender qual é a cidade e o estado.\n"
            "Poderia por favor digitar novamente?\nPrimeiro cidade, depois estado.\n"
            "Exemplo: *Clima Guarapuava PR*", parse_mode='MARKDOWN')
            print("City or state not found!")
            return
        args = re.findall("^[Cc]lima\s+?([-\wÀ-ú ']+?)\s+?([a-zA-Z]{2})$", search)
        city = args[0][0]
        state = args[0][1]
        r = requests.get("http://apiadvisor.climatempo.com.br/api/v1/locale/city?name={}&state={}&token={}".format(city, state, WHEATHER_TOKEN))
        if r.content == b'[]' or r.status_code != 200:
            bot.send_message(CHAT_ID, "⚠ Ops, algo deu errado!\n"
            "Verifique por favor se o nome da cidade está correto e acentuado\n"
            "Ou também se o estado está correto")
            print("error when try to find city id")
            return
        data = r.json()
        objetos = data
        for obj in objetos:
            id = obj['id']
            city = obj['name']
            state = obj['state']
            country = obj['country']
        msg = msg+ "Segundo o site *Clima Tempo*: \n Cidade: *{}* \n Estado: *{}*\n".format(city, state)
        headers = {'Content-Type'  : 'application/x-www-form-urlencoded'}
        data_content = "localeId[]={}".format(id)
        resp = requests.put("http://apiadvisor.climatempo.com.br/api-manager/user-token/{}/locales".format(WHEATHER_TOKEN), data=data_content, headers=headers)
        if resp.status_code != 200:
            bot.send_message(CHAT_ID, "⚠ Error: {}".format(resp.content))
            print("Error when try to register city to wheather token")
            return
        r = requests.get("http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{}/current?token={}".format(id, WHEATHER_TOKEN))
        if r.status_code != 200:
            bot.send_message(CHAT_ID, "⚠ Error: ".format(r.content))
            print("Error when try to get wheather")
            return
        content = r.json()
        events = content['data']
        formated_date = datetime.datetime.strptime(events['date'], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
        formated_hour = datetime.datetime.strptime(events['date'], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
        msg = msg + "📆 Data: {}\n⏰ Hora: {}\n🌡 Temperatura: {}º\n😎 Sensasão térmica: {}º \n💧 Humidade: {}% \n📜 Condição: {}".format(formated_date, formated_hour, events['temperature'], events['sensation'], events['humidity'], events['condition'])
        bot.send_message(CHAT_ID, msg, parse_mode='MARKDOWN')
#        sleep(10)

    elif re.findall("linux",session.text.lower()):
        bot.reply_to(session, "https://media.giphy.com/media/2aPePPqpAf5jwjtt2p/giphy.gif")

    elif re.findall("servlet",session.text.lower()):
        bot.reply_to(session, "https://media.giphy.com/media/3o7TKMEJrkqKFWea5i/giphy.gif")

    elif re.findall("vacilao",session.text.lower()):
        bot.reply_to(session, "Meu pé na tua mão 🙆‍♂️")

    elif re.findall("boa tarde",session.text.lower()):
        bot.reply_to(session, "Boa tarde pra você também {}!".format(session.from_user.first_name))

    elif re.findall("bom dia",session.text.lower()):
        bot.reply_to(session, "Bom dia pra você também {}!".format(session.from_user.first_name))

    elif re.findall("boa noite",session.text.lower()):
        bot.reply_to(session, "Boa noite pra você também {}!".format(session.from_user.first_name))

    elif re.findall("teu maddog",session.text.lower()):
        bot.reply_to(session, "https://avatars1.githubusercontent.com/u/19822650?s=460&v=4")

    elif re.findall("o jogo",session.text.lower()):
        bot.reply_to(session, "Perdi 😭")

    elif re.findall("coronga",session.text.lower()):
        bot.reply_to(session, "😷 Use máscara e lave bem as mãos para se proteger do coronga! \n Para saber detalhes use comando /corona")

    elif re.findall("hoje",session.text.lower()):
        if semana == 5:
            bot.reply_to(session, "Hoje é sexta feira carai! https://www.youtube.com/watch?v=gNkLGEUae_s")
        elif semana == 7:
            bot.reply_to(session, "Fique de boas fera, hoje é dia de descansar 😌")

#bot.polling()
@server.route("/{}".format(TELEGRAM_TOKEN), methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://young-temple-04015.herokuapp.com/' + TELEGRAM_TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
