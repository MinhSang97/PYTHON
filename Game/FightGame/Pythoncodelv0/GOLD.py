import sys,re
sys.stdin = open("GOLD.inp","r")
sys.stdout = open("GOLD.out","w")

s = input()
n = "1234567890"
s1 = ""
t = 0
for i in range(0,len(s)):
    if s[i] in n:
        s1+=s[i]
    else:
        s1+=" "
s1 = s1.split()
for i in range(0,len(s1)):
    t+=int(s1[i])
print(t)