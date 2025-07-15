import micro_processor
instruction_set = ["add","sub","call","jmp","inc","mov.b","mov","mov.w","dec","jne","jnz","jeq","jl","cmp","push","pop","ret","bis","bis.b","rra","rla",
                   ".byte","xor","xor.b","jz","and","and.b"]


labels = {}


code_list = []
data_list = []




class code_line:
    def __init__(self,line_text,line_number):
        self.line_text = line_text
        self.line_number = line_number
    def __str__(self):
        return str(self.line_number)+":"+self.line_text.__repr__()
    def __repr__(self):
        return str(self.line_number)+":"+self.line_text.__repr__()



def convert_execution_list(file_content):
    micro_processor.reset()

    lines = []
    i:str
    file_content = file_content.split("\n")
    for i in range(len(file_content)):
        lowered = file_content[i].lower()
        if ";" in lowered:
            index = lowered.index(";")
            lowered = lowered[:index]
            

        lowered = lowered.replace(' ',',')
        lowered = lowered.replace('\n',',')
        lowered = lowered.replace('\t',',')
        
        
        splitted = lowered.split(",")
        while '' in splitted:
            splitted.remove('') 


        if splitted != []:
            lines.append(code_line(splitted,i))
    
    code_area = []
    data_area = []
    is_reached = False 
    for i in lines:
        if i == ".data":
            is_reached = True
        else:
            if is_reached:
                pass
            else:
                code_area.append(i)

    
    global code_list,data_list
    code_list = code_area
    data_list = data_area


    print(code_area,data_area)


def execute(parameter_list,register_dict:dict,stack:list,memory:list):

    print("given parameters:",parameter_list)
    if parameter_list[0] in instruction_set:
        if parameter_list[0] == 'mov' or parameter_list[0] == 'mov.b' or parameter_list[0] == 'mov.w':
            if parameter_list[1] in register_dict.keys():
                sayi = register_dict[parameter_list[1]]
                if parameter_list[2] in register_dict.keys():
                    register_dict[parameter_list[2]] = sayi 
                    return True, f"Success! mov op is executed, value in register{parameter_list[1]} copied intoregister{parameter_list[2]}"
                
                else:
                    print('boyle bir register yok ki kanka ne diyon')
                    return False,f"Failed!,dst must be valid register but {parameter_list[2]} given?"
            else:
                if parameter_list[1][0] == '#':
                    sayi = convert_to_int(parameter_list[1][1:])
                    if sayi is None and parameter_list[1][1:] in labels.keys():
                        sayi = labels[parameter_list[1][1:]]
                    
                    if parameter_list[2] in register_dict.keys():
                        register_dict[parameter_list[2]] = sayi 
                        return True, f"Success! mov op is executed constant {sayi} moved to register {parameter_list[2]}"
                elif parameter_list[1][0] == '@':
                    if parameter_list[1][1:] in register_dict.keys():
                        sayi = memory[register_dict[parameter_list[1][1:]]]

                    if parameter_list[2] in register_dict.keys():
                        register_dict[parameter_list[2]] = sayi 
                    
                    pass
                else:
                    return False,"Failed!,second parameter should be #constant or register"
        
        
        elif parameter_list[0] == 'inc':
            if parameter_list[1] in register_dict.keys():
                register_dict[parameter_list[1]]+=1
                register_dict['flag_n'] = 1 if register_dict[parameter_list[1]]<0 else 0
                register_dict['flag_z'] = 1 if register_dict[parameter_list[1]]==0 else 0
                return True,f"Success! register {parameter_list[1]} is incremented"
            else:
                return False,f"Failed! parameter should be register for inc op but  {parameter_list[1]} is given ????"
        elif parameter_list[0] == 'dec':
            if parameter_list[1] in register_dict.keys():
                register_dict[parameter_list[1]]-=1
                register_dict['flag_n'] = 1 if register_dict[parameter_list[1]]<0 else 0
                register_dict['flag_z'] = 1 if register_dict[parameter_list[1]]==0 else 0

                return True,f"Success! register {parameter_list[1]} is decremented"
            else:
                return False,f"Failed! parameter should be register for dec op but  {parameter_list[1]} is given ????"
        elif parameter_list[0] == 'rra':
            if parameter_list[1] in register_dict.keys():
                register_dict[parameter_list[1]] >>=1
                register_dict['flag_n'] = 1 if register_dict[parameter_list[1]]<0 else 0
                register_dict['flag_z'] = 1 if register_dict[parameter_list[1]]==0 else 0

                return True,f"Success! register {parameter_list[1]} is decremented"
            else:
                return False,f"Failed! parameter should be register for dec op but  {parameter_list[1]} is given ????"
        elif parameter_list[0] == 'rla':
            if parameter_list[1] in register_dict.keys():
                register_dict[parameter_list[1]] <<=1
                register_dict['flag_n'] = 1 if register_dict[parameter_list[1]]<0 else 0
                register_dict['flag_z'] = 1 if register_dict[parameter_list[1]]==0 else 0

                return True,f"Success! register {parameter_list[1]} is decremented"
            else:
                return False,f"Failed! parameter should be register for dec op but  {parameter_list[1]} is given ????"

        elif parameter_list[0] == 'jmp':
            if parameter_list[1] in labels.keys():
                branch_address = labels[parameter_list[1]]
                register_dict['pc'] = branch_address
                return True,f"Success! jumped to {parameter_list[1]}"
            else:
                return False,f"Failed! invalid label for jmp op, {parameter_list[1]} cannot found"

        elif parameter_list[0] == 'jeq'  or parameter_list[0] == 'jz'  :
            if register_dict['flag_z'] == 1:
                if parameter_list[1] in labels.keys():
                    branch_address = labels[parameter_list[1]]
                    register_dict['pc'] = branch_address
                    return True,f"Success! jumped to {parameter_list[1]}"
                else:
                    return False,f"Failed! invalid label for jmp op, {parameter_list[1]} cannot found"
        
        elif parameter_list[0] == 'jne' or parameter_list[0] == 'jnz' :
            if register_dict['flag_z'] == 0:
                if parameter_list[1] in labels.keys():
                    branch_address = labels[parameter_list[1]]
                    register_dict['pc'] = branch_address
                    return True,f"Success! jumped to {parameter_list[1]}"
                else:
                    return False,f"Failed! invalid label for jmp op, {parameter_list[1]} cannot found"
        
        elif parameter_list[0] == 'jl':
            if register_dict['flag_n'] == 1:
                if parameter_list[1] in labels.keys():
                    branch_address = labels[parameter_list[1]]
                    register_dict['pc'] = branch_address
                    return True,f"Success! jumped to {parameter_list[1]}"
                else:
                    return False,f"Failed! invalid label for jmp op, {parameter_list[1]} cannot found"

        elif parameter_list[0] == 'cmp':
            if parameter_list[1] in register_dict.keys():
                birinci = register_dict[parameter_list[1]] 
            else:
                if parameter_list[1][0] == "#":
                    birinci = convert_to_int(parameter_list[1][1:])
                    if birinci is None and parameter_list[1][1:] in labels.keys():
                        birinci = labels[parameter_list[1][1:]]
                    
            
            if parameter_list[2] in register_dict.keys():
                ikinci = register_dict[parameter_list[2]] 
            else:
                if parameter_list[2][0] == "#":
                    ikinci = convert_to_int(parameter_list[2][1:])
                    if ikinci is None and parameter_list[2][1:] in labels.keys():
                        ikinci = labels[parameter_list[2][1:]]
            print("biriinci ve ikinci :", birinci,ikinci)
            register_dict["flag_z"] = 1 if ikinci == birinci else 0
            register_dict['flag_n'] = 1 if ikinci-birinci<0 else 0

            
        elif parameter_list[0] == 'add':
            if parameter_list[1] in register_dict.keys():
                operand1 = register_dict[parameter_list[1]]
            else:
                if parameter_list[1][0] == "#":
                    operand1 = int(parameter_list[1][1:])
            if parameter_list[2] in register_dict.keys():
                register_dict[parameter_list[2]] += operand1
                register_dict['flag_z'] = 1 if register_dict[parameter_list[2]] == 0 else 0  
                register_dict['flag_n'] = 1 if register_dict[parameter_list[2]]<0 else 0

        elif parameter_list[0] == 'bis' or  parameter_list[0] == 'bis.b' :
            if parameter_list[1] in register_dict.keys():
                operand1 = register_dict[parameter_list[1]]
            else:
                if parameter_list[1][0] == "#":
                    operand1 = convert_to_int(parameter_list[1][1:])
            if parameter_list[2] in register_dict.keys():
                register_dict[parameter_list[2]] |= operand1
                register_dict['flag_z'] = 1 if register_dict[parameter_list[2]] == 0 else 0  
                register_dict['flag_n'] = 1 if register_dict[parameter_list[2]]<0 else 0
        elif parameter_list[0] == 'and' or  parameter_list[0] == 'and.b' :
            if parameter_list[1] in register_dict.keys():
                operand1 = register_dict[parameter_list[1]]
            else:
                if parameter_list[1][0] == "#":
                    operand1 = convert_to_int(parameter_list[1][1:])
            if parameter_list[2] in register_dict.keys():
                register_dict[parameter_list[2]] &= operand1
                register_dict['flag_z'] = 1 if register_dict[parameter_list[2]] == 0 else 0  
                register_dict['flag_n'] = 1 if register_dict[parameter_list[2]]<0 else 0
        
        elif parameter_list[0] == 'xor' or  parameter_list[0] == 'xor.b' :
            if parameter_list[1] in register_dict.keys():
                operand1 = register_dict[parameter_list[1]]
            else:
                if parameter_list[1][0] == "#":
                    operand1 = convert_to_int(parameter_list[1][1:])
            if parameter_list[2] in register_dict.keys():
                register_dict[parameter_list[2]] ^= operand1
                register_dict['flag_z'] = 1 if register_dict[parameter_list[2]] == 0 else 0  
                register_dict['flag_n'] = 1 if register_dict[parameter_list[2]]<0 else 0
            
        elif parameter_list[0] == 'sub':
            if parameter_list[1] in register_dict.keys():
                operand1 = register_dict[parameter_list[1]]
            else:
                if parameter_list[1][0] == "#":
                    operand1 = int(parameter_list[1][1:])
            if parameter_list[2] in register_dict.keys():
                register_dict[parameter_list[2]] -= operand1
                register_dict['flag_z'] = 1 if register_dict[parameter_list[2]] == 0 else 0  
                register_dict['flag_n'] = 1 if register_dict[parameter_list[2]]<0 else 0

        elif parameter_list[0] == 'call':
            if parameter_list[1][0] == '#':
                if parameter_list[1][1:] in labels.keys():
                    stack.append(register_dict['pc'])
                    register_dict['pc'] = labels[parameter_list[1][1:]]

        elif parameter_list[0] == 'ret':
            register_dict['pc'] = stack.pop()
        
        elif parameter_list[0] == 'push':
            if parameter_list[1] in register_dict.keys():
                value = register_dict[parameter_list[1]]
            elif parameter_list[1][0] == "#":
                value = int(parameter_list[1][1:])

            stack.append(value)
        
        elif parameter_list[0] == 'pop':
            if parameter_list[1] in register_dict.keys():
                register_dict[parameter_list[1]] = stack.pop()
           
        elif parameter_list[0] == '.byte':
            pass
        
        elif parameter_list[0] == 'xxx':
            pass
        else:
            return False,f"Failed! cannot execute this op {parameter_list[0]}"
    else:
        if len(parameter_list)>1:
            return execute(parameter_list[1:],register_dict,stack,memory)






def find_labels(code_lines,memory:list):
    for operation_addres in range(len(code_lines)):
        parameter_list = code_lines[operation_addres].line_text
        if parameter_list[0] not in instruction_set:
            if len(parameter_list) > 1 and parameter_list[1] == '.byte':
                labels[parameter_list[0]] = len(memory)
                for i in range(len(parameter_list)-2):
                    memory.append(convert_to_int(parameter_list[i+2])%256)
                labels[code_lines[operation_addres+1][0]] = len(memory)
                return "last_element"
                
            elif len(parameter_list) > 1 and parameter_list[1] == '.bss':
                labels[parameter_list[2]] = len(memory)
                for i in range(int(parameter_list[3])):
                    memory.append(0)
                
            else:
                labels[parameter_list[0]] = operation_addres




        


def convert_to_int(number:str):
    try:
        if number[-1] == 'h':
            return int(number[:-1],16)
        if number[-1] == 'b':
            return int(number[:-1],2)
        if number[-1] == 'd':
            return int(number[:-1])
        else:
            return int(number)
    except:
        return None
    
