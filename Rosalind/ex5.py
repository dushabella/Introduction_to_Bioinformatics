f = open('input.txt', 'r')
o = open('output.txt', 'w')
i = 1
for line in f.readlines():
    if i%2 == 0:
        o.write(line)
    i += 1
