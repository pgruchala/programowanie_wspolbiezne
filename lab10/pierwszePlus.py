import time
import math

l=1000000
r=2000000

def pierwsza(k):
 for i in range (2,k-1):
   if i*i>k:
     return True
   if k%i == 0:
     return False
 return True


def pierwsza1(k,mlp):
 for p in mlp:
   if k%p == 0:
     return False
   if p*p>k:
     return True
 return True


def licz(l,r):
  mlp = []
  s = math.ceil(math.sqrt(r))
  for i in range (2,s+1):
    if pierwsza(i):
       mlp.append(i)
  pierwsze = []
  for i in range (l,r+1):
    if pierwsza1(i,mlp):
       pierwsze.append(i)
  return pierwsze


if __name__ == '__main__':
    print(l,r)
    start = time.time()
    licz(l,r)
    print( time.time()-start)
