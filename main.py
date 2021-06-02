import discord
import os
import requests
import json
import random
import urllib.request,smtplib,ssl
#from keep_alive import keep_alive
from bs4 import BeautifulSoup

client = discord.Client()

def get_score():
  url="https://www.espncricinfo.com/"
  source=urllib.request.urlopen(url).read()
  soup=BeautifulSoup(source,'html.parser')
  div_tag=soup.find_all('div',class_='match-info-HSB')
  teamname=[]
  for d in div_tag:
    try:
      names=d.find_all('div',class_='name-detail')
      score=d.find_all('span',class_='score')
      try:
        first=names[0].text+" ("+score[0].text+")"
      except:
        first=names[0].text
      try:
        Second=names[1].text+" ("+score[1].text+")"
      except:
        Second=names[1].text
      teamname.append(first+" vs "+Second)
    except:
      pass
  return teamname


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_price():
  url_sensex="https://www.moneycontrol.com/sensex/bse/sensex-live"
  url_nifty="https://www.moneycontrol.com/indian-indices/nifty-50-9.html"
  source_sensex=urllib.request.urlopen(url_sensex).read()
  source_nifty=urllib.request.urlopen(url_nifty).read()
  soup1=BeautifulSoup(source_sensex,'html.parser')
  soup2=BeautifulSoup(source_nifty,'html.parser')
  div_tag=soup1.find('span',id='sp_val')
  div_tag_nif=soup2.find('span',id='sp_val')
  price1=div_tag.text
  price2=div_tag_nif.text
  return price1,price2

def get_crypto_price(name):
  url1="https://coinmarketcap.com/currencies/"+name+"/"
  source=urllib.request.urlopen(url1).read()
  soup=BeautifulSoup(source,'html.parser')
  div_tag=soup.find('div',class_='priceValue___11gHJ')
  return div_tag.text

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$cricket'):
    name=get_score()
    for n in name:
      await message.channel.send(n)

  if msg.startswith('$price'):
    p = get_crypto_price(msg[7:])
    await message.channel.send(p)

  if msg.startswith('$market'):
    s,n=get_price()
    sp = "Sensex - "+s
    np = "Nifty - "+n
    await message.channel.send(sp)
    await message.channel.send(np)

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)


  if msg.startswith('$hello'):
    await message.channel.send('Hello!')


#keep_alive()
client.run(os.getenv('TOKEN'))
