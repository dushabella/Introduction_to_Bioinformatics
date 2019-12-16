dnas = []
temp_str = ''
with open('input.txt', 'r') as file:
    for line in file:
        if line.startswith('>'):
            if temp_str != '':
                dnas.append(temp_str)
                temp_str = ''
        else:
            temp_str += line[:-1]
    dnas.append(temp_str)

def count_p_distance(str1: str, str2: str) -> float:
    i = 0
    diff = 0
    if len(str1) != len(str2):
        raise Exception('Compared strings must be the same length!')
    for position in str1:
        if position != str2[i]:
            diff += 1
        i += 1
    p_distance = diff / len(str1)
    return(p_distance)

num_of_chains = len(dnas)

# print D matrix
for i in range(num_of_chains):
    for j in range(num_of_chains):
        p_distance = count_p_distance(dnas[i], dnas[j])
        print(f'{p_distance:.5f}', end=' ')
    print()
