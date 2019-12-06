with open("input.txt", "r") as file:
    lines = file.readlines()

s1 = lines[0] #  string
s2 = lines[1] # substring

len_s1 = len(s1)
len_s2 = len(s2)

# divide s1 string for substring of length(s2)
substrings = [s1[i:i+len_s2] for i in range(len_s1-len_s2-1)]

for i in range( len(substrings) ):
    if substrings[i] == s2:
        print(i+1, end=" ")