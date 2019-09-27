#!/usr/bin/env python3
# coding:utf-8

''' memframe.py '''


import random

from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtGui     import (QPainter, QPalette, QPen, QColor, QFont)
from PyQt5.QtCore    import (Qt, QRect)



# Смещение изображения памяти
X0 = 50
Y0 = 50

# Размер картинки отображения памяти
IMAGEWIDTH  = 256
IMAGEHEIGHT = 256



class MemFrame(QWidget):
  '''
  Квадрат изображения
  '''


  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.content     = None
    self.prevContent = None

    self.mode = 1
    self.modeSelector = {0:self.showNothing, 1:self.showInColor, 2:self.showInBw, 3:self.showChanges, 4:self.showUsing}

    self.address = ""

    self.setFixedSize(X0 + IMAGEWIDTH + 35, Y0 + IMAGEHEIGHT + 20)



  def paintEvent(self, e):
    '''
    Подновляет (рисует) изображение памяти по-пиксельно
    '''
    
    qp = QPainter()
    qp.begin(self)

    # Подписываем адреса
    qp.setFont(QFont('DejaVu Sans Bold', 12, QFont.Bold))
    #qp.setPen(QColor("Blue"))
    rect = QRect(X0 + 0x80 - 60, 0, 120, 20)
    #qp.drawRect(rect)
    qp.drawText(rect, (Qt.AlignVCenter | Qt.AlignHCenter), self.address)

    qp.setFont(QFont('DejaVu Sans', 10))
    #qp.setPen(QColor("Black"))

    # Верхняя шкала
    qp.drawLine(X0,         Y0 - 2, X0,         Y0 - 7)
    qp.drawLine(X0 + 0x40,  Y0 - 2, X0 + 0x40,  Y0 - 7)
    qp.drawLine(X0 + 0x80,  Y0 - 2, X0 + 0x80,  Y0 - 7)
    qp.drawLine(X0 + 0xC0,  Y0 - 2, X0 + 0xC0,  Y0 - 7)
    qp.drawLine(X0 + 0x100, Y0 - 2, X0 + 0x100, Y0 - 7)
    
    rect = QRect(0, Y0 - 25, 35, 14)
    rect.moveLeft(X0 - 17)
    qp.drawText(rect, (Qt.AlignBottom | Qt.AlignHCenter), "0")
    rect.moveLeft(X0 - 17 + 0x40)
    qp.drawText(rect, (Qt.AlignBottom | Qt.AlignHCenter), "40")
    rect.moveLeft(X0 - 17 + 0x80)
    qp.drawText(rect, (Qt.AlignBottom | Qt.AlignHCenter), "80")
    rect.moveLeft(X0 - 17 + 0xC0)
    qp.drawText(rect, (Qt.AlignBottom | Qt.AlignHCenter), "C0")
    rect.moveLeft(X0 - 17 + 0x100)
    qp.drawText(rect, (Qt.AlignBottom | Qt.AlignHCenter), "100")
    #qp.drawRect(rect)

    # Левая шкала
    qp.drawLine(X0 - 7, Y0,         X0 - 2, Y0)
    qp.drawLine(X0 - 7, Y0 + 0x40,  X0 - 2, Y0 + 0x40)
    qp.drawLine(X0 - 7, Y0 + 0x80,  X0 - 2, Y0 + 0x80)
    qp.drawLine(X0 - 7, Y0 + 0xC0,  X0 - 2, Y0 + 0xC0)
    qp.drawLine(X0 - 7, Y0 + 0x100, X0 - 2, Y0 +0x100)
    
    rect = QRect(0, 0, 40, 14)
    rect.moveTop(Y0 - 7)
    qp.drawText(rect, (Qt.AlignRight | Qt.AlignVCenter), "0")
    rect.moveTop(Y0 - 7 + 0x40)
    qp.drawText(rect, (Qt.AlignRight | Qt.AlignVCenter), "4000")
    rect.moveTop(Y0 - 7 + 0x80)
    qp.drawText(rect, (Qt.AlignRight | Qt.AlignVCenter), "8000")
    rect.moveTop(Y0 - 7 + 0xC0)
    qp.drawText(rect, (Qt.AlignRight | Qt.AlignVCenter), "C000")
    rect.moveTop(Y0 - 7 + 0x100)
    qp.drawText(rect, (Qt.AlignRight | Qt.AlignVCenter), "10000")
 
    if self.content == None:
      qp.end()
      return
  
    try:
      self.modeSelector.get(self.mode, self.showNothing)(qp)
    except IndexError:
      pass

    qp.end()



  def newContent(self, content, startaddress):
    '''
    Принимает новое значение содержимого памяти
    '''
    self.address = "0x{:08X}".format(startaddress)
    
    if self.content != None:
      self.prevContent = self.content[:]
    self.content = content
    self.update()



  def setMode(self, mode):
    self.mode = mode


  def showInColor(self, qp):
    '''
    Это цветное изображение памяти
    '''
    for y in range(256):
      for x in range(256):
        c = self.content[y * 256 + x]
        r = (c & 0xE0)
        g = (c & 0x1C) << 3
        b = (c & 0x03) << 6
        qp.setPen(QPen(QColor(r, g, b)))
        qp.drawPoint(X0 + x, Y0 + y)



  def showInBw(self, qp):
    '''
    Это ч/б изображение памяти
    '''
    for y in range(256):
      for x in range(256):
        if self.content[y * 256 + x] == 0x00:
          qp.setPen(Qt.black)
        else:
          qp.setPen(Qt.lightGray)
        
        qp.drawPoint(X0 + x, Y0 + y)


  def showChanges(self, qp):
    '''
    Отмечает изменения относительно предыдущего состояния памяти
    '''
    if self.prevContent == None:
      for y in range(256):
        for x in range(256):
          if self.content[y * 256 + x] == 0xFF:
            qp.setPen(Qt.black)
          else:
            qp.setPen(Qt.lightGray)
      
          qp.drawPoint(X0 + x, Y0 + y)
    else:
      for y in range(256):
        for x in range(256):
          if (self.content[y * 256 + x]) == (self.prevContent[y * 256 + x]):
            qp.setPen(Qt.black)
          else:
            qp.setPen(Qt.green)

          qp.drawPoint(X0 + x, Y0 + y)


  def showUsing(self, qp):
    '''
    Накапливает изменения состояния памяти
    '''
    pass
    

  def showNothing(self, qp):
    pass




if __name__ == "__main__":
  pass
