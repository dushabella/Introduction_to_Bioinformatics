import itertools as it

with open("input.txt", "r") as file:
    file_content = file.readlines()

# upload a set of the letters that defines alphabet
alphabet = str()
alphabet = file_content[0][:-1]
alphabet = alphabet.replace(" ", "")
print(alphabet)

# upload a size of a string
size = int()
size = int(file_content[1][:-1])
print(size)

# define all possible k-mers
kmers = [''.join(x) for x in it.product(alphabet, repeat = size)]

for kmer in kmers:
    print(kmer)