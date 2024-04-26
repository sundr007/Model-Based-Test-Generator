import copy,os,shutil,re,itertools,ast,sys,random
from time import sleep
from csv import reader
from numpy import cumsum
from numpy.random import rand
import networkx as nx
from MBT.ChinesePostMan import CPP

# from ChinesePostMan import CPP

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
 print(seqActions,seqActionVals)
 (seqActions,seqActionVals) = VariationsAlongPath(seqActions,seqActionVals)
 return (seqActions,seqActionVals)

# ==============================================================================
# FSM Class
# ==============================================================================
class TestWriter:
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

    def createRegressionTest(self,ChangesOnly=0,TestLength=10,UseScope=0):
     self.CreateDataAndReportFolders()
     testedTransitions = []
     TotalNumberOfSteps = 0
     j=0
     pushbutton = list()
     self.actionLimits = self.FindActionLimits()
# Use the CPP class to find a solution to the Chinese postman problem which gives an optimal procedure that tests all paths at least once.
     nodes = list(self.TestFSM.states)
     sys = CPP(len(nodes))
     for i,edge in enumerate(self.TestFSM.transitions):
      sys.addArc(i,edge[0],edge[3],1)
     if sys.solve():
      solution = sys.printCPT(0)
      # for (y,z,x) in solution:
      #  print (y,z,x)
      transitions = [x for (y,z,x) in solution]
     else:
      startState = 0
      solution = []
      for i,edge in enumerate(self.TestFSM.transitions):
       (initactions,initactionvalues,TransitionList) 	= self.TestFSM.State2State(startState,edge[0],1)
       solution = solution + TransitionList + [i]
       startState = edge[3]
      transitions = list(solution)
      for x in transitions:
       print (x)
     print("%s transitions found in Chinese Post Man"%len(transitions))
# Break the large test procedure into individual tests of length "TestLength"
     while(len(testedTransitions) < len(self.TestFSM.transitions)):
      # Get to start state
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
      # Get back to state 0
      if len(transitions) > 0:
        startState										= self.TestFSM.transitions[transitions[0]][0]
        if startState ==0:
          ResetTransitionList=[]
        else:
          (initactions,initactionvalues,ResetTransitionList) 	= self.TestFSM.State2State(startState,0,1)
          TransitionList.extend(ResetTransitionList)
      # Count progress
      testedTransitions = testedTransitions + TransitionList
      testedTransitions = sorted(set(testedTransitions))
      TotalNumberOfSteps = TotalNumberOfSteps + len(TransitionList)
      print(j,len(testedTransitions),len(self.TestFSM.transitions),TotalNumberOfSteps)
      print("%s out of %s transistions tested in %s steps"%(len(testedTransitions),len(self.TestFSM.transitions),TotalNumberOfSteps))
      print("%s transitions are left"%len(transitions))
# Setup test parameters
      test = []
      test.append(['Test %s' % str(j+1),])
      j+=1
      test.append([])
      transitionsForReport=[]
      actionvalues=[]
      actions=[]
      scopeShotSignals = self.TestFSM.outputs[:]
      for trans in TransitionList:
       tseq = list()
       vals = self.TestFSM.transitionActionVals(self.TestFSM.transitions[trans])[0]
       act = self.TestFSM.transitionActions(self.TestFSM.transitions[trans])[0]
       arg = (sum(vals)/2,) if len(vals)==2 and type(vals[1]) is not str else vals
       inputsbefore = 0 if type(vals[0]) is not str and vals[0] > 0 else 1
       tseq.append(trans)

       if UseScope:
         scopeShotAction = 'ScopeShot'
         if inputsbefore > 0:
          scopeShotName = str(act)+'-HtoL'
         else:
          scopeShotName = str(act)+'-LtoH'

         if act not in scopeShotSignals:
          scopeShotSignals.append(act)

         (scopeActions,scopeTrig,scopeActionVals,MList) = ScopeSetupParameters(self.TestFSM.transitions,tseq,scopeShotSignals,0,self)
         scopeShotVals = (scopeShotName,{'measurements':MList,'inputsbefore':inputsbefore})

       transitionsForReport.append('%s-%s'%(trans,arg[0]))
       if UseScope:
         actionvalues.append((scopeTrig,scopeActionVals,MList))
       actionvalues.append(arg)
       if UseScope:
         actionvalues.append(scopeShotVals)
         actions.append(scopeActions)
       actions.append(act)
       if UseScope:
         actions.append(scopeShotAction)
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
      if UseScope:
       setups		= [[]]*len(TransitionList)*3
      else:
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
      StateResults = self.FinishProcedure(actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions,ChangesOnly,pushbutton)
# Copy the model used to the test.  Used for generating diagrams and as a copy of what was used.
      shutil.copy2(os.path.join(self.testFilePath,'ModelFSMTest.py'), os.path.join(self.currentTestFilePath,'ModelFSMCopy.py'))
     return (len(actions))

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
      self.createSingleTest(test)

    def createSingleTest(self,test,i=0):
# Test Procedure for PC to perform
     self.InitProcedure(test)
     print(test)
     sys.stdout.flush()
     (actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions) = self.GetProcedureSteps(test)
     # print(actions,actionvalues)
     StateResults = self.FinishProcedure(actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions)
# Test Procedure for report
     if testType != 'step':
      os.system('python TestProcedure.py "%s' % self.currentTestFilePath)
# Test Spec
     self.CreateTestSpec(StateResults)
     if testType == 'step':
      shutil.copy2(os.path.join(self.testFilePath,'ModelFSMTest.py'), os.path.join(self.currentTestFilePath,'ModelFSMCopy.py'))
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

    def FinishProcedure(self,actions,actionvalues,measurements,setups,Procedure,testType,TestTransistions,ChangesOnly=0,pushbuttonList=list()):
     TestName = 'testingFile' #self.tests[TestNumber][1][0]
     TestFile = open(os.path.join(self.currentTestFilePath,TestName+'.py'), 'a')
     listofactions = list()
     listofdelays 	= list()
     listofsetups	= list()
     listofmeasurements	= list()
     # listofstates 	= list()
     listofMooreResultsFromModel = list()
     pushbutton=0
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
      delay = self.FSM.doAction(aname, args) # Execute in model, get result
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
       elif 'Scope' in aname:
        StateResultss['none']=''
       else:
        StateResultss=dict(StateResults)
       listofMooreResultsFromModel.append(StateResultss)
       OldStateResults = dict(StateResults)

       #Sort the test measures by key
       import operator
       StateResultss = sorted(StateResultss.items(), key=operator.itemgetter(0))
       StateRslt     = '{'
       for k in StateResultss:
        k = str(k)
        pattern = '\','
        expStr  = '\':'
        import re
        # only substute the first match
        k = re.sub(pattern, expStr, k, 1)
        val = len(k) - 1
        StateRslt = StateRslt+k[1:val]+', '
       StateResultss = str(StateRslt)[0:len(StateRslt)-2]+'}'
       TestFile.write("    ('%s', %s, %s, %s),\n" % (aname, args, StateResultss,delay))
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
     print(initactions)
     (initactions,initactionvalues) = VariationsAlongPath(preact+initactions,preactval+initactionvalues)
     (initactions,initactionvalues) =([x[0] for x in initactions],[x[0] for x in initactionvalues])
# ------------------------------------------------------
     if ScopeIn(measure):
      (scopeActions,scopeTrig,scopeActionVals,MList) 	= ScopeSetupParameters(self.TestFSM.transitions,tseq,measure,sets,self)
      print('%s\n%s\n%s\n'%(scopeActions,scopeActionVals,MList) )
      (seqActions,midSeqActionVals) 		= SequenceActions(self.TestFSM.transitions,tseq,trans)
      print(MList)
      scopeShotName 	= [[('-'.join(MList[0]),sets,inputsbefore),]] if isinstance(MList[0][0], str) else [[('%s-%s'%(MList[0][0][0],MList[0][1]),sets,inputsbefore),]]
      scopeShotActions	= [['ScopeShot',]]
      seqActionVals		= []
      print(seqActions)
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
     if os.path.isfile(os.path.join(self.currentTestFilePath,TestName+'.py')):
      oldtestFile = open(os.path.join(self.currentTestFilePath,TestName+'.py'))
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
     TestFile = open(os.path.join(self.currentTestFilePath,TestName+'.py'), 'w')
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
     if not os.path.exists(os.path.join(self.testFilePath,"report")):
      os.makedirs(os.path.join(self.testFilePath,"report"))
     if not os.path.exists(os.path.join(self.testFilePath,"report","data")):
      os.makedirs(os.path.join(self.testFilePath,"report","data"))

    def FindActionLimits(self):
     actionLimits = dict()
     for tran in self.TestFSM.transitions:
      key = tran[1][0][0]
      if key in actionLimits:
        if len(tran[1][0][1]) == 2:
          if type(tran[1][0][1][1]) is str:
           min1 = tran[1][0][1][0]
           max1 = tran[1][0][1][0]
          # if the range input is greater than 0
          # elif tran[1][0][1][0]:
          else:
           min1 = min(tran[1][0][1])
           max1 = max(tran[1][0][1])
          # if the range input is 0, then the second value is the minimum
          # else:
           # min1 = tran[1][0][1][1]
           # max1 = max(tran[1][0][1])
        else:
          min1 = min(tran[1][0][1])
          max1 = max(tran[1][0][1])
        # max cannot handle a string so remove it
        if len(actionLimits[key])==2 and type(actionLimits[key][1]) is str:
          del actionLimits[key][1]
          maxR = actionLimits[key][0]
          minR = actionLimits[key][0]
        else:
          maxR = max(actionLimits[key])
          minR = min(actionLimits[key])
        if max1 > maxR and min1 > minR and min1 > maxR:
          actionLimits[key][0]=maxR
          if maxR == minR:
            actionLimits[key].append(min1)
          else:
            actionLimits[key][1]=min1
        elif max1 < maxR and min1 < minR and max1 < minR:
          actionLimits[key][0]=max1
          if maxR == minR:
            actionLimits[key].append(minR)
          else:
            actionLimits[key][1]=minR
      else:
        actionLimits[key]=list(tran[1][0][1])
     return actionLimits

    def CreateTestFolders(self,name):
     self.currentTestFilePath = os.path.join(self.testFilePath,"report","data", name)
     if not os.path.exists(self.currentTestFilePath):
      os.makedirs(self.currentTestFilePath)
     if not os.path.exists(os.path.join(self.currentTestFilePath,"skip")):
      os.makedirs(os.path.join(self.currentTestFilePath,"skip"))
     if not os.path.exists(os.path.join(self.currentTestFilePath,"plots")):
      os.makedirs(os.path.join(self.currentTestFilePath,"plots"))

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

 TransitionTime	= round(sum([TransitionDelay(transitions[i])  for i in tseq])/8,5)

 # Trigger
 triggerCHN		= transitionActions(transitions[tseq[0]])[0]
 triggerPOL		= 1 if transitionActionVals(transitions[tseq[0]])[0][0] else 0

 StartState = self.TestFSM.states[transitions[tseq[0]][0]]
 NextState = self.TestFSM.states[transitions[tseq[0]][3]]
 useTrig=0

 for me in measure:
  if '*' in me:
   (m,specs)     =me.split('*')
  else:
   # break
   # for regression test find measurements and signals to display
   m = me
   if me in self.TestFSM.stateValues[StartState]:
     if 'x' in str(self.TestFSM.stateValues[StartState][me]) or 'x' in str(self.TestFSM.stateValues[NextState][me]):
      SignalList.append(me)
      SpecList.append(me)
     elif self.TestFSM.stateValues[StartState][me] != self.TestFSM.stateValues[NextState][me]:
       m = 'Scope '+triggerCHN+'=>'+me+' DELay'
       useTrig=1
   else:
     SignalList.append(me)
     SpecList.append(me)

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

# The idea here is if the signal is high in the beginning of the sequence,
# and I'm interested in it's transition point.  I know it's going from high to low.
    if useTrig or (signalName[0] not in self.TestFSM.stateValues[StartState]):
     POL1 = triggerPOL
    else:
     POL1 = 0 if self.TestFSM.stateValues[StartState][signalName[0]] > self.TestFSM.stateValues[NextState][signalName[0]] else 1
    POL2 = 0 if self.TestFSM.stateValues[StartState][signalName[1]] > self.TestFSM.stateValues[NextState][signalName[1]] else 1

    signalName.append(POL1)
    signalName.append(POL2)
   MList.append([signalName,Item])

 for i,signal in enumerate(SignalList):
   SignalLevel.append(SpecOf(signal,self,SpecList[i]))

# Trigger
 SignalList.append(triggerCHN)
 SignalLevel.append(SpecOf(triggerCHN,self))
 triggerLevel = self.actionLimits[triggerCHN][0]+(self.actionLimits[triggerCHN][1]-self.actionLimits[triggerCHN][0])/2
 triggerInfo		= dict(CHN=triggerCHN,POL=triggerPOL,LVL=triggerLevel)
# First add the scope setup actions
 scopeAction 		= 'SetupScope'
 scopeActionVals 	= {'TransitionTime':TransitionTime,'SignalList':SignalList,'SignalLevel':SignalLevel,'triggerInfo':triggerInfo}
 return (scopeAction,triggerCHN,scopeActionVals,MList)

def SpecOf(Signal,self,specs=[]):
 state={}
 Value=[]

 for state in self.TestFSM.states:
  for output in self.TestFSM.stateValues[state]:
   if output==Signal:
    # print(state)
    # print(output)
    # print(self.FSM.stateValues[state][output])
    # print(Value)
    Value.append(self.TestFSM.stateValues[state][output])

 # if did not find spec in outputs look in action inputs
 if Value==[]:
   if Signal in self.actionLimits:
     Value.append(self.actionLimits[Signal])

 if Value==[]:
  if '*' in specs:
   specs = ast.literal_eval(specs.split('*')[1].replace(';',','))
   return max(max(specs))
  else:
   return 3.3
 elif 'x' in str(Value):
   tempList=[]
   # remove x and look for max in rest of list
   for i in Value:
     if 'x' not in str(i):
       tempList.append(i)
   if tempList!=[]:
    return max(tempList)
   else:
    return 3.3
 else:
  max1 = max(Value)
  if type(max1) is int:
    maxValue = max1
  else:
    maxValue = max(max1)
  return maxValue

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
