with open('input.txt', 'r') as file:
    lines = file.readlines()

proteins = []
protein_hlpr = []
for line in lines:
    if line.startswith('>'):
        protein_hlpr = ''.join(protein_hlpr)
        proteins.append(protein_hlpr)
        protein_hlpr = []
        continue
    else:
        protein_hlpr.append(line[:-1])
protein_hlpr = ''.join(protein_hlpr)
proteins.append(protein_hlpr)
proteins.remove('')

def edit_distance(a, b):
    """Return the Levenshtein edit distance between two strings *a* and *b*."""
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    if not a:
        return len(b)
    previous_row = range(len(b) + 1)
    for i, column1 in enumerate(a):
        current_row = [i + 1]
        for j, column2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (column1 != column2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

print(edit_distance(proteins[0], proteins[1]))