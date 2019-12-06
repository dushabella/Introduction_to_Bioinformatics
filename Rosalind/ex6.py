with open("input.txt", "r") as f:
    s = f.readline()
s = s.split()

# # method 1
# d={}
# for word in s:
#     d[word] = d.get(word, 0) + 1
# print(d)

# method 2
d = {word: 0 for word in s}  #assign 0 to keys that are the words
for word in s:
    if word in d:
        d[word] += 1
print(d)

for key, value in d.items():
    print(key, value)


# print(f'asdgh {key}')
# qwee = {key: value for key, value in asd.items()} #copy of string
