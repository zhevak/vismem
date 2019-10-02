#!/usr/bin/env python3
# coding:utf-8

''' magnify.py '''


from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtGui     import (QPainter, QPalette, QPen, QColor, QFont)
from PyQt5.QtCore    import (Qt, pyqtSignal, QRect, QPoint)



# Смещение таблицы значений
X0 = 40
Y0 = 32
dX = 25
dY = 16


class Magnify(QWidget):
  '''
  Показывает увеличенный фрагмент памяти
  '''
  
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.setFixedSize(250, 180)
    self.startAddress = None
    self.content      = None



  def setStartAddress(self, startAddress):
    '''
    Устанавливает значение стартового адреса для левой верхней ячейки
    startaddress -- начальный адрес (левый верхний угол)
    '''
    self.startAddress = startAddress
    


  def setContent(self, newContent):
    '''
    Обновляет отображение фрагмента
    content -- содержимое памяти для отображения в HEX-виде
    '''
    
    '''
    for y in range(7):
      for x in range(7):
        print("{:02X}".format(newContent[y][x]), end=" ")
      print()
    print()
    '''
    self.content = newContent[:]
    self.update()
    
    
  
  def paintEvent(self, e):
    '''
    Подновляет (рисует) изображение памяти по-пиксельно
    '''
    if self.startAddress == None:
      return
     
    qp = QPainter()
    qp.begin(self)

    # Подписываем адреса    
    qp.setFont(QFont('DejaVu Sans Bold', 10, QFont.Bold))
    rect = QRect(X0, 0, (dX * 7), dY)
    #qp.drawRect(rect)
    addr = ((self.startAddress ) >> 16) & 0xFFFF  # Берём только цифры ZZZZ....
    txt = "{:04X}".format(addr)
    qp.drawText(rect, (Qt.AlignVCenter | Qt.AlignHCenter), txt)
    
    qp.setFont(QFont('DejaVu Sans', 10))
    for y in range(7):
      rect = QRect(0, (y * dY + Y0), X0, dY)
      #qp.drawRect(rect)
      addr = ((self.startAddress + y * 256) >> 8) & 0xFF  # Берём только цифры ....YY..
      txt = "{:02X}xx".format(addr)
      qp.drawText(rect, (Qt.AlignVCenter | Qt.AlignHCenter), txt)
    
    for x in range(7):
      rect = QRect((x * dX + X0), (Y0 - dY), dX, dY)
      #qp.drawRect(rect)
      addr = (self.startAddress + x) & 0xFF  # Берём только цифры ......XX
      txt = "{:02X}".format(addr)
      qp.drawText(rect, (Qt.AlignVCenter | Qt.AlignHCenter), txt)
    
    #qp.setFont(QFont('DejaVu Sans', 10))
    for y in range(7):
      for x in range(7):
        rect = QRect((x * dX + X0), (y * dY + Y0), dX, dY)
        qp.drawRect(rect)
        
        if self.content != None:
          txt = "{:02X}".format(self.content[y][x])
          qp.drawText(rect, (Qt.AlignVCenter | Qt.AlignHCenter), txt)

    #qp.setFont(QFont('DejaVu Sans Bold', 10, QFont.Bold))
    #qp.setPen(QColor("Blue"))
    # qp.drawText(rect, Qt.Alignment((Qt.AlignVCenter | Qt.AlignHCenter)), self.startAddress)

    #qp.setPen(QColor("Black"))
    
    
    qp.end()




if __name__ == "__main__":
  pass
  
