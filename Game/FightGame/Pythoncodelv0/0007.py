import sys
sys.stdin = open("0007.inp","r")
sys.stdout = open("0007.out","w")

a,b,c = map(int,input().split())
print(min(a,b,c))