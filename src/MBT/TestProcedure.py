
import re
import sys
import os

# ========================================
# Defs
# ========================================
 
def StartThe(file,name='Test Procedure'):
 file.write(r"\noindent" + "\n")
 file.write(name+r"\\" + "\n")
 file.write(r"\noindent\rule{0.5\linewidth}{0.4pt}" + "\n")
 file.write(r"\begin{adjustwidth}{1cm}{}" + "\n")
 file.write(r"\begin{enumerate}" + "\n")
 
def StartTable(file,name='Test Procedure'):
 file.write(r"\begin{table}[H]"+'\n')
 file.write(r"\centering"+'\n')
 file.write(r"\caption{#2}"+'\n')
 file.write(r"\begin{tabular}{|r|l|l|}"+'\n')
 file.write(r"\hline"+'\n')
 file.write(r"Parameter & Min & Max \bigstrut\\"+'\n')
 file.write(r"\hline"+'\n')
 
def AddItemToTable(file,item):
 item = [str(x) for x in item]
 file.write('&'.join(item)+r'\\'+'\n')
 
def EndTable(file):
 file.write(r"\hline"+'\n')
 file.write(r"\end{tabular}%"+'\n')
 file.write(r"\label{tab:#2}%"+'\n')
 file.write(r"\end{table}%"+'\n')
 
def EndThe(file):
 file.write(r"\end{enumerate}"+ "\n") 
 file.write(r"\end{adjustwidth}"+ "\n") 
 file.write(r"\noindent"+ "\n") 
 
def BeginList(file):
 file.write(r"\begin{enumerate}" + "\n")
 
def EndList(file):
 file.write(r"\end{enumerate}" + "\n")
 
# ========================================
# Test Procedure
# ========================================
filepath = str(sys.argv[1])
# filepath = "C:\\Users\\evansundry\\Documents\\Project Folders\\HP Ash\\BBU Model Tester\\report\\data\\Vmain Regulation"
# TestName = 'aa'
# TestName = str(sys.argv[2])
files = os.listdir(filepath)
for file in files:
 if ".py" in file and ".pyc" not in file:
  sys.path.append(filepath)
  testFile = __import__(file.replace('.py',''))
  # import file.replace('.py','') as testFile
  for NtestProcedure,testProcedure in enumerate(testFile.procedure):
   Procedure = open(filepath+'\\Test%s Procedure.tex' % NtestProcedure,'w')
   StartThe(Procedure,'Testing Procedure')
# Add all steps to file
 
   Procedure.write('\item Setup Steps\n')
   BeginList(Procedure)
   for step in testProcedure[0]:
    Procedure.write('\item Set %s.\n' % (step))
   EndList(Procedure)

   Procedure.write('\item Measurement Procedure Steps\n')
   BeginList(Procedure)
   for step in testProcedure[1][0]:
    Procedure.write('\item Set %s.\n' % (step))
   for step in testProcedure[2]:
    Procedure.write('\item Set %s.\n' % (step))
   Procedure.write('\item Repeat for all combinations of Measurement Steps (different inputs, loads, etc).\n')
   EndList(Procedure)

   Procedure.write('\item Finishing Steps\n')
   BeginList(Procedure)
   for step in testProcedure[3]:
    Procedure.write('\item Set %s.\n' % (step))
   EndList(Procedure)
   Procedure.write('\item Repeat for all combinations of Setup Steps (different inputs, loads, etc).\n')
 
   EndThe(Procedure)
   Procedure.close()

# ========================================
# Spec Table
# ========================================

# for file in files:
 # if "testingFile.py" in file and ".pyc" not in file:
  # sys.path.append(filepath)
  # testFile = __import__(file.replace('.py',''))
  # Spec = open(filepath+'\\0Spec '+TestName+'.tex','w')
  # StartTable(Spec,TestName+' Spec')

  # Specs=dict()
  # for step in testFile.testSuite[0]:
   # (aname,args,measurements,measurementKeys) = decodeStep(step)
   # for measurementKey in measurementKeys:
    # if measurementKey not in list(Specs) and measurementKey != 'none':
     # Specs[measurementKey] = measurements[measurementKey]
   # for i in list(Specs):
    # AddItemToTable(Spec,[i,]+list(Specs[i]))
  # EndTable(Spec)
  # Spec.close()
