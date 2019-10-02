#!/usr/bin/env python3
# coding:utf-8

''' main.py '''


import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QToolTip, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFrame, QPushButton, QRadioButton, QButtonGroup)
from PyQt5.QtGui     import QFont
from PyQt5.QtCore    import (QTimer, QPoint)

# from contentprovider import ContentProvider
from udpprovider import UdpProvider
from memframe    import MemFrame
from magnify     import Magnify

PERIOD = 1000

LENGTH = 0x10000

# Flash
#START = 0x08000000
#START = 0x08010000
#START = 0x08020000
#START = 0x08030000
#START = 0x08040000
#START = 0x08050000
#START = 0x08060000
#START = 0x08070000
#START = 0x08080000
#START = 0x08090000
#START = 0x080A0000
#START = 0x080B0000
#START = 0x080C0000
#START = 0x080D0000
#START = 0x080E0000
#START = 0x080F0000

# CCM RAM
#START = 0x10000000

# RAM
#START = 0x20000000
#START = 0x20010000
#START = 0x20020000



class MainWindow(QWidget):

  def __init__(self, contentProvider):
    QWidget.__init__(self)

    self.setWindowTitle("Визуализатор содержимого памяти")
    #self.setToolTip("Байты, со значением равным 0x00, отображаются белым цветом, остальные -- серым")
    QToolTip.setFont(QFont("SansSerif", 8))

    self.startaddress = 0x10000000
    self.magnifyOffset = 0
    self.mode = 0

    self.contentProvider = contentProvider
    self.memframe = MemFrame()
    self.memframe.magnifyPositionChanged.connect(self.onMagnifyPositionChanged)
    
    self.magnify = Magnify()
    
    self.btn1000 = QPushButton("0x10000000")
    self.btn2000 = QPushButton("0x20000000")
    self.btn2001 = QPushButton("0x20010000")
    self.btn2002 = QPushButton("0x20020000")

    self.btn1000.clicked.connect(self.on1000)
    self.btn2000.clicked.connect(self.on2000)
    self.btn2001.clicked.connect(self.on2001)
    self.btn2002.clicked.connect(self.on2002)
    
    self.rbColor   = QRadioButton("Цветное")
    self.rbBw      = QRadioButton("Чёрно/белое")
    self.rbChanges = QRadioButton("Изменения")
    self.rbUsing   = QRadioButton("Пользование")
    self.rbColor.setChecked(True)


    self.rbg = QButtonGroup()
    self.rbg.addButton(self.rbColor)
    self.rbg.addButton(self.rbBw)
    self.rbg.addButton(self.rbChanges)
    self.rbg.addButton(self.rbUsing)

    self.rbColor.toggled.connect(self.onColor)
    self.rbBw.toggled.connect(self.onBw)
    self.rbChanges.toggled.connect(self.onChanges)
    self.rbUsing.toggled.connect(self.onUsing)
    
    
    # Размещение виджетов на морде
    vbox1 = QVBoxLayout()
    vbox1.addWidget(self.memframe)
    
    vbox3 = QVBoxLayout()
    vbox3.addSpacing(50)
    vbox3.addWidget(self.btn1000)
    vbox3.addWidget(self.btn2000)
    vbox3.addWidget(self.btn2001)
    vbox3.addWidget(self.btn2002)
    vbox3.addStretch()
    
    vbox4 = QVBoxLayout()
    vbox4.addSpacing(50)
    vbox4.addWidget(self.rbColor)
    vbox4.addWidget(self.rbBw)
    vbox4.addWidget(self.rbChanges)
    vbox4.addWidget(self.rbUsing)
    vbox4.addStretch()

    hbox1 = QHBoxLayout()
    hbox1.addLayout(vbox3)
    hbox1.addLayout(vbox4)

    vbox2 = QVBoxLayout()
    vbox2.addLayout(hbox1)
    vbox2.addWidget(self.magnify)
    vbox2.addStretch()

    hbox0 = QHBoxLayout()
    hbox0.addLayout(vbox1)
    hbox0.addLayout(vbox2)
    hbox0.addStretch()
    
    self.setLayout(hbox0)
    
    #hbox0.addSpacing(30)
    #hbox0.addLayout(vbox3)


  def update(self):
    content = self.contentProvider.getContent(self.startaddress, LENGTH)
    if content != None:
      self.memframe.setContent(content)  # Подновим изображение "квадрата"

      # Подготовим массив значений из памяти для области увеличения (семь строк по семь значений)
      magnifyContent = [[], [], [], [], [], [], []]
      
      for y in range(7):
        x1 = self.magnifyOffset + (256 * y)
        x2 = x1 + 7
        magnifyContent[y] = content[x1:x2]
      
      self.magnify.setContent(magnifyContent)
    



  def onTimer(self):
    '''
    Периодически опрашивает источник данных провайдера и отображает полученный контент
    '''
    self.update()


  def on1000(self):
    self.startaddress = 0x10000000
    self.memframe.setStartAddress(self.startaddress)
    self.magnify.setStartAddress(self.startaddress)
    self.update()


  def on2000(self):
    self.startaddress = 0x20000000
    self.memframe.setStartAddress(self.startaddress)
    self.magnify.setStartAddress(self.startaddress)
    self.update()


  def on2001(self):
    self.startaddress = 0x20010000
    self.memframe.setStartAddress(self.startaddress)
    self.magnify.setStartAddress(self.startaddress)
    self.update()


  def on2002(self):
    self.startaddress = 0x20020000
    self.memframe.setStartAddress(self.startaddress)
    self.magnify.setStartAddress(self.startaddress)
    self.update()


  def onColor(self):
    if self.sender().isChecked():
      #print("Цвет")
      self.memframe.setMode(1)
    
    
  def onBw(self):
    if self.sender().isChecked():
      #print("Черно-белый")
      self.memframe.setMode(2)

    
  def onChanges(self):
    if self.sender().isChecked():
      #print("Изменения")
      self.memframe.setMode(3)

    
  def onUsing(self):
    if self.sender().isChecked():
      #print("Пользование")
      self.memframe.setMode(4)


  def onMagnifyPositionChanged(self, pos: QPoint):
    '''
    Обработчик измение адреса по указателю на "квадрате" памяти
    pos -- xy-координаты указателя на "квадрате" памяти
    '''
    #print(pos)
    
    # Крректируем позицию чтобы не вылезьти за края "квадрата"
    x0 = pos.x() - 3   # Смещение на три строки вверх
    y0 = pos.y() - 3   # Смещение на три строки влево

    if x0 < 0:
      x0 = 0

    if x0 > 249:
      x0 = 249

    if y0 < 0:
      y0 = 0
      
    if y0 > 249:
      y0 = 249

    self.magnifyOffset = y0 * 256 + x0  # Начальный адрес области увеличения    
    addr = self.startaddress + self.magnifyOffset
    #print("{:08X}".format(self.magnifyStartAddress))
    self.magnify.setStartAddress(addr)



if __name__ == "__main__":
  try:
    #contentProvider = ContentProvider()
    contentProvider = UdpProvider()
  except ConnectionRefusedError:
    print("Сервер не доступен.")
    sys.exit()

  app = QApplication(sys.argv)
  mainWnd = MainWindow(contentProvider)
  mainWnd.show()

  timer = QTimer()
  timer.timeout.connect(mainWnd.onTimer)
  timer.start(PERIOD)

  sys.exit(app.exec_())
