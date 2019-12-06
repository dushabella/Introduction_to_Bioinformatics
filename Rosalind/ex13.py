import itertools as it

# define size of k-mers
k = 4

# read DNA string from input file
dna = str()
with open("input.txt", "r") as file:
    for line in file:
        if line.startswith(">"):
            continue
        else:
            dna += line[:-1]

# devide DNA string for k-mers
kmers_in_dna = [dna[i:i+k] for i in range(len(dna)-1)]

# define all possible k-mers
kmers = [''.join(x) for x in it.product('ACGT', repeat = 4)]

# count and print it in a table
for kmer in kmers:
    counted_kmers = kmers_in_dna.count(kmer)
    print(counted_kmers, end=" ")