from typing import Dict
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
from Bio import pairwise2

def read_file(path: str) -> Dict:
    ''' Reading genes from a file into a dictionary
    in which the keys represent a gene type,
    and the values - the genes of particular species.

    There is 7 different species of each gene. '''

    with open(path, 'r') as file:
        genes = defaultdict(list)
        temp_gene_name = ""
        for i, line in enumerate(file):
            if (i + 1) % 8 == 1:
                temp_gene_name = line
            else:
                values = line.split("\t")
                genes[temp_gene_name].append(values)
    genes = dict(genes)

    return genes

def distance_matrices(genes: Dict) -> Dict: #Dict[List[List[int]]]
    gene_matrices = defaultdict(list)
    for key in genes:
        i=0
        mtrx = []
        for species in genes[key]:
            species_gene1 = species[-1]
            row = []
            for species in genes[key]:
                i+=1
                species_gene2 = species[-1]
                alignment = pairwise2.align.globalms(species_gene1, species_gene2, 1, -1, -2, -2)
                distance = count_distance(alignment[0][0], alignment[0][1])
                row.append(distance)
            mtrx.append(row)
            gene_matrices[key].append(row)

    gene_matrices = dict(gene_matrices)
    return gene_matrices


def count_distance(str1: str, str2: str) ->float:
    ''' Returns the distance between two strings,
    corrected according to Juke-Cantor model.
    http://readiab.org/book/0.1.3/2/4 '''

    res = 0

    # Hamming distance
    i = 0
    if len(str1) != len(str2):
        raise Exception('Compared strings must be the same length!')
    for position in str1:
        if position != str2[i]:
            res += 1
        i += 1

    # Jukes-Cantor correction
    res = res/len(str1)

    # Jukes-Cantor (JC69)
    a = 1 - 4/3 * res
    res = -3/4 * np.log(a)
    return res


def show_dendrograme(distance_matrices: dict) ->None:
    names = ["Bos taurus", "Mus musculus", "Homo sapiens", "Danio rerio", "Canis lupus familiaris", "Rattus norvegicus", "Macaca mulatta"]

    for key in distance_matrices:
        # print(distance_matrices[key])
        upgma = linkage(distance_matrices[key], 'average')
        fig = plt.figure(figsize=(13, 5))
        dn = dendrogram(upgma, above_threshold_color='#bcbddc', orientation='left', labels=names)
        ax = plt.gca()
        ax.tick_params(axis='y', which='major', labelsize=8)
        plt.title(key)
        plt.show()

def distinguishing_distance(distance_matrices: dict) ->Dict:
    ''' Returns the list of distances, which can be the indicator
    of distinguishing between the species.
    Each distance is a difference of the length of longest branch
    (which can have no common anchestor with the others)
    and the length of the second longest branch '''

    res = defaultdict(float)
    for key in distance_matrices:
        upgma = linkage(distance_matrices[key], 'average')
        difference = upgma[5][2] - upgma[4][2]
        res[key[:-1]] = difference

    res = dict(res)
    return res

def best_distinguishing_genes_rank(differences: dict) ->Dict:
    ''' Prints (and returns) the rank of the genes that shows which
    gene is the best to distinguishing between the species (mammals and fish) '''

    rank =  {k: v for k, v in sorted(differences.items(), key=lambda item: item[1], reverse=True)}
    # rank = sorted(differences.items(), key=lambda x: x[1], reverse=True) #list

    print("_______________________________________________________________________", "\n")
    print("Ranking of the genes' ability of distinguish betweeen mammals and fish")
    print("_______________________________________________________________________", "\n")
    i = 0
    for key in rank:
        i += 1
        print(i, end = "")
        print(")", end = " ")
        print(key, "\t", rank[key])

    return rank

genes = read_file('genes.txt')

distances = distance_matrices(genes)

distinguish_distances = distinguishing_distance(distances)

best_distinguishing_genes_rank(distinguish_distances)

show_dendrograme(distances)