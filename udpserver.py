#!/usr/bin/env python3
# coding:utf-8

''' udpserver.py -- эмулятор микроконтроллера

Эмулятор получает запросы от программы Визуализатора и передаёт ему массив байтов.
Байты создаются генератором случайных чисел.

Эмулятор получает от Визуализатора начальный адрес и количество байт памяти.
(Начальный адрес в эмуляторе не используется.)

Эмулятор работает по протоколу UPD.

'''


import random

import time
import struct
from socket import *
from multiprocessing import Process


CLIENTS_IP = "0.0.0.0"
SERV_PORT  = 8000
SERVER = (CLIENTS_IP, SERV_PORT)




if __name__ == "__main__":

  socket = socket(AF_INET, SOCK_DGRAM)
  socket.bind(SERVER)
  
  while True:
    data, client = socket.recvfrom(1024)
    #print("Message: ", data, client)
    
    addr, length = struct.unpack("<II", data)
    
    content = bytearray(length)
    for i in range(length):
      content[i] = random.randint(0, 255)
    
    socket.sendto(content, client)
    
    
    

