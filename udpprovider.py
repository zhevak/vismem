#!/usr/bin/env python3
# coding:utf-8

''' udpprovider.py '''



import struct
from socket import *



#SERV_IP   = "localhost"
SERV_IP   = "172.16.27.126"
SERV_PORT = 8000
SERVER    = (SERV_IP, SERV_PORT)

CHUNKSIZE = 512


class UdpProvider:
  '''
  Обеспечивает получение даных из микроконтроллера по протоколу UDP/IP
  '''
  
  def __init__(self):
    self.socket = socket(AF_INET, SOCK_DGRAM)
    self.socket.settimeout(0.01)  # время в секундах

 
  def __del__(self):
    self.socket.close()
    self.socket = None



  def getChunk(self, address, length):
    '''
    Читает кусок памяти из микроконтроллера
    Возвращает либо считанный кусок памяти, либо None
    '''
    attempt = 10  # Даётся всего 10 попыток прочитать
    #print("Адрес {0:08X}, размер {1:}".format(address, length))
    while (attempt > 0):
      #print("Попытка {}".format(10 - attempt))
      try:
        req = struct.pack("<II", address, CHUNKSIZE)
        self.socket.sendto(req, SERVER)                     # Запрос
        chunk, server = self.socket.recvfrom(CHUNKSIZE)     # Ответ

        '''
        Этот код не работает. По какой-то причине ССистема не знает такого
        исключения -- socket.timeout.
        
      except socket.timeout:  # Превышение времени ожидания ответа
        print("EXCEPT", socket.timeout)
        attempt -= 1
        '''

      except:
        attempt -= 1
        print("Осталось попыток {}".format(attempt))
        print("EXCEPT")
      
      else:
        #print("OK")
        return chunk

    return None
    


  def getContent(self, start:int, length:int) -> b'':
    '''
    Запрашивает источник данных.
    start - начальный адрес данных
    length - длина (в байтах)
    '''
    address = start
    length  = length
   
    answer = []  # Запрошенный объём памяти
    
    # Читаем куски по 512 байт
    while length >= CHUNKSIZE:
      chunk = self.getChunk(address, CHUNKSIZE)

      if chunk == None and chunk == b'':
        print(':(')
        return None
      
      if len(chunk) > 0:
        answer += chunk
      else:
        print("0000")

      address += CHUNKSIZE
      length  -= CHUNKSIZE

    
    # Читаем последний кусок (меньше 512 байт)
    if length > 0:
      chunk = self.getChunk(address, length)
      
      if chunk == None and chunk == b'':
        print(':(')
        return None
      
      if len(chunk) > 0:
        answer += chunk

    print()
    return answer



if __name__ == "__main__":
  pass
