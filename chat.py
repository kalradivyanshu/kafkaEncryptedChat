from kafka import KafkaProducer, KafkaConsumer
import threading
import sys
from Crypto.PublicKey import RSA
from Crypto import Random

name = sys.argv[1]
topic = sys.argv[2]
othername = sys.argv[3]

l = []
keyTop = "42aa600bb7fcb6b3e5e8dfd3f246b4f0"

from tkinter import *

class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    S = Scrollbar(master)
    T = Text(master, height=30, width=100)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """Welcome to CryptChat."""
    T.insert(END, quote)
    self.T = T
    self.entry = Entry(master)
    self.entry.bind("<Return>", self.evaluate)
    self.entry.pack()
    self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
  def send(self, msg, t = None, encode = True):
      if encode:
          self.add(msg, False)
          print(pub_key2.exportKey())
          msg = pub_key2.encrypt(msg.encode(), 32)
          print(msg)
          msg = msg[0]
      if t == None:
          t = topic + name
      print("here", msg)
      self.producer.send(t, msg)
  def evaluate(self, event):
      msg = name + ": " + self.entry.get()
      self.send(msg)
      self.entry.delete(0,END)
  def add(self, msg, decrypt = True):
      if decrypt:
          global key
          msgDecrypt = key.decrypt(msg.value)
          print(key.exportKey())
          print("msg", msg.value)
          print("msgDecrypt", msgDecrypt)
          msg = msgDecrypt.decode('utf-8')
      self.T.insert(END, "\n " + msg)
  def checkmsg(self):
      global l
      while len(l) > 0:
          msg = l.pop()
          self.add(msg)
  def write_slogan(self):
    self.T.insert(END, "\n Tkinter is easy to use!")

def checkForMessages(consumer):
    while True:
        #print("wow")
        global l
        msg = next(consumer)
        l.append(msg)
        #os.system("say "+msg.value.decode('utf-8'))

root = Tk()
app = App(root)
print("Welcome to CryptChat " + name)
print("Generating RSA key...")
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
pub_key = key.publickey()
print("Sending Key..."+topic+"key"+keyTop+name)
app.send(pub_key.exportKey(), topic+"key"+keyTop+name, False)
print("Waiting For Key..."+topic+"key"+keyTop+othername)
cons = KafkaConsumer(topic+"key"+keyTop+othername, bootstrap_servers='localhost:9092', group_id=None, auto_offset_reset='earliest')

pub_key_ofOther = next(cons)
print("debug")
print(pub_key_ofOther.value)
print(pub_key.exportKey())
pub_key2 = RSA.importKey(pub_key_ofOther.value)
print("Got Key.")

consumer = KafkaConsumer(topic+othername, bootstrap_servers='localhost:9092')
thr = threading.Thread(target=checkForMessages, args=(consumer,))
thr.start()
while True:
    root.update_idletasks()
    root.update()
    app.checkmsg()
