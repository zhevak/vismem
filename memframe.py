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
    self.content = None
    self.setFixedSize(X0 + IMAGEWIDTH + 35, Y0 + IMAGEHEIGHT + 20)

    self.address = ""


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

      for y in range(256):
        for x in range(256):
          c = self.content[y * 256 + x]
          r = (c & 0xE0)
          g = (c & 0x1C) << 3
          b = (c & 0x03) << 6
          qp.setPen(QPen(QColor(r, g, b)))
          qp.drawPoint(X0 + x, Y0 + y)

      '''
      Это ч/б изображение памяти
      qp.setPen(Qt.darkGray)

      for y in range(256):
        for x in range(256):
          if self.content[y * 256 + x] != 0x00:
            qp.drawPoint(x, y)
      '''      

    except IndexError:
      pass

    qp.end()



  def newContent(self, content, startaddress):
    '''
    Принимает новое значение содержимого памяти
    '''
    self.address = "0x{:08X}".format(startaddress)
    self.content = content
    self.update()



if __name__ == "__main__":
  pass
