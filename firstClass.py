import copy,os,shutil,re,itertools,ast,sys,random
from time import sleep
from csv import reader
from numpy import cumsum
from numpy.random import rand
import networkx as nx
from ChinesePostMan import CPP

import importlib.util as IMPORTER

# ==============================================================================
# FSM Class
# ==============================================================================

#the computerOutputs param is used to pass in the path to the model directory
class FSM:
# instance variable unique to each instance
    def __init__(self, states, transitions, outputs,DefaultValues , computedOutputs='',SpecFilePath=''):
        if SpecFilePath!='':  
         SpecFile	=open(SpecFilePath,'r')
         self.Specs={}
         for line in SpecFile:
          if line.split(',')[2] == '':
           self.Specs[line.split(',')[0]]='(%s,%s)' % (line.split(',')[1] if line.split(',')[1]!='' else '0',line.split(',')[3].replace('\n','') if line.split(',')[3]!='\n' else '0')
          else:
           self.Specs[line.split(',')[0]]=line.split(',')[2]
         SpecFile.close()
        if computedOutputs != '':
         #loads the inputOutput file from the model directory
         ioSpec = IMPORTER.spec_from_file_location("InputOuputs.py", computedOutputs+'InputOutputs.py') #(module name, path)
         inOutFile = IMPORTER.module_from_spec(ioSpec)
         ioSpec.loader.exec_module(inOutFile)
         self.modelDoutputs = inOutFile.localDoutputs()
         self.computedOutputs = list(self.modelDoutputs.outputs)
         self.computedInputs = list(self.modelDoutputs.inputs)
        else:
         self.computedOutputs = []
         self.computedInputs = []
        self.states 		= [states[x]['name'] for x in list(states)]
        self.stateValues 	= dict()
        for i,state in enumerate(self.states):
         self.stateValues[state] = states[i]['outputs']
        self.stateDelays 	= dict()
        for i,state in enumerate(self.states):
         self.stateDelays[i] = states[i]['delay']
        self.outputs		= list(set(outputs+self.computedOutputs))
        self.outputValues 	= dict()
        for i,output in enumerate(self.outputs):
         self.outputValues[output] = 0
        self.transitions 	= transitions
        self.Allactions 	= list()
        for transition in self.transitions:
         for actAndVal in transition[1]:
          action = actAndVal[0]
          aval = actAndVal[1]
          delay = transition[2]
          if (action,aval,delay) not in self.Allactions:
           self.Allactions.append((action,aval,delay))
        for action in self.computedInputs:
         (aval,delay) = self.modelDoutputs.inputs[action][2]

         self.Allactions.append((action,aval,delay))
        self.Allactions		= list(set(self.Allactions))
        self.actions 		= list(set([action for (action,aval,delay) in self.Allactions]))
        self.actionValues 	= dict()
        for action in self.actions:
         self.actionValues[action]=0
        self.currentState=0

        self.pcurrentState=self.currentState
        self.pactionValues=dict(self.actionValues)
        self.poutputValues=dict(self.outputValues)
# Set the default values for all actions in state 0.
        self.DefaultActions = dict(DefaultValues.DefaultActions)
        self.DefaultOutputs = dict(DefaultValues.DefaultOutputs)
        # for transition in self.transitions:
         # if self.transitionFinalState(transition) == 0:
          # actionval = self.transitionActionVals(transition)[0]
          # action 	= self.transitionActions(transition)[0]
          # actionval = sum(actionval)/2 if len(actionval)==2 else actionval[0]
          # self.DefaultActions[action]=actionval
        self.reset()
        self.ReportError() # Reset Error File

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
# ======================================

    def printToFile(self,numbered=0,highlightedTransitions=[],red=[],green=[]):
# Numbered option=1 changes the delay numbers in diagram to transition number
# Helps with writing tests.
     outfile	=open("HighLevelModel.py",'w')
     outfile.write('# Actions\n')
     for action in self.actions:
      outfile.write('def '+action+'(): pass\n')
     outfile.write('\n# States\n')
     outfile.write('states = {\n')
     for i,state in enumerate(self.states):
      outfile.write(' '+str(i)+" : {'name':'"+str(state)+"' , 'outputs':"+str(self.stateValues[state])+",'delay':"+str(self.stateDelays[i])+'},\n')
     outfile.write('}\n\n')
     outfile.write('initial = 0\n')
     outfile.write('accepting = []\n')
     outfile.write('unsafe = []\n')
     outfile.write('frontier = []\n')
     outfile.write('finished = []\n')
     if highlightedTransitions == []:
      outfile.write('deadend = []\n')
     else:
      outfile.write('graytransitions = ['+','.join(['('+str(self.transitionInitState(self.transitions[int(x)]))+','+str(self.transitionFinalState(self.transitions[int(x)]))+')' for x in highlightedTransitions])+']\n')
     if red != []:
      outfile.write('failedtransitions = ['+','.join([str(x) for x in red])+']\n')
     else:
      outfile.write('failedtransitions = []\n')
     if green != []:
      outfile.write('passtransitions = ['+','.join([str(x) for x in green])+']\n')
     else:
      outfile.write('passtransitions = []\n')
     outfile.write('runstarts = [0]\n\n')
     outfile.write('# State Transitions\n')
     outfile.write('graph = (\n')
     for graph in self.transitions:
      outfile.write(str(graph)+',\n')
     outfile.write(")")
     outfile.close()

    def CreateFSMGraph(self,outname=['HighLevelModel',],inname='HighLevelModel'):
     os.system('move %s.dot CurrentTest\\%s.dot' % (inname,outname[0]))
     sleep(.1)
     if inname == 'ExploredModel' and len(self.transitions)>150:
      os.system('cd CurrentTest & sfdp -T pdf  -Gsize="7.5,7.5" -o %s.pdf %s.dot & cd..' % (outname[0],outname[0]))
     else:
      os.system('cd CurrentTest & dot -T pdf  -Gsize="7.5,7.5" -o %s.pdf %s.dot & cd..' % (outname[0],outname[0]))
     if len(outname)==2:
      os.system('cd CurrentTest & move %s.pdf "%s%s.small.pdf" & cd..' % (outname[0],outname[1],outname[0]))
      os.system('cd CurrentTest & move %s.dot "%s%s.dot" & cd..' % (outname[0],outname[1],outname[0]))
      # os.system('cd CurrentTest & rm %s.dot & cd..' % (outname[0]))

    def WriteStateOutputTable(self):
     outfile	=open("CurrentTest\\State Output Tablestatetable.csv",'w')
     outfile.write(','.join(['State Name']+self.outputs)+'\n')
     for state in self.states:
      outputs=list()
      for output in self.outputs:
       if output in list(self.stateValues[state]):
        outputs.append(str(self.stateValues[state][output]).replace(',','-'))
       else:
        outputs.append('')
      outfile.write(','.join([str(state)]+outputs)+'\n')
     outfile.close()

    def WriteStateTransitionTable(self):
     outfile	=open("CurrentTest\\State Transition Tablestatetable.csv",'w')
     outfile.write(','.join(['Transition Name','Action','Action Value']+self.outputs)+'\n')
     for i,transition in enumerate(self.transitions):
      outputs=list()
      for output in self.outputs:
       # print(self.transitionOutputs(transition))
       if output in list(self.transitionOutputs(transition)):
        outputs.append(str(self.transitionOutputs(transition)[output]).replace(',','-'))
       else:
        outputs.append('')
      arg = str(self.transitionActionVals(transition)[0][0]) if len(self.transitionActionVals(transition)[0])==1 else str(self.transitionActionVals(transition)[0]).replace(',','-')
      outfile.write(','.join([str(i),self.transitionActions(transition)[0],arg]+outputs)+'\n')
     outfile.close()

    def WriteBehavioralModelTable(self):
     outfile	=open("CurrentTest\\Behavioral Actions.tex",'w')
     outfile.write(r'Behavioral Actions:'+'\n\n')
     outfile.write(r'\noindent\rule{0.5\linewidth}{0.4pt}'+'\n')
     outfile.write(r'\begin{labeling}{ClearOFFLOWINPUTbitPagePlus00}'+'\n')
     for action in self.computedInputs:
      (inputChanges,outputs) = self.modelDoutputs.input(action,self.outputValues)
      outputs = ', '.join(['%s:%s' % (key,outputs[key]) for key in list(outputs)])
      outfile.write('\item [%s] %s\n' % (action,outputs))
     outfile.write(r'\end{labeling}'+'\n')
     outfile.close()

    def reset(self):
     for act in list(self.DefaultActions):
      self.doAction(act,self.DefaultActions[act])
     for output in self.outputs:
      if output in list(self.DefaultOutputs):
       self.outputValues[output] = self.DefaultOutputs[output]
     self.ComputeOutputs()
     self.currentState=0

    def saveState(self):
     self.pcurrentState=int(self.currentState)
     self.pactionValues=dict(self.actionValues)
     self.poutputValues=dict(self.outputValues)

    def save(self):
     return (int(self.currentState),dict(self.actionValues),dict(self.outputValues))

    def recall(self,currentState,actionValues,outputValues):
     self.currentState=int(currentState)
     self.actionValues=dict(actionValues)
     self.outputValues=dict(outputValues)
     self.ComputeNextState()
     self.ComputeOutputs()
     self.saveState()

    def undo(self):
     self.currentState=int(self.pcurrentState)
     self.actionValues=dict(self.pactionValues)
     self.outputValues=dict(self.poutputValues)
     self.ComputeNextState()
     self.ComputeOutputs()
     self.saveState()

    def CurrentStateoutputs(self):
     return self.stateValues[self.states[self.currentState]]
    def Currentoutputs(self):
     self.ComputeOutputs()
     return self.outputValues
    def CurrentState(self):
     return self.states[self.currentState]
    def availableActions(self):
     actions=[]
     actionValues=[]
     for transition in self.transitions:
      if transition[0] == self.currentState:
       for actAndVal in transition[1]:
        actions.append(actAndVal[0])
        actionValues.append(actAndVal[1])
     return actions

    def doAction(self,action='',args=''):
     if type(args) is not str:
      self.saveState()
      # print('Action: %s: %s' % (action,args))
      if action in self.computedInputs:
       (inputChanges,outputChanges) = self.modelDoutputs.input(action,self.outputValues)
       for input in list(inputChanges):
        self.actionValues[input] = inputChanges[input]
       for output in list(outputChanges):
        if output in self.outputs:
         self.outputValues[output] = outputChanges[output]
      else:
       self.actionValues[action]=args
      try:
       delay = self.ComputeNextState()
       if action.lower() == 'delay':
        self.actionValues[action]=0
      except:
       self.ReportError('An infinite loop occured while traversing the state machine.')
       self.ReportError('This is typically caused by a path in the state machine that allows it to switch between two states continuously.')
       print('An infinite loop occured while traversing the state machine')
       exit()
       delay=1
      self.ComputeOutputs()
      return delay

    def transitionActions(self,transition):
     actions=[]
     for actAndVal in transition[1]:
      actions.append(actAndVal[0])
     return actions

    def transitionInitState(self,transition):
     return transition[0]
    def transitionFinalState(self,transition):
     return transition[3]
    def transitionDelay(self,transition):
     return transition[2]
    def transitionOutputs(self,transition):
     return transition[4]
    def transitionActionVals(self,transition):
     actionValues=[]
     for actAndVal in transition[1]:
      actionValues.append(actAndVal[1])
     return actionValues

    def ComputeNextState(self):
# Go through every transition and check to see if the conditions are right to follow that transition.
# First check if initial state is current state. Then check to see if action/values are correct.
# Then follow transition unless it's a loop back.
     delay = 0
     delayLoopback = 0
     for transition in self.transitions:
      if self.transitionInitState(transition) == self.currentState:
       actionsAndValuesMatch = 1 # set this to true, if it makes it through the next loop then really is true.
       for TransAction,TransActionValue in zip(self.transitionActions(transition),self.transitionActionVals(transition)):
        if len(TransActionValue) == 2:
         if TransActionValue[0] <= float(self.actionValues[TransAction]) <= TransActionValue[1]:
          actionsAndValuesMatch = actionsAndValuesMatch * 1
         else:
          actionsAndValuesMatch = actionsAndValuesMatch * 0
        else:
         if TransActionValue[0] == float(self.actionValues[TransAction]):
          actionsAndValuesMatch = actionsAndValuesMatch * 1
         else:
          actionsAndValuesMatch = actionsAndValuesMatch * 0
       if actionsAndValuesMatch:
        if self.transitionInitState(transition) != self.transitionFinalState(transition):
# Not a loop back
         self.currentState = self.transitionFinalState(transition)
         if list(self.transitionOutputs(transition)) != []:
          for output in list(self.transitionOutputs(transition)):
           self.outputValues[output] = self.transitionOutputs(transition)[output]
         delay += self.transitionDelay(transition)
         delay += self.stateDelays[self.currentState]
         delay += self.ComputeNextState()
        else:
         delay += self.transitionDelay(transition)
         delay += self.stateDelays[self.currentState]
       else:
        delayLoopback = self.transitionDelay(transition)
     if delay==0:
      delay = 0
     return delay

    def ComputeOutputs(self):
     for output in list(self.CurrentStateoutputs()):
      self.outputValues[output] = self.CurrentStateoutputs()[output]
     if self.computedOutputs != []:
      for output in self.computedOutputs:
       outputValue = self.modelDoutputs.compute(output,self.outputValues)
       outputValue = ast.literal_eval(self.Specs[output+'='+str(outputValue)]) if output+'='+str(outputValue) in list(self.Specs) else outputValue
       self.outputValues[output]=outputValue

    def State2State(self,Start,End,raw=0):
     graph = self.transitions
     nodes = list(self.states)
     G=nx.MultiDiGraph()
     for i,edge in enumerate(graph):
      G.add_edge(edge[0],edge[3],i)
     path = nx.shortest_path(G,Start,End)
     path_edges = zip(path,path[1:])
     TransitionList = []
     for (start,end) in path_edges:
      for i,(star,x,y,en,z) in enumerate(graph):
       if start==star and end==en:
        TransitionList.append(i)
        break
     actions		= [self.transitionActions(graph[transition]) for transition in TransitionList]
     actionvalues	= [self.transitionActionVals(graph[transition]) for transition in TransitionList]
     if raw:
      return (actions,actionvalues,TransitionList)
     else:
      (actions,actionvalues) = VariationsAlongPath(actions,actionvalues)
      return ([x[0] for x in actions],[x[0] for x in actionvalues],TransitionList)


def VariationsAlongPath(actions,actionvalues):
 allactions			= list()
 allactionvalues	= list()
 mainactions		= list()
 mainactionvalues	= list()
 seqActionVals		= list()
 seqActions			= list()
 OneTimeVals		= list()
 OneTimeActs		= list()
 OneTimeValss		= list()
 OneTimeActss		= list()
 for i,actionvalue in enumerate(actionvalues):
  if '*' in actionvalue:
   OneTimeActs.append(actions[i])
   actionvalue=actionvalue.replace('*','')
   OneTimeVals.append(decodeActionVals(actionvalue))
  else:
   seqActions.append(actions[i])
   seqActionVals.append(decodeActionVals(actionvalue))
 for combination in list(itertools.product(*seqActionVals)):
  mainactions.append(seqActions)
  mainactionvalues.append([(a,) for a in combination])
 for combination in list(itertools.product(*OneTimeVals)):
  OneTimeActss.append(OneTimeActs)
  OneTimeValss.append([(a,) for a in combination])
 if OneTimeVals != []:
  for i,OneTimeVal in enumerate(OneTimeValss):
   allactions.extend([[OneTimeActss[i]+mainactions[0]]+mainactions[1::]])
   allactionvalues.extend([[OneTimeVal+mainactionvalues[0]]+mainactionvalues[1::]])
 else:
  allactions		= [[x] for x in mainactions]
  allactionvalues	= [[x] for x in mainactionvalues]
 # print('%s\n%s\n'%(allactions,allactionvalues))
 return (allactions,allactionvalues)

def xfrange(start, stop, step):
 step = max(step,0.1)
 while start < stop:
  yield start
  start += step

def decodeActionVals(actionvalue):
 if '-' in actionvalue and ':' not in actionvalue:
  values = actionvalue.split('-')[1].replace('[','').replace(']','').split(';')
  values = [float(ele) for ele in values]
  return tuple(values)
  # seqActionVals.append(tuple(values))
 elif '-' in actionvalue and actionvalue.count(':')==2:
  (min,step,max)	= [float(ala) for ala in actionvalue.split('-')[1].replace('[','').replace(']','').split(':')]
  values = [round(x,1) for x in xfrange(min, max, step)]
  return tuple(values)
  # seqActionVals.append(tuple(values))
 elif '-' in actionvalue and actionvalue.count(':')==1:
  (min,max)	= [float(ala) for ala in actionvalue.split('-')[1].replace('[','').replace(']','').split(':')]
  values = [round(x,1) for x in xfrange(min, max, 1)]
  return tuple(values)
  # seqActionVals.append(tuple(values))
 else:
  return actionvalue
  # seqActionVals.append(actionvalue)

def TransitionDelay(transition):
 return transition[3]

def transitionActions(transition):
 actions=[]
 for actAndVal in transition[1]:
  actions.append(actAndVal[0])
 return actions

def transitionActionVals(transition):
 actionValues=[]
 for actAndVal in transition[1]:
  actionValues.append(actAndVal[1])
 return actionValues

def SequenceActions(transitions,tseq,trans):
 seqActions=[]
 for i in tseq:
  seqActions.extend(transitionActions(transitions[i]))
 seqActionVals 				= list()
 for i in range(len(tseq)):
  if '-' in trans[i]:
   seqActionVals.append(trans[i])
  else:
   seqActionVals.extend(transitionActionVals(transitions[tseq[i]]))
 # print(seqActions)
 (seqActions,seqActionVals) = VariationsAlongPath(seqActions,seqActionVals)
 return (seqActions,seqActionVals)
# ==============================================================================
# Testing FSM
# ==============================================================================
class TestingFSM:
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

    def CreateFSMGraph(self):
     os.system('python27 pmg.py ModelFSM')
     sleep(.1)
     os.system('move ModelFSM.dot CurrentTest\\TestingModelFSM.dot')
     sleep(.1)
     os.system('cd CurrentTest & dot -T pdf -o TestingModelFSM.pdf TestingModelFSM.dot & cd..')
     # shutil.copy2('CurrentTest\\out.pdf', testReportPath+'report\\data\\'+name+'\\0CurrentModelOverView.small.pdf')

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
      outfile.write(str(graph).replace("'","").replace('"',"'")+',\n')
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
     mp = copy.deepcopy(self.UserFSM)
     istate		= 0
     states		= dict()
     acts		= dict()
     outs		= dict()
     graph		= list()
     if outputsToUse==[]:
      outputsToUse = list(mp.Currentoutputs())
     states[istate] = {'name':mp.CurrentState(),'outputs': { output: mp.Currentoutputs()[output] for output in outputsToUse+ExtraOutputs },'delay':0}
     acts[istate] 		= dict(self.InputActionsValues(mp))
     outs[istate] 		= { output: mp.Currentoutputs()[output] for output in outputsToUse }
     FSMstate 			= mp.save()
     mpp = copy.deepcopy(mp)
     i=self.ExploreActionsInState(self.UserFSM,graph,states,acts,outs,istate,FSMstate,actionsToUse,outputsToUse,ExtraOutputs)
     self.states 		= states
     self.transitions 	= graph
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
        elif act == key and len(actionval)==2 and actionval[0] <= mp.actionValues[key] <= actionval[1]:
          actionVals[key] = actionval[0]
      # print(actionVals)
      return actionVals


    def ExploreActionsInState(self,UserFSM,graph,states,acts,outs,istate,FSMstate,actionsToUse,outputsToUse,ExtraOutputs):
     mp = copy.deepcopy(UserFSM)
     mp.recall(*FSMstate)
     startState = int(istate)
     allActions = list(mp.Allactions)
     newAction=[]
# If actions are limited this will set it.
     if actionsToUse!=[]:
      for i,(action,args,delay) in enumerate(allActions):
       # print(action,actionsToUse)
       if action in actionsToUse:
        newAction.append((action,args,delay))
      allActions=newAction

     for (action,args,delay) in allActions:
      arg = sum(args)/2 if len(args)==2 else args[0]
      stateBefore	     	= str(mp.currentState)
      outputValuesBefore 	= { output: mp.Currentoutputs()[output] for output in outputsToUse } #dict(mp.Currentoutputs())
      actionValuesBefore 	= dict(self.InputActionsValues(mp))
      # print('%s %s' % (action,arg))
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
       # print(mp.CurrentState())
       acts[istate] 	= dict(actionValuesAfter)
       outs[istate] 	= dict(outputValuesAfter) #dict(mp.Currentoutputs())
       endState = int(istate)
       graph.append((startState,[('"%s"' % action,args)],delay,endState,{}))
       # print(str(istate)+str(states[istate]))
       # print('Recursion')
       FSMstates = mp.save()
       # mpp = copy.deepcopy(mp)
       istate=self.ExploreActionsInState(UserFSM,graph,states,acts,outs,istate,FSMstates,actionsToUse,outputsToUse,ExtraOutputs)
       # print('End Recursion')
# Previous State
      elif (inputchange or outputchange) and AlreadyBeenhere[0]:
       print('Previous State')
       graph.append((startState,[('"%s"' % action,args)],delay,AlreadyBeenhere[1],{}))
# Loopback Case
      elif (not inputchange and not outputchange):
       print('Loopback')
       # graph.append((startState,(action,args,1),startState))
      mp.reset()
      mp.recall(*FSMstate)
     return istate

# ==============================================================================

# ==============================================================================
# FSM Class
# ==============================================================================
class SpecTest:
# ====================================
# Static Methods
# ====================================
    def TestSectionName(i,test):
     return test[0][0]
    # def TestName(i,test):
     # return test[1][0]
    def initactions(i,test):
     return test[1]
    def Transitions(i,test):
     return test[2]
    def Inputs(i,test):
     return test[3]
    def InputsBefore(i,test):
     return test[4][0]
    def outputs(i,test):
     return test[5]
    def TestType(i,test):
     return test[6][0]
# class variable shared by all instances
    kind = 'Create and Run Specified Tests'
# instance variable unique to each instance
    def __init__(self, FSM, testFilePath, TestFSM):
        self.FSM 					= FSM
        self.TestFSM 				= TestFSM
        self.testFilePath			= testFilePath
        self.currentTestFilePath   	= testFilePath
        self.tests					= LoadTestsfromTestFile(self.testFilePath)

    def createRegressionTest(self,ChangesOnly=0,TestLength=10):
     self.CreateDataAndReportFolders()
     testedTransitions = []
     TotalNumberOfSteps = 0
     j=0
# Use the CPP class to find a solution to the Chinese postman problem which gives an optimal procedure that tests all paths at least once.
     nodes = list(self.TestFSM.states)
     sys = CPP(len(nodes))
     for i,edge in enumerate(self.TestFSM.transitions):
      sys.addArc(i,edge[0],edge[3],1)
     if sys.solve():
      solution = sys.printCPT(0)
      #for (y,z,x) in solution:
       #print (y,z,x)
      transitions = [x for (y,z,x) in solution]
     else:
      startState = 0
      solution = []
      for i,edge in enumerate(self.TestFSM.transitions):
       (initactions,initactionvalues,TransitionList) 	= self.TestFSM.State2State(startState,edge[0],1)
       solution = solution + TransitionList + [i]
       startState = edge[3]
      transitions = list(solution)
      #for x in transitions:
      # print (x)

# Break the large test procedure into individual tests of length "TestLength"
     while(len(testedTransitions) < len(self.TestFSM.transitions)):
      startState										= self.TestFSM.transitions[transitions[0]][0]
      if startState ==0:
       TransitionList=[]
      else:
       (initactions,initactionvalues,TransitionList) 	= self.TestFSM.State2State(0,startState,1)
      for i in range(TestLength):
       if len(transitions)>0:
        TransitionList.append(transitions[0])
        transitions.pop(0)
       else:
        break
      testedTransitions = testedTransitions + TransitionList
      testedTransitions = sorted(set(testedTransitions))
      TotalNumberOfSteps = TotalNumberOfSteps + len(TransitionList)
      #print(j,len(testedTransitions),len(self.TestFSM.transitions),TotalNumberOfSteps)
# Setup test parameters
      test = []
      test.append(['Test %s' % str(j+1),])
      j+=1
      test.append([])
      transitionsForReport=[]
      actionvalues=[]
      actions=[]
      for trans in TransitionList:
       vals = self.TestFSM.transitionActionVals(self.TestFSM.transitions[trans])[0]
       act = self.TestFSM.transitionActions(self.TestFSM.transitions[trans])[0]
       arg = sum(vals)/2 if len(vals)==2 else vals[0]
       transitionsForReport.append('%s-%s'%(trans,arg))
       actionvalues.append((arg,))
       actions.append(act)
      test.append(transitionsForReport)
      test.append([])
      test.append([0,])
      test.append(list(self.TestFSM.outputs))
      test.append(['step',])
      measure	= list(self.TestFSM.outputs)
      measurement 	= []
      measurement.extend([measure]*(len(actions)))
      measurements=[]
      measurements.extend(measurement)
      setups		= [[]]*len(TransitionList)
      Procedure		= []
      testType 		= 'step'
      TestTransistions = TransitionList
# Create Folders for the new test
      self.CreateTestFolders(self.TestSectionName(test))
      self.DeleteOldTestingFile()
      self.CreateTestFolders(self.TestSectionName(test))
# Create the test
      self.InitProcedure(test) # see if this step can be eliminated???????
      StateResults = self.FinishProcedure(actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions,ChangesOnly)
# Copy the model used to the test.  Used for generating diagrams and as a copy of what was used.
      shutil.copy2('ModelFSMTest.py', self.currentTestFilePath+'\\ModelFSMCopy.py')

    def createTests(self):
     self.CreateDataAndReportFolders()
     for test in self.tests:
      self.CreateTestFolders(self.TestSectionName(test))
      self.DeleteOldTestingFile()
     for test in self.tests:
      self.CreateTestFolders(self.TestSectionName(test))
      if self.outputs(test)[0] == 'all':
# Measure all outputs
       test[5] = self.TestFSM.outputs
      if self.Transitions(test)[0] == 'all':
       testedTransitions = []
       TransitionNumberToUse = 0
       NTransitions = 0
       N = 0
       i=0
# Test all transistions, meant for step by step
       while(len(testedTransitions) < len(self.TestFSM.transitions)):
        # print('%s, %s\n' % (len(testedTransitions),len(self.FSM.transitions)))
        NTransitions = 0
        TransitionNumberToUse = 0
        for transition in range(len(self.TestFSM.transitions)):
         startState										= self.TestFSM.transitions[transition][0]
         (initactions,initactionvalues,TransitionList) 	= self.TestFSM.State2State(0,startState,1)
         TransitionList.append(transition)
         N = 0
         for t in TransitionList:
          if t not in testedTransitions:
           N = N + 1
         if N > NTransitions:
          NTransitions = N
          TransitionNumberToUse = transition
        startState										= self.TestFSM.transitions[TransitionNumberToUse][0]
        (initactions,initactionvalues,TransitionList) 	= self.TestFSM.State2State(0,startState,1)
        TransitionList.append(TransitionNumberToUse)
        testedTransitions = testedTransitions + TransitionList
        testedTransitions = sorted(set(testedTransitions))
        test[2] = [str(item) for item in TransitionList]
        # print(test)
        sys.stdout.flush()
        self.createSingleTest(test,i)
        i+=1
      else:
# Basic Case
       self.createSingleTest(test)

    def createSingleTest(self,test,i=0):
# Test Procedure for PC to perform
     self.InitProcedure(test)
     sys.stdout.flush()
     (actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions) = self.GetProcedureSteps(test)
     StateResults = self.FinishProcedure(actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions)
# Test Procedure for report
     if testType != 'step':
      os.system('python TestProcedure.py "%s' % self.currentTestFilePath)
# Test Spec
     self.CreateTestSpec(StateResults)
     if testType == 'step':
      shutil.copy2('ModelFSMTest.py', self.currentTestFilePath+'\\ModelFSMCopy.py')
      # test[2] = list([x.split('-')[0] for x in test[2]])
      # self.TestFSM.printToFile(0,self.Transitions(test))
      # sleep(0.2)
      # self.TestFSM.CreateFSMGraph(['00Test%sgraph' % i,"%s" % self.currentTestFilePath])
      # sleep(0.2)

    def CreateTestSpec(self,StateResults):
     specList = []
     # print(StateResults)
     for StateResult in StateResults:
      keys = list(StateResult.keys())
      for key in keys:
       if key != 'none' and isinstance(StateResult[key], list) and len(StateResult[key])==2:
        (min,max) = StateResult[key]
        parameter = key.replace('Scope','').replace('=>','-').strip().upper()
        if (parameter,min,max) not in specList:
         specList.append((parameter,min,max))
     if specList != []:
      SpecFile = open("%s00aspec-.tex" % self.currentTestFilePath, 'w')
      SpecFile.write(r"\noindent" + "\n")
      SpecFile.write('Spec'+r"\\" + "\n")
      SpecFile.write(r"\noindent\rule{0.5\linewidth}{0.4pt}" + "\n")
      SpecFile.write(r"\begin{adjustwidth}{1cm}{}" + "\n")
      SpecFile.write(r'\begin{table}[H]'+'\n')
      SpecFile.write(r'\centering'+'\n')
      SpecFile.write(r'\begin{tabular}{|r|l|l|l|l|}'+'\n')
      SpecFile.write(r'\hline'+'\n')
      SpecFile.write(r'Parameter & Min & Nom & Max & Units  \bigstrut\\'+'\n')
      SpecFile.write(r'\hline'+'\n')
      for (parameter,min,max) in specList:
       SpecFile.write('%s & %s &  & %s & \\\\' % (parameter,min,max) + '\n')
      SpecFile.write(r'\hline'+'\n')
      SpecFile.write(r'\end{tabular}'+'\n')
      SpecFile.write(r'\end{table}'+'\n')
      SpecFile.write(r"\end{adjustwidth}"+ "\n")
      SpecFile.write(r"\noindent"+ "\n")
      SpecFile.close()

    def FinishProcedure(self,actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions,ChangesOnly=0):
     TestName = 'testingFile' #self.tests[TestNumber][1][0]
     TestFile = open("%s%s.py" % (self.currentTestFilePath,TestName), 'a')
     listofactions = list()
     listofdelays 	= list()
     listofsetups	= list()
     listofmeasurements	= list()
     # listofstates 	= list()
     listofMooreResultsFromModel = list()
     self.FSM.reset()
     # listofstates.append(self.FSM.CurrentState())
# Put previous test procedures in first.
     if self.oldtestSuites != []:
      for oldtestSuite in self.oldtestSuites:
       for aname,args,meas,delay in oldtestSuite:
        TestFile.write("    ('%s', %s, %s, %s),\n" % (aname,args,meas,delay))
       TestFile.write('  ],\n')
       TestFile.write('  [\n')
     OldStateResults=''
     for i,aname in enumerate(actions):
      args = actionvalues[i]
      delay = self.FSM.doAction(aname, args[0]) # Execute in model, get result
      # listofstates.append(self.FSM.CurrentState())
      listofactions.append('%s[%s]' % (aname, args[0]))
      listofdelays.append('%s' % (delay))
      StateResults = dict(self.FSM.Currentoutputs())
      # AddMeasurementItemsToStateResults(measurements[i],StateResults)
      measuremens = [x.split('*')[0] for x in measurements[i]]
      for key in list(StateResults):
        if key not in measuremens:
         del StateResults[key]
      if list(StateResults)==[]:
       StateResults['none']=''
      if StateResults != None:
       StateResultss = {}
       if ChangesOnly and OldStateResults != '':
        for key in list(StateResults):
         if StateResults[key] == OldStateResults[key]:
          StateResultss[key]=''
         else:
          StateResultss[key]=StateResults[key]
       else:
        StateResultss=dict(StateResults)
       listofMooreResultsFromModel.append(StateResultss)
       OldStateResults = dict(StateResults)
       
       import operator
       StateResultss = sorted(StateResultss.items(), key=operator.itemgetter(0))
       StateRslt     = '{'
       for k in StateResultss:
        k = str(k)
        pattern = '\','
        expStr  = '\':'
        import re
        k = re.sub(pattern, expStr, k)
        val = len(k) - 1
        StateRslt = StateRslt+k[1:val]+', '
       StateResultss = str(StateRslt)[0:len(StateRslt)-2]+'}'
       TestFile.write("    ('%s', %s, %s, %s),\n" % (aname, args, StateResultss,delay))
       # print('    (%s, %s, %s, %s),\n' % (aname, args, StateResults,delay))
      # else:
       # TestFile.write('    (%s, %s),\n' % (aname, args)) # optional missing result
      listofsetups.append(setups[i])
      listofmeasurements.append(measuremens)#.replace('scope ',''))
     TestFile.write('  ],\n')
     TestFile.write(']\n\n')
# Test Report Headers
     TestFile.write('report = [\n')
# Put previous test procedures in first.
     if self.oldreports != []:
      for oldreport in self.oldreports:
       TestFile.write("    %s,\n" % oldreport)
     TestFile.write('    [[%s],[%s]],\n' % (','.join(map(quote,max(listofsetups,key=len))),','.join(map(quote,max(listofmeasurements,key=len)))))
     TestFile.write(']\n\n')
# Test Procedure
     TestFile.write('procedure = [\n')
# Put previous test procedures in first.
     if self.oldprocedures != []:
      for oldreport in self.oldprocedures:
       TestFile.write("    %s,\n" % oldreport)
     TestFile.write('    %s,\n' % Procedure)
     TestFile.write(']\n\n')

# Test Type
     TestFile.write('TestType = [\n')
# Put previous test procedures in first.
     if self.oldTestTypes != []:
      for oldTestType in self.oldTestTypes:
       TestFile.write("    '%s',\n" % oldTestType)
     TestFile.write("    '%s',\n" % testType)
     TestFile.write(']\n\n')

# Transition List
     TestFile.write('TestTransistions = [\n')
# Put previous test procedures in first.
     if self.oldTestTransistions != []:
      for oldTestTransistion in self.oldTestTransistions:
       TestFile.write("    %s,\n" % oldTestTransistion)
     TestFile.write("    %s,\n" % TestTransistions)
     TestFile.write(']\n')

     TestFile.close()
     return listofMooreResultsFromModel

    def GetProcedureSteps(self,test,simple=0):
     measure			= self.outputs(test) # self.tests[TestNumber][4]
     sets				= self.Inputs(test) #self.tests[TestNumber][3]
     trans 				= self.Transitions(test) #self.tests[TestNumber][2]
     preactions			= self.initactions(test)
     testType			= 'table' if self.TestType(test).lower() != 'step' else 'step'
     stepTest			= True if testType == 'step' else False
     inputsbefore		= 1 if self.InputsBefore(test) == '1' else 0
     tseq 				= list()
     initactionvalues 	= list()
     initactions 		= list()
     actionvalues 		= list()
     actions 			= list()
     measurements		= list()
     setups				= list()
# ------------------------------------------------------
     for transition in trans:
      tseq.append(int(transition.split('-')[0]))
# ------------------------------------------------------
     startState		= self.TestFSM.transitions[tseq[0]][0]
     endState 		= self.TestFSM.transitions[tseq[-1]][3]
     resetState 	= 0
     (initactions,initactionvalues,transitionList) 				= self.TestFSM.State2State(resetState,startState,1) # the 1 returns raw values
     (resetactions,resetactionvalues,transitionList) 			= self.TestFSM.State2State(endState,startState,simple)
     (finalresetactions,finalresetactionvalues,transitionList) 	= self.TestFSM.State2State(startState,resetState,simple)
     if simple:
      finalresetactions = [finalresetactions,]
      finalresetactionvalues = [finalresetactionvalues,]
      resetactions = [resetactions,]
      resetactionvalues = [resetactionvalues,]

# ------------------------------------------------------
# add preactions to initactions
     preact		= []
     preactval	= []
     for preaction in preactions:
      if '-' in preaction:
       preact.append(		preaction.split('-')[0])
       preactval.append(	decodeActionVals(preaction))
     (initactions,initactionvalues) = VariationsAlongPath(preact+initactions,preactval+initactionvalues)
     (initactions,initactionvalues) =([x[0] for x in initactions],[x[0] for x in initactionvalues])
# ------------------------------------------------------
     if ScopeIn(measure):
      (scopeActions,scopeActionVals,MList) 	= ScopeSetupParameters(self.TestFSM.transitions,tseq,measure,sets,self)
  # print('%s\n%s\n%s\n'%(scopeActions,scopeActionVals,MList) )
      (seqActions,midSeqActionVals) 		= SequenceActions(self.TestFSM.transitions,tseq,trans)
      # print(MList)
      scopeShotName 	= [[('-'.join(MList[0]),sets,inputsbefore),]] if isinstance(MList[0][0], str) else [[('%s-%s'%(MList[0][0][0],MList[0][1]),sets,inputsbefore),]]
      scopeShotActions	= [['ScopeShot',]]
      seqActionVals		= []
  # print(seqActions)
      for midSeqActionVal in midSeqActionVals:
       seqActionVals.append(scopeActionVals+midSeqActionVal+scopeShotName)
      seqActions 							= [[[x[0] for x in scopeActions]+seqActions[0][0]+[x[0] for x in scopeShotActions]],]*len(seqActions)

     else:
      (seqActions,seqActionVals)			= SequenceActions(self.TestFSM.transitions,tseq,trans)
# ------------------------------------------------------
     if stepTest:
      measurement 	= [measure]*(len(seqActions[0][0])-1) if len(seqActions[0][0])!=1 else []
      measurement.extend([measure]*(len(seqActions[0])))
     else:
      measurement 	= [[]]*(len(seqActions[0][0])-1) if len(seqActions[0][0])!=1 else []
      measurement.extend([measure]*(len(seqActions[0])))
     setup  		= [[]]*(len(seqActions[0][0])-1) if len(seqActions[0][0])!=1 else []
     setup.extend([sets]*(len(seqActions[0])))
# ------------------------------------------------------
     for inita in initactionvalues:
    # Do every combo of actions to get from state 0 to start of sequence.
      actions.extend(initactions[0])
      actionvalues.extend(inita)
      measurements.extend([[]]*(len(inita)))
      setups.extend([[]]*(len(inita)))
      for seqActionVal in seqActionVals:
    # Do every combo of actions in the sequence
       for seqAction in seqActions[0]:
        actions.extend([x for x in seqAction])
        # measurements.extend([[]])
        # setups.extend([[]])
       for f in seqActionVal:
        actionvalues.extend([x for x in f])
       measurements.extend(measurement)
       setups.extend(setup)
       actions.extend(resetactions[0])
       actionvalues.extend(resetactionvalues[0])
       measurements.extend([[]]*len(resetactionvalues[0]))
       setups.extend([[]]*len(resetactionvalues[0]))
      actions.extend(finalresetactions[0])
      actionvalues.extend(finalresetactionvalues[0])
      measurements.extend([[]]*(len(finalresetactions[0])))
      setups.extend([[]]*(len(finalresetactions[0])))
      TestTransistions = list([int(x.split('-')[0]) for x in test[2]])
     return (actions,actionvalues,measurements,setups,[initactions[0],seqActions[0],resetactions[0],finalresetactions[0]],testType,TestTransistions)

    def InitProcedure(self,test):
     TestName = 'testingFile'
     oldActions = []
     if os.path.isfile("%s%s.py" % (self.currentTestFilePath,TestName)):
      oldtestFile = open("%s%s.py" % (self.currentTestFilePath,TestName))
      for line in oldtestFile:
       if 'def' in line and 'pass' in line:
        oldActions.append(re.search('\b(\w*?)(?=\()',line))
        # print(oldActions[-1])
      oldtestFile.close()
      sys.path.append(self.currentTestFilePath)
      oldtestFile = __import__(TestName)
      self.oldtestSuites		= oldtestFile.testSuite
      self.oldreports			= oldtestFile.report
      self.oldprocedures		= oldtestFile.procedure
      self.oldTestTypes			= oldtestFile.TestType
      self.oldTestTransistions	= oldtestFile.TestTransistions
      sys.path.remove(self.currentTestFilePath)
      del sys.modules[TestName]
     else:
      self.oldtestSuites		= []
      self.oldreports			= []
      self.oldprocedures		= []
      self.oldTestTypes			= []
      self.oldTestTransistions	= []
     TestFile = open("%s%s.py" % (self.currentTestFilePath,TestName), 'w')
     TestFile.write('\n# %s' % TestName)
     TestFile.write(' %s\n' % ' '.join(['%s' % state for state in self.TestFSM.states]))
     TestFile.write('\n# actions here are just labels, but must be symbols with __name__ attribute\n\n')
# State Machine Actions
     TestFile.writelines([ 'def %s(): pass\n' % aname for aname in self.TestFSM.actions ])
# Scope Actions
     TestFile.writelines([ 'def %s(): pass\n' % aname for aname in ['SetupScope','ScopeShot']])
# Preactions which may not be included in the state machine actions.
     if self.initactions(test) != ['']:
      initialActions = [action.split('-')[0] for action in self.initactions(test)]
      TestFile.writelines([ 'def %s(): pass\n' % aname for aname in initialActions])
# Old actions
     for oldAction in oldActions:
      if oldAction not in self.TestFSM.actions and oldAction not in ['SetupScope','ScopeShot']:
       if self.initactions(test) != [''] and oldAction not in initialActions and oldAction != None:
        TestFile.write('def %s(): pass\n' % oldAction)
     TestFile.write('\n# action symbols\n')
     TestFile.write('\ntestSuite = [\n')
     TestFile.write('  [\n')
     TestFile.close()

    def CreateDataAndReportFolders(self):
     if not os.path.exists(self.testFilePath+"report\\"):
      os.makedirs(self.testFilePath+"report\\")
     if not os.path.exists(self.testFilePath+"report\\data"):
      os.makedirs(self.testFilePath+"report\\data")

    def CreateTestFolders(self,name):
     self.currentTestFilePath = self.testFilePath+"report\\data\\" + name + "\\"
     if not os.path.exists(self.currentTestFilePath):
      os.makedirs(self.currentTestFilePath)
     if not os.path.exists(self.currentTestFilePath+"\\skip\\"):
      os.makedirs(self.currentTestFilePath+"\\skip\\")
     if not os.path.exists(self.currentTestFilePath+"\\plots\\"):
      os.makedirs(self.currentTestFilePath+"\\plots\\")

    def DeleteOldTestingFile(self):
     TestName = 'testingFile'
     if os.path.isfile("%s%s.py" % (self.currentTestFilePath,TestName)):
      os.remove("%s%s.py" % (self.currentTestFilePath,TestName))



def ScopeIn(measure):
 return sum([(1 if 'scope' in m.lower() else 0) for m in measure])>0

def ScopeSetupParameters(transitions,tseq,measure,sets,self):
 SignalList		= []
 SpecList		= []
 MList			= []
 SignalLevel	= []
 TransitionTime	= round(sum([TransitionDelay(transitions[i])  for i in tseq])/3,5)
 for me in measure:
  (m,specs)     =me.split('*')
  if 'scope' in m.lower():
   signalName 	= m.strip().split(' ')[1]
   Item		= m.strip().split(' ')[2]
   if signalName not in SignalList and '=>' not in signalName:
    SignalList.append(signalName)
    SpecList.append(me)
   elif '=>' in signalName:
    signalNames = signalName.split('=>')
    for signal in signalNames:
     if signal not in SignalList:
      SignalList.append(signal)
      SpecList.append(me)
    signalName = signalNames
    StartState = self.TestFSM.states[transitions[tseq[0]][0]]
# The idea here is if the signal is high in the beginning of the sequence,
# and I'm interested in it's transition point.  I know it's going from high to low.
    POL1		= 0 if self.TestFSM.stateValues[StartState][signalName[0]] else 1
    POL2		= 0 if self.TestFSM.stateValues[StartState][signalName[1]] else 1
    signalName.append(POL1)
    signalName.append(POL2)
   MList.append([signalName,Item])
 for i,signal in enumerate(SignalList):
  SignalLevel.append(SpecOf(signal,self,SpecList[i]))
# Trigger
 triggerCHN		= transitionActions(transitions[tseq[0]])[0]
 triggerPOL		= 1 if transitionActionVals(transitions[tseq[0]])[0][0] else 0
 triggerInfo		= [triggerCHN,triggerPOL]
 SignalList.append(triggerCHN)
 SignalLevel.append(SpecOf(triggerCHN,self))
# First add the scope setup actions
 scopeAction 		= [['SetupScope',]]
 scopeActionVals 	= [[(TransitionTime,SignalList,SignalLevel,triggerInfo,MList,sets),]]
 return (scopeAction,scopeActionVals,MList)

def SpecOf(Signal,self,specs=[]):
 state={}
 Value=[]
 # for i,stateN in enumerate(list(self.FSM.states)):
  # state[stateN]=list(self.FSM.states[i])[0]
 for state in self.TestFSM.states:
  for output in self.TestFSM.stateValues[state]:
   if output==Signal:
    # print(state)
    # print(output)
    # print(self.FSM.stateValues[state][output])
    # print(Value)
    Value.append(self.TestFSM.stateValues[state][output])
 if Value==[]:
  if '*' in specs:
   specs = ast.literal_eval(specs.split('*')[1].replace(';',','))
   return max(max(specs))
  else:
   return 3.3
 else:
  return max(max(Value))

def quote(input):
 return "'%s'" % (input)

def LoadTestsfromTestFile(testFilePath):
 testsToCreate=list()
 if os.path.exists(testFilePath+"\\Tests.csv"):
  testFile = open(testFilePath+"\\Tests.csv",'r')
  for lineItems in reader(testFile):
   if 'Test Section' not in lineItems[0]:
    lineItem = list()
    for item in lineItems:
     lineItem.append(item.split(','))
    testsToCreate.append(lineItem)
  testFile.close()
 else:
  testsToCreate = 0
 return testsToCreate

def AddMeasurementItemsToStateResults(measurements,StateResults):
 for measurement in measurements:
  if '*' in measurement:
   measname = measurement.split('*')[0]
   if measname not in list(StateResults):
    measvalue = ast.literal_eval(measurement.split('*')[1].replace(';',','))
    if measname in list(count):
     count[measname]=count[measname]+1
     if count[measname] >= len(measvalue):
      count[measname]=0
    else:
     count[measname]=0
    StateResults[measname] = tuple(measvalue[count[measname]])
    # print(StateResults)
  else:
   if measurement not in list(StateResults):
    StateResults[measurement] = ''
count=dict() # static variable used in the def above




