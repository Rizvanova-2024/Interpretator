from enum import Enum

class States(Enum):
    NONE        = 0,
    IF          = 1,
    REPEAT      = 2,
    PROCEDURE   = 3,

class CodeTranslator:
    variables : dict          = {}
    procedures: dict          = {}
    states    : list[States]  = []
    errFlag   : bool          = False

    def Run(self, code : str) -> str:
        code = code.replace('\n', ' ').replace('\r', ' ')
        tokens = code.split(' ')
        while("" in tokens):
            tokens.remove("")

        return self.ParseTokens(tokens)

    def Clear(self):
        self.variables.clear()
        self.procedures.clear()
        self.states.clear()
        self.errFlag = False

    def ParseTokens(self, tokens : list[str], start: int = 0) -> str:
        result : str = ''
        if len(self.states) > 3:
            self.errFlag = True
            return '<font color="#f00">Ошибка</font>: Уровень вложенности команд превысил 3!<br />', -1

        for i in range(len(tokens)):
            if i < start:
                continue
            # RIGHT
            if tokens[i] == "RIGHT":
                # IMMEDIATE
                if tokens[i + 1].isnumeric():
                    for j in range(int(tokens[i + 1])):
                        result += 'r'
                    start = i + 2
                # VARIABLE
                elif tokens[i + 1] in self.variables:
                    for j in range(int(self.variables[tokens[i + 1]])):
                        result += 'r'
                    start = i + 2
                else:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Недопустимое число итераций в команде RIGHT: {tokens[i + 1]}<br>', -1
                continue
            # DOWN
            if tokens[i] == "DOWN":
                # IMMEDIATE
                if tokens[i + 1].isnumeric():
                    for j in range(int(tokens[i + 1])):
                        result += 'd'
                    start = i + 2
                # VARIABLE
                elif tokens[i + 1] in self.variables:
                    for j in range(int(self.variables[tokens[i + 1]])):
                        result += 'd'
                    start = i + 2
                else:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Недопустимое число итераций в команде DOWN: {tokens[i + 1]}<br>', -1
                continue
            # LEFT
            if tokens[i] == "LEFT":
                # IMMEDIATE
                if tokens[i + 1].isnumeric():
                    for j in range(int(tokens[i + 1])):
                        result += 'l'
                    start = i + 2
                # VARIABLE
                elif tokens[i + 1] in self.variables:
                    for j in range(int(self.variables[tokens[i + 1]])):
                        result += 'l'
                    start = i + 2
                else:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Недопустимое число итераций в команде LEFT: {tokens[i + 1]}<br>', -1
                continue
            # UP
            if tokens[i] == "UP":
                # IMMEDIATE
                if tokens[i + 1].isnumeric():
                    for j in range(int(tokens[i + 1])):
                        result += 'u'
                    start = i + 2
                # VARIABLE
                elif tokens[i + 1] in self.variables:
                    for j in range(int(self.variables[tokens[i + 1]])):
                        result += 'u'
                    start = i + 2
                else:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Недопустимое число итераций в команде UP: {tokens[i + 1]}<br>', -1
                continue
            # SET
            if tokens[i] == "SET":
                if tokens[i + 2] != '=':
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Синтаксис команды SET: SET <переменная> = <значение><br>', -1
                self.variables[tokens[i + 1]] = int(tokens[i + 3])
                start = i + 4
                continue
            # IFBLOCK
            if tokens[i] == "IFBLOCK":
                if tokens[i + 1] == "RIGHT":
                    self.states.append(States.IF)
                    ret, off = self.ParseTokens(tokens, i + 2)
                    if self.errFlag:
                        return ret, off
                    result += 'R' + ret + '.'
                    start = off + 1
                    self.states.pop()
                    continue
                if tokens[i + 1] == "DOWN":
                    self.states.append(States.IF)
                    ret, off = self.ParseTokens(tokens, i + 2)
                    if self.errFlag:
                        return ret, off
                    result += 'D' + ret + '.'
                    start = off + 1
                    continue
                if tokens[i + 1] == "LEFT":
                    self.states.append(States.IF)
                    ret, off = self.ParseTokens(tokens, i + 2)
                    if self.errFlag:
                        return ret, off
                    result += 'L' + ret + '.'
                    start = off + 1
                    continue
                if tokens[i + 1] == "UP":
                    self.states.append(States.IF)
                    ret, off = self.ParseTokens(tokens, i + 2)
                    if self.errFlag:
                        return ret, off
                    result += 'U' + ret + '.'
                    start = off + 1
                    continue
                self.errFlag = True
                return f'<font color="#f00">Ошибка</font>: Неизвестное направление в команде IFBLOCK: {tokens[i + 1]}<br>', -1
            # ENDIF
            if tokens[i] == "ENDIF":
                if len(self.states) == 0 or self.states[-1] != States.IF:
                    self.errFlag = True
                    return '<font color="#f00">Ошибка</font>: Встретился команда "ENDIF" без предваряющей команды IF!<br>', -1
                return result, i
            # REPEAT
            if tokens[i] == "REPEAT":
                numIters = 0
                if tokens[i + 1].isnumeric():
                    numIters = int(tokens[i + 1])
                elif tokens[i + 1] in self.variables:
                    numIters = int(self.variables[tokens[i + 1]])
                else:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Неизвестный идентификатор итераций команды REPEAT: {tokens[i + 1]}<br>', -1
                self.states.append(States.REPEAT)
                ret, off = self.ParseTokens(tokens, i + 2)
                if self.errFlag:
                    return ret, off
                for j in range(numIters):
                    result += ret
                start = off + 1
                self.states.pop()
                continue
            # ENDIF
            if tokens[i] == "ENDREPEAT":
                if len(self.states) == 0 or self.states[-1] != States.REPEAT:
                    self.errFlag = True
                    return '<font color="#f00">Ошибка</font>: Встретилась команда "ENDREPEAT" без предваряющей команды REPEAT!<br>', -1
                return result, i
            # PROCEDURE
            if tokens[i] == "PROCEDURE":
                if len(self.states) != 0:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Нельзя объявить процедуру внутри блока.<br>', -1
                if tokens[i + 1] in self.procedures:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Процедура с именем {tokens[i + 1]} уже была объявлена ранее.<br>', -1
                self.states.append(States.PROCEDURE)
                ret, off = self.ParseTokens(tokens, i + 2)
                if self.errFlag:
                    return ret, off
                self.procedures[tokens[i + 1]] = ret
                start = off + 1
                self.states.pop()
                continue
            # ENDPROC
            if tokens[i] == "ENDPROC":
                if len(self.states) == 0 or self.states[-1] != States.PROCEDURE:
                    self.errFlag = True
                    return '<font color="#f00">Ошибка</font>: Встретилась команда "ENDPROC" без предваряющей команды PROCEDURE!<br>', -1
                return result, i
            # CALL
            if tokens[i] == "CALL":
                if not tokens[i + 1] in self.procedures:
                    self.errFlag = True
                    return f'<font color="#f00">Ошибка</font>: Вызывается процедура {tokens[i + 1]}, которая не была объявлена ранее.<br>', -1
                result += self.procedures[tokens[i + 1]]
                start = i + 2
                continue
            
            # Any other
            self.errFlag = True
            return f'<font color="#f00">Ошибка</font>: Неизвестная команда: {tokens[i]}<br>', -1
    

        return result, 0
                    
