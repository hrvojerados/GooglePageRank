#!/usr/bin/python3

import numpy as np
import pickle
from copy import deepcopy

H_PATH = "H_matrix_vikidia.npy"
PI_PATH = "pi"
TRAZI = None
# TRAZI = "cat"
# TRAZI = "cat"

# isti kod kao u jupiter notebooku, samo popravljen
def get_H_11_and_H_12(H):
    k = -1
    for i in range(len(H)):
        if not H[i, :].any():
            k = i
            break

    if k == -1:
        return "Error"
    
    H_11 = H[0:k, 0:k]

    H_12 = H[0:k, k:] # pogledati problem u main.ipynb
    
    return H_11, H_12

def pagerank(H, v, w, a, conv = 0.01):
    H_11, H_12 = get_H_11_and_H_12(H)
    k = len(H_11)
    
    w_1_T = w[:k].transpose()
    w_2_T = w[k:].transpose()

    v_1_T = v[:k].transpose()
    v_2_T = v[k:].transpose()
    
    sigma = np.random.rand(k+1)
    sigma = sigma / sum(sigma)
    sigma_T = sigma.transpose()
    
    e = np.ones(k)
    
    err = float("inf")
    while err > conv:
        sigma_T_ = deepcopy(sigma_T)
        sigma_T_[:k] = a * sigma_T[:k] @ H_11 + (1 - a) * v_1_T + a * sigma_T[k] * w_1_T
        sigma_T_[k] = 1 - sigma_T_[:k] @ e
        err = sum(abs(sigma_T_ - sigma_T))
        print(err)
        sigma_T = deepcopy(sigma_T_)

    return np.concatenate((sigma_T_[:k], a * sigma_T_[:k] @ H_12 + (1 - a) * v_2_T + a * sigma_T[k] * w_2_T), axis=None)

def main():
    H = np.load("H_matrix_vikidia.npy")
    print(H.shape)
    w = np.ones((len(H),1))
    w = w / sum(w)
    search_f = open("search.txt", "rb")
    search = pickle.load(search_f)
    print(search)

    if TRAZI is None:
        v = np.ones((len(H),1))
    else:
        v = np.zeros((len(H),1))
        kljucne_rijeci = TRAZI.split(" ")
        for kr in kljucne_rijeci:
            vect = search.get(kr)
            if vect is not None:
                for num in vect:
                    v[num] += 1
    v = v / sum(v)


    pi = pagerank(H, v, w, 0.5, 0.000001)
    print("vektor:", pi)
    np.save(arr=pi, file=PI_PATH)

    imena_f = open("numeration.txt", "rb")
    href_broj = pickle.load(imena_f)
    broj_href = {v: k for k, v in href_broj.items()}
    ranking = [(pi[i], broj_href[i]) for i in range(len(pi))]
    ranking.sort(reverse=True)

    cuttoff_top = 20
    cuttoff_bottom = 20
    for i in range(cuttoff_top):
        print(f"{ranking[i][0]:0.8f}", ranking[i][1])
    print("\t...\t")
    for i in range(len(ranking) - cuttoff_bottom, len(ranking)):
        print(f"{ranking[i][0]:0.8f}", ranking[i][1])

if __name__== "__main__":
    main()
