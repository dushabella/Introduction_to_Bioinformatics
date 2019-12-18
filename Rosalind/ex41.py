from typing import Dict, List

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

def find_subpalindroms(palindrom: str) -> List[int]:
    """search if subpalindroms exist in palindroms and return its' length"""
    res = list()
    palindrom_len = len(palindrom)
    for i in range(palindrom_len):
        temp_str = palindrom[:palindrom_len-i-1]
        if temp_str == reverse_dna(temp_str) and len(temp_str) in range(4, 13):
            lngth = len(temp_str)
            res.append(lngth)
    return res

def find_palindrome(dna: str) -> Dict[int, List[int]]:
    palindroms = dict()
    dna_len = len(dna)
    for pos, nucleotyde in enumerate(dna):
        for i in range(dna_len - pos + 1):
            temp_str = dna[pos:pos+i]
            temp_rev_str = reverse_dna(temp_str)
            if temp_str == temp_rev_str and len(temp_str) in range(4, 13):
                palindroms[pos + 1] = [len(temp_str)]
                subpalindroms = find_subpalindroms(temp_str)
                for i in range(len(subpalindroms)):
                    palindroms[pos + 1].append(subpalindroms[i])
    return(palindroms)

palindroms = find_palindrome(dna)

for key, value in palindroms.items():
        for i in range(len(value)-1, -1, -1):
            print(key, end=" ")
            print(palindroms[key][i])