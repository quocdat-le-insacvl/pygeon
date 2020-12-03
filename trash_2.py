buff = list()
STR = 10 
STR  DEX DEF 
(0 , 0 , 0 , 0 , 0 , 0)
# BUFF de 3 PENDANT 3 TOURS
buff.append((3,0,0,0,0))
buff.append(3)
buff.append(3)
# BUFF DE 2 PENDANT 1 TOURS
if buff[0] != None:
    buff[0] += 2

def passez_tour(buff,STR):
    if len(buff) ==0:
        return STR
    str_buff = STR + buff[0]
    buff.remove(buff[0])
    return str_buff

print(buff,STR) # TOUR 0
str_buff = passez_tour(buff,STR)
print(buff,str_buff) # TOUR 1
str_buff = passez_tour(buff,STR)
print(buff,str_buff) # TOUR 2
str_buff = passez_tour(buff,STR)
print(buff,str_buff) # TOUR 3
str_buff = passez_tour(buff,STR)
print(buff,str_buff) # TOUR 4
