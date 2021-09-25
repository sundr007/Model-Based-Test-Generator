import unittest,os,shutil

from MBT.MBT import MBT

class TestSimple(unittest.TestCase):

    def test_new(self):
        path = "C:\\Users\\esund\\Documents\\Sandbox"
        name = 'oak'
        if os.path.isdir(os.path.join(path,name)):
            shutil.rmtree(os.path.join(path,name))
        oak = MBT(path)
        oak.new(name)
        self.assertEqual(os.path.isdir(os.path.join(path,name)), 1)




if __name__ == '__main__':
    unittest.main()
