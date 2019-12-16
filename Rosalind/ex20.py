dnas = []
with open('input.txt', 'r') as file:
    for line in file:
        dnas.append(line[:-1])

def count_hamming_distance(str1: str, str2: str) -> int:
    i = 0
    hamming_distance = 0
    if len(str1) != len(str2):
        raise Exception('Compared strings must be the same length!')
    for position in str1:
        if position != str2[i]:
            hamming_distance += 1
        i += 1
    return(hamming_distance)

print(count_hamming_distance(dnas[0], dnas[1]))