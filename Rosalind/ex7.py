with open("input.txt", "r") as f:
    s = f.readline()
s = s.split()

d = {word: 0 for word in "ACGT"}  #assign 0 to keys that are the words
for word in s:
    if word in d:
        d[word] += 1

for letter in "ACGT":
    print(d[letter], end=' ')