from typing import Dict

dna = str()
with open("input.txt", "r") as file:
    for line in file:
        if line.startswith(">"):
            continue
        else:
            dna += line[:-1]

def reverse_dna(dna: str) ->str:
    res = dna[::-1]
    res = res.replace("A", "t").replace("T", "a").replace("G", "c").replace("C", "g").upper()
    return(res)

def find_palindrome(dna: str) -> Dict[int, int]:
    palindroms = dict()
    dna_len = len(dna)
    for pos, nucleotyde in enumerate(dna):
        for i in range(dna_len - pos + 1):
            temp_str = dna[pos:pos+i]
            temp_rev_str = reverse_dna(temp_str)
            if temp_str == temp_rev_str and len(temp_str) in range(4, 12):
                palindroms[pos + 1] = len(temp_str)
    return(palindroms)

palindroms = find_palindrome(dna)

for key, value in palindroms.items():
    print (key, value)