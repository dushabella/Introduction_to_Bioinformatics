from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62

seqs = []
with open('input.txt', 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        seqs.append(record.seq)

s = seqs[0]
t = seqs[1]

alignments = pairwise2.align.globalds(s, t, blosum62, -11, -1)

print(round(alignments[0][2]))
print(alignments[0][0])
print(alignments[0][1])