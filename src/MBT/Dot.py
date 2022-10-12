"""
Dot - generate graphics in dot language
"""

import os.path
from time import sleep
from PyPDF2 import PdfMerger

def state(n, fsm,BlackStates=0):
 if BlackStates==0 or n in BlackStates:
     style = 'filled'
 else:
     style = 'invisible'
 StateName = fsm.states[n]['name']
 outputs = fsm.states[n]['outputs']
 outputs = '<BR/>'.join(['%s:%s' % (key,outputs[key]) for key in list(outputs)])
 label = '<%s<BR/> <FONT POINT-SIZE="10">%s</FONT>>' % (StateName,outputs)
 return '%s [ style=%s, shape=ellipse,penwidth = 1, peripheries=1, fillcolor=white, color=black, fontcolor=black , label=%s]' % (StateName,style,label)

def quote_string(x):
    if isinstance(x,tuple):
        return str(x)
    else:
        return "'%s'" % x if isinstance(x, str) else "%s" % x

def rlabel(result):
    return '/%s' % quote_string(result) if result != None else ''

def transition(n,t,fsm,BlackTransitions=0):
    if len(t[1])==1:
        current, [(action, args)], Delay, next, outputs = t
    else:
        current, [(action, args),(action1, args1)], Delay, next, outputs = t
    try:
        if n in fsm.failedtransitions:
            color = 'red'
        elif n in fsm.passtransitions:
            color = 'green'
        else:
            color = 'black'
    except:
     color = 'black'
    if BlackTransitions != 0 and n not in BlackTransitions:
        style=',style=invis'
    else:
        style=''
    if len(args)==2:
     args = args
    elif len(args)==1 and args[0] == 'pushbutton':
     args = '(%s)'% args[0]
    elif len(args)==1 and type(args[0])==str:
     args = '(%s)'% args[0]
    else:
     args = '(%s)'%int(args[0])
    # args = args if len(args)==2 else '(%s)'%int(args[0])
    outputs = '<BR/>'.join(['%s:%s' % (key,outputs[key]) for key in list(outputs)])
    if outputs != '' and len(t[1])==1:
     label = '<%s%s, delay:%s Sec<BR/> <FONT POINT-SIZE="10">%s</FONT>>' % (action,args,Delay,outputs)
    elif outputs != '' and len(t[1])==2:
     label = '<%s%s AND %s%s, delay:%s Sec<BR/> <FONT POINT-SIZE="10">%s</FONT>>' % (action,args,action1,args1,Delay,outputs)
    elif len(t[1])==1:
     label = '<%s%s, delay:%s Sec>' % (action,args,Delay)
    else:
     label = '<%s%s AND %s%s, delay:%s Sec>' % (action,args,action1,args1,Delay)

    return '%s -> %s [ penwidth = 1,label=%s, color=%s, fontcolor=%s %s]' % (fsm.states[current]['name'], fsm.states[next]['name'], label, color, color,style)

def dotfile(fname, fsm):
    f = open(fname, 'w')
    f.write('digraph %s {\n' % os.path.basename(fname).partition('.')[0])
    f.write('K=2;\n')
    f.write('overlap=scale;\n')
# States
    f.write('\n  // Nodes\n')
    f.writelines([ '  %s\n' % state(n,fsm) for n in fsm.states ])
# Transitions
    f.write('\n  // Transitions\n')
    f.writelines([ '  %s\n' % transition(n,t,fsm) for n,t in enumerate(fsm.graph) ])
    f.write('}\n')
    f.close()
    print('Dot File Written')
    if len(fsm.graph)>150:
        os.system('sfdp -T pdf -o %s.pdf %s & cd ..' % ('%s'%('Frame'),fname))
    else:
        os.system('dot -T pdf -o %s.pdf %s & cd ..' % ('%s'%('Frame'),fname))
    print('Dot or sfdp run')

def dotfilesForAnimation(fname, fsm,path):
    workingDir = path
    animationPath = os.path.join(workingDir,'animation')
    if not os.path.isdir(animationPath):
        os.makedirs(animationPath)
    os.chdir(animationPath)
    merger = PdfMerger()
    files2delete=[]
    for i in range(len(fsm.EventTracker)):
        BlackStates      = []
        BlackTransitions = []
        for j in range(i):
            event = fsm.EventTracker[j]
            if 'state' in event:
                BlackStates.append(int(event.split(' ')[1]))
            else:
                BlackTransitions.append(int(event.split(' ')[1]))
        f = open('%s'%(fname), 'w')
        f.write('digraph %s {\n' % os.path.basename(fname).partition('.')[0])
        f.write('K=2;\n')
        f.write('overlap=scale;\n')
    # States
        f.write('\n  // Nodes\n')
        f.writelines([ '  %s\n' % state(n,fsm,BlackStates) for n in fsm.states ])
    # Transitions
        f.write('\n  // Transitions\n')
        f.writelines([ '  %s\n' % transition(n,t,fsm,BlackTransitions) for n,t in enumerate(fsm.graph) ])
        f.write('}\n')
        f.close()
        if len(fsm.graph)>150:
            os.system('sfdp -T pdf  -o %s.pdf %s & cd ..' % ('%s%s'%('Frame',i),fname))
        else:
            os.system('dot -T pdf -o %s.pdf %s & cd ..' % ('%s%s'%('Frame',i),fname))
        sleep(0.1)
        merger.append("%s.pdf"%'%s%s'%('Frame',i))
        files2delete.append("%s.pdf"%'%s%s'%('Frame',i))
    sleep(1)
    merger.write("animation.pdf")
    merger.close()
    for file in files2delete:
        os.remove(file)
    os.chdir(workingDir)
