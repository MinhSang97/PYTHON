import sys
sys.stdin = open("0239.inp","r")
sys.stdout = open("0239.out","w")

def ktnt(n):
    i = 2
    while (i*i <=n) and (n%i!=0):
        i += 1
    return (i*i >n) and ( n>1)

def tong(n):
    s = str(n)
    k = 0 
    for i in s:
        k+=int(i)
    return k
n = int(input())
a = []
b = []
c = []
d = 0

for i in range(1,n):
    if ktnt(i)== True:
        d = 1
        a.append(i)
if d==0:
    print("-")
else:
    for i in range(0,len(a)):
        b.append(tong(a[i]))
    M = max(b)
    for i in range(0,len(b)):
        if b[i]==M:
            c.append(a[i])
    c = str(c)
    print(c)
    for i in range(0,len(c)):
        print(c[i],end=" ")