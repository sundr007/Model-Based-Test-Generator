# ======================================
#
# Name: Specified Tester
#
# Purpose: Runs the test contains in test files and returns the outputs.
# ======================================

from time import sleep
import os,shutil,sys,imp,re,fileinput,TesterOptions,xlsxwriter,xlrd
from importlib.machinery import SourceFileLoader
from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.utility import xl_range

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

def actionsInTestFile(testFile,krun):
 done=0
 i=0
 actions=['AC','PSON','PSKILL','ClearFaultsFF','ACoff']
 while not done:
  (aname, args, measurements, delay, done) = SelectAction(krun,i,testFile)
  i=i+1
  if aname not in actions:
   actions.append(aname)
 return actions
   
# ======================================
# Create Work Sheet
# ======================================
def CreateWorkSheet(wb,name,testFile,krun,TemplateSetupTab):
 ws = wb.add_worksheet('Setup')
 wsReport = wb.add_worksheet('ReportTable CSV')
 OrangeCell = wb.add_format({'fg_color': 'orange','bottom': 1,'top': 1})
 TestNum = wb.add_format({'fg_color': 'gray','bottom': 1,'top': 1})
 OptionC = wb.add_format({'fg_color': 'silver','bottom': 1,'top': 1})
 merge_format = wb.add_format({
    'border': 1,
    'align': 'center',
	'text_wrap': 1,
    'valign': 'vcenter',})
 ws.merge_range(xl_range(4, 1, 4, 6),'Test Number (dont change)',TestNum)
 ws.merge_range(xl_range(5, 1, 5, 6),'Options 1',OptionC)
 ws.merge_range(xl_range(6, 1, 6, 6),'Options 2',OptionC)
 actions 		= actionsInTestFile(testFile,krun)
 measurements 	= testFile.report[0][1]
 icol=7
 actionCol={}
 actionOptions={}
 for col in range(100):
  cell = TemplateSetupTab.cell(0,col)
  if cell.value in actions:
   CellRange=xl_range(0, icol, 3, icol)
   ws.merge_range(CellRange,TemplateSetupTab.cell(2,col).value, merge_format)
   ws.write(4,icol,TemplateSetupTab.cell(6,col).value,TestNum)
   ws.write(5,icol,TemplateSetupTab.cell(7,col).value,OptionC)
   ws.write(6,icol,TemplateSetupTab.cell(8,col).value,OptionC) 
   ws.write(7,icol,'',OrangeCell)
   actionCol[cell.value]=icol
   if TemplateSetupTab.cell(0,col).value != '':
    actionOptions[cell.value]=TemplateSetupTab.cell(1,col).value
   icol=icol+1  
# Put delay in
 CellRange=xl_range(0, icol, 3, icol)
 ws.merge_range(CellRange,'Delay', merge_format)
 ws.write(4,icol,12,TestNum)
 ws.write(5,icol,'',OptionC)
 ws.write(6,icol,'',OptionC) 
 ws.write(7,icol,'',OrangeCell)
 actionCol['Delay']=icol
 icol=icol+1 
 for measurement in list(measurements):
  col=0
  while TemplateSetupTab.cell(0,col).value != measurement:
   col=col+1
  cell = TemplateSetupTab.cell(0,col)
  if cell.value in measurements:
   CellRange=xl_range(0, icol, 3, icol)
   ws.merge_range(CellRange,TemplateSetupTab.cell(2,col).value, merge_format)
   ws.write(4,icol,TemplateSetupTab.cell(6,col).value,TestNum)
   ws.write(5,icol,TemplateSetupTab.cell(7,col).value,OptionC)
   ws.write(6,icol,TemplateSetupTab.cell(8,col).value,OptionC) 
   ws.write(7,icol,'',OrangeCell)
   actionCol[cell.value]=icol
   icol=icol+1 
 Row=8
 FirstRow=['Step','Action','Source']+list(measurements)+['Result']
 wsReport.write_row('A1',FirstRow)
 return (ws,actionCol,actionOptions,Row,wsReport) 

# ======================================
# Write Reset Steps
# ======================================
def PerformActions(wb,ws,actionCol,actionOptions,startRow,Actions):
 Colo = 7
 NumberColumns=len(actionCol)+Colo
 Row=startRow
 Col=7
 dataInFormat = wb.add_format({'fg_color': '#B2FF66','border': 1})
 NodataFormat = wb.add_format({'fg_color': '#FEFEFE','border': 1})
 for Action in Actions:
  while Col != actionCol[Action[0]]:
   ws.write(Row,Col,'',NodataFormat)
   Col=Col+1
   if Col==NumberColumns:
    Row = Row+1
    Col = Colo
  if Action[0] in list(actionOptions):
   if actionOptions[Action[0]]=='invert':
    actionVal=1 if int(float(Action[1]))==0 else 0
   else:
    actionVal=Action[1]
  else:
   actionVal=Action[1]
  ws.write(Row,Col,actionVal,dataInFormat)
  Col=Col+1
  if Col==NumberColumns:
   Row = Row+1
   Col = Colo
 if Col != Colo:
  while Col != NumberColumns:
   ws.write(Row,Col,'',NodataFormat)
   Col=Col+1
  Row=Row+1
 return Row
   
# ======================================
# Write Test Steps and Report Tab
# ======================================
def WriteTestActionsAndReport(wb,ws,actionCol,actionOptions,startRow,testFile,krun,wsReport):
 done = 0
 isteps = 0
 while not done:
  (aname, args, includemeasurements, delay, done) = SelectAction(krun,isteps,testFile)
  if includemeasurements != {}:
   measurements 	= testFile.report[0][1]
  else:
   measurements=[]
  actions = [[aname, ','.join(str(x) for x in args)],['Delay',delay]]+[[x,'yes'] for x in list(measurements)]
  startRow = PerformActions(wb,ws,actionCol,actionOptions,startRow,actions)
  wsReport.write_row('A%s'%str(isteps*3+2),[str(isteps+1),'%s[%s]'%(aname, args)])
  wsReport.write_row('C%s'%str(isteps*3+3),['Spec',]+[str(includemeasurements[x]) for x in list(measurements)])
  wsReport.write_row('C%s'%str(isteps*3+4),['Actual',])
  formula=[]
  for i,measurement in enumerate(list(measurements)):
   wsReport.write_formula(xl_rowcol_to_cell(isteps*3+3,3+i),'=Setup!%s'%xl_rowcol_to_cell(startRow-1,7+len(actionCol)-len(list(measurements))+i))
   if len(str(includemeasurements[measurement]))==1:
    formula.append('%s=%s'%(xl_rowcol_to_cell(isteps*3+3,3+i),xl_rowcol_to_cell(isteps*3+2,3+i)))
   else:
    (result,spec) = (xl_rowcol_to_cell(isteps*3+3,3+i),xl_rowcol_to_cell(isteps*3+2,3+i))
    formula.append('AND(%s*1>1*MID(%s,2,FIND(",",%s)-2),%s*1<1*MID(%s,FIND(",",%s)+1,LEN(%s)-FIND(",",%s)-1))'%(result,spec,spec,result,spec,spec,spec,spec))
  wsReport.write_formula(xl_rowcol_to_cell(isteps*3+3,3+len(list(measurements))),'=if(and(%s),"Pass","fail")'%','.join(formula))
  isteps=isteps+1
 return startRow
 
def FinalTouches(wb,ws,actionCol,startRow,testFile,krun,wsReport):
 ws.write_formula('A1','=round(sum(%s)/60,2)&" Min"'%xl_range(8,actionCol['Delay'],startRow,actionCol['Delay']))
 ws.write('C1',len(actionCol))
 ws.write('C2',startRow-8)
 
# ------------------- End of Run Test File----------------------------

def main():
  (options, args) = TesterOptions.parse_args()
  # args can include model programs, FSMs, test suites
  if not args:
    TesterOptions.print_help()  # must have at least one arg, not optional
    exit()
# Path Setup
  testReportPath = options.testreport
  sys.path.append(testReportPath)
  TemplateWorkBook = xlrd.open_workbook(testReportPath+'BaseTemplate.xls')
  TemplateSetupTab = TemplateWorkBook.sheet_by_name('Setup')
# ======================================
# Determine which tests should be run based on spec file.
# ======================================
  SpecFolders=[]
  for file in os.listdir(testReportPath+'report'):
   if 'spec.tex' in file:
    spec=open(testReportPath+'report\\spec.tex','r')
    for line in spec:
     if "section{" in line:# and "%" not in line:
      TestName=re.findall('{([^"]*)}', line)[0]
      SpecFolders.append(TestName)
# ======================================
# Loop through folder structure and run tests
# ======================================
  ResetActions = [['AC','220,50'],['PSON','1'],['PSKILL','1'],['Delay','1'],['PSON','0'],['PSKILL','0'],['Delay','1'],['PSON','1'],['PSKILL','1'],['Delay','1'],['AC','1,50'],['Delay','1'],['ClearFaultsFF','1'],['Delay','1']]
  FinishingActions = [['ACoff','off'],]
  currentDir 	= os.getcwd()
  os.chdir(currentDir)
  for folder in os.listdir(testReportPath+'report\\data'):
   if SpecFolders!= []:# and folder in SpecFolders: 
    for file in os.listdir(testReportPath+'report\\data\\'+folder):
     if file=='testingFile.py':
      testPath = testReportPath+'report\\data\\'+folder+'\\'
      testFile = SourceFileLoader("testingFile",testPath+file).load_module()
      strategyRuns = len(testFile.testSuite)
      krun = 0
      os.chdir(testPath)
      wb = xlsxwriter.Workbook("Report.xlsx")
      while krun < strategyRuns:
# Create WorkSheet
        (ws,actionCol,actionOptions,Row,wsReport) = CreateWorkSheet(wb,'Test%s' % krun,testFile,krun,TemplateSetupTab)
# Write the reset actions needed to get to state 0
        Row = PerformActions(wb,ws,actionCol,actionOptions,Row,ResetActions)
# Write the test actions and measurements
        Row = WriteTestActionsAndReport(wb,ws,actionCol,actionOptions,Row,testFile,krun,wsReport)
# Write any standard finishing actions like turn off AC.
        Row = PerformActions(wb,ws,actionCol,actionOptions,Row,FinishingActions)
        FinalTouches(wb,ws,actionCol,Row,testFile,krun,wsReport)
        krun += 1
      if krun > 1:
        print( 'Test finished, completed %s runs' % krun)
      wb.close() 
	  
# ------------------ end main function ------------------------------------

# ======================================
# Main Program Call
# ======================================
if __name__ == '__main__':
      main()
