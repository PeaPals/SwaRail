# # cook your dish here
# def gcd(a, b):
#     if (b == 0):
#          return a
#     return gcd(b, a%b)
    
    
# def lcm(a, b):
#     return (a / gcd(a, b)) * b
    

# def solve(ans, n):
#     pass



    
# for t in range(int(input())):
#     n - int(input())
#     arr = list(map(int, input().split(' ')))
    
#     ans = solve(arr, n)
#     print(ans)






from ursina import *

from ursina import EditorCamera

UI = Ursina()

point = [Vec3(i / 31, curve.in_out_sine(i / 31), 0) for i in range(32)]

model = Entity(
    model=Mesh(vertices=point, mode='line', thickness=4)
)

UI.run()