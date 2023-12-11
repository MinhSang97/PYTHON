import sys,math
sys.stdin = open("0016.inp","r")
sys.stdout = open("0016.out","w")
def ktcp(n):
    if n<0:
        return False
    x = int(math.sqrt(n))
    return(x*x == n)

a = list(map(int,input().split()))
d = 0
t = 0
for i in range(0,len(a)):
    if ktcp(a[i]) == True:
        d+=1
        t+=a[i]
if d == 0:
    print("-")
else:
    tbc = t/d
    print("%0.1f"%tbc)