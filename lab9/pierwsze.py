# wyszukanie liczb pierwszych z zakresu od l do r

def pierwsza(k):
# sprawdzenie, czy k jest pierwsza
 for i in range (2,k-1):
   if i*i>k:
     return True
   if k%i == 0:
     return False
 return True


def gen_pierwsza(start, end):
    pierwsze=[]
    for i in range(start,end+1):
        if pierwsza(i):
            pierwsze.append(i)
    return pierwsze


