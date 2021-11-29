import unittest,os,shutil

from MBT.MBT import MBT

path = "C:\\Users\\esund\\Documents\\Sandbox"
name = 'oak'

class TestSimple(unittest.TestCase):

    # def test_new(self):
    #     if os.path.isdir(os.path.join(path,name)):
    #         shutil.rmtree(os.path.join(path,name))
    #     oak = MBT(path)
    #     oak.new(name)
    #     self.assertEqual(os.path.isdir(os.path.join(path,name)), 1)

    # def test_load(self):
    #     oak = MBT(os.path.join(path,name))
    #     self.assertEqual(oak.load(), 1)

    def test_explore(self):
        if os.path.isdir(os.path.join(path,name)):
            shutil.rmtree(os.path.join(path,name))
        oak = MBT(path)
        oak.new(name)
        self.assertEqual(os.path.isdir(os.path.join(path,name)), 1)
        oak = MBT(os.path.join(path,name))
        oak.load()
        actionsToUse=['A', 'B','C']
        outputsToUse = ['OUT',]
        (States,Transistions) = oak.exploreModel(actionsToUse,outputsToUse)
        print(States,Transistions)
        self.assertEqual(States, 8)
        self.assertEqual(Transistions, 24)
        self.assertEqual(oak.createTests(),24)



if __name__ == '__main__':
    unittest.main()
