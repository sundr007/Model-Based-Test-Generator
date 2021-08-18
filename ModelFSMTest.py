# Actions
def ClearUVPbit(): pass
def ClearFanFaultbit(): pass
def A(): pass
def ClearUVWbit(): pass
def MaskUVPbitPage00(): pass
def MaskOffLowInputbitPage00(): pass
def MaskUVWbitPage00(): pass
def ClearUVWbitPagePlus01(): pass
def ClearUVPbitPagePlus01(): pass
def MaskFanFaultbitPage01(): pass
def Imain(): pass
def ClearOTPbitPagePlus00(): pass
def ClearFanFaultbitPagePlus01(): pass
def MaskOffLowInputbitPage01(): pass
def MaskUVWbitPage01(): pass
def C(): pass
def ClearUVWbitPagePlus00(): pass
def B(): pass
def clearFaults(): pass
def ClearVoutOVbitPagePlus01(): pass
def ClearOFFLOWINPUTbitPagePlus01(): pass
def ClearOFFLOWINPUTbit(): pass
def ClearVoutUVbitPagePlus01(): pass
def ClearVoutUVbitPagePlus00(): pass
def PSKILL(): pass
def ClearOFFLOWINPUTbitPagePlus00(): pass
def ClearUVPbitPagePlus00(): pass
def ClearOTPbitPagePlus01(): pass
def MaskVoutOVbitPage00(): pass
def MaskOTPbitPage00(): pass
def page(): pass
def MaskFanFaultbitPage00(): pass
def ClearVoutOVbitPagePlus00(): pass
def ClearOTPbit(): pass
def MaskUVPbitPage01(): pass
def MaskVoutUVbitPage00(): pass
def MaskVoutUVbitPage01(): pass
def ClearVoutOVbit(): pass
def ClearVoutUVbit(): pass
def MaskVoutOVbitPage01(): pass
def ClearFanFaultbitPagePlus00(): pass
def MaskOTPbitPage01(): pass
Outputs = ['OUT']
# States
states = {
 0 : {'name': 'OFF', 'outputs': {'OUT': 0}, 'delay': 0},
 1 : {'name': 1, 'outputs': {'OUT': 0}, 'delay': 0},
 2 : {'name': 2, 'outputs': {'OUT': 0}, 'delay': 0},
 3 : {'name': 3, 'outputs': {'OUT': 0}, 'delay': 0},
 4 : {'name': 4, 'outputs': {'OUT': 0}, 'delay': 0},
 5 : {'name': 5, 'outputs': {'OUT': 0}, 'delay': 0},
 6 : {'name': 6, 'outputs': {'OUT': 0}, 'delay': 0},
 7 : {'name': 7, 'outputs': {'OUT': 0}, 'delay': 0},
 8 : {'name': 8, 'outputs': {'OUT': 0}, 'delay': 0},
 9 : {'name': 9, 'outputs': {'OUT': 0}, 'delay': 0},
 10 : {'name': 10, 'outputs': {'OUT': 0}, 'delay': 0},
 11 : {'name': 11, 'outputs': {'OUT': 0}, 'delay': 0},
}

# State Transitions
graph = (
(0, [('MaskUVPbitPage00', (0,))], 0, 1, {}),
(1, [('MaskUVPbitPage00', (1,))], 0, 0, {}),
(1, [('MaskUVPbitPage01', (1,))], 0, 2, {}),
(2, [('MaskUVPbitPage01', (0,))], 0, 1, {}),
(2, [('MaskUVPbitPage00', (1,))], 0, 3, {}),
(3, [('MaskUVPbitPage00', (0,))], 0, 2, {}),
(3, [('MaskUVPbitPage01', (0,))], 0, 0, {}),
(3, [('page', ('01',))], 0, 4, {}),
(4, [('MaskUVPbitPage00', (0,))], 0, 5, {}),
(5, [('MaskUVPbitPage01', (0,))], 0, 6, {}),
(6, [('page', ('00',))], 0, 1, {}),
(6, [('MaskUVPbitPage00', (1,))], 0, 7, {}),
(7, [('MaskUVPbitPage00', (0,))], 0, 6, {}),
(7, [('page', ('00',))], 0, 0, {}),
(7, [('MaskUVPbitPage01', (1,))], 0, 4, {}),
(7, [('page', ('FF',))], 0, 8, {}),
(8, [('MaskUVPbitPage00', (0,))], 0, 9, {}),
(9, [('page', ('00',))], 0, 1, {}),
(9, [('MaskUVPbitPage00', (1,))], 0, 8, {}),
(9, [('MaskUVPbitPage01', (1,))], 0, 10, {}),
(10, [('MaskUVPbitPage01', (0,))], 0, 9, {}),
(10, [('page', ('00',))], 0, 2, {}),
(10, [('MaskUVPbitPage00', (1,))], 0, 11, {}),
(11, [('MaskUVPbitPage00', (0,))], 0, 10, {}),
(11, [('MaskUVPbitPage01', (0,))], 0, 8, {}),
(11, [('page', ('00',))], 0, 3, {}),
(11, [('page', ('01',))], 0, 4, {}),
(10, [('page', ('01',))], 0, 5, {}),
(9, [('page', ('01',))], 0, 6, {}),
(8, [('page', ('00',))], 0, 0, {}),
(8, [('MaskUVPbitPage01', (1,))], 0, 11, {}),
(8, [('page', ('01',))], 0, 7, {}),
(6, [('MaskUVPbitPage01', (1,))], 0, 5, {}),
(6, [('page', ('FF',))], 0, 9, {}),
(5, [('page', ('00',))], 0, 2, {}),
(5, [('MaskUVPbitPage00', (1,))], 0, 4, {}),
(5, [('page', ('FF',))], 0, 10, {}),
(4, [('MaskUVPbitPage01', (0,))], 0, 7, {}),
(4, [('page', ('00',))], 0, 3, {}),
(4, [('page', ('FF',))], 0, 11, {}),
(3, [('page', ('FF',))], 0, 11, {}),
(2, [('page', ('01',))], 0, 5, {}),
(2, [('page', ('FF',))], 0, 10, {}),
(1, [('page', ('01',))], 0, 6, {}),
(1, [('page', ('FF',))], 0, 9, {}),
(0, [('MaskUVPbitPage01', (1,))], 0, 3, {}),
(0, [('page', ('01',))], 0, 7, {}),
(0, [('page', ('FF',))], 0, 8, {}),
)
# Exploration Order
EventTracker = (
"state 0",
"state 1",
"graph 1",
"graph 2",
"state 2",
"graph 3",
"graph 4",
"state 3",
"graph 5",
"graph 6",
"graph 7",
"state 4",
"graph 8",
"state 5",
"graph 9",
"state 6",
"graph 10",
"graph 11",
"state 7",
"graph 12",
"graph 13",
"graph 14",
"graph 15",
"state 8",
"graph 16",
"state 9",
"graph 17",
"graph 18",
"graph 19",
"state 10",
"graph 20",
"graph 21",
"graph 22",
"state 11",
"graph 23",
"graph 24",
"graph 25",
"graph 26",
"graph 27",
"graph 28",
"graph 29",
"graph 30",
"graph 31",
"graph 32",
"graph 33",
"graph 34",
"graph 35",
"graph 36",
"graph 37",
"graph 38",
"graph 39",
"graph 40",
"graph 41",
"graph 42",
"graph 43",
"graph 44",
"graph 45",
"graph 46",
"graph 47",
"graph 48",
)