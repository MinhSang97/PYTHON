import sys
sys.stdin = open("BAI4_9.inp","r")
sys.stdout = open("BAI4_9.out","w")
s = input()
s1 = ""
d = 0
i = 0
while i<len(s):
    s2 = s1[::-1]
    i+=1
    if s1 == s2:
        d+=1
        s1 = ""
    
    else:
        s1+=s[i]

print(d)