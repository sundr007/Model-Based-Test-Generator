"""
Simple equipment interface to experiment with timeouts in pmt
"""

from time import sleep


def TestAction(aname, args, modelResult):
    if aname == 'A':
        #<put action in for A>
        sleep(modelResult)
    elif aname == 'B':
        #<put action in for B>
        sleep(modelResult)
    elif aname == 'C':
        #<put action in for C>
        sleep(modelResult)
    elif aname == 'Clear':
        #<put action in for Clear>
        sleep(modelResult)
    elif aname == 'delay':
        (delay,) = args
        sleep(float(delay))

    else:
        raise (NotImplementedError, 'action not supported by stepper: %s' % aname)


		
def Measure(aname, args=''):
    # print(aname)
    if aname == 'OUT':
        return 1
    if aname == 'otherOutput':
        return 1
    elif aname == 'None':
        return ''
    elif aname == 'delay':
        (delay,) = args
        sleep(delay)
    else:
        raise (NotImplementedError, 'action not supported by stepper: %s' % aname)
		
def ResetRoutine():
 TestAction('A',(0,),1) 
 TestAction('B',(1,),1) 
 TestAction('C',(1,),1) 
 TestAction('Clear',(0,),1) 
 TestAction('delay',(1,),1) 

def Reset():
 try:
  ResetRoutine()
 except:
  sleep(10)
