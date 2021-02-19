from database import Database, Character
from functions import function, local

class Line:
    def __init__(self, line):
        self.line = line # The contents of the line of code
        self.skip = 1    # If the code evaluates to false, skip this many lines.
    
    def __repr__(self):
        line = self.line
        i = 0
        while i < len(line):
            if line[i] == '\n':
                line = line[:i] + line[i + 1:]
                i -= 1
            i += 1
        return "%s : %i" % (line, self.skip)

class Interpreter:

    def __init__(self, filename):
        self.parts    = []
        self.lines    = []
        self.sublines = []
        self.error    = None
        self.root     = "Sprint 2/story/"
        self.filename = filename

        local['file'       ] = filename
        local['db'         ] = Database()
        local['interpreter'] = self
        for character in local['db'].loadCharacters():
            local[character.name] = character

    def __repr__(self):
            return "Lines: \n%s\nParts:\n%s" % (self.lines, self.parts)
        
    def merge(self, delim):
        open = False
        hold = ''
        i    = len(self.parts) - 1
        while i >= 0:
            if self.parts[i] == delim:
                if open: 
                    open = False
                    del self.parts[i]
                    self.parts.insert(i, hold)
                    hold = ''
                else: 
                    open = True
                    del self.parts[i]
            elif open:
                hold = self.parts.pop(i) + hold
            i -= 1
        return not open
    
    def executeAt(self, location):
        try:
            if not self.parts[location + 1] in function: 
                self.error = 'Undefined Function'
                return 
            if self.parts[location + 2] != "(":
                self.error = 'Missing "(" in Function Call'
                return 
        except IndexError:
            self.error = 'Expected Function Call'
            return
        args = []
        while location + 3 < len(self.parts):
            if self.parts[location + 3] == ")": 
                del self.parts[location + 3]
                break
            args.append(self.parts.pop(location + 3))
        if location + 3 == len(self.parts) + 1:
            self.error = 'Missing Parenthetical'
            return 
        if len(args) != function[self.parts[location + 1]].argc:
            self.error = 'Unexptected Number of Arguments'
            return 
        return function[self.parts[location + 1]].func(args)

    def start(self):
        while self.filename != 'stop':
            self.filename = local['file']
            try:    self.readFile()
            except:
                print("Fatal Read Error with file %s." % self.filename)
                print("Debug Info: ")
                print(self)
                raise
            if self.error:
                print("Read error : %s" % (self.error))
                print("Debug Info: ")
                print(self)
                return 1
            i = 0
            while i < len(self.lines):
                if local['stop']: 
                    local['stop'] = False
                    break
                try: result = self.interpret(self.lines[i].line)
                except:
                    print("Fatal Error on line %i." % (i + 1))
                    print("Debug Info: ")
                    print(self)
                    raise
                if self.error:
                    print("Error on line %i : %s" % (i + 1, self.error))
                    print("Debug Info: ")
                    print(self)
                    return 1
                if not result: i += self.lines[i].skip
                else:          i += 1 
        return 0

    def readFile(self):
        self.error = None
        self.parts = ['']
        self.lines = []
        with open(self.root + local['file']) as reader:

            #Reading files into lines
            for line in reader: 
                if line == '': continue
                if '#' in line:
                    for i in range(0, len(line)):
                        if line[i] == '#': self.parts[0] += line[:i]
                else: self.parts[0] += line
            start = 0
            opn = False
            self.parts = self.parts[0].split(';')
            for i in range(0, len(self.parts)):
                if self.parts[i] == '\n' or self.parts[i] == ' ':               continue
                if self.parts[i] == '' and not self.parts[i] == self.parts[-1]: 
                    self.error = "Expected ';' Symbol"
                    return
                elif self.parts[i] == '':                                       continue
                while self.parts[i][ 0] in (' ', '\n'): self.parts[i] = self.parts[i][1:  ]
                while self.parts[i][-1] in (' ', '\n'): self.parts[i] = self.parts[i][ :-1]
                if '{' in self.parts[i]:
                    if opn: 
                        self.error = "Unexpected '{' Symbol"
                        return
                    else:
                        opn  = True
                        start = i
                        self.lines.append(Line(self.parts[i].split('{')[0]))
                        self.lines.append(Line(self.parts[i].split('{')[1]))
                elif self.parts[i] == '}':
                    if not opn: 
                        self.error = "Unexpected '}' Symbol"
                        return
                    else:
                        opn = False
                        self.lines[start].skip = i - start + 1
                else: self.lines.append(Line(self.parts[i]))

            if self.parts[-1] != '': 
                self.error = 'Missing ";"'
                return

    def interpret(self, command):
        self.error = None # No Error
        self.parts = []

        #Disassembly
        word = ''
        for letter in command:
            if not letter in [' ', '(', ')', '{', '}', ';', ',', "'", '"', '%', '$', '.']: word += letter
            else:
                if word != '' and word != '\n': self.parts.append(word)
                self.parts.append(letter)
                word = ''
        self.parts.append(word)
        while self.parts[0] in (' ', ''): self.parts = self.parts[1:]

        #Error Checks
        if not self.parts[0] in ["$", "%"]:
            self.error = 'Invalid Line Code'
            return

        # Reassembly
        if not self.merge('"'):
            self.error = 'Mismatched Parenthetical' 
            return
        if not self.merge("'"):
            self.error = 'Mismatched Parenthetical'
            return
        if self.parts.count("(") != self.parts.count(")"):
            self.error = 'Mismatched Parenthetical' 
            return

        # Deletion
        while "," in self.parts: self.parts.remove(',')
        while " " in self.parts: self.parts.remove(' ')

        # Variable Insertion
        i = len(self.parts) - 1
        while i > 0:
            if   self.parts[i] == '%':
                if not self.parts[i + 1] in local: 
                    self.error = 'Undefined Variable'
                    return
                try:
                    if self.parts[i + 2] == '.':
                        self.parts.insert(i, getattr(local[self.parts[i + 1]], self.parts[i + 3]))
                        del self.parts[i + 1 : i + 5]
                    else:
                        self.parts.insert(i, local[self.parts[i + 1]])
                        del self.parts[i + 1 : i + 3]
                except IndexError:
                    self.parts.insert(i, local[self.parts[i + 1]])
                    del self.parts[i + 1 : i + 3]
            i -= 1

        # Expression Evaluation
        i = len(self.parts) - 1
        while i > 0:
            if   self.parts[i] == "+":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) +  int(self.parts[i + 1]))
                except ValueError: self.parts.insert(i - 1,     self.parts[i - 1]  +      self.parts[i + 1])
                del self.parts[i : i + 3]
            elif self.parts[i] == "-":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) -  int(self.parts[i + 1]))
                except ValueError:
                    self.error = 'Invalid Operands'
                    return
                del self.parts[i : i + 3]
            elif self.parts[i] == "*":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) *  int(self.parts[i + 1]))
                except ValueError:
                    self.error = 'Invalid Operands'
                    return
                del self.parts[i : i + 3]
            elif self.parts[i] == "/":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) /  int(self.parts[i + 1]))
                except ValueError:
                    self.error = 'Invalid Operands'
                    return
                del self.parts[i : i + 3]
            elif self.parts[i] == ">":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) >  int(self.parts[i + 1]))
                except ValueError:
                    self.error = 'Invalid Operands'
                    return
                del self.parts[i : i + 3]
            elif self.parts[i] == ">=":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) >= int(self.parts[i + 1]))
                except ValueError:
                    self.error = 'Invalid Operands'
                    return
                del self.parts[i : i + 3]
            elif self.parts[i] == "<":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) <  int(self.parts[i + 1]))
                except ValueError:
                    self.error = 'Invalid Operands'
                    return
                del self.parts[i : i + 3]
            elif self.parts[i] == "<=":
                try:               self.parts.insert(i - 1, int(self.parts[i - 1]) <= int(self.parts[i + 1]))
                except ValueError:
                    self.error = 'Invalid Operands'
                    return
                del self.parts[i : i + 3]
            elif self.parts[i] == "==":
                self.parts.insert(i - 1, self.parts[i - 1] == self.parts[i + 1])
                del self.parts[i : i + 3]
            elif self.parts[i] == "!=":
                self.parts.insert(i - 1, self.parts[i - 1] != self.parts[i + 1])
                del self.parts[i : i + 3]
            i -= 1

        # Function Execution
        i = len(self.parts) - 1
        while i > 0:
            if   self.parts[i] == '$':
                self.parts.insert(i, self.executeAt(i))
                if self.parts[i] == "error": return
                del self.parts[i + 1 : i + 4]
            i -= 1

        # Line Result
        if self.parts[0] == "%":
            try:
                if self.parts[2] == ".":
                    if   self.parts[4] == "=" : setattr(local[self.parts[1]], self.parts[3],   self.parts[5])
                    elif self.parts[4] == "+=": 
                        try:                    setattr(local[self.parts[1]], self.parts[3], 
                                                getattr(local[self.parts[1]], self.parts[3]) + int(self.parts[5]))
                        except TypeError:       setattr(local[self.parts[1]], self.parts[3], 
                                                getattr(local[self.parts[1]], self.parts[3]) +     self.parts[5])
                    else:
                        self.error = 'Variable Unassigned'
                        return
                    return getattr(local[self.parts[1]], self.parts[3])
                else:
                    if   self.parts[2] == "=" : local.update({self.parts[1] : self.parts[3]})
                    elif self.parts[2] == "+=": local[self.parts[1]] += self.parts[3]
                    else:
                        self.error = 'Variable Unassigned'
                        return
                    return local[self.parts[1]]
            except KeyError:
                self.error = 'Undefined Variable'
                return
        elif self.parts[0] == "$":
            self.parts.insert(0, self.executeAt(0))
            if self.parts[0] == "error": return
            return self.parts[0]
