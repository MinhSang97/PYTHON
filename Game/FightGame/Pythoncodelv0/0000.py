import sys
sys.stdin = open("0000.inp","r")
sys.stdout = open("0000.out","w")
t,m = map(int,input().split())
a,b = t,m
while a!=b:
    if a>b:
        a=a-b
    else:
        b =b-a
t /=a
m/=a
print(int(t),"/",int(m),sep="")