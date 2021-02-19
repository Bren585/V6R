from command import Line

def clean(text):
    lines = []
    open = False
    text = text.split(';')
    for i in range(0, len(text)):
        if text[i] == '\n':                           continue
        if text[i] == '' and not text[i] == text[-1]: return
        elif text[i] == '':                           continue
        while text[i][ 0] in (' ', '\n'):             text[i] = text[i][1:  ]
        while text[i][-1] in (' ', '\n'):             text[i] = text[i][ :-1]
        if '{' in text[i]:
            if open: return
            else:
                open  = True
                start = i
                lines.append(Line(text[i].split('{')[0]))
                lines.append(Line(text[i].split('{')[1]))
        elif text[i] == '}':
            if not open: return
            else:
                open = False
                lines[start].skip = i - start
        else: lines.append(Line(text[i]))
    return lines

print(clean("""
a
{
    b;
    c;
};
d;
"""))