char = list(input())

for i in range(len(char)):
     print(chr(ord(char[i])-7),end="")