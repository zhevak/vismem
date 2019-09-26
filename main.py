#!/usr/bin/env python3
# coding:utf-8

''' main.py '''


import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QToolTip, QVBoxLayout)
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
START = 0x20000000
#START = 0x20010000
#START = 0x20020000


class MainWindow(QWidget):

  def __init__(self, contentProvider):
    QWidget.__init__(self)

    self.setWindowTitle("Визуализатор содержимого памяти")
    self.setToolTip("Байты, со значением равным 0x00, отображаются белым цветом, остальные -- серым")
    QToolTip.setFont(QFont("SansSerif", 8))

    self.contentProvider = contentProvider

    self.memFrame = MemFrame()

    vbox = QVBoxLayout()
    vbox.addWidget(self.memFrame)
    self.setLayout(vbox)


  def onTimer(self):
    '''
    Периодически опрашивает источник данных провайдера и отображает полученный контент
    '''
    #print("onTimer()")
    content = self.contentProvider.getContent(START, LENGTH)
    #print("CONTENT:\n{}\n\n".format(content))
    self.memFrame.newContent(content, )

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
