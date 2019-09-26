#!/usr/bin/env python3
# coding:utf-8

''' contentprovider.py '''



import struct
from socket import *


#SERV_IP   = "localhost"
SERV_IP   = "172.16.27.126"
SERV_PORT = 8000
SERVER    = (SERV_IP, SERV_PORT)




class ContentProvider():
  '''
  Поставщик контента
  Подключается к источнику данных по TCP/IP и получает от него содержимое его памяти  
  '''


  def __init__(self):
    self.socket = socket(AF_INET, SOCK_STREAM)
    self.socket.connect(SERVER)


    
  def __del__(self):
    self.socket.close()
    self.socket = None



  def getContent(self, start:int=0x20000000, length:int=0x10000) -> b'':
    '''
    Запрашивает источник данных.
    start - начальный адрес данных
    length - длина (в байтах)
    '''
    self.start    = start
    self.length   = length
  
    requestpacket = struct.pack("<II", self.start, self.length)
    self.socket.send(requestpacket)    

    #print("Отправлен запрос")

    answer = []
    demandedLength = self.length
    
    while demandedLength > 0:
      #print("Ожидаем {} байт".format(demandedLength))
      chunk = self.socket.recv(demandedLength)
      
      if chunk == None and chunk == b'':
        print(':(')
        return None
      
      if len(chunk) > 0:
        #print("Принято {0:} байт".format(chunkLength))
        demandedLength -= len(chunk)
        answer += chunk

    return answer



if __name__ == "__main__":
  pass
