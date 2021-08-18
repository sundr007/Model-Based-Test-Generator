# Actions
def ClearUVWbitPagePlus00(): pass
def MaskVoutOVbitPage01(): pass
def Imain(): pass
def B(): pass
def ClearOTPbitPagePlus01(): pass
def C(): pass
def MaskUVPbitPage00(): pass
def MaskVoutUVbitPage01(): pass
def ClearVoutUVbitPagePlus01(): pass
def ClearUVPbitPagePlus00(): pass
def page(): pass
def ClearOTPbit(): pass
def ClearOFFLOWINPUTbit(): pass
def ClearVoutOVbit(): pass
def ClearUVWbitPagePlus01(): pass
def MaskOffLowInputbitPage00(): pass
def MaskUVPbitPage01(): pass
def ClearOFFLOWINPUTbitPagePlus00(): pass
def ClearUVPbit(): pass
def ClearVoutOVbitPagePlus01(): pass
def ClearFanFaultbitPagePlus00(): pass
def MaskOffLowInputbitPage01(): pass
def MaskFanFaultbitPage01(): pass
def MaskOTPbitPage01(): pass
def ClearUVWbit(): pass
def ClearVoutUVbitPagePlus00(): pass
def ClearUVPbitPagePlus01(): pass
def ClearVoutOVbitPagePlus00(): pass
def MaskFanFaultbitPage00(): pass
def PSKILL(): pass
def ClearFanFaultbitPagePlus01(): pass
def MaskVoutUVbitPage00(): pass
def A(): pass
def MaskVoutOVbitPage00(): pass
def MaskUVWbitPage01(): pass
def MaskUVWbitPage00(): pass
def clearFaults(): pass
def MaskOTPbitPage00(): pass
def ClearVoutUVbit(): pass
def ClearOTPbitPagePlus00(): pass
def ClearOFFLOWINPUTbitPagePlus01(): pass
def ClearFanFaultbit(): pass

# States
states = {
 0 : {'name':'ON' , 'outputs':{'OUT': 1},'delay':0},
 1 : {'name':'OFF' , 'outputs':{'OUT': 0},'delay':0},
 2 : {'name':'OffA' , 'outputs':{'OUT': 0},'delay':0},
 3 : {'name':'OffB' , 'outputs':{'OUT': 0},'delay':0},
}

initial = 0
accepting = []
unsafe = []
frontier = []
finished = []
deadend = []
failedtransitions = []
passtransitions = []
runstarts = [0]

# State Transitions
graph = (
(0, [('A', (0.0,))], 1.0, 3, {}),
(3, [('A', (1.0,))], 4.0, 0, {}),
(1, [('B', (0.0,)), ('C', (1.0,))], 0.6, 3, {}),
(3, [('B', (1.0,))], 0.4, 1, {}),
(0, [('B', (1.0,))], 0.4, 2, {}),
(2, [('B', (0.0,)), ('C', (1.0,))], 0.6, 0, {}),
(2, [('A', (0.0,))], 1.0, 1, {}),
(1, [('A', (1.0,))], 4.0, 2, {}),
(3, [('C', (0.0,))], 0.4, 1, {}),
(0, [('C', (0.0,))], 0.4, 2, {}),
)