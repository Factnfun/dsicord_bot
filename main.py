import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "angry", "unhappy"]

starter_enc = ["Cheer up!", "Hang in there", "You are a great person / bot!"]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def update_enc(enc_message):
    if "enc" in db.keys():
        enc = db["enc"]
        enc.append(enc_message)
        db["enc"] = enc
    else:
      db["enc"] = [enc_message]
def delete_enc(index):
  enc = db["enc"]
  if len(enc) > index :
    del enc[index]
    db["enc"] = enc
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  if msg.startswith('!random'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_enc
    if "enc" in db_keys():
      options = options + db["enc"]
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  if msg.startswith("!del"):
    enc = []
    if "enc" in db.keys():
      index = int(msg.split("!del",1)[1])
      delete_enc(index)
      enc = db["enc"]
    await message.channel.send(enc)
  if msg.startswith("!list"):
    enc = []
    if "enc" in db["enc"]:
      enc = db["enc"]
    await message.channel.send(enc)
  if msg.startswith("!responding"):
    value = msg.split("!responding",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getnv("TOKEN"))
    
