

# ========================================
# input functions
# These functions can directly change outputs or inputs.
# These are often used for setting bits that would make the base state machine too large.
# ========================================
def Clear(arg=''):
 outputChange   ={'OUT':0,}
 inputChange	={'A':arg,'B':arg,}
 defaultValue   = 0
 return (inputChange,outputChange,defaultValue)


# ========================================
# output functions
# These are outputs that dependent upon other outputs or inputs.
# ========================================

def notOUT(OUT):
 return 0 if OUT[0] else 1


class localDoutputs:
    def __init__(self):
        pass

# ========================================
# function dictionary
# ========================================

    inputs =\
    {
        'Clear':(Clear,('',),((1,0),1)),
    }
# ensure that a comma is at the end of a single entry list below.
    outputs =\
    {
        'notOUT':(notOUT,('OUT',)),
    }


##########################################################################

    #do not modify this function, or model's will not be able to explore
    def input(self,input,outputValues,inputValues,arg):
        args = [arg,]
        for out in self.inputs[input][1]:
            if out != '':
                if out in outputValues:
                    args.append(outputValues[out])
                elif out in inputValues:
                    args.append(inputValues[out])
                else:
                    print('Input failed: %s'%input)
                    return ({},{},{})
                # args.append(outputValues[out])
        args=tuple(args)
        # print(input,args)
        (inputChange,outputChange,defaultValue)    = self.inputs[input][0](*args)
        return (inputChange,outputChange,defaultValue)

    #do not modify this function, or model's will not be able to explore
    def compute(self, output, outputValues, inputValues):
        args = []
        for out in self.outputs[output][1]: # find output or input that is used to set output
            if out in outputValues:
                args.append(outputValues[out])
            elif out in inputValues:
                args.append(inputValues[out])
            else:
                args.append(0)
        args = tuple(args)
        return self.outputs[output][0](args)
