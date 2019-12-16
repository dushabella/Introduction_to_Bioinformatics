from typing import List

with open('input.txt', 'r') as file:
    lines = file.readlines()

strings = []
temp = []
for line in lines:
    if line.startswith('>'):
        temp = ''.join(temp)
        strings.append(temp)
        temp = []
        continue
    else:
        temp.append(line[:-1])
temp = ''.join(temp)
strings.append(temp)
strings.remove('')

dna = strings[0]
strings.remove(dna)
introns = strings

rna_codon_table = {
    'UUU': 'F',     'CUU': 'L',     'AUU': 'I',     'GUU': 'V',
    'UUC': 'F',     'CUC': 'L',     'AUC': 'I',     'GUC': 'V',
    'UUA': 'L',     'CUA': 'L',     'AUA': 'I',     'GUA': 'V',
    'UUG': 'L',     'CUG': 'L',     'AUG': 'M',     'GUG': 'V',
    'UCU': 'S',     'CCU': 'P',     'ACU': 'T',     'GCU': 'A',
    'UCC': 'S',     'CCC': 'P',     'ACC': 'T',     'GCC': 'A',
    'UCA': 'S',     'CCA': 'P',     'ACA': 'T',     'GCA': 'A',
    'UCG': 'S',     'CCG': 'P',     'ACG': 'T',     'GCG': 'A',
    'UAU': 'Y',     'CAU': 'H',     'AAU': 'N',     'GAU': 'D',
    'UAC': 'Y',     'CAC': 'H',     'AAC': 'N',     'GAC': 'D',
    'UAA': '',      'CAA': 'Q',     'AAA': 'K',     'GAA': 'E',
    'UAG': '',      'CAG': 'Q',     'AAG': 'K',     'GAG': 'E',
    'UGU': 'C',     'CGU': 'R',     'AGU': 'S',     'GGU': 'G',
    'UGC': 'C',     'CGC': 'R',     'AGC': 'S',     'GGC': 'G',
    'UGA': '',      'CGA': 'R',     'AGA': 'R',     'GGA': 'G',
    'UGG': 'W',     'CGG': 'R',     'AGG': 'R',     'GGG': 'G'
}

def remove_introns(sequence: str, introns: List[str]) -> str:
    """ Removes the introns from codon string
        An intron is a contiguous interval of a gene that is thrown out
        during RNA splicing and does not belong to the resulting molecule
        of mRNA that is translated into protein. """
    for intron in introns:
        if intron in sequence:
            sequence = sequence.replace(intron, '')
    return(sequence)

rna = remove_introns(dna, introns)

rna = rna.replace('T', 'U')

# divide rna chain for codons
codons = [rna[i:i+3] for i in range(0, len(rna)-1, 3)]

for codon in codons:
    print(rna_codon_table[codon], end="")