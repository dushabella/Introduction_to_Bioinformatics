from typing import List

with open('input.txt', 'r') as file:
    dna = file.readline()[:-1]

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

def revert_genome(sequence: str) -> str:
    reverted = sequence[::-1]
    reverted = reverted.replace("G", "c").replace("C", "g").replace("A", "t").replace("T", "a").upper()
    return reverted

def distinguish_codons(sequence: str) -> List[List[str]]:
    codons = list()
    sequence_len = len(sequence)
    for j in range(3):
        codons.append([sequence[i+j:i+j+3] for i in range(0, sequence_len, 3)])
        if len(codons[j][-1]) < 3:
            del(codons[j][-1])
    print(codons)
    return codons

def find_orfs(sequence: List[str]) -> List[List[str]]:
    orfs = []
    for position, codon in enumerate(sequence):
        if codon == 'ATG':
            possible_orf = [codon]
            for orf_codon in sequence[position+1 :]:
                possible_orf.append(orf_codon)
                if orf_codon in ['TAA', 'TAG', 'TGA']:
                    break
            orfs.append(possible_orf)
    return(orfs)

def find_longest_orf(orfs: List[List[str]]) -> List[str]:
    maxOrf = max(orfs, key = len)
    return(maxOrf)

reverted_dna = revert_genome(dna)
codons = distinguish_codons(dna)
codons += distinguish_codons(reverted_dna)
print(type(codons))
print(codons)

# generate all possible orf sequences
orfs = []
for i in range(6):
    print(codons[i])
    orfs += find_orfs(codons[i])
print(orfs)

print("najdluzszy")
print(find_longest_orf(orfs))
