

# ========================================
# input functions
# ========================================
def PSKILL(arg=''):
 # print(arg)
 outputChange   =dict()
 inputChange	={'PSKILL':arg,}
 return (inputChange,outputChange)
  
def clearFaults00(arg=''):
 outputsToChange0 = {'FANSFAN1F0': 0, 'WORDPgood0': 0, 'VOUTOV0': 0, 'OFFLOWINPUT0': 0, 'FANSFAN1W0': 0, 'IOUTOPP0': 0, 'IOUTOCW0': 0, 'UVP0': 0, 'TEMPOTW0': 0, 'VOUTTONMAX0': 0, 'INOPW0': 0, 'UVW0': 0, 'VOUTUV0': 0, 'INOCW0': 0, 'FANSFAN1Speed0': 0, 'IOUTOCP0': 0, 'IOUTOPW0': 0, 'TEMPOTP0': 0, 'WORDOther0': 0}
 outputChange  =dict(outputsToChange0)
 inputChange	={'ClearFaults00':0}
 return (inputChange,outputChange)
def clearFaults01(arg=''):
 outputsToChange1 = {'FANSFAN1F1': 0, 'WORDPgood1': 0, 'VOUTOV1': 0, 'OFFLOWINPUT1': 0, 'FANSFAN1W1': 0, 'IOUTOPP1': 0, 'IOUTOCW1': 0, 'UVP1': 0, 'TEMPOTW1': 0, 'VOUTTONMAX1': 0, 'INOPW1': 0, 'UVW1': 0, 'VOUTUV1': 0, 'INOCW1': 0, 'FANSFAN1Speed1': 0, 'IOUTOCP1': 0, 'IOUTOPW1': 0, 'TEMPOTP1': 0, 'WORDOther1': 0}
 outputChange  =dict(outputsToChange1)
 inputChange	={'ClearFaults01':0}
 return (inputChange,outputChange)
def clearFaultsFF(arg=''):
 # outputsToChange1 = {'FANSFAN1F1': 0, 'WORDPgood1': 0, 'VOUTOV1': 0, 'OFFLOWINPUT1': 0, 'FANSFAN1W1': 0, 'IOUTOPP1': 0, 'IOUTOCW1': 0, 'UVP1': 0, 'TEMPOTW1': 0, 'VOUTTONMAX1': 0, 'INOPW1': 0, 'UVW1': 0, 'VOUTUV1': 0, 'INOCW1': 0, 'FANSFAN1Speed1': 0, 'IOUTOCP1': 0, 'IOUTOPW1': 0, 'TEMPOTP1': 0, 'WORDOther1': 0}
 outputChange = {'FANSFAN1F0': 0, 'WORDPgood0': 0, 'VOUTOV0': 0, 'OFFLOWINPUT0': 0, 'FANSFAN1W0': 0, 'IOUTOPP0': 0, 'IOUTOCW0': 0, 'UVP0': 0, 'TEMPOTW0': 0, 'VOUTTONMAX0': 0, 'INOPW0': 0, 'UVW0': 0, 'VOUTUV0': 0, 'INOCW0': 0, 'FANSFAN1Speed0': 0, 'IOUTOCP0': 0, 'IOUTOPW0': 0, 'TEMPOTP0': 0, 'WORDOther0': 0,'FANSFAN1F1': 0, 'WORDPgood1': 0, 'VOUTOV1': 0, 'OFFLOWINPUT1': 0, 'FANSFAN1W1': 0, 'IOUTOPP1': 0, 'IOUTOCW1': 0, 'UVP1': 0, 'TEMPOTW1': 0, 'VOUTTONMAX1': 0, 'INOPW1': 0, 'UVW1': 0, 'VOUTUV1': 0, 'INOCW1': 0, 'FANSFAN1Speed1': 0, 'IOUTOCP1': 0, 'IOUTOPW1': 0, 'TEMPOTP1': 0, 'WORDOther1': 0}
 # outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	= {'ClearFaultsFF':0}
 return (inputChange,outputChange)
  
# UVW Bit
  
def ClearUVWbitPagePlus00(arg=''):
 outputChange = {'UVW0': 0,}
 inputChange	={'ClearUVWbitPagePlus00':0}
 return (inputChange,outputChange)
  
def ClearUVWbitPagePlus01(arg=''):
 outputChange = {'UVW1': 0,}
 inputChange	={'ClearUVWbitPagePlus01':0}
 return (inputChange,outputChange)
 
def ClearUVWbitPagePlusFF(arg=''):
 outputChange = {'UVW0': 0,'UVW1': 0}
 inputChange	={'ClearUVWbitPagePlusFF':0}
 return (inputChange,outputChange)
  
def ClearUVWbit00(arg=''):
 outputChange = {'UVW0': 0,}
 inputChange	={'ClearUVWbit00':0}
 return (inputChange,outputChange)
  
def ClearUVWbit01(arg=''):
 outputChange = {'UVW1': 0,}
 inputChange	={'ClearUVWbit01':0}
 return (inputChange,outputChange)
 
def ClearUVWbitFF(arg=''):
 outputChange = {'UVW0': 0,'UVW1': 0}
 inputChange	={'ClearUVWbitFF':0}
 return (inputChange,outputChange)
  
# UVP Bit
  
def ClearUVPbitPagePlus00(arg=''):
 outputChange = {'UVP0': 0,}
 inputChange	={'ClearUVPbitPagePlus00':0}
 return (inputChange,outputChange)
  
def ClearUVPbitPagePlus01(arg=''):
 outputChange = {'UVP1': 0,}
 inputChange	={'ClearUVPbitPagePlus01':0}
 return (inputChange,outputChange)
 
def ClearUVPbitPagePlusFF(arg=''):
 outputChange = {'UVP0': 0,'UVP1': 0}
 inputChange	={'ClearUVPbitPagePlusFF':0}
 return (inputChange,outputChange)
  
def ClearUVPbit00(arg=''):
 outputChange = {'UVP0': 0,}
 inputChange	={'ClearUVPbit00':0}
 return (inputChange,outputChange)
  
def ClearUVPbit01(arg=''):
 outputChange = {'UVP1': 0,}
 inputChange	={'ClearUVPbit01':0}
 return (inputChange,outputChange)
  
def ClearUVPbitFF(arg=''):
 outputChange = {'UVP0': 0,'UVP1': 0}
 inputChange	={'ClearUVPbitFF':0}
 return (inputChange,outputChange)
  
# OFFLOWINPUT Bit
  
def ClearOFFLOWINPUTbitPagePlus00(arg=''):
 outputChange = {'OFFLOWINPUT0': 0,}
 inputChange	={'ClearOFFLOWINPUTbitPagePlus00':0}
 return (inputChange,outputChange)
  
def ClearOFFLOWINPUTbitPagePlus01(arg=''):
 outputChange = {'OFFLOWINPUT1': 0,}
 inputChange	={'ClearOFFLOWINPUTbitPagePlus01':0}
 return (inputChange,outputChange)
  
def ClearOFFLOWINPUTbitPagePlusFF(arg=''):
 outputChange = {'OFFLOWINPUT0': 0,'OFFLOWINPUT1': 0}
 inputChange	={'ClearOFFLOWINPUTbitPagePlusFF':0}
 return (inputChange,outputChange)
  
def ClearOFFLOWINPUTbit00(arg=''):
 outputChange = {'OFFLOWINPUT0': 0,}
 inputChange	={'ClearOFFLOWINPUTbit00':0}
 return (inputChange,outputChange)
  
def ClearOFFLOWINPUTbit01(arg=''):
 outputChange = {'OFFLOWINPUT1': 0,}
 inputChange	={'ClearOFFLOWINPUTbit01':0}
 return (inputChange,outputChange)
  
def ClearOFFLOWINPUTbitFF(arg=''):
 outputChange = {'OFFLOWINPUT0': 0,'OFFLOWINPUT1': 0}
 inputChange	={'ClearOFFLOWINPUTbitFF':0}
 return (inputChange,outputChange)
  
# Clear Faults Bit
  
def ClearFANSFAN1Fbit(arg=''):
 outputChange = {'FANSFAN1F0': 0,'FANSFAN1F1': 0}
 inputChange	={'ClearFANSFAN1Fbit':0}
 return (inputChange,outputChange)
  
def ClearVOUTOVbit(arg=''):
 outputChange = {'VOUTOV0': 0,'VOUTOV1': 0}
 inputChange	={'ClearVOUTOVbit':0}
 return (inputChange,outputChange)
  
def ClearFANSFAN1Wbit(arg=''):
 outputChange = {'FANSFAN1W0': 0,'FANSFAN1W1': 0}
 inputChange	={'ClearFANSFAN1Wbit':0}
 return (inputChange,outputChange)
  
def ClearIOUTOPPbit(arg=''):
 outputChange = {'IOUTOPP0': 0,'IOUTOPP1': 0}
 inputChange	={'ClearIOUTOPPbit':0}
 return (inputChange,outputChange)
  
def ClearIOUTOCWbit(arg=''):
 outputChange = {'IOUTOCW0': 0,'IOUTOCW1': 0}
 inputChange	={'ClearIOUTOCWbit':0}
 return (inputChange,outputChange)
  
def ClearTEMPOTWbit(arg=''):
 outputChange = {'TEMPOTW0': 0,'TEMPOTW1': 0}
 inputChange	={'ClearTEMPOTWbit':0}
 return (inputChange,outputChange)
  
def ClearINOPWbit(arg=''):
 outputChange = {'INOPW0': 0,'INOPW1': 0}
 inputChange	={'ClearINOPWbit':0}
 return (inputChange,outputChange)
  
def ClearVOUTUVbit(arg=''):
 outputChange = {'VOUTUV0': 0,'VOUTUV1': 0}
 inputChange	={'ClearVOUTUVbit':0}
 return (inputChange,outputChange)
  
def ClearINOCWbit(arg=''):
 outputChange = {'INOCW0': 0,'INOCW1': 0}
 inputChange	={'ClearINOCWbit':0}
 return (inputChange,outputChange)
  
def ClearFANSFAN1Speedbit(arg=''):
 outputChange = {'FANSFAN1Speed0': 0,'FANSFAN1Speed1': 0}
 inputChange	={'ClearFANSFAN1Speedbit':0}
 return (inputChange,outputChange)
  
def ClearIOUTOCPbit(arg=''):
 outputChange = {'IOUTOCP0': 0,'IOUTOCP1': 0}
 inputChange	={'ClearIOUTOCPbit':0}
 return (inputChange,outputChange)
  
def ClearIOUTOPWbit(arg=''):
 outputChange = {'IOUTOPW0': 0,'IOUTOPW1': 0}
 inputChange	={'ClearIOUTOPWbit':0}
 return (inputChange,outputChange)
  
def ClearTEMPOTPbit(arg=''):
 outputChange = {'TEMPOTP0': 0,'TEMPOTP1': 0}
 inputChange	={'ClearTEMPOTPbit':0}
 return (inputChange,outputChange)
  
# ========================================
# output functions
# ========================================

def Vmain(VmainSS,PSKILL):
 print(VmainSS[1],PSKILL)
 return 1 if VmainSS[1] > 10 and not PSKILL else 0
def Pok(Vmain):
 return 1 if Vmain > 10 else 0
def WORDInput(INOCW,INOPW,UVW,UVP,OFFLOWINPUT):
 return 1 if INOCW or INOPW or UVW or UVP or OFFLOWINPUT else 0
def WORDPgood(Vmain):
 return 1 if Vmain[1] < 10 else 0
def WORDVout(VOUTUV,VOUTOV,VOUTTONMAX):
 return 1 if VOUTUV or VOUTOV or VOUTTONMAX else 0
def WORDIout(IOUTOCP,IOUTOCW,IOUTOPW,IOUTOPP):
 return 1 if IOUTOCP or IOUTOCW or IOUTOPW or IOUTOPP else 0
def WORDFans(FANSFAN1F,FANSFAN1W,FANSFAN1Speed):
 return 1 if FANSFAN1F or FANSFAN1W or FANSFAN1Speed else 0
def BYTEVinUV(UVP):
 return 1 if UVP else 0
def BYTEOFF(Vmain,Vsb):
 return 1 if Vmain[1] < 10 or Vsb[1] < 10 else 0
def BYTETemp(TEMPOTP,TEMPOTW):
 return 1 if TEMPOTP or TEMPOTW else 0
def BYTEVoutOV(VOUTOV):
 return 1 if VOUTOV else 0
def BYTEIoutOC(IOUTOCP):
 return 1 if IOUTOCP else 0
 


class localDoutputs:
    def __init__(self):
        pass

# ========================================
# function dictionary
# ========================================

    inputs =\
    {
        'PSKILL':(PSKILL,('',),((1,0),1)),
        # 'PSKILL':(PSKILL,('',),((0,),1)),
	
        'ClearFaults00':(clearFaults00,('',),((1,),1)),
        'ClearFaults01':(clearFaults01,('',),((1,),1)),
        'ClearFaultsFF':(clearFaultsFF,('',),((1,),1)),
        
        'ClearUVWbitPagePlus00':(ClearUVWbitPagePlus00,('',),((1,),1)),
        'ClearUVWbitPagePlus01':(ClearUVWbitPagePlus01,('',),((1,),1)),
        'ClearUVWbitPagePlusFF':(ClearUVWbitPagePlusFF,('',),((1,),1)),
        'ClearUVWbit00':(ClearUVWbit00,('',),((1,),1)),
        'ClearUVWbit01':(ClearUVWbit01,('',),((1,),1)),
        'ClearUVWbitFF':(ClearUVWbitFF,('',),((1,),1)),
        
        'ClearUVPbitPagePlus00':(ClearUVPbitPagePlus00,('',),((1,),1)),
        'ClearUVPbitPagePlus01':(ClearUVPbitPagePlus01,('',),((1,),1)),
        'ClearUVPbitPagePlusFF':(ClearUVPbitPagePlusFF,('',),((1,),1)),
        'ClearUVPbit00':(ClearUVPbit00,('',),((1,),1)),
        'ClearUVPbit01':(ClearUVPbit01,('',),((1,),1)),
        'ClearUVPbitFF':(ClearUVPbitFF,('',),((1,),1)),
        
        'ClearOFFLOWINPUTbitPagePlus00':(ClearOFFLOWINPUTbitPagePlus00,('',),((1,),1)),
        'ClearOFFLOWINPUTbitPagePlus01':(ClearOFFLOWINPUTbitPagePlus01,('',),((1,),1)),
        'ClearOFFLOWINPUTbitPagePlusFF':(ClearOFFLOWINPUTbitPagePlusFF,('',),((1,),1)),
        'ClearOFFLOWINPUTbit00':(ClearOFFLOWINPUTbit00,('',),((1,),1)),
        'ClearOFFLOWINPUTbit01':(ClearOFFLOWINPUTbit01,('',),((1,),1)),
        'ClearOFFLOWINPUTbitFF':(ClearOFFLOWINPUTbitFF,('',),((1,),1)),
 
 # 'ClearFANSFAN1Fbit':(ClearFANSFAN1Fbit,('',),((1,),1)),
 # 'ClearVOUTOVbit':(ClearVOUTOVbit,('',),((1,),1)),
 # 'ClearFANSFAN1Wbit':(ClearFANSFAN1Wbit,('',),((1,),1)),
 # 'ClearIOUTOPPbit':(ClearIOUTOPPbit,('',),((1,),1)),
 # 'ClearIOUTOCWbit':(ClearIOUTOCWbit,('',),((1,),1)),
 # 'ClearTEMPOTWbit':(ClearTEMPOTWbit,('',),((1,),1)),
 # 'ClearINOPWbit':(ClearINOPWbit,('',),((1,),1)),
 # 'ClearVOUTUVbit':(ClearVOUTUVbit,('',),((1,),1)),
 # 'ClearINOCWbit':(ClearINOCWbit,('',),((1,),1)),
 # 'ClearFANSFAN1Speedbit':(ClearFANSFAN1Speedbit,('',),((1,),1)),
 # 'ClearIOUTOCPbit':(ClearIOUTOCPbit,('',),((1,),1)),
 # 'ClearIOUTOPWbit':(ClearIOUTOPWbit,('',),((1,),1)),
 # 'ClearTEMPOTPbit':(ClearTEMPOTPbit,('',),((1,),1)),
    }

    outputs =\
    {
        'Vmain':(Vmain,('VmainSS','PSKILL')),
        'Pok':(Pok,('Vmain',)),
 
 # 'WORDInput0':(WORDInput,('INOCW0','INOPW0','UVW0','UVP0','OFFLOWINPUT0')),
 # 'WORDPgood0':(WORDPgood,('Vmain',)),
 # 'WORDVout0':( WORDVout,('VOUTUV0','VOUTOV0','VOUTTONMAX0')),
 # 'WORDIout0':( WORDIout,('IOUTOCP0','IOUTOCW0','IOUTOPW0','IOUTOPP0')),
 # 'WORDFans0':( WORDFans,('FANSFAN1F0','FANSFAN1W0','FANSFAN1Speed0')),
 # 'BYTEVinUV0':( BYTEVinUV,('UVP0',)),
 # 'BYTEOFF0':( BYTEOFF,('Vmain','Vsb')),
 # 'BYTETemp0':( BYTETemp,('TEMPOTP0','TEMPOTW0')),
 # 'BYTEVoutOV0':( BYTEVoutOV,('VOUTOV0',)),
 # 'BYTEIoutOC0':( BYTEIoutOC,('IOUTOCP0',)),
 
 # 'WORDInput1':(WORDInput,('INOCW1','INOPW1','UVW1','UVP1','OFFLOWINPUT1')),
 # 'WORDPgood1':(WORDPgood,('Vmain',)),
 # 'WORDVout1':( WORDVout,('VOUTUV1','VOUTOV1','VOUTTONMAX1')),
 # 'WORDIout1':( WORDIout,('IOUTOCP1','IOUTOCW1','IOUTOPW1','IOUTOPP1')),
 # 'WORDFans1':( WORDFans,('FANSFAN1F1','FANSFAN1W1','FANSFAN1Speed1')),
 # 'BYTEVinUV1':( BYTEVinUV,('UVP1',)),
 # 'BYTEOFF1':( BYTEOFF,('Vmain','Vsb')),
 # 'BYTETemp1':( BYTETemp,('TEMPOTP1','TEMPOTW1')),
 # 'BYTEVoutOV1':( BYTEVoutOV,('VOUTOV1',)),
 # 'BYTEIoutOC1':( BYTEIoutOC,('IOUTOCP1',)),
    }


##########################################################################

    #do not modify this function, or model's will not be able to explore
    def input(self,input,outputValues,arg):
        args = [arg,]
        for out in self.inputs[input][1]:
            if out != '':
                args.append(outputValues[out])
        args=tuple(args)
        (inputChange,outputChange)    = self.inputs[input][0](*args)
        return (inputChange,outputChange)

    #do not modify this function, or model's will not be able to explore
    def compute(self, output, outputValues, inputValues):
        args = []
        for out in self.outputs[output][1]: # find output or input that is used to set output
            if out in outputValues:
                args.append(outputValues[out])
            elif out in inputValues:
                args.append(inputValues[out])
            else:
                args.append(0)
        args = tuple(args)
        return self.outputs[output][0](*args)

#do not modify this function, or model's will not be able to explore
# def input(self,input,outputValues):
    # args = []
    # for out in self.inputs[input][1]:
        # if out != '':
            # args.append(outputValues[out])
    # args=tuple(args)
    # (inputChange,outputChange)    = self.inputs[input][0](*args)
    # return (inputChange,outputChange)

#do not modify this function, or model's will not be able to explore
# def compute(self,output,outputValues):
    # args = []
    # for out in self.outputs[output][1]:
        # args.append(outputValues[out])
    # args=tuple(args)
    # return self.outputs[output][0](*args)

