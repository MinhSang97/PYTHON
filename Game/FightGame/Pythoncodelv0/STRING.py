import sys,re
sys.stdin = open("STRING.inp","r")
sys.stdout = open("STRING.out","w")

s = input()
s1 = re.sub("[^0-9] +"," ",s)
a = s1.split()
if len(a)==0:
    print(0)
else:
    M = max(a,key=len)
    print(len(M))
    print(M)
