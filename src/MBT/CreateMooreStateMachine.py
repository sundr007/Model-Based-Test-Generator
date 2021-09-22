import copy,os,shutil,re,itertools,ast,sys,random
from time import sleep

# ==============================================================================
# Testing FSM
# ==============================================================================
class CreateMooreStateMachine:
# instance variable unique to each instance
    def __init__(self, UserFSM):
        self.UserFSM 		= UserFSM
        self.states 		= UserFSM.states
        self.transitions 	= UserFSM.transitions
	
    # def reset(self):
     # self.currentState=0
# ======================================
# Error Reporting
# ======================================
    def ReportError(self,newline=''): 
     if newline=='':
      file = open('Temp\\ExploreProgress.txt','w')
     else:
      file = open('Temp\\ExploreProgress.txt','a')
      file.write(newline+'\n')
     file.close()
	  
    def printToFile(self,outputsToUse=[],ExtraOutputs=[]):
     outfile	=open("ModelFSMTest.py",'w')
     outfile.write('# Actions\n')
     for action in self.UserFSM.actions:
      outfile.write('def '+action+'(): pass\n')
     if outputsToUse!=[]:
      outfile.write('Outputs = '+str(outputsToUse+ExtraOutputs))
     else:
      outfile.write('Outputs = '+str(self.UserFSM.outputs))
     outfile.write('\n# States\n')
     outfile.write('states = {\n') 
     for state in self.states:
      outfile.write(' '+str(state)+' : '+str(self.states[state])+',\n')
     outfile.write('}\n\n')
     outfile.write('# State Transitions\n')
     outfile.write('graph = (\n')
     for graph in self.transitions:
      outfile.write(str(graph).replace("''","'")+',\n')
      # outfile.write(str(graph).replace("'","").replace('"',"'")+',\n')
     outfile.write(")\n")
     outfile.write('# Exploration Order\n')
     outfile.write('EventTracker = (\n')
     for event in self.EventTracker:
      outfile.write('"'+str(event)+'",\n')
     outfile.write(")")
     outfile.close()
	 
    def WriteStateOutputTable(self):
     outfile	=open("CurrentTest\\ModelFSMTest State Output Table.csv",'w')
     stateName = self.states[0]['name']
     outfile.write(','.join(['State Name']+list(self.states[0]['outputs']))+'\n')
     for state in self.states:
      stateName = self.states[state]['name']
      outfile.write(','.join([str(stateName)]+[str(self.states[state]['outputs'][x]).replace(',','-') for x in list(self.states[state]['outputs'])])+'\n')
     outfile.close()
	  
    def Explore(self,actionsToUse=[],outputsToUse=[],ExtraOutputs=[]):
     print(actionsToUse)
     mp = copy.deepcopy(self.UserFSM)
     istate		= 0
     states		= dict()
     acts		= dict()
     outs		= dict()
     graph		= list()
     EventTracker = list()
     if outputsToUse==[]:
      outputsToUse = list(mp.Currentoutputs())
     states[istate] = {'name':mp.CurrentState(),'outputs': { output: mp.Currentoutputs()[output] for output in outputsToUse+ExtraOutputs },'delay':0}
     print(mp.CurrentState())
     acts[istate] 		= dict(self.InputActionsValues(mp))
     outs[istate] 		= { output: mp.Currentoutputs()[output] for output in outputsToUse }
     EventTracker.append('state %s'%istate)
     FSMstate 			= mp.save()
     mpp = copy.deepcopy(mp)
     i=self.ExploreActionsInState(self.UserFSM,graph,states,acts,outs,istate,FSMstate,actionsToUse,outputsToUse,ExtraOutputs,EventTracker)
     print(states)
     self.states 		= states
     self.transitions 	= graph
     self.EventTracker = EventTracker
     self.ReportError('%s States' % len(states))
     self.ReportError('%s Transitions' % len(graph))
     self.ReportError('Exploration Successful')
	 
    def InputActionsValues(self,mp):
      actionVals = dict()
      # print(mp.actionValues)
      for key in list(mp.actionValues):
       for (act,actionval,delay) in list(mp.Allactions):
        if act == key and len(actionval)==1:
          actionVals[key] = mp.actionValues[key]
        elif act == key and len(actionval)==2 and type(actionval[1]) is str:
          actionVals[key] = mp.actionValues[key]
        elif act == key and len(actionval)==2 and actionval[0] <= mp.actionValues[key] <= actionval[1]:
          actionVals[key] = actionval[0]
      # print(actionVals)
      return actionVals

	 
    def ExploreActionsInState(self,UserFSM,graph,states,acts,outs,istate,FSMstate,actionsToUse,outputsToUse,ExtraOutputs,EventTracker):
     mp = copy.deepcopy(UserFSM)
     mp.recall(*FSMstate)
     startState = int(istate)
     allActions = list(mp.Allactions) 
    #  print(allActions)
     newAction=[]
# If actions are limited this will set it. 
     if actionsToUse!=[]:
      for i,(action,args,delay) in enumerate(allActions):
      #  print(action,args)
       if action in actionsToUse:
        newAction.append((action,args,delay))
      allActions=newAction
	  
     for (action,args,delay) in allActions:
      arg = (sum(args)/2,) if len(args)==2 and type(args[1]) is not str else args
      stateBefore	     	= str(mp.currentState)
      outputValuesBefore 	= { output: mp.Currentoutputs()[output] for output in outputsToUse } #dict(mp.Currentoutputs())
      actionValuesBefore 	= dict(self.InputActionsValues(mp))
      print('%s %s' % (action,args))
      delay = mp.doAction(action,arg)
      stateAfter	     	= str(mp.currentState)
      outputValuesAfter 	= { output: mp.Currentoutputs()[output] for output in outputsToUse } #dict(mp.Currentoutputs())
      actionValuesAfter 	= dict(self.InputActionsValues(mp))
      inputchange 			= actionValuesBefore != actionValuesAfter
      outputchange 			= outputValuesBefore != outputValuesAfter
      statechange			= stateBefore != stateAfter
      AlreadyBeenhere 		= (0,0)
      for i in range(istate+1):
       if acts[i] == actionValuesAfter and outs[i] == outputValuesAfter:
        AlreadyBeenhere 	= (1,i)
# New State
      if (inputchange or outputchange) and not AlreadyBeenhere[0]:
       print('New State')
       print(actionValuesBefore)
       print(actionValuesAfter)
       istate +=1
       outputsMatchCurrentState = [mp.Currentoutputs()[stateValue]==mp.stateValues[mp.CurrentState()][stateValue] for stateValue in list(mp.stateValues[mp.CurrentState()])]
       outputsMatchCurrentState = 0 if 'False' in outputsMatchCurrentState else 1
       nameNotinUse = 1 if mp.CurrentState() not in [states[x]['name'] for x in list(states)] else 0
       if statechange and outputsMatchCurrentState and nameNotinUse:
        states[istate] 	= {'name':mp.CurrentState(),'outputs': { output: mp.Currentoutputs()[output] for output in outputsToUse+ExtraOutputs },'delay':0}
       # elif nameNotinUse:
        # states[istate] 	= {mp.CurrentState()+action: outputValuesAfter}
       else:
        states[istate] 	= {'name':istate, 'outputs': { output: mp.Currentoutputs()[output] for output in outputsToUse+ExtraOutputs },'delay':0}
       EventTracker.append('state %s'%istate)
       print(states)
       acts[istate] 	= dict(actionValuesAfter)
       outs[istate] 	= dict(outputValuesAfter) #dict(mp.Currentoutputs())
       endState = int(istate)
       graph.append((startState,[('%s' % action,args)],delay,endState,{}))
       EventTracker.append('graph %s'%len(graph))
       # print(str(istate)+str(states[istate]))
       # print('Recursion')
       FSMstates = mp.save()
       # mpp = copy.deepcopy(mp)
       istate=self.ExploreActionsInState(UserFSM,graph,states,acts,outs,istate,FSMstates,actionsToUse,outputsToUse,ExtraOutputs,EventTracker)
       # print('End Recursion')
# Previous State
      elif (inputchange or outputchange) and AlreadyBeenhere[0]:
       print('Previous State')
       graph.append((startState,[('%s' % action,args)],delay,AlreadyBeenhere[1],{}))
       EventTracker.append('graph %s'%len(graph))
# Loopback Case
      elif (not inputchange and not outputchange):
       print('Loopback')
       # graph.append((startState,(action,args,1),startState))
      mp.reset()
      mp.recall(*FSMstate)
     return istate

# ==============================================================================
