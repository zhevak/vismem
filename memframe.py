#!/usr/bin/env python3
# coding:utf-8

''' memframe.py '''


from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtGui     import (QPainter, QPalette, QPen, QColor, QFont)
from PyQt5.QtCore    import (Qt, pyqtSignal, QRect, QPoint)



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

  magnifyPositionChanged = pyqtSignal(QPoint)  # Сигнал с параметром


  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.content     = None
    self.prevContent = None

    self.mode = 1
    self.modeSelector = {1:self.showInColor, 2:self.showInBw, 3:self.showChanges, 4:self.showUsing}

    self.startAddress = 0
    self.address = ""

    self.setFixedSize(X0 + IMAGEWIDTH + 35, Y0 + IMAGEHEIGHT + 20)
    self.mouseTracking = True    



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
      self.modeSelector.get(self.mode)(qp)
    except IndexError:
      pass

    qp.end()



  def setStartAddress(self, startAddress):
    '''
    Устанавливает новое значение начального адреса
    '''
    self.startAddress = startAddress
    self.address = "0x{:08X}".format(startAddress)
 


  def setContent(self, content):
    '''
    Принимает новое значение содержимого памяти
    '''
    if self.content != None:
      self.prevContent = self.content[:]
    self.content = content
    self.update()



  def setMode(self, mode):
    self.mode = mode
    
    if mode == 4:
      # Только для перехода в режим накопления изменений
      self.clearAccumulator()



  def showInColor(self, qp):
    '''
    Это цветное изображение памяти
    '''
    for y in range(256):
      for x in range(256):
        c = self.content[y * 256 + x]
        '''
        r = (c & 0xE0)
        g = (c & 0x1C) << 3
        b = (c & 0x03) << 6
        qp.setPen(QPen(QColor(r, g, b)))
        '''
        r = (c >> 5) & 0x07
        g = (c >> 2) & 0x07
        b = (c)      & 0x03
        qp.setPen(QColor(r << 5, g << 5, b << 6))

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
      # Первый раз
      for y in range(256):
        for x in range(256):
          if self.content[y * 256 + x] == 0xFF:
            # Содержимое памяти по этому адресу не изменилось
            qp.setPen(Qt.black)
          else:
            # Есть изменения содержимого памяти по этому адресу
            qp.setPen(Qt.grееn)
      
          qp.drawPoint(X0 + x, Y0 + y)
    else:
     # Второй и следущие разы
      for y in range(256):
        for x in range(256):
          if (self.content[y * 256 + x]) == (self.prevContent[y * 256 + x]):
            # Содержимое памяти по этому адресу не изменилось
            qp.setPen(Qt.black)
          else:
            # Есть изменения содержимого памяти по этому адресу
            qp.setPen(Qt.green)

          qp.drawPoint(X0 + x, Y0 + y)


  def showUsing(self, qp):
    '''
    Накапливает изменения состояния памяти
    '''
    if self.prevContent == None:
      # Первый раз
      for y in range(256):
        for x in range(256):
          if self.content[y * 256 + x] == 0xFF:
            # Содержимое памяти по этому адресу не изменилось
            qp.setPen(Qt.black)
          else:
            # Есть изменения содержимого памяти по этому адресу
            qp.setPen(Qt.green)
            self.accumulator[y * 256 + x] += 1            
      
          qp.drawPoint(X0 + x, Y0 + y)
    else:
     # Второй и следущие разы
      for y in range(256):
        for x in range(256):
          if (self.content[y * 256 + x]) == (self.prevContent[y * 256 + x]):
            # Содержимое памяти по этому адресу не изменилось
            if self.accumulator[y * 256 + x] == 0:
              # Изменений по этому адресу в прошлом не было
              qp.setPen(Qt.black)
            else:
              # В прошлом наблюдались изменения по этому адресу
              qp.setPen(Qt.gray)
          else:
            # Есть изменения содержимого памяти по этому адресу
            qp.setPen(Qt.green)
            self.accumulator[y * 256 + x] += 1
          
          qp.drawPoint(X0 + x, Y0 + y)
    

  
  def clearAccumulator(self):
    '''
    Обнуляет массив накопления изменений
    '''
    self.accumulator = [0 for i in range(IMAGEWIDTH * IMAGEHEIGHT)]



  def mousePressEvent(self, event):
    '''
    Обработчик щелчка мышкой по "квадрату"
    '''
    position = event.pos() - QPoint(X0 + 2, Y0 + 3)
    if (0 <= position.x() <= 255) and (0 <= position.y() <= 255):
      self.magnifyPositionChanged.emit(position)  # Отправляем сигнал



if __name__ == "__main__":
  pass
