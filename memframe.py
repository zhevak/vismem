#!/usr/bin/env python3
# coding:utf-8

''' memframe.py '''


import random

from PyQt5.QtWidgets import (QWidget, QFrame)
from PyQt5.QtGui     import (QPainter, QPalette, QPen, QColor)
from PyQt5.QtCore    import Qt


class MemFrame(QWidget):

  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.content = None
    self.setFixedSize(256, 256)



  def paintEvent(self, e):
    if self.content == None:
      return
 
    try:
      qp = QPainter()
      qp.begin(self)
      

      for y in range(256):
        for x in range(256):
          c = self.content[y * 256 + x]
          r = (c & 0xE0)
          g = (c & 0x1C) << 3
          b = (c & 0x03) << 6
          #print("{0:} {1:} {2:}".format(r, g, b))
          qp.setPen(QPen(QColor(r, g, b)))
          qp.drawPoint(x, y)

      '''
      qp.setPen(Qt.darkGray)

      for y in range(256):
        for x in range(256):
          if self.content[y * 256 + x] != 0x00:
            qp.drawPoint(x, y)
      '''      
      qp.end()

    except IndexError:
      pass



  def newContent(self, content):    
    #print(content)
    self.content = content
    self.update()



if __name__ == "__main__":
  pass
