import sys
sys.stdin = open("0022.inp","r")
sys.stdout = open("0022.out","w")

a,b,c = map(int,input().split())
TBC=(a+b+c)/3
print("%0.1f"%TBC)