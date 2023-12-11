import sys
sys.stdin = open("0237.inp","r")
sys.stdout = open("0237.out","w")

def tong(n):
    s = str(n)
    k = 0 
    for i in s:
        k+=int(i)
    return k

a = int(input())
b = int(input())
d = 0 
for i in range(a,b+1):
    if tong(i)%2==0:
        d+=1
print(d)