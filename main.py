#!/usr/bin/env python3
# coding:utf-8

''' main.py '''


import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QToolTip, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QRadioButton, QButtonGroup)
from PyQt5.QtGui     import QFont
from PyQt5.QtCore    import QTimer

# from contentprovider import ContentProvider
from udpprovider import UdpProvider
from memframe        import MemFrame


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
    self.setToolTip("Байты, со значением равным 0x00, отображаются белым цветом, остальные -- серым")
    QToolTip.setFont(QFont("SansSerif", 8))

    self.startaddress = 0x10000000
    self.mode = 0

    self.contentProvider = contentProvider
    self.memFrame = MemFrame()
    
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
    vbox1.addWidget(self.memFrame)
    
    vbox2 = QVBoxLayout()
    vbox2.addSpacing(50)
    vbox2.addWidget(self.btn1000)
    vbox2.addWidget(self.btn2000)
    vbox2.addWidget(self.btn2001)
    vbox2.addWidget(self.btn2002)
    vbox2.addStretch()
    
    vbox3 = QVBoxLayout()
    vbox3.addSpacing(50)
    vbox3.addWidget(self.rbColor)
    vbox3.addWidget(self.rbBw)
    vbox3.addWidget(self.rbChanges)
    vbox3.addWidget(self.rbUsing)
    vbox3.addStretch()


    hbox0 = QHBoxLayout()
    hbox0.addLayout(vbox1)
    hbox0.addLayout(vbox2)
    hbox0.addSpacing(30)
    hbox0.addLayout(vbox3)
    
    self.setLayout(hbox0)



  def update(self):
    content = self.contentProvider.getContent(self.startaddress, LENGTH)
    if content != None:
      self.memFrame.newContent(content, self.startaddress)



  def onTimer(self):
    '''
    Периодически опрашивает источник данных провайдера и отображает полученный контент
    '''
    self.update()


  def on1000(self):
    self.startaddress = 0x10000000
    self.update()


  def on2000(self):
    self.startaddress = 0x20000000
    self.update()


  def on2001(self):
    self.startaddress = 0x20010000
    self.update()


  def on2002(self):
    self.startaddress = 0x20020000
    self.update()


  def onColor(self):
    if self.sender().isChecked():
      #print("Цвет")
      self.memFrame.setMode(1)
    
  def onBw(self):
    if self.sender().isChecked():
      #print("Черно-белый")
      self.memFrame.setMode(2)

    
  def onChanges(self):
    if self.sender().isChecked():
      #print("Изменения")
      self.memFrame.setMode(3)

    
  def onUsing(self):
    if self.sender().isChecked():
      #print("Пользование")
      self.memFrame.setMode(4)

    
    
    

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
