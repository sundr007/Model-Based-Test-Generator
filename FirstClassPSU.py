import stepper,os,sys
from time import sleep

# ==============================================================================
# Testing FSM
# ==============================================================================
class PSUFSM:
# class variable shared by all instances
    kind = 'Testing Model FSM'             
	
# instance variable unique to each instance
    def __init__(self, Actions,Outputs,defaultActions):
        # self.UserFSM 				= UserFSM
        self.states 				= ['Off',]
        self.stateValues 			= {}
        self.outputs				= Outputs
        self.outputValues 			= {}
        for Output in Outputs:
         self.outputValues[Output] 	= 0
        self.transitions 			= ()
        self.Allactions				= Actions
        self.actions 				= list(set([action for (action,aval,delay) in Actions]))
        self.defaultActions			= defaultActions
        self.actionValues 			= dict()
        for action in self.actions:
         self.actionValues[action]	= 0
        # self.currentState			= 0
		
    # def reset(self):
     # self.currentState=0
	  
    def CreateFSMGraph(self):
     os.system('python27 C:\\autotest\\ModelTester\\pmg.py ModelFSM')
     sleep(.1)
     os.system('move ModelFSM.dot CurrentTest\\TestingModelFSM.dot')
     sleep(.1)
     os.system('cd CurrentTest & dot -T pdf -o TestingModelFSM.pdf TestingModelFSM.dot & cd..')
     # shutil.copy2('CurrentTest\\out.pdf', testReportPath+'report\\data\\'+name+'\\0CurrentModelOverView.small.pdf')
	  
    def printToFile(self):
     outfile	=open("C:\\autotest\\ModelTester\\ModelFSM.py",'w')
     outfile.write('# Actions\n')
     for action in self.actions:
      outfile.write('def '+action+'(): pass\n')
     outfile.write('\n# States\n')
     outfile.write('states = {\n') 
     for state in self.states:
      outfile.write(' '+str(state)+' : '+str(self.states[state])+',\n')
     outfile.write('}\n\n')
     outfile.write('initial = 0\n')
     outfile.write('accepting = []\n')
     outfile.write('unsafe = []\n')
     outfile.write('frontier = []\n')
     outfile.write('finished = []\n')
     outfile.write('deadend = []\n')
     outfile.write('runstarts = [0]\n\n')
     outfile.write('# State Transitions\n')
     outfile.write('graph = (\n')
     for graph in self.transitions:
      outfile.write(str(graph).replace("'","")+',\n')
     outfile.write(")")
     outfile.close()
	 
    def WriteStateOutputTable(self):
     outfile	=open("CurrentTest\\Expanded Model State Output Table.csv",'w')
     stateName = list(self.states[0])[0]
     outputs = list(self.states[0][stateName])
     outfile.write(','.join(['State Name']+outputs)+'\n')
     for state in self.states:
      stateName = list(self.states[state])[0]
      outfile.write(','.join([str(stateName)]+[str(self.states[state][stateName][x]).replace(',','-') for x in outputs])+'\n')
     outfile.close()
	 
    def Currentoutputs(self):
     for Output in Outputs:
      self.outputValues[Output] 	= stepper.Measure(Output)
     return self.outputValues
	 
    def recall(self,actions):
     stepper.Reset()
     for (act,arg,delay) in actions:
      if len(arg)==2:
       stepper.TestAction(act,(sum(arg)/2,),delay)
       self.actionValues[act] = (sum(arg)/2,)
      else:
       stepper.TestAction(act,arg,delay)
       self.actionValues[act] = arg
	   
    def Explore(self,defaultActions=[],maxTransitions=10):
     # mp 			= self.UserFSM
     istate			= 0
     states			= dict()
     acts			= dict()
     outs			= dict()
     graph			= list()
     Explored		= list()
     # SetupActions 	= list()
# Set the default values for all actions in state 0.  
     self.recall(self.defaultActions)

     states[istate] = {istate: dict(self.Currentoutputs())}
     acts[istate] 		= dict(self.actionValues)
     outs[istate] 		= dict(self.Currentoutputs())
     Explored.append(istate)
     FSMstate 			= self.defaultActions
     i=self.ExploreActionsInState(graph,states,acts,outs,istate,Explored,FSMstate)
     self.states 		= dict(states)
     self.transitions 	= list(graph)
	 
    def ExploreActionsInState(self,graph,states,acts,outs,istate,Explored,FSMstate):
     FSMstate = FSMstate
     self.recall(FSMstate)
     startState = int(istate)
     allActions = self.Allactions
     allActionsWithoutDelay = list()
     for action in allActions:
      if action[0] != 'delay':
       allActionsWithoutDelay.append(action)
     # if 'delay' in mp.availableActions():
      # allActionsWithoutDelay=allActions
     for (action,args,delay) in allActionsWithoutDelay:
      self.states 		= dict(states)
      self.transitions 	= list(graph)
      self.printToFile()
      self.CreateFSMGraph()
      self.WriteStateOutputTable()
      arg = (sum(args)/2,) if len(args)==2 else args
      stateBefore	     	= int(istate)
      actionValuesBefore 	= dict(self.actionValues)
      outputValuesBefore 	= dict(self.Currentoutputs())
      # print('%s %s' % (action,arg))
      stepper.TestAction(action,arg,delay)
      self.actionValues[action] = arg
      stateAfter	     	= int(istate)
      actionValuesAfter 	= dict(self.actionValues)
      outputValuesAfter 	= dict(self.Currentoutputs())
      inputchange 			= actionValuesBefore != actionValuesAfter
      outputchange 			= outputValuesBefore != outputValuesAfter
      statechange			= stateBefore != stateAfter
      AlreadyBeenhere 		= (0,0)
      print(istate)
      for i in range(istate+1):
       # print('%s %s' % (acts[i],actionValuesAfter))
       # print('%s %s' % (outs[i],outputValuesAfter))
       if acts[i] == actionValuesAfter and outs[i] == outputValuesAfter:
        AlreadyBeenhere 	= (1,i)
        break
      sys.stdout.flush()
# New State
      if (inputchange or outputchange) and not AlreadyBeenhere[0]:
       print('New State')
       sys.stdout.flush()
       istate +=1
       # outputsMatchCurrentState = [outputValuesAfter[stateValue]==mp.stateValues[mp.CurrentState()][stateValue] for stateValue in mp.stateValues[mp.CurrentState()]]
       # outputsMatchCurrentState = 0 # if 'False' in outputsMatchCurrentState else 1
       # nameNotinUse = 1 if stateAfter not in [list(states[x])[0] for x in list(states)] else 0
       # if statechange and outputsMatchCurrentState and nameNotinUse:
        # states[istate] 	= {mp.CurrentState(): outputValuesAfter}
       # if nameNotinUse:
        # states[istate] 	= {istate: outputValuesAfter}
       # else:
       states[istate] 	= {istate: outputValuesAfter}
       # print(mp.CurrentState())
       acts[istate] 	= dict(actionValuesAfter)
       outs[istate] 	= dict(outputValuesAfter)
       graph.append((startState,(action,args,delay),istate))
       # print(str(istate)+str(states[istate]))

       if istate not in Explored:
        Explored.append(istate)
        print('Recursion')
        sys.stdout.flush()
        FSMstates = list(FSMstate)
        FSMstates.append((action,args,delay))
        istate=self.ExploreActionsInState(graph,states,acts,outs,istate,Explored,FSMstates)
        # self.recall(FSMstate)
        print('End Recursion')
        sys.stdout.flush()
# Previous State
      elif (inputchange or outputchange) and AlreadyBeenhere[0]:
       print('Previous State')
       graph.append((startState,(action,args,delay),AlreadyBeenhere[1]))
# Loopback Case
      elif (not inputchange and not outputchange):
       print('Loopback')
       # graph.append((startState,(action,args,1),startState))
      sys.stdout.flush()
      self.recall(FSMstate)
     return istate

# ==============================================================================

Actions 		= [	('PSON',(0,)	,1),
					('PSON',(1,)	,1),
					('PSKILL',(0,)	,1),
					('PSKILL',(1,)	,1),
					('AC',(180,264)	,4),
					('AC',(0,2)		,3)
					# ('PAGE00',(0,),0),
					# ('PAGE01',(0,),0),
					# ('PAGEFF',(0,),0),
					# ('ClearFaults',(0,),0)
				]
defaultActions 	= [('PSON',(1,),1),('PSKILL',(1,),1),('AC',(0,2),3)]
Outputs 		= 	[	'Vmain',
						# 'Vstby',
# Status
						# 'BYTE_OFF',
						# 'BYTE_Vout_OV',
						# 'BYTE_Iout_OC',
						# 'BYTE_Vin_UV',
						# 'BYTE_Temp',
						# 'BYTE_CML',
						# 'WORD_Vout',
						# 'WORD_Iout',
						# 'WORD_Input',
						# 'WORD_Pgood',
						# 'WORD_Fans',
						# 'WORD_Other',
						# 'VOUT_OV',
						# 'VOUT_UV',
						# 'VOUT_TON_MAX',
						# 'IOUT_OCP',
						# 'IOUT_OCW',
						# 'IOUT_OPP',
						# 'IOUT_OPW',
						'UVW0',
						'UVP0',
						'OFFLOWINPUT0',
						'UVW1',
						'UVP1',
						'OFFLOWINPUT1',
						# 'INPUT_OCW',
						# 'INPUT_OPW',
						# 'TEMP_OTP',
						# 'TEMP_OTW',
						# 'CML_INVALID_CMD',
						# 'CML_INVALID_DATA',
						# 'CML_PEC',
						# 'FANS_FAN1F',
						# 'FANS_FAN1W',
						# 'FANS_FAN1Speed'
					]

TestingFSM 	= PSUFSM(Actions,Outputs,defaultActions)

TestingFSM.Explore()
TestingFSM.printToFile()
TestingFSM.CreateFSMGraph()
TestingFSM.WriteStateOutputTable()










