from typing import Set, List

dna = str()
with open("input.txt", "r") as file:
    for line in file:
        if line.startswith(">"):
            continue
        else:
            dna += line[:-1]
print(dna)

# set of prefixes ending at k-1
# prefixes = [1, l] where l = <1, k-1>
def find_prefixes(sequence: str, k:int) -> Set[str]:
    prefixes = [sequence[:x] for x in range(k+1)]
    prefixes = set(prefixes)
    return prefixes

# set of suffixes ending at k
# suffixes = [j, k] where j = <2, k>
def find_suffixes(sequence: str, k:int) -> Set[str]:
    suffixes = [sequence[x+1:k+1] for x in range(k+2)]
    suffixes = set(suffixes)
    return suffixes

#TODO: ask Piotrek how to run functions in a pretty way
# - I mean how to run failure_array which is "main" function

def failure_array(sequence: str, k:int) -> List[int]:
    for i in range(k):
        prefixes = find_prefixes(sequence, i)
        suffixes = find_suffixes(sequence, i)
        intersected = prefixes.intersection(suffixes)
        longest = max(intersected, key=len)
        len_of_longest = len(longest)
        print(len_of_longest, end=" ")

failure_array(dna, len(dna))