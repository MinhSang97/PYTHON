import sys
sys.stdin = open("0236.inp","r")
sys.stdout = open("0236.out","w")
def tong(n):
    s = str(n)
    k = 0 
    for i in s:
        k+=int(i)
    return k

def demnut(a):
    t = tong(a)
    while len(str(t)) != 1:
        t = str(tong(int(t)))
    return t
a = list(map(str,input().split()))
for i in range(0,len(a)):
    print(demnut(a[i]),end=" ")