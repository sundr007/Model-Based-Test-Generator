import copy,os,shutil,re,itertools,ast,sys,random
from time import sleep
from csv import reader
from numpy import cumsum
from numpy.random import rand
import networkx as nx

from shutil import move

import importlib.util as IMPORTER

# ==============================================================================
# FSM Class
# ==============================================================================
class SystemModel:
# instance variable unique to each instance
#the computerOutputs param is used to pass in the path to the model directory
    def __init__(self,fPath,Name,UseIOfile,DefaultValues,SpecFilePath=''):
# Load Modules
        #loads the ModelFSM file from the model directory
        ioSpec = IMPORTER.spec_from_file_location(Name, fPath+Name) #(module name, path)
        ModelFSM = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(ModelFSM)
        #loads the inputOutput file from the model directory
        ioSpec = IMPORTER.spec_from_file_location("InputOuputs.py", fPath+'InputOutputs.py') #(module name, path)
        inOutFile = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(inOutFile)
# Specs
        if SpecFilePath!='':
         SpecFile	=open(SpecFilePath,'r')
         self.Specs={}
         for line in SpecFile:
          if line.split(',')[2] == '':
           self.Specs[line.split(',')[0]]='(%s,%s)' % (line.split(',')[1] if line.split(',')[1]!='' else '0',line.split(',')[3].replace('\n','') if line.split(',')[3]!='\n' else '0')
          else:
           self.Specs[line.split(',')[0]]=line.split(',')[2]
         SpecFile.close()
        else:
         self.Specs = []
# input output file
        if UseIOfile:
         self.Doutputs = inOutFile.localDoutputs()
         self.computedOutputs = list(self.Doutputs.outputs)
         self.computedInputs = list(self.Doutputs.inputs)
        #  print('Computed inputs are: %s' % self.computedInputs)
        else:
         self.computedOutputs = []
         self.computedInputs = []
        self.states 		= [ModelFSM.states[x]['name'] for x in list(ModelFSM.states)]
        # print('states in model are   : %s' % self.states )
        self.stateValues 	= dict()
        for i,state in enumerate(self.states):
         self.stateValues[state] = ModelFSM.states[i]['outputs']
        self.stateDelays 	= dict()
        for i,state in enumerate(self.states):
         self.stateDelays[i] = ModelFSM.states[i]['delay']
        self.outputs		= list(set(ModelFSM.Outputs+self.computedOutputs))

        self.outputValues 	= dict()
        for i,output in enumerate(self.outputs):
         self.outputValues[output] = 0
        self.transitions 	= ModelFSM.graph
        self.Allactions 	= list()
        for transition in self.transitions:
         for actAndVal in transition[1]:
          action = actAndVal[0]
          aval = actAndVal[1]
          delay = transition[2]
          if (action,aval,delay) not in self.Allactions:
           self.Allactions.append((action,aval,delay))
        for action in self.computedInputs:
         (aval,delay) = self.Doutputs.inputs[action][2]
        #  print((action,aval,delay))
         if aval == (1,0):
           self.Allactions.append((action,(0,),delay))
           self.Allactions.append((action,(1,),delay))
         elif len(aval) > 2:
           for a in aval:
             self.Allactions.append((action,(a,),delay))
         else:
          self.Allactions.append((action,aval,delay))
        self.Allactions		= list(set(self.Allactions))
        self.actions 		= list(set([action for (action,aval,delay) in self.Allactions]))
        self.actionValues 	= dict()
        for action in self.actions:
         self.actionValues[action]=0
        if not hasattr(ModelFSM, 'DefaultState'):
         self.DefaultState = 0
        else:
         self.DefaultState = self.states.index(ModelFSM.DefaultState)
        self.currentState=self.DefaultState

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
        self.InitOutputsValues()
        for i,action in enumerate(self.Allactions):
         print('action %s: %s' %(i,action))
        self.reset()
        self.ReportError() # Reset Error File

# ======================================
# Error Reporting
# ======================================
    def ReportError(self,newline=''):
     if newline=='':
      file = open(os.path.join('Temp','ExploreProgress.txt'),'w')
     else:
      file = open(os.path.join('Temp','ExploreProgress.txt'),'a')
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
     # os.system('move %s.dot CurrentTest\\%s.dot' % (inname,outname[0]))
     sleep(.1)
     move('%s.dot'%inname,os.path.join('CurrentTest','%s.dot'%outname[0]))
     sleep(.1)
     # if inname == 'ExploredModel' and len(self.transitions)>150:
     #  os.system('cd CurrentTest & sfdp -T pdf  -Gsize="7.5,7.5" -o %s.pdf %s.dot & cd ..' % (outname[0],outname[0]))
     # else:
     #  pass
      # os.system('dot -T pdf  -Gsize="7.5,7.5" -o %s.pdf %s.dot' % (os.path.join('CurrentTest',outname[0]),os.path.join('CurrentTest',outname[0])))
      # os.system('cd CurrentTest & dot -T pdf  -Gsize="7.5,7.5" -o %s.pdf %s.dot & cd ..' % (outname[0],outname[0]))
     # if len(outname)==2:
     #  os.system('cd CurrentTest & mv %s.pdf "%s%s.small.pdf" & cd ..' % (outname[0],outname[1],outname[0]))
     #  os.system('cd CurrentTest & mv %s.dot "%s%s.dot" & cd ..' % (outname[0],outname[1],outname[0]))
      # os.system('cd CurrentTest & rm %s.dot & cd..' % (outname[0]))

    def WriteStateOutputTable(self):
     outfile	=open(os.path.join('CurrentTest','State-Output-Tablestatetable.csv'),'w')
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
     outfile	=open(os.path.join('CurrentTest','State-Transition-Tablestatetable.csv'),'w')
     outfile.write(','.join(['Transition Name','Action','Action Value']+self.outputs)+',\n')
     for i,transition in enumerate(self.transitions):
      outputs=list()
      for output in self.outputs:
       if output in list(self.transitionOutputs(transition)):
        outputs.append(str(self.transitionOutputs(transition)[output]).replace(',','-'))
       else:
        outputs.append('')
      arg = str(self.transitionActionVals(transition)[0][0]) if len(self.transitionActionVals(transition)[0])==1 else str(self.transitionActionVals(transition)[0]).replace(',','-')
      outfile.write(','.join([str(i),self.transitionActions(transition)[0],arg]+outputs)+',\n')
     outfile.close()

    def WriteBehavioralModelTable(self):
     outfile	=open(os.path.join('CurrentTest','Behavioral-Actions.tex'),'w')
     outfile.write(r'Behavioral Actions:'+'\n\n')
     outfile.write(r'\noindent\rule{0.5\linewidth}{0.4pt}'+'\n')
     outfile.write(r'\begin{labeling}{ClearOFFLOWINPUTbitPagePlus00}'+'\n')
     for action in self.computedInputs:
      (inputChanges,outputs,defaultValue) = self.Doutputs.input(action,self.outputValues,self.actionValues,1)
      outputs = ', '.join(['%s:%s' % (key,outputs[key]) for key in list(outputs)])
      outfile.write('\item [%s] %s\n' % (action,outputs))
     outfile.write(r'\end{labeling}'+'\n')
     outfile.close()

    def reset(self):
     for act in list(self.DefaultActions):
      self.doAction(act,(self.DefaultActions[act],))
     for act in list(self.computedInputs):
      (inputChanges,outputChanges,defaultValue) = self.Doutputs.input(act,self.outputValues,self.actionValues,0)
      self.doAction(act,(defaultValue,))
     for output in self.outputs:
      if output in list(self.DefaultOutputs):
       self.outputValues[output] = self.DefaultOutputs[output]
     self.ComputeOutputs()
     self.currentState=self.DefaultState

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
     pushbutton=0
     begin=self.CurrentState()
     if type(args) is not str:
      self.saveState()
      # print('Action: %s: %s' % (action,args))
      if action in self.computedInputs:
       (inputChanges,outputChanges,defaultValue) = self.Doutputs.input(action,self.outputValues,self.actionValues,args[0])
       for input in list(inputChanges):
        self.actionValues[input] = inputChanges[input]
       for output in list(outputChanges):
        if output in self.outputs:
         self.outputValues[output] = outputChanges[output]
      else:
       self.actionValues[action]=args[0]

      try:
       delay = self.ComputeNextState(action)

      except:
       self.ReportError('An infinite loop occured while traversing the state machine.')
       self.ReportError('This is typically caused by a path in the state machine that allows it to switch between two states continuously.')
       print('An infinite loop occured while traversing the state machine')
       print('Action: %s %s Begin State: %s End State: %s \n\tInputs %s'%(action,args,begin,self.CurrentState(),self.pactionValues))
       info='\nAction: {} {}'.format(action,args)+' Begin State: {}'.format(begin)+' End State: {}'.format(self.CurrentState())+'\n\tInputs {}'.format(self.pactionValues)
       self.ReportError(info)
       exit()
       delay=1

      if len(args)==2 and 'pushbutton' in args[1]:
           pushbutton = 1
      else:
           pushbutton = 0
      if action.lower() == 'delay' or (pushbutton and args[0]>0):
        self.actionValues[action]=0
      # if pushbutton and args[0]==0:
      # print(self.actionValues)
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

    def ComputeNextState(self,action=''):
# Go through every transition and check to see if the conditions are right to follow that transition.
# First check if initial state is current state. Then check to see if action/values are correct.
# Then follow transition unless it's a loop back.
     delay = 0
     delayLoopback = 0
     for transition in self.transitions:
      if self.transitionInitState(transition) == self.currentState:
       actionsAndValuesMatch = 1 # set this to true, if it makes it through the next loop then really is true.
       for TransAction,TransActionValue in zip(self.transitionActions(transition),self.transitionActionVals(transition)):
        pushbutton = False
        if len(TransActionValue) == 2:
         if type(TransActionValue[1]) is str:
           if 'pushbutton' in TransActionValue[1].lower() and TransActionValue[0] == float(self.actionValues[TransAction]):
             actionsAndValuesMatch = actionsAndValuesMatch * 1
             pushbutton = True
           elif TransAction == action and TransActionValue[0] == float(self.actionValues[TransAction]):
          # if TransActionValue[0] == float(self.actionValues[TransAction]):
            actionsAndValuesMatch = actionsAndValuesMatch * 1
            # print('Found string2: %s %s for %s %s and actionValue %s'%(TransAction,TransActionValue,action,delay,self.actionValues[TransAction]))
           else:
            actionsAndValuesMatch = actionsAndValuesMatch * 0
         elif TransActionValue[0] <= float(self.actionValues[TransAction]) <= TransActionValue[1]:
          actionsAndValuesMatch = actionsAndValuesMatch * 1
         else:
          actionsAndValuesMatch = actionsAndValuesMatch * 0
        else:
         if TransActionValue[0] == float(self.actionValues[TransAction]):
          actionsAndValuesMatch = actionsAndValuesMatch * 1
         else:
          actionsAndValuesMatch = actionsAndValuesMatch * 0
       if actionsAndValuesMatch:
        if self.transitionInitState(transition) != self.transitionFinalState(transition) or pushbutton:
# Not a loop back or a it's a push button transition
         if pushbutton:
          if self.actionValues[action] == 1:
            self.actionValues[action] = 0
          else:
            self.actionValues[action] = 1
         self.currentState = self.transitionFinalState(transition)
         if list(self.transitionOutputs(transition)) != []:
          for output in list(self.transitionOutputs(transition)):
           self.outputValues[output] = self.transitionOutputs(transition)[output]
         delay += self.transitionDelay(transition)
         delay += self.stateDelays[self.currentState]
         delay += self.ComputeNextState(action)
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
       outputValue = self.Doutputs.compute(output,self.outputValues,self.actionValues)
       outputValue = ast.literal_eval(self.Specs[output+'='+str(outputValue)]) if output+'='+str(outputValue) in list(self.Specs) else outputValue
       self.outputValues[output]=outputValue

    def InitOutputsValues(self):
     if self.computedOutputs != []:
      for output in self.outputValues:
       outputValue = 0
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
     actions		= [x[0] for x in actions]
     actionvalues	= [x[0] for x in actionvalues]
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
 # return transition[3]
 return transition[2]

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
