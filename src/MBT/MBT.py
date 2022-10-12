import os,shutil,pkg_resources
from collections import OrderedDict
from time import sleep


import importlib.util as IMPORTER
import MBT.Dot as Dot

from MBT.ImportFromFizzim import importFizzim
from MBT.CreateMooreStateMachine import CreateMooreStateMachine
from MBT.SystemModel import SystemModel
from MBT.TestWriter import TestWriter

# import Dot as Dot
#
# from ImportFromFizzim import importFizzim
# from CreateMooreStateMachine import CreateMooreStateMachine
# from SystemModel import SystemModel
# from TestWriter import TestWriter

# from ImportFromFizzim import importFizzim
# from CreateMooreStateMachine import CreateMooreStateMachine
# from SystemModel import SystemModel
# from TestWriter import TestWriter
# ==============================================================================
# MTB Class
# ==============================================================================
class MBT:
# ====================================
# Init
# ====================================
    def __init__(self,path=""):
        if path=="":
            self.path=os.getcwd()
        else:
            self.path=path
# ====================================
# Public Functions
# ====================================
    def new(self,name):
        self.copyNewProject2folder(name)
        self.path=os.path.join(self.path,name)
# ====================================
    def open(self,name):
        path = os.path.join(self.path,name)
        if os.path.isdir(path):
            self.path=path
        else:
            print('%s is not a directory'%path)
# ====================================
    def edit(self):
        DATA_PATH = pkg_resources.resource_filename('MBT', 'Editor/')
        os.system('%s %s'%(os.path.join(DATA_PATH,'StateMachineEditor.jar'),os.path.join(self.path,self.FizzimFile())))
# ====================================
    def load(self):
        return importFizzim(self.SpecFile(),
                     self.InputOutputsFile(),
                     self.FizzimFile(),
                     self.path)
# ====================================
    def exploreModel(self,actionsToUse=[],outputsToUse=[]):
        ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", os.path.join(self.path,self.DefaultValuesFile())) #(module name, path)
        DefaultValues = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(DefaultValues)

        UserFSM = SystemModel(self.path,"ModelFSM.py",True,DefaultValues)
        TestFSM = CreateMooreStateMachine(UserFSM)
        (States,Transistions) = TestFSM.Explore(actionsToUse,outputsToUse)
        TestFSM.printToFile(self.path,outputsToUse)
        return (States,Transistions)
# ====================================
    def createTests(self):
        ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", os.path.join(self.path,self.DefaultValuesFile())) #(module name, path)
        DefaultValues = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(DefaultValues)

        UserFSM 	= SystemModel(self.path,"ModelFSM.py",True,DefaultValues)
        TestFSM	    = SystemModel(self.path,"ModelFSMTest.py",False,DefaultValues)
        Tester		= TestWriter(UserFSM,self.path,TestFSM)
        ChangesOnly=0
        # CreateModelInformationSection()
        return Tester.createRegressionTest(ChangesOnly,30,0)
# ====================================
    def show(self):
        ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", os.path.join(self.path,self.DefaultValuesFile())) #(module name, path)
        DefaultValues = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(DefaultValues)

        UserFSM 	= SystemModel(self.path,"ModelFSM.py",True,DefaultValues)
        fsm = UserFSM.printToFile(numbered=0,highlightedTransitions=[],red=[],green=[])
        UserFSM.CreateFSMGraph(fsm)
        sleep(0.5)
        shutil.copyfile('Frame.pdf',os.path.join(self.path,'InputModel.pdf'))
# ====================================
    def showE(self):
        ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", os.path.join(self.path,self.DefaultValuesFile())) #(module name, path)
        DefaultValues = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(DefaultValues)

        UserFSM 	= SystemModel(self.path,"ModelFSMTest.py",True,DefaultValues)
        fsm = UserFSM.printToFile(numbered=0,highlightedTransitions=[],red=[],green=[])
        UserFSM.CreateFSMGraph(fsm)
        sleep(0.5)
        shutil.copyfile('Frame.pdf',os.path.join(self.path,'ExploredModel.pdf'))
# ====================================
    def AnimateExploration(self):
        ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", os.path.join(self.path,self.DefaultValuesFile())) #(module name, path)
        DefaultValues = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(DefaultValues)

        UserFSM 	= SystemModel(self.path,"ModelFSMTest.py",False,DefaultValues)
        fsm = UserFSM.printToFile(numbered=0,highlightedTransitions=[],red=[],green=[])
        Dot.dotfilesForAnimation('ExploredModel.dot',fsm,self.path)

        # shutil.copyfile('Frame.pdf',os.path.join(self.path,'ExploredModel.pdf'))


# ====================================
# Private Functions
# ====================================
    def copyNewProject2folder(self,name):
        if os.path.isdir(os.path.join(self.path,name)):
            print('failed to create new, folder name already exists')
        else:
            DATA_PATH = pkg_resources.resource_filename('MBT', 'newProject/')
            shutil.copytree(DATA_PATH, os.path.join(self.path,name))
# ====================================
    def fileWith(self,keyword):
        fName=''
        for i in os.listdir(self.path):
            if keyword in i:
                fName = i
        if fName!='':
            return os.path.join(self.path,fName)
        else:
            raise Exception("can't find file with %s keyword in it." % keyword)
# ====================================
    def interpretFile(self,file):
        with open(file,'rb') as fin:
            parsed =  eval( fin.read() )
            return parsed
        # try:
        # d = ast.literal_eval(data)
        # return d
        # except:
        #     print('A problem occured while interpretting Python data in %s'%file)
# ====================================
    def FizzimFile(self):       return self.fileWith(".fzm")
    def SpecFile(self):         return self.fileWith("Specs")
    def InputOutputsFile(self): return self.fileWith("InputOutputs")
    def DefaultValuesFile(self):return self.fileWith("DefaultValues")
# ====================================

def main():
    path = "/home/sundry/Documents/MBT/"
    name = 'oak'
    # oak = MBT(os.path.join(path,name))
    oak = MBT(path)
    oak.open(name)
    # oak.new(name)
    # oak.edit()
    oak.load()
    (States,Transistions)=oak.exploreModel(['A', 'B','C'],['OUT',])
    print(States,Transistions)
    print(oak.createTests())
    oak.show()
    oak.showE()
    oak.AnimateExploration()

if __name__ == '__main__':
    main()
