import sys
sys.stdin = open("0001.inp","r")
sys.stdout = open("0001.out","w")

d,r = map(int,input().split())
for i in range(0,d):
    print("*",end="",sep="")
print()
for i in range(0,r-2):
    print("*"," "*(d-2),"*",sep="")
for i in range(0,d):
    print("*",end="",sep="")
