import sys
sys.stdin = open("0012.inp","r")
sys.stdout = open("0012.out","w")
s = input()
s1 = s[::-1]
d = 0 
for i in range(0,len(s)):
    if s[i]==s1[i]:
        d+=1
if d == 0:
    print("No") 
else:
    print("Yes")