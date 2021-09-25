# Actions
Actions = ['A', 'B', 'C', 'Imain', 'PSKILL']
Outputs = ['OUT', 'notOUT']
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