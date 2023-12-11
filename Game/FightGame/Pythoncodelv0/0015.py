import sys
sys.stdin = open("0015.inp","r")
sys.stdout = open("0015.out","w")
n = int(input())
if n%5==0:
    print("Yes")
else:
    print("No")