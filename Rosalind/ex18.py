from typing import List

dna = str()
with open("input.txt", "r") as file:
    for line in file:
        if line.startswith(">"):
            continue
        else:
            dna += line[:-1]

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
    return codons

def find_orfs(sequence: List[str]) -> List[List[str]]:
    orfs = []
    for position, codon in enumerate(sequence):
        if codon == 'ATG':
            possible_orf = [codon]
            add = 0
            for orf_codon in sequence[position+1 :]:
                possible_orf.append(orf_codon)
                if orf_codon in ['TAA', 'TAG', 'TGA']:
                    add = 1
                    break
            if add == 1:
                orfs.append(possible_orf)
    return(orfs)

def replace_t_with_u(orf: List) -> List:
    orf = [nucleotyde.replace('T', 'U') for nucleotyde in orf]
    return orf

# generate the second part of genome
reverted_dna = revert_genome(dna)

# divide a whole gemone into parts
codons = distinguish_codons(dna)
codons += distinguish_codons(reverted_dna)

# generate all possible orf sequences
orfs = []
for i in range(6):
    orfs += find_orfs(codons[i])

# put all possible orf sequences into one list of lists
# replace T with U in orf chain
protein_candidates = []
protein_candidate = ""
for orf_sequence in orfs:
    orf_sequence = replace_t_with_u(orf_sequence)
    for codon in orf_sequence:
        protein_candidate += rna_codon_table[codon]
    if protein_candidate not in protein_candidates:
        protein_candidates.append(protein_candidate)
    protein_candidate = ""

for word in protein_candidates:
    print(word)