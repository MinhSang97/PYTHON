import sys
sys.stdin = open("0004.inp","r")
sys.stdout = open("0004.out","w")

s = input().split()
s1 = s[::-1]
print(s1[0])