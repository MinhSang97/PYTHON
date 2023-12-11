import sys
sys.stdin = open("0005.inp","r")
sys.stdout = open("0005.out","w")

def ktnt(n):
    i = 2
    while (i*i <=n) and (n%i!=0):
        i += 1
    return (i*i >n) and ( n>1)

m,n = map(int,input().split())
dem=0
t = 0 

for i in range(m,n+1):
    if ktnt(i)==True:
        t+=i
        dem+=1

if dem==0:
    print("-")
else:
    tbc = t/dem
    print("%0.2f"%tbc)