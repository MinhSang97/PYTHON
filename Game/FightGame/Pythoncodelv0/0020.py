import sys
sys.stdin = open("0020.inp","r")
sys.stdout = open("0020.out","w")
n = int(input())
s = list(map(int,input().split()))
a = []
d = []
for i in range(0,len(s)):
    if s[i]<0:
        a.append(s[i])
    elif s[i]>0:
        d.append(s[i])
print(len(d),len(a))
print(*d)
print(*a)