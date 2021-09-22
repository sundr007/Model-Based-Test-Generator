import sys,os
import re
import importlib.util as IMPORTER

### Read directly from the .fzm file

# SpecFilePath = str(sys.argv[1])
# DependantOutputsPath = str(sys.argv[2])
# inputfile = str(sys.argv[3])

def importFizzim(SpecFilePath,DependantOutputsPath,inputfile):
    # inputfile = 'ModelFSM.v'
    outputfile = 'ModelFSM.py'

    statevariables	=list()
    Inputs			=list()
    Outputs			=list()
    states			=dict()
    stateValues		=list()
    actions			=list()
    actionArgs		=list()
    actionIfs		=list()
    actionResults	=list()
    actionIfResults	=list()
    transitions		=list()
    OneTimeOutputs	=dict()
    resetState=""
    currentState=""
    stateNumber=-1
    tranNumber=-1
    DefaultActions=dict()
    DefaultOutputs=dict()
    ResetActions=dict()
    ResetOutputs=dict()
    TestTransitions=list()
    TransitionOrder=dict()
    Preactions=list()

    fizzim = dict()
    keyList=[]
    start = re.compile(r'\<(\w+)\>')
    finish = re.compile(r'\</(\w+)\>')
    comments = re.compile(r'\#\#')
    notWhiteSpace = re.compile(r'(\S+)')
    actionMatch = re.compile(r'(\w+)\(+(\S+)\)+')

    # ======================================
    # Report Progress to Labview
    # ======================================
    def WriteToLabview(newline=''):
     if not os.path.isdir('Temp'):
       os.mkdir('Temp')
     if newline=='':
      file = open(os.path.join('Temp','ImportProgress.txt'),'w')
      # file.write('Start of Testing:\n')
     else:
      file = open(os.path.join('Temp','ImportProgress.txt'),'a')
      file.write(newline+'\n')
     file.close()
    # ======================================

    # ======================================
    # Find Spec in model
    # ======================================
    def FindSpec(input,value):
      outname = input+'='+str(value)
      # print("outname ",outname)
      if outname in list(Specs):
        outputValue = Specs[outname]
      else:
        try:
          outputValue = int(value)
        except:
          outputValue = value
        print("Warning did not find %s in Spec file"%(outname))
        # WriteToLabview('%s added to spec file, please update manually' % outname)
        # try:
          # SpecFile	=open(SpecFilePath,'a')
          # SpecFile.write("%s=%s,%s,%s,%s\n" % (input,outputValue,'',outputValue,''))
          # SpecFile.close()
        # except:
          # WriteToLabview('Error: Spec File Append Failed')


      return outputValue
    # ======================================

    # Clear log file
    WriteToLabview()

    # ======================================
    # Read in the Spec File
    # ======================================
    try:
     outputsInFile=list()
     SpecFile	=open(SpecFilePath,'r')
     for line in SpecFile:
      outputsInFile.append(line.split(',')[0])
     print("Read in spec file ",SpecFilePath)

     SpecFile	=open(SpecFilePath,'r')
     Specs={}
     for line in SpecFile:
      specLine = line.split(',')
      if line=='\n':
       WriteToLabview('Warning found blank line in spec file: '+SpecFilePath)
       print(SpecFilePath)
      elif len(specLine)>5:
       if "scope" in str(specLine[5]).lower():
         Specs[specLine[0]]=str(specLine[5].rstrip())
         print("Found scope: ",str(specLine[5].rstrip()))
      elif specLine[2] == '':
       # Specs[line.split(',')[0]]='(%s,%s)' % (line.split(',')[1] if line.split(',')[1]!='' else '0',line.split(',')[3].replace('\n','') if line.split(',')[3]!='\n' else '0')
       # use a number instead of a string
       min = float(specLine[1]) if specLine[1]!='' else 0
       max = float(specLine[3].replace('\n','')) if specLine[3]!='\n' else 0
       Specs[specLine[0]]=(min,max)
      else:
       Specs[specLine[0]]=int(specLine[2])
     SpecFile.close()
    except:
     WriteToLabview('Error: Spec File Read in Failed')
     exit()
    # ======================================


    # ======================================
    # Read in the inFile
    # ======================================
    infile	=open(inputfile,'r')

    for line in infile:
      key = ()
      # get information from fizzim file
      if comments.match(line) is not None:
        # print("Ignore comments: ",line)
        pass
      elif finish.search(line) is not None:
        m=finish.search(line)
        keyList.remove(m.group(1))
      elif start.search(line) is not None:
        m=start.search(line)
        keyList.append(m.group(1))
      elif notWhiteSpace.search(line) is not None:
        key = tuple(keyList)
        m=notWhiteSpace.search(line)
        fizzim[key]=m.group(1)

      # get state information
      if len(key) == 4:
        if key[0] == 'state' and key[1] == 'attributes':
          if key[3] == 'value':
            if key[2] == 'name':
             stateNumber = stateNumber+1
             states[stateNumber]={'name':fizzim[key]}
            elif key[2] == 'delay':
             states[stateNumber]['delay']=int(fizzim[key])
            elif key[2] == 'transitionOrder':
             states[stateNumber]['transitionOrder']=fizzim[key]
            elif 'outputs' in states[stateNumber]:
              outputValue = FindSpec(key[2],fizzim[key])
              states[stateNumber]['outputs'][key[2]]=outputValue
            else:
              outputValue = FindSpec(key[2],fizzim[key])
              states[stateNumber]['outputs']={key[2]:outputValue}
          elif key[3] == 'color' and fizzim[key]!= '-16777216':
              states[stateNumber]['color']='notBlack'
              # print("state color ",fizzim[key])
          elif key[3] == 'comment':
            states[stateNumber]['comment']=fizzim[key]
            Preactions.append(fizzim[key])
      # get transition information
        elif key[0] == 'transition' and key[1] == 'attributes':
          if key[3] == 'value':
            if key[2] == 'name':
             tranNumber = tranNumber+1
             transitions.append({'name':fizzim[key]})
            elif key[2] == 'equation':
             transitions[tranNumber]['equation']=fizzim[key]
            elif key[2] == 'delay':
             transitions[tranNumber]['delay']=float(fizzim[key])
            elif key[2] == 'transitionOrder':
             transitions[tranNumber]['transitionOrder']=fizzim[key]
            elif 'outputs' in transitions[tranNumber]:
              outputValue = FindSpec(key[2],fizzim[key])
              transitions[tranNumber]['outputs'][key[2]]=outputValue
             # transitions[tranNumber]['outputs'][key[2]]=fizzim[key]
            else:
             # transitions[tranNumber]['outputs']={key[2]:fizzim[key]}
              outputValue = FindSpec(key[2],fizzim[key])
              transitions[tranNumber]['outputs']={key[2]:outputValue}
          elif key[3] == 'color' and fizzim[key]!='-16777216':
            transitions[tranNumber]['color']='notBlack'
            # print("transition1 color %s and number %s"%(fizzim[key],tranNumber))
            if tranNumber not in TestTransitions:
              TestTransitions.append(tranNumber)
        # get input information
        elif key[0] == 'globals':
          if key[1] =='machine':
            if key[2] =='reset_state':
              if key[3] =='value':
                resetState = fizzim[key]
          elif key[1] == 'inputs':
            if key[2] not in Inputs:
              Inputs.append(key[2])
            if key[3] == 'value':
              DefaultActions[key[2]]=int(fizzim[key])
            if key[3] == 'resetval':
              ResetActions[key[2]]=int(fizzim[key])
      # get output information
          elif key[1].lower() == 'outputs':
            if key[2] not in Outputs:
              Outputs.append(key[2])
            if key[3] == 'value':
              DefaultOutputs[key[2]]=int(fizzim[key])
            if key[3] == 'resetval':
              ResetOutputs[key[2]]=int(fizzim[key])
      # get state or transition output information
          elif key[1] == 'state' or key[1] == 'trans' and key[3] == 'type':
            # print("Found output not defined in global outputs: ",key[2])
            # Append all outputs except for reserved words
            if fizzim[key].lower() == 'output' and key[2] not in Outputs and key[2]!='delay' and key[2]!='name' and key[2]!='equation' and key[2]!='transitionOrder':
              Outputs.append(key[2])
      # get more transition information
      elif len(key) == 2 and key[0].lower() == 'transition':
        if key[1] == 'startState' or key[1] == 'endState':
          transitions[tranNumber][key[1]]=fizzim[key]
        elif key[1].lower() == 'color' and fizzim[key]!='-16777216':
          transitions[tranNumber][key[1]]='notBlack'
          # print("transition2 color %s and number %s"%(fizzim[key],tranNumber))
          if tranNumber not in TestTransitions:
              TestTransitions.append(tranNumber)
        elif key[1].lower() == 'comment':
          transitions[tranNumber]['scopeMeas']=fizzim[key]


    infile.close()
    # ======================================

    # ======================================
    # Append new outputs not in spec file already to the spec file.
    # This user will manually update the specs later.
    # ======================================
    # print("outputs in spec file: ",outputsInFile)
    # SpecFile	=open(SpecFilePath,'a')
    # for stateValue in states:
     # for output in states[stateValue]['outputs']:
      # outputValue = states[stateValue]['outputs'][output]
      # outname = output+'='+str(outputValue)
      # print("output %s = %s in state %s\n"%(output,outputValue,stateValue))
      # for char in (',','-','#'):
       # if char in output:
        # WriteToLabview('Error: "%s" in output name "%s"'%(char,output))
        # exit()
      # if outname not in outputsInFile:
       # print("output %s not in spec file: "%(output))
       # WriteToLabview('%s added to spec file, please update manually' % output)
       # #SpecFile.write("%s,%s,%s,%s\n" % (output,'',output.split('=')[1],''))
       # SpecFile.write("%s=%s,%s,%s,%s\n" % (output,outputValue,'',outputValue,''))
       # outputsInFile.append(output)
    # print("outputs in spec file: ",outputsInFile)
    # SpecFile.close()
    # ======================================

    # ======================================
    # Sort out the data read in before writing to file.
    # ======================================
    for n,tran in enumerate(transitions):
     actionAndArgs = [tran.get('equation'),]
     tranActionAndArgs = list()
     argList = list()
     if '&&' in tran.get('equation'):
       actionAndArgs = tran.get('equation').split('&&')
     for a in actionAndArgs:
       # print(a)
       m=re.match(actionMatch,a)
       if m is None:
          WriteToLabview('Error matching action for transition: %s from state %s to state %s\n\taction: %s\n'%(tran.get('name'),tran.get('startState'),tran.get('endState'),a))
          print('Error matching action for transition: %s\n\taction: %s\n'%(tran.get('name'),a))
          exit()
       else:
        # model based test accepts 2 types of action args: float or string
        # either action(float,string) or action(string) or action(float,float) or action(float)
        # specified test accepts action(string) or any of model base test actions
        if m.group(1) not in Inputs:
          print("Adding %s to inputs %s"%(m.group(1),Inputs))
          Inputs.append(m.group(1))
        # do not split by comma if there is a square bracket
        if '[' in m.group(2):
          argList.append(m.group(2).rstrip(','))
          print("Found square bracket: ",argList)
        # split by comma to handle previous models`
        elif ',' in m.group(2):
          argList = m.group(2).split(',')
          try:
            arg1 = float(argList[0])
          except:
            arg1 = argList[0]
            specValue = FindSpec(m.group(1),arg1)
            if specValue == arg1:
              print("Warning did not find number in arg1 for transition: %s from state %s to state %s\n\taction: %s\n"%(tran.get('name'),tran.get('startState'),tran.get('endState'),a))
            else:
              print("arg1: %s and specValue: %s"%(arg1,specValue))
              arg1 = specValue
          argList[0] = arg1
          if argList[1] != '':
            try:
              arg2 = float(argList[1])
            except:
              arg2 = argList[1]
              print("Warning did not find number in arg2 for transition: %s from state %s to state %s\n\taction: %s\n"%(tran.get('name'),tran.get('startState'),tran.get('endState'),a))
            argList[1] = arg2
          else:
            del argList[1]
        # determine if number or look for spec definition
        else:
          try:
            arg1 = float(m.group(2))
          except:
            arg1 = m.group(2)
            specValue = FindSpec(m.group(1),arg1)
            if specValue == arg1:
              print("Warning did not find number in arg1 for transition: %s from state %s to state %s\n\taction: %s\n"%(tran.get('name'),tran.get('startState'),tran.get('endState'),a))
            else:
              print("no commas arg1: %s and specValue: %s"%(arg1,specValue))
              arg1 = specValue
          argList.append(arg1)
        argt = tuple(argList)
        tranActionAndArgs.append((m.group(1),argt))
     # print("action and args: ",tranActionAndArgs)
     transitions[n]['actionAndArgs']=tranActionAndArgs


    # for stateValue in states:
     # for output in states[stateValue]['outputs']:
      # try:
       # stateValues[stateValues.index(stateValue)][stateValue.index(output)] = output.split('=')[0]+'='+Specs[output]
       # state[stateValue][stateValue.index(output)] = output+'='+Specs[output+'='+str(stateValue[stateValue]['outputs'][output])]
      # except:
       # WriteToLabview('Error: One of the outputs has a name with a bad character in it.')
       # exit()


    # for (currentState,actionAndArgs,nextState,delay,output) in transitions:
     # for out in list(output):
      # if out not in Outputs:
       # Outputs.append(out)
    # for state in list(OneTimeOutputs):
     # for out in list(OneTimeOutputs[state]):
      # if out not in Outputs:
       # Outputs.append(out)
    # for stateValue in stateValues:
     # for out in stateValue:
      # out = out.split('=')[0]
      # if out not in Outputs:
       # Outputs.append(out)
    # print('Inputs: '+str(Inputs))
    # print('Outputs: '+str(Outputs))
    # print('OneTimeOutputs: '+str(OneTimeOutputs))
    # print('States: '+str(states))
    # print('State Values: '+str(stateValues))
    # print('actions: '+str(actions))
    # print('Action Args: '+str(actionArgs))
    # print('action Ifs: '+str(actionIfs))
    # print('actions Results: '+str(actionResults))
    # print('actions Ifs Results: '+str(actionIfResults))

    # ======================================
    actions = sorted(set(Inputs))
    # ======================================
    # Default Values
    # ======================================
    # DefaultActions=dict()
    # DefaultOutputs=dict()
    # import DefaultValues
    for action in actions:
     if action not in list(DefaultActions):
      # if action in list(DefaultValues.DefaultActions):
       # DefaultActions[action] = DefaultValues.DefaultActions[action]
      # else:
       DefaultActions[action] = 0
    if 'delay' in Outputs:
     Outputs.remove('delay')
    if 'transitionOrder' in Outputs:
     Outputs.remove('transitionOrder')

    for Output in DefaultOutputs:
      outname = Output+'='+str(DefaultOutputs[Output])
      if outname in list(Specs):
        DefaultOutputs[Output] = Specs[outname]
    # for Output in Outputs:
     # if Output not in list(DefaultOutputs):
      # if Output in list(DefaultValues.DefaultOutputs):
        # DefaultOutputs[Output] = DefaultValues.DefaultOutputs[Output]
      # else:
        # DefaultOutputs[Output] = 0

    if 'delay' in DefaultOutputs:
      del DefaultOutputs['delay']
      # WriteToLabview("Warning delay is a reserved output")
    if 'transitionOrder' in DefaultOutputs:
      del DefaultOutputs['transitionOrder']
      WriteToLabview("Warning transitionOrder is a reserved output")


    DefaultValuesFile = open('DefaultValues.py','w')
    DefaultValuesFile.write('DefaultActions = '+str(DefaultActions)+'\n')
    DefaultValuesFile.write('DefaultOutputs = '+str(DefaultOutputs)+'\n')
    DefaultValuesFile.close()

    #change to load the specified file
    # DependantOutputsPath
    # from DependentInputOuputs import Doutputs
    #load the model specific inputs and outputs
    ioSpec = IMPORTER.spec_from_file_location("InputOuputs.py", DependantOutputsPath) #(module name, path)
    inOutFile = IMPORTER.module_from_spec(ioSpec)
    try:
     ioSpec.loader.exec_module(inOutFile)
    except:
     WriteToLabview('Error: loading module from file InputOutputs.py')
     exit()
    modelDoutputs = inOutFile.localDoutputs()

    # ======================================
    # Order the test transitions
    # ======================================

    test = dict()
    star = list()
    TestTranOrdered = list()
    # Find the transition order output from model
    for n,tran in enumerate(transitions):
     # print(tran)
     order = tran.get('transitionOrder')
     if order is not None:
       print("found order number ",order)
       if n in TestTransitions:
        test[order]=n
       else:
        WriteToLabview('Warning transitionOrder assigned to transition with no color')
        WriteToLabview('Not adding to TestTransitions\ntransition:\n\t %s from state %s to state %s\n\taction: %s\n'%(tran.get('name'),tran.get('startState'),tran.get('endState'),tran.get('equation')))
        print("Warning did not add %s to TestTransitions"%n)
    # sort the transition number based on transition order number
    keyOrder = sorted(test)
    for key in keyOrder:
      if '*' in key:
        star.append(test[key])
      TestTranOrdered.append(test[key])
    # Add at the end any not black transitions not ordered
    for t in TestTransitions:
      if t not in TestTranOrdered:
        TestTranOrdered.append(t)
    # Add a * to transition number if indicated in order number
    for s in star:
      if s in TestTranOrdered:
        i = TestTranOrdered.index(s)
        TestTranOrdered[i]=str(TestTranOrdered[i])+'*'
    TestTransitions = TestTranOrdered


    # ======================================
    # Write the output file
    # ======================================
    outfile	=open(outputfile,'w')
    # delays=dict()
    # for state in states:
     # n = states.index(state)
     # if 'delay' in list(OneTimeOutputs[state]):
      # delays[n] = OneTimeOutputs[state]['delay']
      # del OneTimeOutputs[state]['delay']
     # else:
      # delays[n] = 0

    # Write the actions list (this allows the file to be imported by Python later without errors)
    outfile.write('# Actions\n')
    outfile.write('Actions = '+str(actions+list(modelDoutputs.inputs))+'\n')
    # outfile.write('\n')
    combOutputs = sorted(set(Outputs+list(modelDoutputs.outputs)))
    outfile.write('Outputs = '+str(combOutputs)+'\n')
    outfile.write('# Default Values\n')
    outfile.write('DefaultActions = '+str(DefaultActions)+'\n')
    outfile.write('DefaultOutputs = '+str(DefaultOutputs)+'\n')
    outfile.write("DefaultState = '"+resetState+"'\n")
    outfile.write('# Test select Transitions\n')
    outfile.write('Preactions = '+str(Preactions)+'\n')
    outfile.write('TestTransitions = '+str(TestTransitions)+'\n')
    outfile.write('\n# States\n')
    outfile.write('states = {\n')

    # Write the states
    for n in states:
     # n = states.index(state)
     # outs = (",'".join(stateValues[n])).replace('=',"':")+','+','.join(["'%s':%s"%(x,OneTimeOutputs[state][x]) for x in list(OneTimeOutputs[state])])
     # outfile.write(' '+str(n)+" : {'name': '"+str(state)+"' ,'outputs': {'"+str(outs)+"},'delay': "+str(delays[n])+'},\n')
     outs = str(states[n]).replace('"','')
     outfile.write(' '+str(n)+" : "+str(outs)+',\n')
     # outfile.write(' '+str(n)+" : "+str(states[n])+',\n')
    outfile.write('}\n\n')

    # Write the transitions
    outfile.write('# State Transitions\n')
    outfile.write('graph = (\n')
    # for (currentState,actionAndArgs,nextState,delay,outputs) in transitions:
    for n,tran in enumerate(transitions):
     currentState = -1
     nextState = -1
     for s in states:
      if tran.get('startState') == states[s].get('name'):
        currentState = s
      if tran.get('endState') == states[s].get('name'):
        nextState = s
     if currentState < 0 or nextState < 0:
        WriteToLabview('Error finding states for transition: %s\n\t current state %s(%s) and next state %s(%s)'%(tran.get('name'),tran.get('startState'),currentState,tran.get('endState'),nextState))
        exit()
     delay = tran.get('delay',1)
     outputs = tran.get('outputs',{})
     tranActionAndArgs = tran.get('actionAndArgs',())
     # print("action and args: ",tranActionAndArgs)
     outfile.write("(%s, %s, %s, %s, %s),\n" % (currentState,tranActionAndArgs,delay,nextState,outputs))

    outfile.write(")")
    outfile.close()

    # ======================================
    # Error Check
    # ======================================
    if states=={}:
     WriteToLabview('Error with Fizzim Model, Please check it for completeness')
     exit()
    for state in states:
     # print(state)
     for char in ("$",' '):
      if char in states[state].get('name'):
       WriteToLabview('Error: %s in state name %s - %s'%(char,state,states[state].get('name')))
       exit()

    from difflib import SequenceMatcher as SM
    for action in actions:
     ratios = []
     for otheraction in actions:
      ratios.append(SM(None,action,otheraction).ratio())
     for i,ratio in enumerate(ratios):
      otheraction = actions[i]
      # print(ratio)
      if ratio > .8 and ratio < 1:
       WriteToLabview('Warning: Action %s name is close to action name %s, was one mispelled?'%(action,otheraction))
    # ======================================
    # Report Success to Labview
    # ======================================
    WriteToLabview('%s Inputs'%len(actions))
    WriteToLabview('%s Outputs'%len(Outputs))
    WriteToLabview('%s States'%len(states))
    WriteToLabview('%s Transitions'% len(transitions))
    WriteToLabview('Import Was Successful')
