from PyQt5.QtWidgets import ( 
    QMainWindow, 
    QWidget, 
    QAction, 
    qApp,
    QFileDialog,
    QTextEdit )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

from FieldPainter import FieldPainter
from CodeEditor   import CodeEditor
from CodeTranslator   import CodeTranslator

class MainWindow(QMainWindow):
    codeToExecute : str = ''
    codeIP        : int = 0
    codeTimer     : QTimer = None
    fileName      : str = ''
    def __init__(self, parent : QWidget = None):
        super().__init__(parent)
        self.InitGUI()
        self.InitBars()
        self.codeTimer = QTimer()
        self.codeTimer.timeout.connect(self.MakeCodeStep)

    def InitGUI(self):
        self.resize(880, 610)
        self.move(300, 300)
        self.setWindowTitle('Среда разработки GridMaster')

        self.code = CodeEditor(self)
        self.drp  = FieldPainter(self)
        self.log  = QTextEdit(self)
        self.log.move(10, 490)
        self.log.resize(860, 100)
        self.log.setStyleSheet("""QTextEdit{
	        font-family:'Consolas'; 
            font-size: 12px;}""")

        self.show()

    def InitBars(self):
        # Actions
        actFileOpen = QAction(QIcon('icons/file-open.png'), '&Открыть...', self)
        actFileOpen.setShortcut('Ctrl+O')
        actFileOpen.setStatusTip('Открыть файл с кодом для исполнения')
        actFileOpen.triggered.connect(self.OnMenuFileOpen)

        actFileSave = QAction(QIcon('icons/file-save.png'), '&Сохранить', self)
        actFileSave.setShortcut('Ctrl+S')
        actFileSave.setStatusTip('Сохранить текущий код')
        actFileSave.triggered.connect(self.OnMenuFileSave)

        actFileSaveAs = QAction('&Сохранить как...', self)
        actFileSaveAs.setShortcut('Ctrl+Shift+S')
        actFileSaveAs.setStatusTip('Сохранить код в новый файл')
        actFileSaveAs.triggered.connect(self.OnMenuFileSaveAs)

        actFileExit = QAction(QIcon('icons/app-exit.png'), '&Выход', self)
        actFileExit.setShortcut('Alt+X')
        actFileExit.setStatusTip('Завершить раоту программы GridMaster')
        actFileExit.triggered.connect(qApp.quit)

        actCodeRun = QAction(QIcon('icons/code-run.png'), '&Запустить', self)
        actCodeRun.setShortcut('F5')
        actCodeRun.setStatusTip('Начать выполнение кода')
        actCodeRun.triggered.connect(self.OnMenuCodeRun)

        actCodeStop = QAction(QIcon('icons/code-stop.png'), '&Остановить', self)
        #actCodeStop.setShortcut('')
        actCodeStop.setStatusTip('Остановить выполнение кода')
        actCodeStop.triggered.connect(self.OnMenuCodeStop)

        # Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(actFileOpen)
        fileMenu.addSeparator()
        fileMenu.addAction(actFileSave)
        fileMenu.addAction(actFileSaveAs)
        fileMenu.addSeparator()
        fileMenu.addAction(actFileExit)
        codeMenu = menubar.addMenu('&Код')
        codeMenu.addAction(actCodeRun)
        codeMenu.addSeparator()
        codeMenu.addAction(actCodeStop)
    
        # Toolbar
        toolbar = self.addToolBar('Главный')
        toolbar.addAction(actFileOpen)
        toolbar.addAction(actFileSave)
        toolbar.addSeparator()
        toolbar.addAction(actCodeRun)
        toolbar.addAction(actCodeStop)
    
        # Statusbar
        self.statusBar().showMessage('Готов')

    def OnMenuFileOpen(self):
      fname = QFileDialog.getOpenFileName(self, "Открыть код", "examples", "Файлы с кодом (*.txt);;Все файлы(*.*)")
      if fname[0] and len(fname[0]) > 0:
        self.fileName = fname[0]
        infile = open(self.fileName, 'r')
        self.code.setPlainText(infile.read())

    def OnMenuFileSave(self):
        if self.fileName == '':
            self.OnMenuFileSaveAs()
            return
        with open(self.fileName, 'w') as file:
            file.write(self.code.toPlainText())
        self.log.insertHtml(f'<font color="#0a0">Данные сохранены</font> в файл {self.fileName}.<br>')

    def OnMenuFileSaveAs(self):
      fname = QFileDialog.getSaveFileName(self, "Сохранить код", "examples", "Файлы с кодом (*.txt);;Все файлы(*.*)")
      if fname[0] and len(fname[0]) > 0:
        self.fileName = fname[0]
        self.OnMenuFileSave()
          

    def OnMenuCodeRun(self):
        translator = CodeTranslator()
        text,retCode = translator.Run(self.code.toPlainText())
        translator.Clear()
        if retCode == -1:
            self.log.insertHtml(text)
            return
        self.drp.Reset()
        self.log.insertHtml('=== Начато выполнение кода ===<br>')
        self.codeToExecute = text
        self.codeTimer.start(500)

    def OnMenuCodeStop(self):
        self.StopCodeExecution()

    def StopCodeExecution(self): 
        if self.codeTimer.isActive():
            self.codeTimer.stop()
            self.codeIP = 0
            self.codeToExecute = ''
            self.log.insertHtml('<font color="#900">Выполнение кода остановлено!</font><br>')

    def MakeCodeStep(self):
        if self.codeToExecute == '':
            return
        
        if self.codeToExecute[self.codeIP] == '.':
            self.codeIP += 1

        if self.codeToExecute[self.codeIP] == 'r':
            if self.drp.CanMoveRight():
                self.drp.MoveRight()
            else:
                self.log.insertHtml('<font color="#f00">Ошибка</font> Наткнулся на границу при перемещении вправо.<br>')
                self.StopCodeExecution()
                return
        elif self.codeToExecute[self.codeIP] == 'd':
            if self.drp.CanMoveDown():
                self.drp.MoveDown()
            else:
                self.log.insertHtml('<font color="#f00">Ошибка</font> Наткнулся на границу при перемещении вниз.<br>')
                self.StopCodeExecution()
                return
        elif self.codeToExecute[self.codeIP] == 'l':
            if self.drp.CanMoveLeft():
                self.drp.MoveLeft()
            else:
                self.log.insertHtml('<font color="#f00">Ошибка</font> Наткнулся на границу при перемещении влево.<br>')
                self.StopCodeExecution()
                return
        elif self.codeToExecute[self.codeIP] == 'u':
            if self.drp.CanMoveUp():
                self.drp.MoveUp()
            else:
                self.log.insertHtml('<font color="#f00">Ошибка</font> Наткнулся на границу при перемещении вверх.<br>')
                self.StopCodeExecution()
                return

        elif self.codeToExecute[self.codeIP] == 'R':
            if self.drp.CanMoveRight():
                self.log.insertHtml('<font color="#a00">[IFBLOCK]</font> Границы справа нет. Пропускаю оператор IFBLOCK.<br>')
                while self.codeToExecute[self.codeIP] != '.':
                    self.codeIP += 1
            else:
                self.log.insertHtml('<font color="#0a0">[IFBLOCK]</font> Справа встретил границу. Исполняю оператор IFBLOCK.<br>')
        elif self.codeToExecute[self.codeIP] == 'L':
            if self.drp.CanMoveLeft():
                self.log.insertHtml('<font color="#a00">[IFBLOCK]</font> Границы слева нет. Пропускаю оператор IFBLOCK.<br>')
                while self.codeToExecute[self.codeIP] != '.':
                    self.codeIP += 1
            else:
                self.log.insertHtml('<font color="#0a0">[IFBLOCK]</font> Слева встретил границу. Исполняю оператор IFBLOCK.<br>')
        elif self.codeToExecute[self.codeIP] == 'U':
            if self.drp.CanMoveUp():
                self.log.insertHtml('<font color="#a00">[IFBLOCK]</font> Границы сверху нет. Пропускаю оператор IFBLOCK.<br>')
                while self.codeToExecute[self.codeIP] != '.':
                    self.codeIP += 1
            else:
                self.log.insertHtml('<font color="#0a0">[IFBLOCK]</font> Сверху встретил границу. Исполняю оператор IFBLOCK.<br>')
        elif self.codeToExecute[self.codeIP] == 'D':
            if self.drp.CanMoveDown():
                self.log.insertHtml('<font color="#a00">warning [IFBLOCK]</font> Границы снизу нет. Пропускаю оператор IFBLOCK.<br>')
                while self.codeToExecute[self.codeIP] != '.':
                    self.codeIP += 1
            else:
                self.log.insertHtml('<font color="#0a0">[IFBLOCK]</font> Снизу встретил границу. Исполняю оператор IFBLOCK.<br>')

        self.codeIP += 1
        if self.codeIP >= len(self.codeToExecute):
            self.codeTimer.stop()
            self.codeIP = 0
            self.codeToExecute = ''
            self.log.insertHtml('<font color="#090">Выполнение кода завершено успешно!</font><br>')
        
if __name__ == "__main__":
    print('This module can\'t be executed')
    exit(1)