import sys
sys.stdin = open("USUM.inp","r")
sys.stdout = open("USUM.out","w")
def ktcp(n):
    i = 0
    while i*i<n:
        i+=1
    return i*i==n
def TongUoc(n):
    t = 0
    for i in range(1,n+1):
        if n%i==0:
            t+=i
    return t

n= int(input())
t = 0
for i in range(1,n+1):
    if n%i==0 and ktcp(i)==True:
        t+=TongUoc(i)
print(t)