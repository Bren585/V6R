from database import Database, Character

# Function Definition
class Function:
    def __init__(self, argc, func):
        self.argc = argc
        self.func = func

# Function Shortcuts
def cap(text, case):
    if not case: return text
    return text[0].upper() + text[1:]

def treat(text):
    words = text.split()

    i = 0
    new = ''
    case = False
    while i < len(words):
        if words[i] == "^":
            case = True
        else:
            if words[i][0] == '%':
                if '.' in words[i]:
                    hold = words[i][1:].split('.')
                    if hold[0] in local:
                        new += cap(str(getattr(local[hold[0]], hold[1])), case) + ' '
                    else:
                        new += cap(words[i], case) + ' '
                elif words[i][1:] in local:
                    new += cap(local[words[i][1:]], case) + ' '
                else:
                    new += cap(words[i], case) + ' '
            elif words[i][0] == '+':
                new = new[:-1] + cap(words[i][1:], case) + ' '
            else:
                new += cap(words[i], case) + ' '
            case = False
        i += 1
    return new

# Long Functions
def jump(argv):         # Jump to file argv[0] 
    local['file'] = argv[0]
    local['stop'] = True
def stop(argv):         # Stop the program 
    local['interpreter'].filename = "stop"
    local['stop'] = True
def loadFile(argv):     # Pull filename from savedata in database 
    local['db'].cursor.execute("SELECT filename FROM savedata WHERE id = 1")
    return local['db'].cursor.fetchall()[0][0]
def loadUser(argv):     # Pull username from savedata in database 
    local['db'].cursor.execute("SELECT username FROM savedata WHERE id = 1")
    return local['db'].cursor.fetchall()[0][0]
def saveFile(argv):     # Set filename in savedata to argv[0] 
    local['db'].cursor.execute("UPDATE savedata SET filename = '%s' WHERE id = 1" % (argv[0]))
def saveUser(argv):     # Set username in savedata to argv[0] 
    local['db'].cursor.execute("UPDATE savedata SET username = '%s' WHERE id = 1" % (argv[0]))
def clear(argv):        # Print 50 blank lines 
    for i in range(0, 50): print()
def speak(argv):        # Print a treated message argv[1] from argv[0] 
    print("[{:<10}] : {}".format(argv[0], treat(argv[1])))
def announce(argv):     # Print a treated message argv[0] 
    print(treat(argv[0]))
def pause(argv):        # Wait for user input before continuing, then clears 
    input()
    clear(argv)

local = {'stop' : False}

function = {
# Console Functions
'print'        : Function(1, lambda argv : print(argv[0])                                           ),
'input'        : Function(1, lambda argv : input(argv[0])                                           ),
'clear'        : Function(0, clear                                                                  ),

# Logic Functions
'if'           : Function(1, lambda argv : argv[0]                                                  ),

# Database Functions
## User Functions
'loadFile'     : Function(0, loadFile                                                               ),
'loadUser'     : Function(0, loadUser                                                               ),
'saveFile'     : Function(1, saveFile                                                               ),
'saveUser'     : Function(1, saveUser                                                               ),
## Character Functions
'create'       : Function(1, lambda argv : local['db'].create(argv[0])                              ),
'load'         : Function(1, lambda argv : Character(local['db'], argv[0])                          ),
'save'         : Function(1, lambda argv : argv[0].save()                                           ),

# Story Functions
'speak'        : Function(2, speak                                                                  ), 
'announce'     : Function(1, announce                                                               ),
'pause'        : Function(0, pause                                                                  ),
'jump'         : Function(1, jump                                                                   ),
'stop'         : Function(0, stop                                                                   )

}
