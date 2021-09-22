# Actions
def ClearFanFaultbit(): pass
def clearFaults(): pass
def MaskUVWbitPage00(): pass
def ClearUVPbitPagePlus01(): pass
def ClearOTPbitPagePlus00(): pass
def MaskUVPbitPage00(): pass
def ClearOFFLOWINPUTbit(): pass
def MaskVoutUVbitPage00(): pass
def ClearVoutUVbitPagePlus01(): pass
def B(): pass
def ClearVoutOVbit(): pass
def page(): pass
def ClearUVPbit(): pass
def ClearVoutUVbitPagePlus00(): pass
def MaskOTPbitPage01(): pass
def MaskFanFaultbitPage01(): pass
def ClearVoutOVbitPagePlus00(): pass
def ClearOFFLOWINPUTbitPagePlus01(): pass
def ClearUVWbitPagePlus01(): pass
def MaskUVPbitPage01(): pass
def ClearVoutOVbitPagePlus01(): pass
def MaskVoutOVbitPage00(): pass
def A(): pass
def C(): pass
def ClearFanFaultbitPagePlus01(): pass
def ClearUVPbitPagePlus00(): pass
def ClearVoutUVbit(): pass
def MaskUVWbitPage01(): pass
def ClearOTPbitPagePlus01(): pass
def ClearOTPbit(): pass
def PSKILL(): pass
def MaskOffLowInputbitPage01(): pass
def ClearOFFLOWINPUTbitPagePlus00(): pass
def Imain(): pass
def MaskOTPbitPage00(): pass
def ClearFanFaultbitPagePlus00(): pass
def MaskFanFaultbitPage00(): pass
def MaskVoutOVbitPage01(): pass
def MaskVoutUVbitPage01(): pass
def ClearUVWbitPagePlus00(): pass
def MaskOffLowInputbitPage00(): pass
def ClearUVWbit(): pass
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
(0, [('page', ('FF',))], 0, 1, {}),
(1, [('page', ('00',))], 0, 0, {}),
(1, [('page', ('01',))], 0, 2, {}),
(2, [('page', ('00',))], 0, 0, {}),
(2, [('page', ('FF',))], 0, 1, {}),
(2, [('MaskUVPbitPage01', (1,))], 0, 3, {}),
(3, [('page', ('00',))], 0, 4, {}),
(4, [('page', ('FF',))], 0, 5, {}),
(5, [('page', ('00',))], 0, 4, {}),
(5, [('page', ('01',))], 0, 3, {}),
(5, [('MaskUVPbitPage00', (0,))], 0, 6, {}),
(6, [('page', ('00',))], 0, 7, {}),
(7, [('page', ('FF',))], 0, 6, {}),
(7, [('MaskUVPbitPage00', (1,))], 0, 4, {}),
(7, [('page', ('01',))], 0, 8, {}),
(8, [('page', ('00',))], 0, 7, {}),
(8, [('page', ('FF',))], 0, 6, {}),
(8, [('MaskUVPbitPage00', (1,))], 0, 3, {}),
(8, [('MaskUVPbitPage01', (0,))], 0, 9, {}),
(9, [('page', ('00',))], 0, 10, {}),
(10, [('page', ('FF',))], 0, 11, {}),
(11, [('page', ('00',))], 0, 10, {}),
(11, [('MaskUVPbitPage00', (1,))], 0, 1, {}),
(11, [('page', ('01',))], 0, 9, {}),
(11, [('MaskUVPbitPage01', (1,))], 0, 6, {}),
(10, [('MaskUVPbitPage00', (1,))], 0, 0, {}),
(10, [('page', ('01',))], 0, 9, {}),
(10, [('MaskUVPbitPage01', (1,))], 0, 7, {}),
(9, [('page', ('FF',))], 0, 11, {}),
(9, [('MaskUVPbitPage00', (1,))], 0, 2, {}),
(9, [('MaskUVPbitPage01', (1,))], 0, 8, {}),
(7, [('MaskUVPbitPage01', (0,))], 0, 10, {}),
(6, [('MaskUVPbitPage00', (1,))], 0, 5, {}),
(6, [('page', ('01',))], 0, 8, {}),
(6, [('MaskUVPbitPage01', (0,))], 0, 11, {}),
(5, [('MaskUVPbitPage01', (0,))], 0, 1, {}),
(4, [('page', ('01',))], 0, 3, {}),
(4, [('MaskUVPbitPage00', (0,))], 0, 7, {}),
(4, [('MaskUVPbitPage01', (0,))], 0, 0, {}),
(3, [('page', ('FF',))], 0, 5, {}),
(3, [('MaskUVPbitPage00', (0,))], 0, 8, {}),
(3, [('MaskUVPbitPage01', (0,))], 0, 2, {}),
(2, [('MaskUVPbitPage00', (0,))], 0, 9, {}),
(1, [('MaskUVPbitPage01', (1,))], 0, 5, {}),
(1, [('MaskUVPbitPage00', (0,))], 0, 11, {}),
(0, [('page', ('01',))], 0, 2, {}),
(0, [('MaskUVPbitPage01', (1,))], 0, 4, {}),
(0, [('MaskUVPbitPage00', (0,))], 0, 10, {}),
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
"graph 5",
"state 3",
"graph 6",
"state 4",
"graph 7",
"state 5",
"graph 8",
"graph 9",
"graph 10",
"state 6",
"graph 11",
"state 7",
"graph 12",
"graph 13",
"graph 14",
"state 8",
"graph 15",
"graph 16",
"graph 17",
"graph 18",
"state 9",
"graph 19",
"state 10",
"graph 20",
"state 11",
"graph 21",
"graph 22",
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