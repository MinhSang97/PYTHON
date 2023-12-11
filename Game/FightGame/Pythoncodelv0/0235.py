import sys
sys.stdin = open("0235.inp","r")
sys.stdout = open("0235.out","w")

def tong(n):
    s = str(n)
    t = 0 
    for i in s:
        t+=int(i)
    return t

n = input()
while len(n)!=1:
    n = str(tong(int(n)))
print(n)