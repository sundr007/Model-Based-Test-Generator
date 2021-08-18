#!/usr/bin/env python

import os,Dot,sys,subprocess
from SystemModel import SystemModel
from TestWriter import TestWriter
from CreateMooreStateMachine import CreateMooreStateMachine
from shutil import copyfile
from shutil import copy
import importlib.util as IMPORTER
from ImportFromFizzim import importFizzim

if len(sys.argv) > 1:
    action = str(sys.argv[1])
    filepath = str(sys.argv[2])+'\\'
    scriptFilePath = str(sys.argv[3])+'\\'
else:
    # action = 'Import'
    # action = 'Explore'
    action = 'ShowExploredModel'
    filepath = os.path.join(os.path.expanduser('~'), 'Documents', 'Sandbox', 'MBT-Paths', 'simple-MBT','') #"/Documents/Sandbox/MBT-Paths/simple-MBT/"
    scriptFilePath = os.path.join(os.path.expanduser('~'), 'github', 'ModelBasedTester-AllPaths','') #'/github/ModelBasedTester-AllPaths'

#  os.chdir(os.path.dirname(__file__)) #needed for PyDev IDE debugging

# Added a command line arg for TestLength in Test Generation Tab
testLength=30
if len(sys.argv)>4:
  testLength=int(sys.argv[4])

# Added flag to use scope in testing
useScope=0
if len(sys.argv)>5:
  useScope=int(sys.argv[5])

files = os.listdir(filepath)
DoutputsFile=''
foundStepper=0
for file in files:
    if '.fzm' in file:
        fzmFile = file
    if 'Specs.csv' in file:
        SpecFile = file
    if 'InputOutputs.py' in file:
        DoutputsFile = file
    if 'DefaultValues.py' in file:
        DefaultValFile = file
    if 'ScopeCHN.csv' in file:
        ScopeFile = file
    if 'EquipmentInterface.py' in file:
      foundStepper=1
    if 'Stepper.py' in file:
      StepperFile = file
# if 'DefaultValues.py' not in files:
    # copyfile('DefaultValues.py',filepath+'DefaultValues.py')
if foundStepper:
  StepperFile=''


cases = ''

def Import():
    if type(DoutputsFile) is str:
        copy(os.path.join(filepath,DoutputsFile),scriptFilePath)
    else:
        print("Did not find InputOutputs in path ",filepath)

    print("Using EquipmentInterface.py in path ",filepath)

    # if type(ScopeFile) is str:
    #     copy(os.path.join(filepath,ScopeFile),scriptFilePath)
    # else:
    #     print("Did not find ScopeCHN.py in path ",filepath)

    copy(os.path.join(filepath,SpecFile),scriptFilePath)
    copy(os.path.join(filepath,fzmFile),scriptFilePath)
    importFizzim(os.path.join(filepath,SpecFile),
                 os.path.join(filepath,'InputOutputs.py'),
                 os.path.join(filepath,fzmFile)
                )
    copy('DefaultValues.py',filepath)
    copy('ModelFSM.py',filepath)
    copy('ModelFSM.py',os.path.join(filepath,'ModelFSMTest.py'))

def Explore():
    ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", filepath+"DefaultValues.py") #(module name, path)
    DefaultValues = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(DefaultValues)
    for line in open(os.path.join(scriptFilePath,'Temp','ExploreSettings.py'),'r').readlines():
        print(line)
        exec(line.replace('\n',''),globals())
    UserFSM 	                    = SystemModel(filepath,"ModelFSM.py",True,DefaultValues,SpecFile)
    TestFSM 						= CreateMooreStateMachine(UserFSM)
    actionsToUse 					= Actions
    outputsToUse 					= Outputs
    ExtraOutputsNotUsedInCombos 	= ExtraOutputs
    TestFSM.Explore(actionsToUse,outputsToUse,ExtraOutputsNotUsedInCombos)
    TestFSM.printToFile(outputsToUse,ExtraOutputsNotUsedInCombos)
    TestFSM.WriteStateOutputTable()
    copy('ModelFSMTest.py',os.path.join(filepath,'ModelFSMTest.py'))
    # os.system('copy ModelFSMTest.py "%s\\ModelFSMTest.py"'%filepath)

def CreateModelInformationSection():
    file=open('debug.txt','w')

    ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", filepath+"DefaultValues.py") #(module name, path)
    DefaultValues = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(DefaultValues)

    ioSpec = IMPORTER.spec_from_file_location("ModelFSM.py", filepath+"ModelFSM.py") #(module name, path)
    ModelFSM = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(ModelFSM)

    UserFSM 	= SystemModel(filepath,"ModelFSM.py",True,DefaultValues,SpecFile)
    # UserFSM.printToFile(1)
    Dot.dotfile('BehavioralModel.dot',ModelFSM)
    UserFSM.CreateFSMGraph(['BehavioralModel',],'BehavioralModel')
    UserFSM.WriteStateOutputTable()
    UserFSM.WriteStateTransitionTable()
    UserFSM.WriteBehavioralModelTable()
    os.system('move CurrentTest\\BehavioralModel.pdf "CurrentTest\\Behavioral Model\\BehavioralModel.pdf"')
    os.system('move "CurrentTest\\Behavioral Actions.tex" "CurrentTest\\Behavioral Model\\cBehavioral Actions.tex"')
    os.system('robocopy "%sCurrentTest\\Behavioral Model" "%sreport\\data\\Behavioral Model"' % (scriptFilePath,filepath))
    file.write('robocopy "%sCurrentTest\\Behavioral Model" "%sreport\\data\\Behavioral Model"' % (scriptFilePath,filepath) + '\n')
    file.write('Behavioral Done\n')

    ioSpec = IMPORTER.spec_from_file_location("ModelFSMTest.py", filepath+"ModelFSMTest.py") #(module name, path)
    ModelFSMTest = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(ModelFSMTest)

    TestFSM	= SystemModel(filepath,"ModelFSMTest.py",False,DefaultValues,SpecFile)
    # TestFSM.printToFile(1)
    Dot.dotfile('ExploredModel.dot',ModelFSMTest)
    TestFSM.CreateFSMGraph(['ExploredModel',],'ExploredModel')
    TestFSM.WriteStateOutputTable()
    TestFSM.WriteStateTransitionTable()
    os.system('move CurrentTest\\ExploredModel.pdf "CurrentTest\\Explored Model\\aExploredModel.pdf"')
    os.system('move "CurrentTest\\State Output Tablestatetable.csv" "CurrentTest\\Explored Model\\Explored Model State Output Table Reportstatetable.csv"')
    os.system('move "CurrentTest\\State Transition Tablestatetable.csv" "CurrentTest\\Explored Model\\Explored Model State Transition Table Reportstatetable.csv"')
    os.system('robocopy "%sCurrentTest\\Explored Model" "%sreport\\data\\Explored Model"' % (scriptFilePath,filepath))
    if useScope:
     os.system('robocopy "%sCurrentTest\\Measurements" "%sreport\\data\\Measurements"' % (scriptFilePath,filepath))
    os.system('robocopy "%sCurrentTest\\Testing Strategy" "%sreport\\data\\Generating Tests"' % (scriptFilePath,filepath))
    file.close()

def RegressionTest():
    ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", filepath+"DefaultValues.py") #(module name, path)
    DefaultValues = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(DefaultValues)
    UserFSM 	= SystemModel(filepath,"ModelFSM.py",True,DefaultValues,SpecFile)
    TestFSM	= SystemModel(filepath,"ModelFSMTest.py",False,DefaultValues,SpecFile)
    Tester		= TestWriter(UserFSM,filepath,TestFSM)
    ChangesOnly=0
    Tester.CreateDataAndReportFolders()
    CreateModelInformationSection()
    Tester.createRegressionTest(ChangesOnly,testLength,useScope)

def ShowBehavioralModel():
    ioSpec = IMPORTER.spec_from_file_location("ModelFSM.py", filepath+"ModelFSM.py") #(module name, path)
    ModelFSM = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(ModelFSM)

    ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", filepath+"DefaultValues.py") #(module name, path)
    DefaultValues = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(DefaultValues)

    UserFSM 	= SystemModel(filepath,"ModelFSM.py",True,DefaultValues,SpecFile)
    UserFSM.printToFile(0,ModelFSM.TestTransitions)
    # Dot.dotfile('BehavioralModel.dot',ModelFSM)
    import HighLevelModel
    Dot.dotfile('BehavioralModel.dot',HighLevelModel)
    UserFSM.CreateFSMGraph(['BehavioralModel',os.path.join(scriptFilePath,'CurrentTest')],'BehavioralModel')
    os.system('move CurrentTest\\BehavioralModel.small.pdf "CurrentTest\\BehavioralModel.pdf"')
    os.system('start AcroRd32.exe "CurrentTest\\BehavioralModel.pdf"')

def test():
    ioSpec = IMPORTER.spec_from_file_location("ModelFSM.py", filepath+"ModelFSM.py") #(module name, path)
    ModelFSM = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(ModelFSM)

    ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", filepath+"DefaultValues.py") #(module name, path)
    DefaultValues = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(DefaultValues)

    UserFSM 	= SystemModel(filepath,"ModelFSM.py",True,DefaultValues,SpecFile)
    print(UserFSM.CurrentState())
    # UserFSM.doAction('AC',(222,))
    print(UserFSM.CurrentState())
    # UserFSM.doAction('PSON',(0,))
    print(UserFSM.CurrentState())
    print(UserFSM.actionValues)
    UserFSM.doAction('ACDrop',(1.0,"pushbutton"))
    print(UserFSM.actionValues)
    print(UserFSM.CurrentState())
    # print(UserFSM.actionValues)

def ShowExploredModel():
    ioSpec = IMPORTER.spec_from_file_location("ModelFSMTest.py", filepath+"ModelFSMTest.py") #(module name, path)
    ModelFSMTest = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(ModelFSMTest)

    ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", filepath+"DefaultValues.py") #(module name, path)
    DefaultValues = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(DefaultValues)

    TestFSM	= SystemModel(filepath,"ModelFSMTest.py",False,DefaultValues,SpecFile)
    Dot.dotfile('ExploredModel.dot',ModelFSMTest)
    TestFSM.CreateFSMGraph(['ExploredModel',],'ExploredModel')
    # TestFSM.WriteStateOutputTable()
    # TestFSM.WriteStateTransitionTable()
    # os.system('move CurrentTest\\ExploredModel.pdf "CurrentTest\\ExploredModel.pdf"')
    # os.system('start AcroRd32.exe "CurrentTest\\ExploredModel.pdf"')

def AnimateExploration():
    ioSpec = IMPORTER.spec_from_file_location("ModelFSMTest.py", filepath+"ModelFSMTest.py") #(module name, path)
    ModelFSMTest = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(ModelFSMTest)

    ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", filepath+"DefaultValues.py") #(module name, path)
    DefaultValues = IMPORTER.module_from_spec(ioSpec)
    ioSpec.loader.exec_module(DefaultValues)
    TestFSM	= SystemModel(filepath,"ModelFSMTest.py",False,DefaultValues,SpecFile)
    Dot.dotfilesForAnimation('ExploredModel.dot',ModelFSMTest)


UseBehavioralModelForTest = [
 ('Make Test File',
  'copy ModelFSM.py ModelFSMTest.py'),
]

RunFindAllMeasurements = [
    ('Post process measurement information from scope',
        'python CalcMeasures.py ModelFSM -o Specs2.csv -i EquipmentInterface -m "'+filepath),
]

RunSpecifiedTests = [
    ('Run All Specifed Tests',
        'python SpecifiedTester.py ModelFSM -o output -i EquipmentInterface -m "'+filepath),
]

GeneralTests = [
    ('Run All Specifed Tests',
        'python TestFileToGeneralTest.py ModelFSM -o output -i EquipmentInterface -m "'+filepath),
]

if action =='Import':
    Import()
if action =='Explore':
    Explore()
    # CreateSpecifiedTests()
if action =='ShowBehavioralModel':
    ShowBehavioralModel()
if action =='CreateModelInformationSection':
    CreateModelInformationSection()
if action =='ShowExploredModel':
    ShowExploredModel()
if action =='animate':
    AnimateExploration()
if action =='test':
    test()
if action =='CreateAllTests':
    RegressionTest()
if action =='GeneralTests':
    cases = GeneralTests
if action =='RunSpecifiedTests':
    cases = RunSpecifiedTests
if action =='FindMeasures':
 cases = RunFindAllMeasurements
if cases != '':
    for (description, cmd) in cases:
        print(description)
        os.system(cmd)
