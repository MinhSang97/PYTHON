import sys
from fractions import Fraction

sys.stdin = open("0013.inp","r")
sys.stdout = open("0013.out","w")

# def hons(n):
#     s = str(int(Fraction(n)))
#     t = s[0]
#     m = s[2]
#     hon = int(t)%int(m)
#     return (hon,",",hon,m)
a,b = map(int,input().split())
c,d = map(int,input().split())

cong = (a/b)+(c/d)
tru = (a/b)- (c/d)
nhan = (a/b) * (c/d)
chia = (a/b) * (d/c)
kq =[]
#Cộng

print(Fraction(1.35))
    
    
