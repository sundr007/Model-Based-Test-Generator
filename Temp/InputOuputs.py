

# ========================================
# input functions
# ========================================
def PSKILL(arg=''):
 outputChange   =dict()
 inputChange	={'PSKILL':arg,}
 defaultValue   = 0
 return (inputChange,outputChange,defaultValue)
 
def page(arg=''):
 outputChange   =dict()
 inputChange	={'page':arg,}
 defaultValue='00'
 return (inputChange,outputChange,defaultValue)
 
def Imain(arg=''):
 outputChange   =dict()
 inputChange	={'Imain':arg,}
 defaultValue   = 10
 return (inputChange,outputChange,defaultValue)
 
def FanWarn(arg=''):
 outputChange   ={'FanWarn0':1,'FanWarn1':1}
 inputChange	={'FanWarn':0,}
 defaultValue   = 0
 return (inputChange,outputChange,defaultValue)
 
def MaskUVWbitPage00(arg=''):
 outputChange   =dict()
 inputChange	={'MaskUVWbitPage00':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskUVWbitPage01(arg=''):
 outputChange   =dict()
 inputChange	={'MaskUVWbitPage01':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskUVPbitPage00(arg=''):
 outputChange   =dict()
 inputChange	={'MaskUVPbitPage00':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskUVPbitPage01(arg=''):
 outputChange   =dict()
 inputChange	={'MaskUVPbitPage01':arg,}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
 
def MaskOffLowInputbitPage00(arg=''):
 outputChange   =dict()
 inputChange	={'MaskOffLowInputbitPage00':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskOffLowInputbitPage01(arg=''):
 outputChange   =dict()
 inputChange	={'MaskOffLowInputbitPage01':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskVoutOVbitPage00(arg=''):
 outputChange   =dict()
 inputChange	={'MaskVoutOVbitPage00':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskVoutOVbitPage01(arg=''):
 outputChange   =dict()
 inputChange	={'MaskVoutOVbitPage01':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskVoutUVbitPage00(arg=''):
 outputChange   =dict()
 inputChange	={'MaskVoutUVbitPage00':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskVoutUVbitPage01(arg=''):
 outputChange   =dict()
 inputChange	={'MaskVoutUVbitPage01':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskOTPbitPage00(arg=''):
 outputChange   =dict()
 inputChange	={'MaskOTPbitPage00':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskOTPbitPage01(arg=''):
 outputChange   =dict()
 inputChange	={'MaskOTPbitPage01':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskFanFaultbitPage00(arg=''):
 outputChange   =dict()
 inputChange	={'MaskFanFaultbitPage00':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
 
def MaskFanFaultbitPage01(arg=''):
 outputChange   =dict()
 inputChange	={'MaskFanFaultbitPage01':arg,}
 defaultValue=1
 return (inputChange,outputChange,defaultValue)
  
def clearFaults(arg,page):
 outputsToChange0 = {'FANSFAN1F0': 0, 'WORDPgood0': 0, 'VoutOV0': 0, 'OFFLOWINPUT0': 0, 'FANSFAN1W0': 0, 'IOUTOPP0': 0, 'IOUTOCW0': 0, 'UVP0': 0, 'TEMPOTW0': 0, 'VOUTTONMAX0': 0, 'INOPW0': 0, 'UVW0': 0, 'VOUTUV0': 0, 'INOCW0': 0, 'FANSFAN1Speed0': 0, 'IOUTOCP0': 0, 'IOUTOPW0': 0, 'TEMPOTP0': 0, 'WORDOther0': 0}
 outputsToChange1 = {'FANSFAN1F1': 0, 'WORDPgood1': 0, 'VoutOV1': 0, 'OFFLOWINPUT1': 0, 'FANSFAN1W1': 0, 'IOUTOPP1': 0, 'IOUTOCW1': 0, 'UVP1': 0, 'TEMPOTW1': 0, 'VOUTTONMAX1': 0, 'INOPW1': 0, 'UVW1': 0, 'VOUTUV1': 0, 'INOCW1': 0, 'FANSFAN1Speed1': 0, 'IOUTOCP1': 0, 'IOUTOPW1': 0, 'TEMPOTP1': 0, 'WORDOther1': 0}
 if page == 0:
  page = '00'
 if page == '00':
  outputChange  = dict(outputsToChange0)
 elif page == '01':
  outputChange  = dict(outputsToChange1)
 elif page == 'FF':
  outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	={'ClearFaults':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
  
def clearFaults00(arg=''):
 outputsToChange0 = {'FANSFAN1F0': 0, 'WORDPgood0': 0, 'VoutOV0': 0, 'OFFLOWINPUT0': 0, 'FANSFAN1W0': 0, 'IOUTOPP0': 0, 'IOUTOCW0': 0, 'UVP0': 0, 'TEMPOTW0': 0, 'VOUTTONMAX0': 0, 'INOPW0': 0, 'UVW0': 0, 'VOUTUV0': 0, 'INOCW0': 0, 'FANSFAN1Speed0': 0, 'IOUTOCP0': 0, 'IOUTOPW0': 0, 'TEMPOTP0': 0, 'WORDOther0': 0}
 outputChange  =dict(outputsToChange0)
 inputChange	={'ClearFaults00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
def clearFaults01(arg=''):
 outputsToChange1 = {'FANSFAN1F1': 0, 'WORDPgood1': 0, 'VoutOV1': 0, 'OFFLOWINPUT1': 0, 'FANSFAN1W1': 0, 'IOUTOPP1': 0, 'IOUTOCW1': 0, 'UVP1': 0, 'TEMPOTW1': 0, 'VOUTTONMAX1': 0, 'INOPW1': 0, 'UVW1': 0, 'VOUTUV1': 0, 'INOCW1': 0, 'FANSFAN1Speed1': 0, 'IOUTOCP1': 0, 'IOUTOPW1': 0, 'TEMPOTP1': 0, 'WORDOther1': 0}
 outputChange  =dict(outputsToChange1)
 inputChange	={'ClearFaults01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
def clearFaultsFF(arg=''):
 # outputsToChange1 = {'FANSFAN1F1': 0, 'WORDPgood1': 0, 'VoutOV1': 0, 'OFFLOWINPUT1': 0, 'FANSFAN1W1': 0, 'IOUTOPP1': 0, 'IOUTOCW1': 0, 'UVP1': 0, 'TEMPOTW1': 0, 'VOUTTONMAX1': 0, 'INOPW1': 0, 'UVW1': 0, 'VOUTUV1': 0, 'INOCW1': 0, 'FANSFAN1Speed1': 0, 'IOUTOCP1': 0, 'IOUTOPW1': 0, 'TEMPOTP1': 0, 'WORDOther1': 0}
 outputChange = {'FANSFAN1F0': 0, 'WORDPgood0': 0, 'VoutOV0': 0, 'OFFLOWINPUT0': 0, 'FANSFAN1W0': 0, 'IOUTOPP0': 0, 'IOUTOCW0': 0, 'UVP0': 0, 'TEMPOTW0': 0, 'VOUTTONMAX0': 0, 'INOPW0': 0, 'UVW0': 0, 'VOUTUV0': 0, 'INOCW0': 0, 'FANSFAN1Speed0': 0, 'IOUTOCP0': 0, 'IOUTOPW0': 0, 'TEMPOTP0': 0, 'WORDOther0': 0,'FANSFAN1F1': 0, 'WORDPgood1': 0, 'VoutOV1': 0, 'OFFLOWINPUT1': 0, 'FANSFAN1W1': 0, 'IOUTOPP1': 0, 'IOUTOCW1': 0, 'UVP1': 0, 'TEMPOTW1': 0, 'VOUTTONMAX1': 0, 'INOPW1': 0, 'UVW1': 0, 'VOUTUV1': 0, 'INOCW1': 0, 'FANSFAN1Speed1': 0, 'IOUTOCP1': 0, 'IOUTOPW1': 0, 'TEMPOTP1': 0, 'WORDOther1': 0}
 # outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	= {'ClearFaultsFF':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
# UVW Bit
  
def ClearUVWbitPagePlus00(arg=''):
 outputChange = {'UVW0': 0,}
 inputChange	={'ClearUVWbitPagePlus00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearUVWbitPagePlus01(arg=''):
 outputChange = {'UVW1': 0,}
 inputChange	={'ClearUVWbitPagePlus01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearUVWbit(arg,page):
 outputsToChange0 = {'UVW0': 0,}
 outputsToChange1 = {'UVW1': 0,}
 paging = {'00':dict(outputsToChange0),'01':dict(outputsToChange1),'FF':{**outputsToChange0, **outputsToChange1}}
 outputChange = paging.get(page,dict(outputsToChange0))
 inputChange	={'ClearUVWbit':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
# def ClearUVWbit00(arg=''):
 # outputChange = {'UVW0': 0,}
 # inputChange	={'ClearUVWbit00':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearUVWbit01(arg=''):
 # outputChange = {'UVW1': 0,}
 # inputChange	={'ClearUVWbit01':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
 
# def ClearUVWbitFF(arg=''):
 # outputChange = {'UVW0': 0,'UVW1': 0}
 # inputChange	={'ClearUVWbitFF':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# UVP Bit
  
def ClearUVPbitPagePlus00(arg=''):
 outputChange = {'UVP0': 0,}
 inputChange	={'ClearUVPbitPagePlus00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearUVPbitPagePlus01(arg=''):
 outputChange = {'UVP1': 0,}
 inputChange	={'ClearUVPbitPagePlus01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearUVPbit(arg,page):
 outputsToChange0 = {'UVP0': 0,}
 outputsToChange1 = {'UVP1': 0,}
 if page == 0:
  page = '00'
 if page == '00':
  outputChange  = dict(outputsToChange0)
 elif page == '01':
  outputChange  = dict(outputsToChange1)
 elif page == 'FF':
  outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	={'ClearUVPbit':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
 
 # paging = {'00':dict(outputsToChange0),'01':dict(outputsToChange1),'FF':{**outputsToChange0, **outputsToChange1}}
 # outputChange = paging.get(page,dict(outputsToChange0))
 # inputChange	={'ClearUVPbit':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearUVPbit00(arg=''):
 # outputChange = {'UVP0': 0,}
 # inputChange	={'ClearUVPbit00':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearUVPbit01(arg=''):
 # outputChange = {'UVP1': 0,}
 # inputChange	={'ClearUVPbit01':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearUVPbitFF(arg=''):
 # outputChange = {'UVP0': 0,'UVP1': 0}
 # inputChange	={'ClearUVPbitFF':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# OFFLOWINPUT Bit
  
def ClearOFFLOWINPUTbitPagePlus00(arg=''):
 outputChange = {'OFFLOWINPUT0': 0,}
 inputChange	={'ClearOFFLOWINPUTbitPagePlus00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearOFFLOWINPUTbitPagePlus01(arg=''):
 outputChange = {'OFFLOWINPUT1': 0,}
 inputChange	={'ClearOFFLOWINPUTbitPagePlus01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearOFFLOWINPUTbit(arg,page):
 outputsToChange0 = {'OFFLOWINPUT0': 0,}
 outputsToChange1 = {'OFFLOWINPUT1': 0,}
 paging = {'00':dict(outputsToChange0),'01':dict(outputsToChange1),'FF':{**outputsToChange0, **outputsToChange1}}
 outputChange = paging.get(page,dict(outputsToChange0))
 inputChange	={'ClearOFFLOWINPUTbit':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
# def ClearOFFLOWINPUTbit00(arg=''):
 # outputChange = {'OFFLOWINPUT0': 0,}
 # inputChange	={'ClearOFFLOWINPUTbit00':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearOFFLOWINPUTbit01(arg=''):
 # outputChange = {'OFFLOWINPUT1': 0,}
 # inputChange	={'ClearOFFLOWINPUTbit01':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearOFFLOWINPUTbitFF(arg=''):
 # outputChange = {'OFFLOWINPUT0': 0,'OFFLOWINPUT1': 0}
 # inputChange	={'ClearOFFLOWINPUTbitFF':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# VoutOV Bit
  
def ClearVoutOVbitPagePlus00(arg=''):
 outputChange = {'VoutOV0': 0,}
 inputChange	={'ClearVoutOVbitPagePlus00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearVoutOVbitPagePlus01(arg=''):
 outputChange = {'VoutOV1': 0,}
 inputChange	={'ClearVoutOVbitPagePlus01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearVoutOVbit(arg,page):
 outputsToChange0 = {'VoutOV0': 0,}
 outputsToChange1 = {'VoutOV1': 0,}
 if page == 0:
  page = '00'
 if page == '00':
  outputChange  = dict(outputsToChange0)
 elif page == '01':
  outputChange  = dict(outputsToChange1)
 elif page == 'FF':
  outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	={'ClearVoutOVbit':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
# def ClearVoutOVbit00(arg=''):
 # outputChange = {'VoutOV0': 0,}
 # inputChange	={'ClearVoutOVbit00':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearVoutOVbit01(arg=''):
 # outputChange = {'VoutOV1': 0,}
 # inputChange	={'ClearVoutOVbit01':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
   
# def ClearVoutOVbitFF(arg=''):
 # outputChange = {'VoutOV0': 0,'VoutOV1': 0}
 # inputChange	={'ClearVoutOVbitFF':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
 
# VoutUV Bit
  
def ClearVoutUVbitPagePlus00(arg=''):
 outputChange = {'VoutUV0': 0,}
 inputChange	={'ClearVoutUVbitPagePlus00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearVoutUVbitPagePlus01(arg=''):
 outputChange = {'VoutUV1': 0,}
 inputChange	={'ClearVoutUVbitPagePlus01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearVoutUVbit(arg,page):
 outputsToChange0 = {'VoutUV0': 0,}
 outputsToChange1 = {'VoutUV1': 0,}
 if page == 0:
  page = '00'
 if page == '00':
  outputChange  = dict(outputsToChange0)
 elif page == '01':
  outputChange  = dict(outputsToChange1)
 elif page == 'FF':
  outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	={'ClearVoutUVbit':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
# def ClearVoutUVbit00(arg=''):
 # outputChange = {'VoutUV0': 0,}
 # inputChange	={'ClearVoutUVbit00':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearVoutUVbit01(arg=''):
 # outputChange = {'VoutUV1': 0,}
 # inputChange	={'ClearVoutUVbit01':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
   
# def ClearVoutUVbitFF(arg=''):
 # outputChange = {'VoutUV0': 0,'VoutUV1': 0}
 # inputChange	={'ClearVoutUVbitFF':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
 
# OTP Bit
  
def ClearOTPbitPagePlus00(arg=''):
 outputChange = {'OTP0': 0,}
 inputChange	={'ClearOTPbitPagePlus00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearOTPbitPagePlus01(arg=''):
 outputChange = {'OTP1': 0,}
 inputChange	={'ClearOTPbitPagePlus01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearOTPbit(arg,page):
 outputsToChange0 = {'OTP0': 0,}
 outputsToChange1 = {'OTP1': 0,}
 if page == 0:
  page = '00'
 if page == '00':
  outputChange  = dict(outputsToChange0)
 elif page == '01':
  outputChange  = dict(outputsToChange1)
 elif page == 'FF':
  outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	={'ClearOTPbit':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
# def ClearOTPbit00(arg=''):
 # outputChange = {'OTP0': 0,}
 # inputChange	={'ClearOTPbit00':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearOTPbit01(arg=''):
 # outputChange = {'OTP1': 0,}
 # inputChange	={'ClearOTPbit01':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
   
# def ClearOTPbitFF(arg=''):
 # outputChange = {'OTP0': 0,'OTP1': 0}
 # inputChange	={'ClearOTPbitFF':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
 
# FanFault Bit
  
def ClearFanFaultbitPagePlus00(arg=''):
 outputChange = {'FanFault0': 0,}
 inputChange	={'ClearFanFaultbitPagePlus00':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearFanFaultbitPagePlus01(arg=''):
 outputChange = {'FanFault1': 0,}
 inputChange	={'ClearFanFaultbitPagePlus01':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
def ClearFanFaultbit(arg,page):
 outputsToChange0 = {'FanFault0': 0,}
 outputsToChange1 = {'FanFault1': 0,}
 if page == 0:
  page = '00'
 if page == '00':
  outputChange  = dict(outputsToChange0)
 elif page == '01':
  outputChange  = dict(outputsToChange1)
 elif page == 'FF':
  outputChange  = {**outputsToChange0, **outputsToChange1}
 inputChange	={'ClearFanFaultbit':0}
 defaultValue=0
 return (inputChange,outputChange,defaultValue)
  
# def ClearFanFaultbit00(arg=''):
 # outputChange = {'FanFault0': 0,}
 # inputChange	={'ClearFanFaultbit00':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# def ClearFanFaultbit01(arg=''):
 # outputChange = {'FanFault1': 0,}
 # inputChange	={'ClearFanFaultbit01':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
   
# def ClearFanFaultbitFF(arg=''):
 # outputChange = {'FanFault0': 0,'FanFault1': 0}
 # inputChange	={'ClearFanFaultbitFF':0}
 # defaultValue=0
 # return (inputChange,outputChange,defaultValue)
  
# ========================================
# output functions
# ========================================

def Vmain(VmainSS,PSKILL):
 return 1 if VmainSS[1] > 10 and not PSKILL else 0
def Pok(Vmain):
 return 1 if Vmain[1] > 10 else 0
def SMBAlert(Vmain,UVW0,UVW1,MaskUVWbitPage00,MaskUVWbitPage01,UVP0,UVP1,MaskUVPbitPage00,MaskUVPbitPage01,OFFLOWINPUT0,OFFLOWINPUT1,MaskOffLowInputbitPage00,MaskOffLowInputbitPage01,VoutOV0,VoutOV1,MaskVoutOVbitPage00,MaskVoutOVbitPage01,VoutUV0,VoutUV1,MaskVoutUVbitPage00,MaskVoutUVbitPage01,OTP0,OTP1,MaskOTPbitPage00,MaskOTPbitPage01,FanFault0,FanFault1,MaskFanFaultbitPage00,MaskFanFaultbitPage01):
 return 1 if not ((UVW0 and not MaskUVWbitPage00) or (UVW1 and not MaskUVWbitPage01) or (UVP0 and not MaskUVPbitPage00) or (UVP1 and not MaskUVPbitPage01) or (OFFLOWINPUT0 and not MaskOffLowInputbitPage00) or (OFFLOWINPUT1 and not MaskOffLowInputbitPage01) or (VoutOV0 and not MaskVoutOVbitPage00) or (VoutOV1 and not MaskVoutOVbitPage01) or (VoutUV0 and not MaskVoutUVbitPage00) or (VoutUV1 and not MaskVoutUVbitPage01) or (OTP0 and not MaskOTPbitPage00) or (OTP1 and not MaskOTPbitPage01) or (FanFault0 and not MaskFanFaultbitPage00) or (FanFault1 and not MaskFanFaultbitPage01)) else 0

def readPage(page):
 return page
 
def UVPbitNoPage (UVP0,UVP1,page):
 paging = {'00':UVP0,'01':UVP1,'FF':UVP0 or UVP1}
 return paging.get(page,UVP0)
def UVWbitNoPage (UVW0,UVW1,page):
 paging = {'00':UVW0,'01':UVW1,'FF':UVW0 or UVW1}
 return paging.get(page,UVW0)
def OFFLOWINPUTbitNoPage (OFFLOWINPUT0,OFFLOWINPUT1,page):
 paging = {'00':OFFLOWINPUT0,'01':OFFLOWINPUT1,'FF':OFFLOWINPUT0 or OFFLOWINPUT1}
 return paging.get(page,OFFLOWINPUT0)
def VoutOVbitNoPage (VoutOV0,VoutOV1,page):
 paging = {'00':VoutOV0,'01':VoutOV1,'FF':VoutOV0 or VoutOV1}
 return paging.get(page,VoutOV0)
def VoutUVbitNoPage (VoutUV0,VoutUV1,page):
 paging = {'00':VoutUV0,'01':VoutUV1,'FF':VoutUV0 or VoutUV1}
 return paging.get(page,VoutUV0)
def OTPbitNoPage (OTP0,OTP1,page):
 paging = {'00':OTP0,'01':OTP1,'FF':OTP0 or OTP1}
 return paging.get(page,OTP0)
def OTWbitNoPage (OTW0,OTW1,page):
 paging = {'00':OTW0,'01':OTW1,'FF':OTW0 or OTW1}
 return paging.get(page,OTW0)
def FanFaultbitNoPage (FanFault0,FanFault1,page):
 paging = {'00':FanFault0,'01':FanFault1,'FF':FanFault0 or FanFault1}
 return paging.get(page,FanFault0)
def FanWarnbitNoPage (FanWarn0,FanWarn1,page):
 paging = {'00':FanWarn0,'01':FanWarn1,'FF':FanWarn0 or FanWarn1}
 return paging.get(page,FanWarn0)
 
 
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
	
        'Imain':(Imain,('',),((1,196),1)),
        'PSKILL':(PSKILL,('',),((1,0),1)),
		
		'page':(page,('',),(('00','01','FF'),1)),
		
        'MaskUVWbitPage00':(MaskUVWbitPage00,('',),((1,0),1)),
        'MaskUVWbitPage01':(MaskUVWbitPage01,('',),((1,0),1)),
		
        'MaskUVPbitPage00':(MaskUVPbitPage00,('',),((1,0),1)),
        'MaskUVPbitPage01':(MaskUVPbitPage01,('',),((1,0),1)),
	
        'MaskOffLowInputbitPage00':(MaskOffLowInputbitPage00,('',),((1,0),1)),
        'MaskOffLowInputbitPage01':(MaskOffLowInputbitPage01,('',),((1,0),1)),
		
        'MaskVoutOVbitPage00':(MaskVoutOVbitPage00,('',),((1,0),1)),
        'MaskVoutOVbitPage01':(MaskVoutOVbitPage01,('',),((1,0),1)),
		
        'MaskVoutUVbitPage00':(MaskVoutUVbitPage00,('',),((1,0),1)),
        'MaskVoutUVbitPage01':(MaskVoutUVbitPage01,('',),((1,0),1)),
	
        'MaskOTPbitPage00':(MaskOTPbitPage00,('',),((1,0),1)),
        'MaskOTPbitPage01':(MaskOTPbitPage01,('',),((1,0),1)),
		
        'MaskFanFaultbitPage00':(MaskFanFaultbitPage00,('',),((1,0),1)),
        'MaskFanFaultbitPage01':(MaskFanFaultbitPage01,('',),((1,0),1)),
	
        'clearFaults':(clearFaults,('page',),((1,),1)),
	
        # 'ClearFaults00':(clearFaults00,('',),((1,),1)),
        # 'ClearFaults01':(clearFaults01,('',),((1,),1)),
        # 'ClearFaultsFF':(clearFaultsFF,('',),((1,),1)),
        
        'ClearUVWbitPagePlus00':(ClearUVWbitPagePlus00,('',),((1,),1)),
        'ClearUVWbitPagePlus01':(ClearUVWbitPagePlus01,('',),((1,),1)),
		'ClearUVWbit':(ClearUVWbit,('page',),((1,),1)),
        # 'ClearUVWbit00':(ClearUVWbit00,('',),((1,),1)),
        # 'ClearUVWbit01':(ClearUVWbit01,('',),((1,),1)),
        # 'ClearUVWbitFF':(ClearUVWbitFF,('',),((1,),1)),
        
        'ClearUVPbitPagePlus00':(ClearUVPbitPagePlus00,('',),((1,),1)),
        'ClearUVPbitPagePlus01':(ClearUVPbitPagePlus01,('',),((1,),1)),
		'ClearUVPbit':(ClearUVPbit,('page',),((1,),1)),
        # 'ClearUVPbit00':(ClearUVPbit00,('',),((1,),1)),
        # 'ClearUVPbit01':(ClearUVPbit01,('',),((1,),1)),
        # 'ClearUVPbitFF':(ClearUVPbitFF,('',),((1,),1)),
        
        'ClearOFFLOWINPUTbitPagePlus00':(ClearOFFLOWINPUTbitPagePlus00,('',),((1,),1)),
        'ClearOFFLOWINPUTbitPagePlus01':(ClearOFFLOWINPUTbitPagePlus01,('',),((1,),1)),
		'ClearOFFLOWINPUTbit':(ClearOFFLOWINPUTbit,('page',),((1,),1)),
        # 'ClearOFFLOWINPUTbit00':(ClearOFFLOWINPUTbit00,('',),((1,),1)),
        # 'ClearOFFLOWINPUTbit01':(ClearOFFLOWINPUTbit01,('',),((1,),1)),
        # 'ClearOFFLOWINPUTbitFF':(ClearOFFLOWINPUTbitFF,('',),((1,),1)),
		
        'ClearVoutOVbitPagePlus00':(ClearVoutOVbitPagePlus00,('',),((1,),1)),
        'ClearVoutOVbitPagePlus01':(ClearVoutOVbitPagePlus01,('',),((1,),1)),
		'ClearVoutOVbit':(ClearVoutOVbit,('page',),((1,),1)),
        # 'ClearVoutOVbit00':(ClearVoutOVbit00,('',),((1,),1)),
        # 'ClearVoutOVbit01':(ClearVoutOVbit01,('',),((1,),1)),
        # 'ClearVoutOVbitFF':(ClearVoutOVbitFF,('',),((1,),1)),

        'ClearVoutUVbitPagePlus00':(ClearVoutUVbitPagePlus00,('',),((1,),1)),
        'ClearVoutUVbitPagePlus01':(ClearVoutUVbitPagePlus01,('',),((1,),1)),
		'ClearVoutUVbit':(ClearVoutUVbit,('page',),((1,),1)),
        # 'ClearVoutUVbit00':(ClearVoutUVbit00,('',),((1,),1)),
        # 'ClearVoutUVbit01':(ClearVoutUVbit01,('',),((1,),1)),
        # 'ClearVoutUVbitFF':(ClearVoutUVbitFF,('',),((1,),1)),
		
        'ClearOTPbitPagePlus00':(ClearOTPbitPagePlus00,('',),((1,),1)),
        'ClearOTPbitPagePlus01':(ClearOTPbitPagePlus01,('',),((1,),1)),
		'ClearOTPbit':(ClearOTPbit,('page',),((1,),1)),
        # 'ClearOTPbit00':(ClearOTPbit00,('',),((1,),1)),
        # 'ClearOTPbit01':(ClearOTPbit01,('',),((1,),1)),
        # 'ClearOTPbitFF':(ClearOTPbitFF,('',),((1,),1)),
		
        'ClearFanFaultbitPagePlus00':(ClearFanFaultbitPagePlus00,('',),((1,),1)),
        'ClearFanFaultbitPagePlus01':(ClearFanFaultbitPagePlus01,('',),((1,),1)),
		'ClearFanFaultbit':(ClearFanFaultbit,('page',),((1,),1)),
        # 'ClearFanFaultbit00':(ClearFanFaultbit00,('',),((1,),1)),
        # 'ClearFanFaultbit01':(ClearFanFaultbit01,('',),((1,),1)),
        # 'ClearFanFaultbitFF':(ClearFanFaultbitFF,('',),((1,),1)),
 
    }

    outputs =\
    {
        # 'Vmain':(Vmain,('VmainSS','PSKILL')),
        # 'Pok':(Pok,('Vmain',)),
        # 'SMBAlert':(SMBAlert,('Vmain','UVW0','UVW1','MaskUVWbitPage00','MaskUVWbitPage01','UVP0','UVP1','MaskUVPbitPage00','MaskUVPbitPage01','OFFLOWINPUT0','OFFLOWINPUT1','MaskOffLowInputbitPage00','MaskOffLowInputbitPage01','VoutOV0','VoutOV1','MaskVoutOVbitPage00','MaskVoutOVbitPage01','VoutUV0','VoutUV1','MaskVoutUVbitPage00','MaskVoutUVbitPage01','OTP0','OTP1','MaskOTPbitPage00','MaskOTPbitPage01','FanFault0','FanFault1','MaskFanFaultbitPage00','MaskFanFaultbitPage01')),
 
		# 'readPage':(readPage,('page',)),
 
		# 'UVPbitNoPage':(UVPbitNoPage,('UVP0','UVP1','page')),
		# 'UVWbitNoPage':(UVWbitNoPage,('UVW0','UVW1','page')),
		# 'OFFLOWINPUTbitNoPage':(OFFLOWINPUTbitNoPage,('OFFLOWINPUT0','OFFLOWINPUT1','page')),
		# 'VoutOVbitNoPage':(VoutOVbitNoPage,('VoutOV0','VoutOV1','page')),
		# 'VoutUVbitNoPage':(VoutUVbitNoPage,('VoutUV0','VoutUV1','page')),
		# 'OTPbitNoPage':(OTPbitNoPage,('OTP0','OTP1','page')),
		# 'OTWbitNoPage':(OTWbitNoPage,('OTW0','OTW1','page')),
		# 'FanFaultbitNoPage':(FanFaultbitNoPage,('FanFault0','FanFault1','page')),
		# 'FanWarnbitNoPage':(FanWarnbitNoPage,('FanWarn0','FanWarn1','page')),
		
 # 'WORDInput0':(WORDInput,('INOCW0','INOPW0','UVW0','UVP0','OFFLOWINPUT0')),
 # 'WORDPgood0':(WORDPgood,('Vmain',)),,'
 # 'WORDVout0':( WORDVout,('VOUTUV0','VoutOV0','VOUTTONMAX0')),
 # 'WORDIout0':( WORDIout,('IOUTOCP0','IOUTOCW0','IOUTOPW0','IOUTOPP0')),
 # 'WORDFans0':( WORDFans,('FANSFAN1F0','FANSFAN1W0','FANSFAN1Speed0')),
 # 'BYTEVinUV0':( BYTEVinUV,('UVP0',)),
 # 'BYTEOFF0':( BYTEOFF,('Vmain','Vsb')),
 # 'BYTETemp0':( BYTETemp,('TEMPFanFault0','TEMPOTW0')),
 # 'BYTEVoutOV0':( BYTEVoutOV,('VoutOV0',)),
 # 'BYTEIoutOC0':( BYTEIoutOC,('IOUTOCP0',)),
 
 # 'WORDInput1':(WORDInput,('INOCW1','INOPW1','UVW1','UVP1','OFFLOWINPUT1')),
 # 'WORDPgood1':(WORDPgood,('Vmain',)),
 # 'WORDVout1':( WORDVout,('VOUTUV1','VoutOV1','VOUTTONMAX1')),
 # 'WORDIout1':( WORDIout,('IOUTOCP1','IOUTOCW1','IOUTOPW1','IOUTOPP1')),
 # 'WORDFans1':( WORDFans,('FANSFAN1F1','FANSFAN1W1','FANSFAN1Speed1')),
 # 'BYTEVinUV1':( BYTEVinUV,('UVP1',)),
 # 'BYTEOFF1':( BYTEOFF,('Vmain','Vsb')),
 # 'BYTETemp1':( BYTETemp,('TEMPFanFault1','TEMPOTW1')),
 # 'BYTEVoutOV1':( BYTEVoutOV,('VoutOV1',)),
 # 'BYTEIoutOC1':( BYTEIoutOC,('IOUTOCP1',)),
    }


##########################################################################

    #do not modify this function, or model's will not be able to explore
    def input(self,input,outputValues,inputValues,arg):
        args = [arg,]
        for out in self.inputs[input][1]:
            if out != '':
                if out in outputValues:
                    args.append(outputValues[out])
                elif out in inputValues:
                    args.append(inputValues[out])
                else:
                    print('Input failed: %s'%input)
                    return ({},{},{})
                # args.append(outputValues[out])
        args=tuple(args)
        # print(input,args)
        (inputChange,outputChange,defaultValue)    = self.inputs[input][0](*args)
        return (inputChange,outputChange,defaultValue)

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
 # return (inputChange,outputChange,defaultValue)

#do not modify this function, or model's will not be able to explore
# def compute(self,output,outputValues):
    # args = []
    # for out in self.outputs[output][1]:
        # args.append(outputValues[out])
    # args=tuple(args)
    # return self.outputs[output][0](*args)
	
	
# test = localDoutputs()
# test.input('page',{},{},'00')

