import sys
sys.stdin = open("0217.inp","r")
sys.stdout = open("0217.out","w")

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
a = list(map(int,input().split()))
for  i in range(0,len(a)):
    k = tong(a[i])
    if ktnt(k)==True:
        print(a[i],end=" ")
        d = 1
if d==0:
    print("-")
else:
    for  i in range(0,len(a)):
        t = tong(a[i])
    if ktnt(t)==True:
        print(a[i],end=" ")

