'''
Created on Oct 29, 2022

@author: Duy Le
'''


import sys


opCodes = {'push': 0, 'pop': 1, 'pushr': 2, 'popr': 3, 'pushi': 4,                  # push-pop 
          'add': 5, 'sub': 6, 'or': 7, 'and': 8, 'xor': 9, 'sl': 10, 'sr': 11,      # arithmetic and bitwise
          'jal': 12, 'jr': 13, 'j': 14, 'beq': 15, 'blt': 16, 'bgt': 17}            # jump and branch

                                      
lines = []
labelTable = {}
lineCount = 0
cleanLines = []         
hexLines = []
error = False   

def twoByTwoHexFormat(strLine):
    cur = ''
    for i in range(len(strLine)//2):
        cur = cur +  strLine[2*i]+ strLine[2*i+1]+' '
    
    return cur[:len(cur)-1]

def toBinary(value, size):
    if value>=0:
        return  bin(value)[2:].zfill(size)
    else:
        return bin(value+(1<<size))[2:]


# A class that check if a string is a valid decimal, binary, or hexadecimal    
class NumberChecker:
    numVal =0
    isDecimal, isBinary, isHex = False, False, False
    isValidNum = False
    
    def __init__(self,numb):
        self.isValidNum = self.toNumber(numb)
      
    def toNumber(self,numb):   
        try:
            self.numVal=int(numb, 16)
            self.isHex = True
        except ValueError:
            self.isHex = False
            
        try:
            self.numVal=int(numb, 2)
            self.isBinary = True
        except ValueError:
            self.isBinary = False
            
        try:
            self.numVal=int(numb, 10)
            self.isDecimal = True
        except ValueError:
            self.isDecimal = False
            
        return (self.isBinary or self.isDecimal or self.isHex)


# Get the file name from user input
if len(sys.argv) < 2: print('File name missing, please try again'); exit(1)

fileName = sys.argv[1]
try: f = open(fileName, 'r')                  
except: print("ERROR: Can't find file \'" + sys.argv[1] + "\'."); exit(1)

# Read the file
while True:
    line = f.readline()
    if not line: break
    strippedLine = line.strip()
    if strippedLine!='':                                   # cut out empty lines
        parsedLine = strippedLine.split()
        
        # Collect LABELs to the table:
        if parsedLine[0].find(':')!=-1:
            labelTable[parsedLine[0][: len(parsedLine[0])-1]] = lineCount
            parsedLine[0] = ''                             # null the LABELs
            
        # Skip lines having no instruction
        if parsedLine[0]=='' and len(parsedLine)==1:       # LABEL-only
            lineCount+=0
        elif parsedLine[0]==''and parsedLine[1][0]=='#':   # LABEL + Comment-only
            lineCount+=0
        elif parsedLine[0]!='' and parsedLine[0][0]=='#':  # Comment-only
            lineCount+=0
        
        # Add lines having instructions
        else:
            lines.append(parsedLine)
            lineCount+=1
                           
f.close()



# Cut out LABELs and comments part
for i in range(len(lines)):
    cleanLine = []
    for k in range(len(lines[i])):
        if lines[i][k]!='':
            if lines[i][k][0]=='#': break
            cleanLine.append(lines[i][k])         
    cleanLines.append(cleanLine)
          

# Turn instructions into hex or binary and detect error    
for i in range(len(cleanLines)):
    hexLine = []
    # Turn mnemonic into hex:
    decCode = opCodes.get(cleanLines[i][0], -1)
    if decCode==-1:
        print("Error: "+ cleanLines[i][0]+" is not a valid instruction")
        error = True
        break
    #hexCode = '%02.2x' % (decCode & 0xff)
    hexCode = toBinary(decCode, 8)
    hexLine.append(hexCode)
    
    if len(cleanLines[i])>2:
        print("Invalid instruction format (maybe excessive operand number)")
        error = True
        break
    
    # Jump and branch instructions
    if decCode>=12 and decCode!=13:
            
        if len(cleanLines[i]) <=1:
            print("Error: No Label for "+ cleanLines[i][0])   
            error = True 
            break             
        labelAddr = labelTable.get(cleanLines[i][1], -1)
        if labelAddr==-1:
            print("Error: Label "+ cleanLines[i][1]+" does not exist")
            error = True
            break
        imm = (labelAddr-i)
        
        # hexImm = '00'
        # hexImm += '%04.4x' % (imm & 0xffff)
        
        hexImm = '00000000'
        hexImm+= toBinary(imm, 16)
        
        hexLine.append(hexImm)
        
    # Push-pop instructions
    elif decCode<=4 and decCode>=0: 
        if len(cleanLines[i]) <=1:
            print("Error: No immediate for "+ cleanLines[i][0])
            error = True
            break
        numbChecker = NumberChecker(cleanLines[i][1])
        if numbChecker.isValidNum:
            imm = numbChecker.numVal
        else:
            print("Error: Invalid number format for immediate")
            error = True
            break
        # hexImm = '00'
        # hexImm += '%04.4x' % (imm & 0xffff)
        
        hexImm = '00000000'
        hexImm+= toBinary(imm, 16)
        
        hexLine.append(hexImm)
        
    # Arithmetic and bitwise instructions
    else:
        if len(cleanLines[i])>1:
            print("Error: Invalid S type instruction format")
            error = True
            break
        hexLine.append('000000000000000000000000')
    
    completedHexLine = hexLine[1] + hexLine[0] 
    formatedHexLine =  completedHexLine                     #twoByTwoHexFormat(completedHexLine)
    hexLines.append(formatedHexLine)
            

# Export a machine code file   
if not error:
    with open('mcCode_', 'w') as f:
        f.write('\n'.join(hexLines))
        f.close
    
    
    
        
# Testing: display on console
if not error: 
    for i in range(len(hexLines)):
        print(hexLines[i])   
    
    # LABELs table display:
    print(" ")
    print("Display LABEL table:")
    print(labelTable)



