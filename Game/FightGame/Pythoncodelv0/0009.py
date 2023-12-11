import sys
sys.stdin = open("0009.inp","r")
sys.stdout = open("0009.out","w")

def ktnt(n):
    i = 2
    while (i*i <=n) and (n%i!=0):
        i += 1
    return (i*i >n) and ( n>1)

k = int(input())
n=0
dem = 0
while k>dem:
    if ktnt(n)==True:    
        print(n,end=" ")
        dem+=1
    n+=1