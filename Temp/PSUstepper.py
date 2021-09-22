"""
Simple Stepper to experiment with timeouts in pmt
"""
import my_imports
from time import sleep
import ac,daq,load,I2C,scope,powermeter,sys

def TestAction(aname, args, modelResult):
    if aname == 'AC':
        (voltage,) = args
        if voltage>10:
         ac.set(voltage,50,'high')
        else:
         ac.off()
        sleep(modelResult)
    elif aname == 'ACOFF':
        (voltage,) = args
        ac.off()
        sleep(modelResult)
    elif aname == 'PSON':
        (on,) = args
        if not on:
         I2C.GPIO(7,0) # Enable PSU
        else:
         I2C.GPIO(7,1) # Disable PSU
        sleep(.5)
    elif aname == 'PSKILL':
        (on,) = args
        if not on:
         I2C.GPIO(6,0) # Enable PSU
        else:
         I2C.GPIO(6,1) # Disable PSU
        sleep(.5)
    elif aname == 'ClearFaults00':
        (delay,) = args
        I2C.comm('w,00,00')
        I2C.comm('w,03')
        sleep(.1)
    elif aname == 'ClearFaults01':
        (delay,) = args
        I2C.comm('w,00,01')
        I2C.comm('w,03')
        sleep(.1)
    elif aname == 'ClearFaultsFF':
        (delay,) = args
        I2C.comm('w,00,FF')
        sleep(.1)
        I2C.comm('w,03')
        sleep(.1)
    elif aname == 'ClearOFFLOWINPUTbit00':
        I2C.comm('w,05,03,00,7C,08')
        sleep(.1)
    elif aname == 'ClearOFFLOWINPUTbit01':
        I2C.comm('w,05,03,01,7C,08')
        sleep(.1)
    elif aname == 'ClearOFFLOWINPUTbitFF':
        I2C.comm('w,05,03,FF,7C,08')
        sleep(.1)
    elif aname == 'ClearUVWbit00':
        I2C.comm('w,05,03,00,7C,20')
        sleep(.1)
    elif aname == 'ClearUVWbit01':
        I2C.comm('w,05,03,01,7C,20')
        sleep(.1)
    elif aname == 'ClearUVWbitFF':
        I2C.comm('w,05,03,FF,7C,20')
        sleep(.1)
    elif aname == 'ClearUVPbit00':
        I2C.comm('w,05,03,00,7C,10')
        sleep(.1)
    elif aname == 'ClearUVPbit01':
        I2C.comm('w,05,03,01,7C,10')
        sleep(.1)
    elif aname == 'ClearUVPbitFF':
        I2C.comm('w,05,03,FF,7C,10')
        sleep(.1)
    elif aname == 'delay':
        (delay,) = args
        sleep(float(delay))
    elif aname == 'Imain':
        (Imain,) = args
        load.main(int(Imain))
        # sleep(0.1)
    elif aname == 'SetupScope':
        (TransitionTime,SignalList,SignalLevel,triggerInfo,Measurements) = args
        scope.setup(TransitionTime,SignalList,SignalLevel,triggerInfo,Measurements)
        sleep(0.1)
    elif aname == 'ScopeShot':
        (name,actionLabels) = args
        timeout=60
        while(scope.trigger('done') != 'READY' and not timeout):
         sleep(1)
         timeout -= 1
        scope.shot('%s-%s'%(name,'-'.join(['%s %s'%(a,Measure(a)) for a in actionLabels])))
    else:
        raise (NotImplementedError, 'action not supported by stepper: %s' % aname)

def getByte(I2CCMD,page='',address='B0'):
 N = int(I2CCMD.split(',')[-1])
 I2CCMD = I2CCMD.replace('r,%s' % N,'r,%s' % (N+2))
 I2CCMD = I2CCMD.replace('w','w,06,02,%s'%page)
 data = []
 for cmd in I2CCMD.split(','):
  if cmd == 'r':
   break
  if cmd != 'w':
   data.append(cmd)
 passes=2
 while True:
  bytes = I2C.comm(I2CCMD,address)
  byte		= bytes.split(' ')
  del byte[-1]
  PECByte 	= int(bytes.split(' ')[-1],16)
  PECByteSpec   = int(I2C.PEC(address+' '+' '.join(data)+' B1 '+' '+' '.join(byte)),16)
  if PECByte == PECByteSpec:
   break
  else:
   passes -=1
  if passes == 0:
   break
  sleep(0.1)
 del byte[0]
 byte		= ' '.join(byte)
 if ' ' in byte:
  byte = byte.split(' ')[1]
 sleep(0.1)
 return byte
 
def bit(byte,bit):
 bit = int('1'+'0'*bit,2)
 return 1 if (int(byte,16) & bit) == bit else 0
		
# bit('32',0)
		
def Measure(aname, args=''):
    # print(aname)
    if aname == 'Pok':
        return round(daq.volt(303),3)
    elif aname == 'IPOK':
        return round(daq.volt('IPOK'),2)
    elif aname == 'Vmain':
        return 1 if round(daq.volt(301),3) > 10 else 0
    elif aname == 'Vsb':
        return 12#round(daq.volt(302),3)
    elif aname == 'Installed':
        return round(daq.volt('Installed'),2)
    elif aname == 'Imain':
        return round(load.main(),1)
    elif aname == 'AC':
        return ac.set()[0]
    elif aname == 'Freq':
        return ac.set()[1]
    elif aname == 'PF':
        return powermeter.PF()
# ==================================================
# Status Bits page 00
# ==================================================
# Status Input
    elif aname == 'UVW0':
        return bit(getByte('w,7C,r,1','00'),5)
    elif aname == 'UVP0':
        return bit(getByte('w,7C,r,1','00'),4)
    elif aname == 'OFFLOWINPUT0':
        return bit(getByte('w,7C,r,1','00'),3)
    elif aname == 'INOCW0':
        return bit(getByte('w,7C,r,1','00'),1)
    elif aname == 'INOPW0':
        return bit(getByte('w,7C,r,1','00'),0)
# Status Byte
    elif aname == 'BYTEOFF0':
        return bit(getByte('w,78,r,1','00'),6)
    elif aname == 'BYTEVoutOV0':
        return bit(getByte('w,78,r,1','00'),5)
    elif aname == 'BYTEIoutOC0':
        return bit(getByte('w,78,r,1','00'),4)
    elif aname == 'BYTEVinUV0':
        return bit(getByte('w,78,r,1','00'),3)
    elif aname == 'BYTETemp0':
        return bit(getByte('w,78,r,1','00'),2)
    elif aname == 'BYTECML0':
        return bit(getByte('w,78,r,1','00'),1)
# Status Word
    elif aname == 'WORDVout0':
        return bit(getByte('w,79,r,2','00'),7)
    elif aname == 'WORDIout0':
        return bit(getByte('w,79,r,2','00'),6)
    elif aname == 'WORDInput0':
        return bit(getByte('w,79,r,2','00'),5)
    elif aname == 'WORDPgood0':
        return bit(getByte('w,79,r,2','00'),3)
    elif aname == 'WORDFans0':
        return bit(getByte('w,79,r,2','00'),2)
    elif aname == 'WORDOther0':
        return bit(getByte('w,79,r,2','00'),1)
# Status Vout
    elif aname == 'VOUTOV0':
        return bit(getByte('w,7A,r,1','00'),7)
    elif aname == 'VOUTUV0':
        return bit(getByte('w,7A,r,1','00'),4)
    elif aname == 'VOUTTONMAX0':
        return bit(getByte('w,7A,r,1','00'),2)
# Status Iout
    elif aname == 'IOUTOCP0':
        return bit(getByte('w,7B,r,1','00'),7)
    elif aname == 'IOUTOCW0':
        return bit(getByte('w,7B,r,1','00'),5)
    elif aname == 'IOUTOPP0':
        return bit(getByte('w,7B,r,1','00'),1)
    elif aname == 'IOUTOPW0':
        return bit(getByte('w,7B,r,1','00'),0)
# Status Temp
    elif aname == 'TEMPOTP0':
        return bit(getByte('w,7D,r,1','00'),7)
    elif aname == 'TEMPOTW0':
        return bit(getByte('w,7D,r,1','00'),6)
# Status CML
    elif aname == 'CMLINVALIDCMD0':
        return bit(getByte('w,7E,r,1','00'),7)
    elif aname == 'CMLINVALIDDATA0':
        return bit(getByte('w,7E,r,1','00'),6)
    elif aname == 'CMLPEC0':
        return bit(getByte('w,7E,r,1','00'),5)
# Status Fans
    elif aname == 'FANSFAN1F0':
        return 0#bit(getByte('w,81,r,1','00'),7)
    elif aname == 'FANSFAN1W0':
        return 0#bit(getByte('w,81,r,1','00'),5)
    elif aname == 'FANSFAN1Speed0':
        return 0#bit(getByte('w,81,r,1','00'),3)
# ==================================================

# ==================================================
# Status Bits page 01
# ==================================================
# Status Input
    elif aname == 'UVW1':
        return bit(getByte('w,7C,r,1','01'),5)
    elif aname == 'UVP1':
        return bit(getByte('w,7C,r,1','01'),4)
    elif aname == 'OFFLOWINPUT1':
        return bit(getByte('w,7C,r,1','01'),3)
    elif aname == 'INOCW1':
        return bit(getByte('w,7C,r,1','01'),1)
    elif aname == 'INOPW1':
        return bit(getByte('w,7C,r,1','01'),0)
# Status Byte
    elif aname == 'BYTEOFF1':
        return bit(getByte('w,78,r,1','01'),6)
    elif aname == 'BYTEVoutOV1':
        return bit(getByte('w,78,r,1','01'),5)
    elif aname == 'BYTEIoutOC1':
        return bit(getByte('w,78,r,1','01'),4)
    elif aname == 'BYTEVinUV1':
        return bit(getByte('w,78,r,1','01'),3)
    elif aname == 'BYTETemp1':
        return bit(getByte('w,78,r,1','01'),2)
    elif aname == 'BYTECML1':
        return bit(getByte('w,78,r,1','01'),1)
# Status Word
    elif aname == 'WORDVout1':
        return bit(getByte('w,79,r,2','01'),7)
    elif aname == 'WORDIout1':
        return bit(getByte('w,79,r,2','01'),6)
    elif aname == 'WORDInput1':
        return bit(getByte('w,79,r,2','01'),5)
    elif aname == 'WORDPgood1':
        return bit(getByte('w,79,r,2','01'),3)
    elif aname == 'WORDFans1':
        return bit(getByte('w,79,r,2','01'),2)
    elif aname == 'WORDOther1':
        return bit(getByte('w,79,r,2','01'),1)
# Status Vout
    elif aname == 'VOUTOV1':
        return bit(getByte('w,7A,r,1','01'),7)
    elif aname == 'VOUTUV1':
        return bit(getByte('w,7A,r,1','01'),4)
    elif aname == 'VOUTTONMAX1':
        return bit(getByte('w,7A,r,1','01'),2)
# Status Iout
    elif aname == 'IOUTOCP1':
        return bit(getByte('w,7B,r,1','01'),7)
    elif aname == 'IOUTOCW1':
        return bit(getByte('w,7B,r,1','01'),5)
    elif aname == 'IOUTOPP1':
        return bit(getByte('w,7B,r,1','01'),1)
    elif aname == 'IOUTOPW1':
        return bit(getByte('w,7B,r,1','01'),0)
# Status Temp
    elif aname == 'TEMPOTP1':
        return bit(getByte('w,7D,r,1','01'),7)
    elif aname == 'TEMPOTW1':
        return bit(getByte('w,7D,r,1','01'),6)
# Status CML
    elif aname == 'CMLINVALIDCMD1':
        return bit(getByte('w,7E,r,1','01'),7)
    elif aname == 'CMLINVALIDDATA1':
        return bit(getByte('w,7E,r,1','01'),6)
    elif aname == 'CMLPEC1':
        return bit(getByte('w,7E,r,1','01'),5)
# Status Fans
    elif aname == 'FANSFAN1F1':
        return 0#bit(getByte('w,81,r,1','01'),7)
    elif aname == 'FANSFAN1W1':
        return 0#bit(getByte('w,81,r,1','01'),5)
    elif aname == 'FANSFAN1Speed1':
        return 0#bit(getByte('w,81,r,1','01'),3)
# ==================================================
		
    elif aname == 'scope measure':
        (slot,) = args
        return scope.measure(slot)
    elif aname == 'None':
        return ''
    elif aname == 'delay':
        (delay,) = args
        sleep(delay)
    else:
        raise (NotImplementedError, 'action not supported by stepper: %s' % aname)
		
def ResetRoutine():
 ac.set(220,50,'high') 
 TestAction('PSON',(1,),1) 
 TestAction('PSKILL',(1,),1) 
 sleep(1) 
 TestAction('PSON',(0,),1) 
 TestAction('PSKILL',(0,),1) 
 sleep(1) 
 TestAction('PSON',(1,),1) 
 TestAction('PSKILL',(1,),1) 
 sleep(1) 
 ac.set(1,50,'high') 
 load.main(10) 
 sleep(1) 
 # load.stby(1) 
 TestAction('ClearFaultsFF',(1,),1) 
 sleep(1) 

def Reset():
 try:
  ResetRoutine()
 except:
  sleep(10)
 # if Measure('UVW0')==1 or Measure('OFFLOWINPUT0')==0:
  # ac.off()
  # sleep(10)
  # ResetRoutine()
  # print('Reset Fail')
  # sys.stdout.flush()
 
# print(Measure('FANSFAN1F1'))
# ac.set(220,50,'high')
# Reset()