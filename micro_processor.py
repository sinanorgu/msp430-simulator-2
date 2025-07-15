

stack = []
memory = []

registers = {}

registers['r1'] = 0
registers['r2'] = 0
registers['r3'] = 0
registers['r4'] = 0
registers['r5'] = 0
registers['r6'] = 0
registers['r7'] = 0
registers['r8'] = 0
registers['r9'] = 0
registers['r10'] = 0
registers['r11'] = 0
registers['r12'] = 0
registers['r14'] = 0
registers['r15'] = 0

registers['pc'] = 0
registers['&p2in'] = 0
registers['&p1in'] = 0
registers['&p1dir'] = 0
registers['&p2dir'] = 0
registers['&p1out'] = 0
registers['&p2out'] = 0




registers["flag_z"] = 0
registers["flag_n"] = 0

def reset():
    global stack,memory,registers
    stack = []
    memory = []

    registers['r1'] = 0
    registers['r2'] = 0
    registers['r3'] = 0
    registers['r4'] = 0
    registers['r5'] = 0
    registers['r6'] = 0
    registers['r7'] = 0
    registers['r8'] = 0
    registers['r9'] = 0
    registers['r10'] = 0
    registers['r11'] = 0
    registers['r12'] = 0
    registers['r14'] = 0
    registers['r15'] = 0

    registers['pc'] = 0
    registers['&p2in'] = 0
    registers['&p1in'] = 0
    registers['&p1dir'] = 0
    registers['&p2dir'] = 0
    registers['&p1out'] = 0
    registers['&p2out'] = 0




    registers["flag_z"] = 0
    registers["flag_n"] = 0