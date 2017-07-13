# coding: utf-8
# Distributed under the terms of the MIT license.
import os
import json

import numpy as np
# import spglib

# from ababe.stru.element import Specie

# Loads bucky-ball structure data from json file
with open(os.path.join(os.path.dirname(__file__),
                            "buckyball.json"), "rt") as f:
    _buckyball = json.load(f)

# Loads buckyball's permutation table from .npy
_perm_table = np.load(os.path.join(os.path.dirname(__file__),
                                    "bucky_permu_table.npy"))
PERM = _perm_table

OR_ARR = np.array([2**i for i in range(60)])
#if '__builtin__' not in dir() or not hasattr(__builtin__, 'profile'): 
#    def profile(func):
#        def inner(*args, **kwargs): 
#            return func(*args, **kwargs)
#        return inner

def bucky_decode(int_seq):
    """
    This decode an int into a np.array 0,1 sequence.
    ex 43 -> array([0,0,0...,1,0,1,0,1,1])
    """
    #return np.array([i for i in bin(int_seq)[2:].zfill(60)], dtype=np.uint8)
    new_arr = np.unpackbits(np.array([int_seq], dtype='>i8').view(np.uint8))
    return new_arr[4:]
#@profile
def bucky_code(arr_seq):
    """
    This code an array of 01 sequence into an int.
    ex np.array([1]*60) -> 2**60-1
    """
    out = 0
    for bit in arr_seq.tolist():
            out = (out << 1) | bit
    return out

def bucky_code_arr(arr):
    c = 2**np.arange(arr.shape[1])[::-1]
    return arr.dot(c)


#@profile
def add_speckle_int(int_seq):
    """
    This convert an int to an array of its add_one_speckle sequence
    ??? May add unique to use less memory with performance down?
    """
    dup_add_one = np.bitwise_or(OR_ARR, int_seq)
    index = np.argwhere(dup_add_one==int_seq)
    out = np.delete(dup_add_one, index)
    return out

#@profile
def add_speckle_all(arr):
    dual_dup =  np.array([add_speckle_int(i) for i in arr])
    return np.unique(dual_dup)

#@profile
def int_to_id_int(int_seq):
    arr = bucky_decode(int_seq)
    new_arr = np.array([arr[ind] for ind in PERM])
    ## perm_arr_int = np.array([bucky_code(arr[ind]) for ind in PERM])
    #perm_arr_int = np.array([bucky_code(i) for i in new_arr])
    #id_int = np.amin(perm_arr_int)
    #return id_int
    #c = 2**np.arange(new_arr.shape[1])[::-1]
    #return np.amin(new_arr.dot(c))
    return np.amin(bucky_code_arr(new_arr))

i2i_fun = np.frompyfunc(int_to_id_int, 1, 1)
vec_i2i = np.vectorize(int_to_id_int)
def nodup_int_arr(dup_int_arr):
    arr = i2i_fun(dup_int_arr)
    return np.unique(arr)

def nodup_ini_arr_new(dup_int_arr):
    dup_mat = np.array([bucky_decode(i) for i in dup_int_arr])
    # perm act at structures once
    all_perm_stru = np.array([dup_mat.T[perm].T for perm in PERM])
    last_code_strus = np.array([bucky_code_arr(arr) for arr in all_perm_stru])
    return np.unique(np.amin(last_code_strus, axis=0))
