with open("input.txt", "r") as f:
    s = f.readline()

print(s)

# reverse the string
s = s[::-1]

# replace A with C and G with C of each other
s = s.replace("A", "t").replace("T", "a").replace("G", "c").replace("C", "g").upper()

print(s)