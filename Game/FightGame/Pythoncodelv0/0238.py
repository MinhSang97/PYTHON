import sys
sys.stdin = open("0238.inp","r")
sys.stdout = open("0238.out","w")

n = int(input())
s = input()
da = 0
db = 0
for i in s:
    if i == "A":
        da+=1
    if i == "B":
        db+=1
if da>db:
    print("A")
elif db>da:
    print("B")
else:
    print("Tie")