"""
Mini project #3:
---------------

The project is focused on finding the minimum length k of k-mers for which it is possible to obtain unique cyclic genome.
Implementation of a whole method for constructing Hamiltionian cycle which recovers the genome wasn't necessary.

Good source of knowledge: https://www.youtube.com/watch?v=0JlUy_l-RTk&t=2s
"""

from typing import Dict, List, Tuple
from collections import defaultdict

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


def suffix_prefix(kmers: List[str]) ->Tuple[Dict, int]:
    """
    Returns a prefix and a suffix of each k-mer from the list.

    :param kmers: A list of error-free DNA k-mers taken from the strand of circular chromosome
    :return unique: 1 - assembled genome will be unique; 0 - ambiguous
    """

    # Quick result: at the end, check if the len(result) is the same as len(kmers)\
    # if yes - the circular genome won't be ambiguous (will be unique)

    kmer_len = len(kmers)
    unique = 0

    result = defaultdict(list)
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        result[suffix].append(prefix)
        # print("suffix:", suffix, "prefiks: ", result[suffix])
        # print("__________")
    result = dict(result)
    result_len = len(result)
    # print('\033[93m' + "dict[suffix] = prefix:" + '\033[0m', result)
    if kmer_len == result_len:
        print('\033[94m' + "The number of kmers and distinctive prefixes are the same, so circular gene will be unique!" + '\033[0m')
        unique = 1

    return(result, unique)


def is_unique(pref_suf: Dict) -> int:
    """
    Checks if the circular genome assembled with these mers will be unique.

    :param pref_suf: A dictionary that contains suffixes of kmers and prefixes which correspond them: pref_suf[suffix] = prefixes
    :return unique: 1 - assembled genome will be unique; 0 - ambiguous
    """

    unique = 1 # assembled genome will be unique

    # check if in lists of prefixes that correspond to each suffix are redundances \
    # if yes - leave only one of each prefix
    for key in pref_suf:
        prefixes = pref_suf[key]
        # print("Prefixes of the suffix", key, "are", prefixes)

        for prefix in prefixes:
            number = prefixes.count(prefix)
            if number > 1:
                prefixes.remove(prefix)
        pref_suf[key] = prefixes

    # check how many prefixes is in each list
    # if each list of prefixes still consist of more than one element - assembled genome will be ambiguous for sure
    for key in pref_suf:
        prefixes = pref_suf[key]
        if len(prefixes) > 1:
            unique = 0
            print('\033[91m' + "Suffix has more than one distinguishable prefix, so circular gene will be ambiguous!" + '\033[0m')
            break

    if unique == 1:
        print('\033[94m' + "Circular gene will be unique!" + '\033[0m')

    return(unique)

def simple_reconstruction(kmers: List[str]) ->str: #->List[str]:
    """
    Reconstruction of a circular string from a k-mers using de Bruijn graph.
    http://rosalind.info/problems/grep/

    For example:
        circular string assembled from the cycle "AC" -> "CT" -> "TA" -> "AC" is simply (ACT)
    :param kmers: A list of error-free DNA (k+1) mers taken from the strand of circular chromosome
    :return result: one of the circular strings assembled by complete cycles in the Bruijn graph. """

    result = ""
    i = 0
    for kmer in kmers:
        if i == 0:
            result = kmer
        elif i < len(kmers) - len(kmer) + 1:
            result += kmer[-1]
        i += 1

    # print(result)
    return(result)


def main():
    result = dict()

    genomes = read_file("genomes.txt")
    for key in genomes:
        print("____________________________________")
        print("Name:", key)
        genome = genomes[key]
        print("genome:", genome)

        result[key] = None

        for i in range(len(genome)):
            k = i+1
            kmers = composition(genome, k)
            simple_reconstruction(kmers)
            pref_suf, unique = suffix_prefix(kmers)
            if unique == 1:
                result[key] = k
                # reconstruction for checking
                break
            else:
                unique2 = is_unique(pref_suf)
                if unique2 == 1:
                    result[key] = k
                    break

    print(result)


if __name__ == "__main__":
    main()