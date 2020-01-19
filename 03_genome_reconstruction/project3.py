"""
Mini project #3:
---------------
A project is focused on finding the minimum length k of k-mers for which it is possible to obtain unique cyclic genome.
It bases on constructing de Bruijn graph with k-mers on a nodes, which indeed is a solution of Eulerian path problem.

Good source of knowledge:
http://www.bioinformatika.matf.bg.ac.rs/predavanja/literatura/Phillip%20Compeau,%20Pavel%20Pevzner%20-%20Bioinformatics%20Algorithms_%20An%20Active%20Learning%20Approach.%201-Active%20Learning%20Publ.%20(2015).pdf
[pages 121-138]
"""

from typing import Dict, List, Set, Tuple
from sys import getrecursionlimit, setrecursionlimit


def read_file(path: str) -> Dict:
    """ Reading genes from a file into a dictionary
    in which keys represent a genome name,
    and a values - the genomes. """
    genomes = dict()
    dict_hlpr = ""
    with open(path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                dict_hlpr = line[2:-1]
                # print(dict_hlpr)
            else:
                genomes[dict_hlpr] = line[:-1]
                # print(line[:-1])

    return(genomes)


def composition(genomes: str, k_len: int) -> List[str]:
    """
    Takes a circular genes and divide it for all possible k-mers (fragments) of a size of "k-mer" parameter
    and returns a list of k-mers that "wrap around" the end.
    For example:
        in: composition(“ATACGGTC”, 3)
        out: [“ATA”, “TAC”, “ACG”, “CGG”, “GGT”, “GTC”, “TCA”, “CAT”]
    :param gene: gene for reconstruction
    :param k_len: size of each divided kmer (fragment)
    :return fragments: list of kmers """

    fragments = list()
    length = len(genomes)

    hlpr = ""
    for i in range(length):
        hlpr = genomes[i : i+k_len]
        len2 = len(hlpr)
        if len2 < k_len:
            hlpr = hlpr + genomes[: k_len-len2]
        fragments.append(hlpr)

    return(fragments)


def simple_reconstruction(kmers: List[str]) ->str: #->List[str]:
    """
    Reconstruction of a circular genome of k-mers
    For example:
        circular string assembled from the cycle "AC" -> "CT" -> "TA" is simply (ACT)
    :param kmers: A list of mers
    :return result: circular string """

    result = ""
    i = 0
    for kmer in kmers:
        result += kmer[-1]
        i += 1

    return(result)


def assembly(kmers: List[str], assembled: List[str], found_genomes: Set[str]) -> Set[str]:
    """
    Recursive function for genome assembly using k-mers as edges of de Bruijn graph and prefixes/suffixes as nodes.
    It solves Eulerian path problem in effect.

    :param kmers: list of k-mers of genome sequence
    :param assembled: [RECURSION PARAM] put empty list here
    :param found_genomes: [RECURSION PARAM] put empty set here

    :return found_genomes: genomes that might be constructed from given fragments. """

    if len(kmers) == 0:  # end
        new_genome = simple_reconstruction(assembled)
        found_genomes.add(new_genome)

        return found_genomes

    elif len(assembled) == 0:  # begin
        assembled.append(kmers[0])
        found_genomes = assembly(kmers[1:], assembled, found_genomes)
    else:
        possible_to_join_id = [i for i, mer in enumerate(kmers) if mer[:-1] == assembled[-1][1:]] # if suffix == prefix
        for index in possible_to_join_id:
            assembled.append(kmers[index])
            found_genomes = assembly(kmers[:index] + kmers[index+1:], assembled, found_genomes)
            del assembled[-1]

    return found_genomes


def is_same_as_original(original: str, assembled: str) -> bool:
    """
    Checks if achieved genome assembly is same as original genome.

    :param original:
    :param created:

    :return the_same: True - identical or identical but shifted """
    concatenated = assembled + assembled
    the_same = original in concatenated
    return the_same


def remove_redundant(found_genomes: Set[str]) -> List[str]:
    """
    Removes redundant found_genomes genomes (like 'CTGACATA' and 'CATACTGA')

    :param found_genomes:

    :return result: list with unique found_genomes genome """
    found_genomes = list(found_genomes)
    i = 0
    while i < len(found_genomes):
        if any([is_same_as_original(found_genomes[i], found_genomes[k]) for k in range(len(found_genomes)) if i != k]):
            del found_genomes[i]
        else:
            i += 1
    return found_genomes


def find_min_k(genome: str, k: int=30) -> str:
    """
    Returns minimum k found for building k-mers that will achieve only one unique and correct genome from genome assembly
    operation.
    Starts from high value of k because the recursive assembly function is getting slow for low k.

    :param genome: input genom that is first decomposed for k-mers
    :param k: k-mer length from which the searching algorithm starts
    :return min_k: minimum found k """

    while k > 5:
        comp = composition(genome, k)
        created = assembly(comp, list(), set())
        created = remove_redundant(created)
        if len(created) > 1:
            return k+1
        last = created[0]
        k -= 1
    return k+1


def main():
    setrecursionlimit(getrecursionlimit()*2)

    genomes = read_file("genomes.txt")
    for key in genomes:
        print("____________________________________")
        print("Name:", key)
        genome = genomes[key]
        print("genome:", genome)
        min_k = find_min_k(genome)
        print("min k: ", min_k)


if __name__ == "__main__":
    main()