# Actions
Actions = ['A', 'B', 'C', 'Imain', 'Imain', 'PSKILL', 'page', 'MaskUVWbitPage00', 'MaskUVWbitPage01', 'MaskUVPbitPage00', 'MaskUVPbitPage01', 'MaskOffLowInputbitPage00', 'MaskOffLowInputbitPage01', 'MaskVoutOVbitPage00', 'MaskVoutOVbitPage01', 'MaskVoutUVbitPage00', 'MaskVoutUVbitPage01', 'MaskOTPbitPage00', 'MaskOTPbitPage01', 'MaskFanFaultbitPage00', 'MaskFanFaultbitPage01', 'clearFaults', 'ClearUVWbitPagePlus00', 'ClearUVWbitPagePlus01', 'ClearUVWbit', 'ClearUVPbitPagePlus00', 'ClearUVPbitPagePlus01', 'ClearUVPbit', 'ClearOFFLOWINPUTbitPagePlus00', 'ClearOFFLOWINPUTbitPagePlus01', 'ClearOFFLOWINPUTbit', 'ClearVoutOVbitPagePlus00', 'ClearVoutOVbitPagePlus01', 'ClearVoutOVbit', 'ClearVoutUVbitPagePlus00', 'ClearVoutUVbitPagePlus01', 'ClearVoutUVbit', 'ClearOTPbitPagePlus00', 'ClearOTPbitPagePlus01', 'ClearOTPbit', 'ClearFanFaultbitPagePlus00', 'ClearFanFaultbitPagePlus01', 'ClearFanFaultbit']
Outputs = ['OUT']
# Default Values
DefaultActions = {'A': 0, 'B': 1, 'C': 1, 'Imain': 10}
DefaultOutputs = {'OUT': 0}
DefaultState = 'OFF'
# Test select Transitions
Preactions = []
TestTransitions = []

# States
states = {
 0 : {'name': 'ON', 'outputs': {'OUT': 1}, 'delay': 0},
 1 : {'name': 'OFF', 'outputs': {'OUT': 0}, 'delay': 0},
 2 : {'name': 'OffA', 'outputs': {'OUT': 0}, 'delay': 0},
 3 : {'name': 'OffB', 'outputs': {'OUT': 0}, 'delay': 0},
}

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