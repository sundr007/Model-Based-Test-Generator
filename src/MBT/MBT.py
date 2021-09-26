import os,shutil,pkg_resources
from collections import OrderedDict

import importlib.util as IMPORTER

from MBT.ImportFromFizzim import importFizzim
from MBT.CreateMooreStateMachine import CreateMooreStateMachine
from MBT.SystemModel import SystemModel
from MBT.TestWriter import TestWriter
# ==============================================================================
# MTB Class
# ==============================================================================
class MBT:
# ====================================
# Static Methods
# ====================================


# ====================================
# Init
# ====================================
    def __init__(self):
        self.path=os.getcwd()
# ====================================
# Public Functions
# ====================================
    def new(self,name):
        self.copyNewProject2folder(name)
        self.path=os.path.join(self.path,name)
# ====================================
    def edit(self):
        DATA_PATH = pkg_resources.resource_filename('MBT', 'Editor/')
        os.system('%s %s'%(os.path.join(DATA_PATH,'StateMachineEditor.jar'),os.path.join(self.path,self.FizzimFile())))
# ====================================
    def import(self):
        importFizzim(self.SpecFile(),
                     self.InputOutputsFile(),
                     self.FizzimFile(),
                     self.path
                    )
# ====================================
    def exploreModel(self,actionsToUse,outputsToUse):
        ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", os.path.join(self.path,"DefaultValues.py")) #(module name, path)
        DefaultValues = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(DefaultValues)

        UserFSM = SystemModel(self.path,"ModelFSM.py",True,DefaultValues,self.SpecFile())
        TestFSM = CreateMooreStateMachine(UserFSM)
        TestFSM.Explore(actionsToUse,outputsToUse)
        TestFSM.printToFile(self.path,outputsToUse)
# ====================================
    def createTests(self):
        ioSpec = IMPORTER.spec_from_file_location("DefaultValues.py", os.path.join(self.path,"DefaultValues.py")) #(module name, path)
        DefaultValues = IMPORTER.module_from_spec(ioSpec)
        ioSpec.loader.exec_module(DefaultValues)

        UserFSM 	= SystemModel(self.path,"ModelFSM.py",True,DefaultValues,self.SpecFile())
        TestFSM	    = SystemModel(self.path,"ModelFSMTest.py",False,DefaultValues,self.SpecFile())
        Tester		= TestWriter(UserFSM,self.path,TestFSM)
        ChangesOnly=0
        # CreateModelInformationSection()
        Tester.createRegressionTest(ChangesOnly,30,0)
# ====================================
    def show(self):pass
# ====================================
    def ExploredModel():pass

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
    path = "C:\\Users\\esund\\Documents\\Sandbox"
    name = 'oak'
    oak = MBT(os.path.join(path,name))
    oak.edit()
    # oak.imports()
    # oak.exploreModel(['AC', 'ACDrop', 'clearFaults', 'ClearUVPbit', 'ClearUVPbitPagePlus00', 'ClearUVPbitPagePlus01', 'MaskUVPbitPage00', 'MaskUVPbitPage01', 'Operation', 'page', 'PSON'],['OUT',])
    # oak.createTests()
    # oak.show()

if __name__ == '__main__':
    main()
