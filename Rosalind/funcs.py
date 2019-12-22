import numpy as np

def viterbi(x, states, alphabet, emission, transition):

    De = {}

    for i in range(len(states)):
        de = {}
        for j in range(len(alphabet)):
            de.update({alphabet[j]:emission[i][j]})
        De.update({states[i]:de})

    Dt = {}

    for i in range(len(states)):
        dt = {}
        for j in range(len(states)):
            dt.update({states[j]:transition[i][j]})
        Dt.update({states[i]:dt})

    viterbi = np.zeros((len(x)+1, len(states)))

    start = 1

    for i in range(len(states)):
        viterbi[1][i] = De[states[i]][x[0]]*max(start*0.5,0)

    for i in range(2, len(x)+1):
        ch = x[i-1]

        first = []
        for j in range(len(states)):
            first.append(De[states[j]][ch])

        before = []
        for j in range(len(states)):
            before.append(viterbi[i-1][j])

        values = []
        for j in range(len(states)):
            for k in range(len(states)):
                values.append(before[k]*Dt[states[k]][states[j]])
            viterbi[i][j] = first[j]*max(values)
            values = []

    maxInd = 0
    for j in range(1,len(states)):
        if viterbi[-1][j] > viterbi[-1][maxInd]:
            maxInd = j

    res = states[maxInd]

    for i in range(1,len(viterbi)-1):
        thiscar = res[0]
        indMax = 0
        for j in range(1,len(states)):
            if viterbi[len(viterbi)-i-1][j]*Dt[states[j]][thiscar] > viterbi[len(viterbi)-i-1][indMax]*Dt[states[indMax]][thiscar]:
                indMax = j
        res = states[indMax] + res

    return res