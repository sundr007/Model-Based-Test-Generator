# ======================================
#
# Name: Specified Tester
#
# Purpose: Runs the test contains in test files and returns the outputs.
# ======================================

from time import sleep
import os,shutil,sys,imp,re,fileinput,Dot,importlib
from importlib.machinery import SourceFileLoader
from SystemModel import SystemModel
from optparse import OptionParser

# ======================================
# Parser for when this program is called
# ======================================
usage = """pmt [options] models  """
parser = OptionParser(usage=usage)

def parse_args():
  parser.add_option('-i', '--iut', type='string', default='',
                  help = 'Implementation (stepper module name), omit to just run model')
  parser.add_option('-o', '--output', type='string', default='',
                  help = 'Output test suite module name (with no .py suffix), no default (no output file if omitted)')
  parser.add_option('-m', '--testreport', type="string", default='',
                  help = 'Creates a test report.  Do not include file extension. no default (no output file if omitted)')
  return parser.parse_args()



# ======================================
# Tell Labview the Test is Complete
# ======================================
def TellLabviewtheTestisComplete():
 stopfile = open('Temp\\PythonToLabview.txt','w')
 stopfile.write('Stop')
 stopfile.close()

# ======================================
# Tell Labview the overall progress
# ======================================
def TellLabviewtheOverallProgress(newline=''):
 if newline=='':
  stopfile = open('Temp\\TestProgress.txt','w')
  stopfile.write('Start of Testing:\n')
 else:
  stopfile = open('Temp\\TestProgress.txt','a')
  stopfile.write(newline+'\n')
 stopfile.close()

# ======================================
# Tell Labview the current test progress
# ======================================
def TellLabviewtheCurrentTestProgress(newline=''):
 if newline=='':
  stopfile = open('Temp\\CurrentTestProgress.txt','w')
  stopfile.write('Start of Test:\n')
 else:
  stopfile = open('Temp\\CurrentTestProgress.txt','a')
  stopfile.write(newline+'\n')
 stopfile.close()

# ======================================
# Python and Labview cannot directly talk.
# To stop this tester, Labview can write messages to a file that Python can read.
# If "Stop" is in this file then the test must be terminated.
# ======================================
def ShouldTheTestBeStopped():
 stopfile = open('Temp\\LabviewToPython.txt','r')
 if 'Stop' in stopfile.readline():
  print('Tester stopped by GUI')
  TellLabviewtheOverallProgress('Tester stopped by GUI')
  sys.stdout.flush()
  exit()
 stopfile.close()

# ======================================
# Tell Labview the Test is in progress
# ======================================
def TellLabviewtheTestisRunning():
 stopfile = open('Temp\\PythonToLabview.txt','w')
 stopfile.write('Go')
 stopfile.close()

# ======================================
# extracts parameters from a single step in the test file.  Used for measurements.
# ======================================
def decodeStep(step):
 aname 				= step[0]
 args				= step[1]
 measurements 		= step[2]
 measurementKeys 	= list(step[2])
 return (aname,args,measurements,measurementKeys)

# ======================================
# Returns actions and arguments for a given step in a test file.
# ======================================
def SelectAction(krun,isteps,testFile):
   aname 			= testFile.testSuite[krun][isteps][0]
   args				= testFile.testSuite[krun][isteps][1]
   measurements		= testFile.testSuite[krun][isteps][2]
   delay			= testFile.testSuite[krun][isteps][3]
   done				= 1 if isteps+2 > len(testFile.testSuite[krun]) else 0
   return (aname, args, measurements, delay, done)

# ======================================
# Select action from test file
# ======================================
def RunTest(options, stepper, strategy, krun,testReportPath,testFile,folder='Test0'):
# Parameters and Setup
  isteps 						= 0
  scopeshots 					= 0
  listofactions 				= list()
  listofMooreResultsFromModel 	= list()
  listofMooreResultsFromStepper = list()
  inputs 						= testFile.report[krun][0]
  outputs 						= testFile.report[krun][1]
  TestType						= testFile.TestType[krun]
  TestTransistions				= list(testFile.TestTransistions[krun])
  InputPositions				= {}
  done 							= 0
  triggered = 1
# Initialize the input measurement arrays
  for input in inputs:
   InputPositions[input]		=[]#[stepper.Measure(input),]

# Loop over steps in test file and perform actions and measurements
  while not done:
# ======================================
# See if Labview is commanded the test to stop.
# ======================================
    ShouldTheTestBeStopped()
# ======================================
# Select action from test file
# ======================================
    (aname, args, measurements, delay, done) = strategy.SelectAction(krun,isteps,testFile)
    listofactions.append('%s[%s]' % (aname, args[0]))
    listofMooreResultsFromModel.append(measurements)
    isteps = isteps + 1
    SystemResults = {}

    if aname == 'ScopeShot' and TestType == 'step':
      # Add triggered information to scope args to skip scope shot if not triggered
      args[1]['triggered']=triggered
      # Make filename unique by adding Testname and step number
      StepNo = int(isteps/3)
      ScopeShotFilename =str(folder)+'-Step'+str(StepNo)+'-'+str(args[0])
      args = (ScopeShotFilename,args[1])
    elif len(args) == 2:
      # remove string for TestAction
      args = (args[0],)

# ======================================
# Perform the action using the stepper
# ======================================
    try:
     currentDir 	= os.getcwd()
     os.chdir(testReportPath)
     print('action: %s args: %s delay: %s'%(aname,args,delay))
     result 		= stepper.TestAction(aname, args, delay)
     os.chdir(currentDir)
     # print(aname)
     sys.stdout.flush()
     if aname == 'ScopeShot':
      scopeshots = 1
      SystemResults['Link']=result
     elif aname == 'SetupScope' and TestType == 'step':
      if result>0:
        triggered=1
      else:
        triggered=0
    except:
     print('could not do action: %s' % (aname,))
     os.chdir(currentDir)
     TellLabviewtheCurrentTestProgress('Error: could not do action: %s' % (aname,))
     if aname == 'SetupScope':
       result 		= stepper.TestAction(aname, args, delay)
       TellLabviewtheCurrentTestProgress('Try action again: %s' % (aname,))
     else: 
      TellLabviewtheOverallProgress('Error: Stopping the Test')
      TellLabviewtheTestisComplete()
      stepper.Reset()
      exit()

    TellLabviewtheCurrentTestProgress('%s (%s)' % (aname, args[0]))
# ======================================
# Measure Outputs
# ======================================
    if 'none' not in list(measurements) or 'ScopeShot' in aname:
     for output in list(measurements):
      if 'scope' in output.lower():
       me = []
       for step in testFile.testSuite[krun]:
        (aname,args,measurements,measurementKeys) = decodeStep(step)
        if aname == 'SetupScope':
         me = list(args[4])
         break
       i=0
       for m in me:
        i = i + 1
        if not isinstance(m[0],str):
         m = ['=>'.join([m[0][0],m[0][1]]),m[1]]
        if ' '.join(m) in output:
         break
       result = stepper.Measure('scope measure',(i,))
       SystemResults[output]=result
      else:
       currentDir 	= os.getcwd()
       os.chdir(testReportPath)
       try:
        if measurements[output] != '':
         result 		= stepper.Measure(output)
        else:
         result = ''
       except:
        print('could not measure: %s' % output)
        os.chdir(currentDir)
        TellLabviewtheCurrentTestProgress('Error: could not measure: %s' % output)
        TellLabviewtheOverallProgress('Error: Stopping the Test')
        TellLabviewtheTestisComplete()
        stepper.Reset()
        sys.stdout.flush()
        exit()
       os.chdir(currentDir)
       SystemResults[output]=result
    else:
     for output in list(measurements):
      SystemResults[output]=1
    listofMooreResultsFromStepper.append(SystemResults)

# ======================================
# Measure Inputs
# ======================================
    for input in inputs:
     try:
      InputPositions[input].append(str(stepper.Measure(input)))
     except:
      print('could not measure: %s' % input)
      TellLabviewtheCurrentTestProgress('Error: could not measure: %s' % input)
      TellLabviewtheOverallProgress('Error: Stopping the Test')
      TellLabviewtheTestisComplete()
      stepper.Reset()
      sys.stdout.flush()
      exit()

# ----------------- End of While Loop------------------------------------

# ======================================
# Test Reporting table
# ======================================
  passingReport = 1
  if TestType != 'step':
# Create the report file
   currentreport = open(testReportPath+"\\Test%s Report.csv" % krun , 'w')
# Write the first line
   if scopeshots:
    currentreport.write(','.join(inputs)+','+','.join(outputs)+',result,Link,\n')
   else:
    currentreport.write(','.join(inputs)+','+','.join(outputs)+',result\n')
# Write the data lines
   numberOfsections = len(listofactions)
   for i in range(1,numberOfsections):
    if 'none' not in list(testFile.testSuite[krun][i-0][2]) or 'ScopeShot' in listofactions[i]:
     for input in inputs:
      currentreport.write(InputPositions[input][i]+',')
     for output in outputs:
      currentreport.write(str(listofMooreResultsFromStepper[i][output])+',')
    if outputs[0] in list(listofMooreResultsFromModel[i]) and len(listofMooreResultsFromModel[i][outputs[0]])==2:
     a = 1
     for output in outputs:
      if type(listofMooreResultsFromModel[i][output]) is tuple:
       min	= listofMooreResultsFromModel[i][output][0] #if 'Scope' not in output else -100000
       value	= listofMooreResultsFromStepper[i-0][output]
       max	= listofMooreResultsFromModel[i][output][1] #if 'Scope' not in output else 1000000
      else:
       min	= listofMooreResultsFromModel[i][output] #if 'Scope' not in output else -100000
       value	= listofMooreResultsFromStepper[i-0][output]
       max	= listofMooreResultsFromModel[i][output] #if 'Scope' not in output else 1000000
      a = a and (min <= value <= max)
     result = 'Pass' if a else 'Fail'
    else:
     result = 'Pass' if listofMooreResultsFromModel[i] == listofMooreResultsFromStepper[i] else 'Fail'
    if result == 'Fail' and 'none' not in list(testFile.testSuite[krun][i-0][2]):
     passingReport = 0
    if 'none' not in list(testFile.testSuite[krun][i-0][2]):
     if scopeshots:
      currentreport.write('%s,%s\n' % (result,listofMooreResultsFromStepper[i]['Link']))
     else:
      currentreport.write(result+'\n')
    elif 'ScopeShot' in listofactions[i]:
     currentreport.write(',\n')
    else:
     pass
# Close the file
   currentreport.close()

# ======================================
# Test Reporting step by step
# ======================================
  else:
   blankOutputList = {}
   TransitionFailListForThisTest=[]
   TransitionPassListForThisTest=[]
   sortedOutputs = sorted(outputs)
   for output in outputs:
    blankOutputList[output]=''
   listofMooreResultsFromModel.insert(0,dict(blankOutputList))
   listofMooreResultsFromStepper.insert(0,dict(blankOutputList))
# Create the report file
   # currentreport = open(testReportPath+"\\Test%s Step Reportstatetable.csv" % krun , 'w')
   currentreport = open(testReportPath+"\\%s Output Reportstatetable.csv" % folder , 'w')
# Write the first line
   currentreport.write('Step,Action,Source,')
   currentreport.write(','.join(sortedOutputs)+',Result,')
   if scopeshots:
     currentreport.write('Link,')
# Write the data lines
   numberOfsections = len(listofactions)+1
   isteps=0

   for i in range(1,numberOfsections):
    if 'none' not in list(listofMooreResultsFromModel[i]):
     isteps=isteps+1
# Action
     currentreport.write('\n'+str(isteps)+','+str(listofactions[i-1])+',,,'+','*len(outputs)+'\n')
# Model Results
     currentreport.write(',,Spec')
     for output in sortedOutputs:
      if 'x' in str(listofMooreResultsFromModel[i][output]):
       currentreport.write(',None')
      else:
       currentreport.write(','+str(listofMooreResultsFromModel[i][output]).replace(', ','-'))
     if scopeshots:
       currentreport.write(',,\n')
     else:
       currentreport.write(',\n')
# System Results
     currentreport.write(',,Actual')
     a=1
     for output in sortedOutputs:
      currentreport.write(','+str(listofMooreResultsFromStepper[i][output]))
      if (type(listofMooreResultsFromModel[i][output]) is tuple or type(listofMooreResultsFromModel[i][output]) is list) and listofMooreResultsFromStepper[i][output] != '':
       if 'x' not in str(listofMooreResultsFromModel[i][output][0]):
        a = a and (listofMooreResultsFromModel[i][output][0] <= listofMooreResultsFromStepper[i][output] <= listofMooreResultsFromModel[i][output][1])
      elif listofMooreResultsFromStepper[i][output] != '':
       a = a and listofMooreResultsFromModel[i][output] == listofMooreResultsFromStepper[i][output]
     if a:
      result = 'Pass'
      TransitionPassListForThisTest.append(TestTransistions[0])
     else:
      result = 'Fail'
      TransitionFailListForThisTest.append(TestTransistions[0])
      passingReport = 0
     TestTransistions.pop(0)
     if scopeshots:
      if listofMooreResultsFromStepper[i+1]['Link'] == 0:
       currentreport.write(',%s,' %result)
      else:
       currentreport.write(',%s,%s' % (result,listofMooreResultsFromStepper[i+1]['Link']))
     else:
      currentreport.write(','+result)
# Close the file
   currentreport.close()
# ======================================
# Test Reporting state diagram with highlighted transitions.
# ======================================
   shutil.copyfile(testReportPath+'\\ModelFSMCopy.py', 'ModelFSMCopy.py')
   import ModelFSMCopy
   import DefaultValues
   if len(ModelFSMCopy.graph) < 2000:
    UserFSM = SystemModel(ModelFSMCopy.states,ModelFSMCopy.graph,ModelFSMCopy.Outputs,DefaultValues)
    UserFSM.printToFile(0,[],TransitionFailListForThisTest,TransitionPassListForThisTest)
    import HighLevelModel
    importlib.reload(HighLevelModel)  
    Dot.dotfile('ExploredModel.dot',HighLevelModel)
    UserFSM.CreateFSMGraph(['ExploredModel',testReportPath],'ExploredModel')

# ======================================
# Pass/Fail for the report
# ======================================
   if passingReport:
    open(testReportPath+'\\pass', 'a').close()
    TellLabviewtheOverallProgress('\tPass')
    if os.path.isfile(testReportPath+'\\fail'):
     os.remove(testReportPath+'\\fail')
   else:
    open(testReportPath+'\\fail', 'a').close()
    TellLabviewtheOverallProgress('\tFail')
    if os.path.isfile(testReportPath+'\\pass'):
     os.remove(testReportPath+'\\pass')

# ======================================
# Extra Defs
# ======================================
def SortFolderNumerically(testReportPath):
    folders = os.listdir(testReportPath)
    foldersInOrder = folders[:]
    numberFoldersInOrder = len(folders)
    maxTestCase = 0
    minTestCase = numberFoldersInOrder

    for folder in folders:
        try:
            seqNum = int(folder.split()[1])

            if seqNum < minTestCase:
             minTestCase = seqNum
            if seqNum > numberFoldersInOrder:
             foldersInOrder.append(folder)
            else:
             foldersInOrder[seqNum-1]=folder
        except:
            seqNum = 0
        if seqNum > maxTestCase:
            maxTestCase = seqNum
    
    if minTestCase == numberFoldersInOrder:
     del foldersInOrder[0:minTestCase]
     print('Warning: minTestCase %s == numberFoldersInOrder %s array %s'%(minTestCase,numberFoldersInOrder,foldersInOrder))
    elif minTestCase > 1:
     del foldersInOrder[0:minTestCase-1]
     print('minTestCase => %s numberFoldersInOrder => %s'%(minTestCase,numberFoldersInOrder))
    if maxTestCase > len(folders):
     print('Warning exceeded array size\n\t',foldersInOrder)
    extras = maxTestCase-len(folders)
    if extras < -2:
     del foldersInOrder[extras:-1]
     del foldersInOrder[-1]
     print("folders in order: ",foldersInOrder)
    return (maxTestCase,foldersInOrder)
	
def numofTests(testReportPath):
	folders = os.listdir(testReportPath)
	numTests = 0
	for folder in folders:
		if "Test " in folder:
			numTests += 1
	return numTests

# ------------------- End of Run Test File----------------------------

def main():
  (options, args) = parse_args()
  # args can include model programs, FSMs, test suites
  if not args:
    exit()
# Path Setup
  testReportPath = options.testreport
  sys.path.append(testReportPath)

# Setup Stepper which links the actions/measurements to the hardware
  stepper = __import__(options.iut) if options.iut else None
  if stepper:
    if hasattr(stepper, 'testaction'):
      stepper.TestAction = stepper.testaction
    if hasattr(stepper, 'test_action'):
      stepper.TestAction = stepper.test_action
    if hasattr(stepper, 'Measure'):
      stepper.Measure = stepper.Measure
    if hasattr(stepper, 'reset'):
      stepper.Reset = stepper.reset

# Setup Strategy module which will select actions and measurements from test file.
  strategy = imp.new_module('strategy')
  strategy.SelectAction = SelectAction

# ======================================
# Determine which tests should be run based on spec file.
# ======================================
  SpecFolders=[]
  for file in os.listdir(testReportPath+'report'):
   if 'spec.tex' in file:
    spec=open(testReportPath+'report\\spec.tex','r')
    for line in spec:
     if "section{" in line and "%" not in line:
      TestName=re.findall('{([^"]*)}', line)[0]
      SpecFolders.append(TestName)
  if SpecFolders==[]:
   # No spec file, just run all folders
    SpecFolders = os.listdir(testReportPath+'report\\data')
    print("Did not find spec.tex file in path ",testReportPath+'report')
  TellLabviewtheTestisRunning()
  TellLabviewtheOverallProgress()
  TellLabviewtheCurrentTestProgress()
# ======================================
# Loop through folder structure and run tests
# ======================================
  currentDir 	= os.getcwd()
  os.chdir(currentDir)
  # folders = os.listdir(testReportPath+'report\\data')
  # totalTests = numofTests(testReportPath +'report\\data')
  testDataPath = testReportPath+str('report\\data')
  (maxTestCase,folders) = SortFolderNumerically(testDataPath)
  testDataPath = testDataPath+str('\\Test ')
  for folder in folders:
   # folder = testDataPath+str(str(folderNum))
   testCase = folder #'Test '+str(folderNum)
   if SpecFolders!= [] and testCase in SpecFolders:
    for file in os.listdir(testReportPath+'report\\data\\'+testCase):
     if file=='testingFile.py':
      print('%s of %s' % (testCase,len(folders)))
      TellLabviewtheOverallProgress('%s of %s' % (testCase,maxTestCase))
      TellLabviewtheCurrentTestProgress()
      sys.stdout.flush()
      testPath = testReportPath+'report\\data\\'+testCase+'\\'
      testFile = SourceFileLoader("testingFile",testPath+file).load_module()
      strategyRuns = len(testFile.testSuite)
      krun = 0
      while krun < strategyRuns:
        try:
         stepper.Reset()
        except:
         TellLabviewtheCurrentTestProgress('Error: Reset Function Failed')
         TellLabviewtheOverallProgress('Error: Stopping the Test')
         TellLabviewtheTestisComplete()
        RunTest(options, stepper, strategy, krun,testPath,testFile,folder)
        krun += 1
      if krun > 1:
        print( 'Test finished, completed %s runs' % krun)
      stepper.Reset()
  print( 'All tests were run.')
  sys.stdout.flush()
  TellLabviewtheOverallProgress('All tests were run.')
  TellLabviewtheCurrentTestProgress()
  TellLabviewtheTestisComplete()

# ------------------ end main function ------------------------------------

# ======================================
# Main Program Call
# ======================================
if __name__ == '__main__':
      main()
