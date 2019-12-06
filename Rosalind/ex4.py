a=4984
b=9352
r = b-a

set = []
for i in range(r):
    el = i+a+1
    if el%2 == 1:
        set.append(el)
        # print(el)

sum = sum(set)

print(set)
print(sum)