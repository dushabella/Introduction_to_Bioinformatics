DNA = dict()
current_DNA_hlpr = ""
with open("input.txt", "r") as file:
    for line in file:
        if line.startswith(">"):
            current_DNA_hlpr = line[1:-1]
            DNA[current_DNA_hlpr] = ""
        else:
            DNA[current_DNA_hlpr] += line[:-1]

print(DNA)

def calculate_gc_content_factor(dna: str) -> float:
    content_factor = ((dna.count("G") + dna.count("C")) / len(dna) * 100)
    return content_factor

# create a dictionary of GC content factors
GC_contents = {id: calculate_gc_content_factor(dna) for id, dna in DNA.items()}

# maximum content factor
best_one = max(GC_contents, key=GC_contents.get)
# print(best_one)
print(f"{best_one}\n{GC_contents[best_one]}")

