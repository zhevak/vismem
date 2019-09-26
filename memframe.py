#!/usr/bin/env python3
# coding:utf-8

''' memframe.py '''


import random

from PyQt5.QtWidgets import (QWidget, QFrame)
from PyQt5.QtGui     import (QPainter, QPalette, QPen, QColor, QFont)
from PyQt5.QtCore    import Qt



# Смещение изображения памяти
X0 = 100
Y0 = 20

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
    self.setFixedSize(X0 + IMAGEWIDTH, Y0 + IMAGEHEIGHT)


  def paintEvent(self, e):
    '''
    Подновляет (рисует) изображение памяти по-пиксельно
    '''
    
    # Подписываем адреса
    qp = QPainter()
    qp.begin(self)      

    # qp.setPen(QColor("Green"))
    qp.setFont(QFont('DejaVu Sans', 10))
    qp.drawText(0, 0, X0, Y0, (Qt.AlignRight | Qt.AlignVCenter), "+0")
    qp.drawText(0, 0, X0, Y0 + 0x40, (Qt.AlignRight | Qt.AlignVCenter), "+4000")
    #qp.drawText(X0, Y0 + 0x80, Qt.AlignLeft, "+8000")
    #qp.drawText(X0, Y0 + 0xC0, Qt.AlignLeft, "+C000")
    #qp.drawText(X0, Y0 + 0x100, Qt.AlignLeft, "+10000")
 
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



  def newContent(self, content):
    '''
    Принимает новое значение содержимого памяти
    '''
    self.content = content
    self.update()



if __name__ == "__main__":
  pass
