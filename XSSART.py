# -*- coding: utf-8 -*-
"""
Created on Sat May  9 22:35:59 2020

@author: MHIT
"""

import numpy as np
from random import randrange
import requests 
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import concurrent.futures


f = np.load("xssart_features.npy")
d = np.load("sqli_dataset.npy")

def foo(f, d, p, name):
    k = 10
    
    def test_payload(payload):
        
        #print(payload)
        s = requests.Session()
        headers = requests.utils.default_headers()
        headers.update({'Cookie': "pid="+payload,})
        retries = Retry(total=25,
                        backoff_factor=0.5,
                        status_forcelist=[ 500, 502, 503, 504 ])
    
        s.mount('http://', HTTPAdapter(max_retries=retries))
        PARAMS = {'payload':'payload'}
        r = s.get(url = URL, params = PARAMS, headers=headers)
        if r.status_code == 200:
            return True
        else:
            return False
    
    URL = 'http://192.168.56.102'
    results = []
    for t in range(100):
        print(str(p) + ":" + "test number ", t)
        blocked = []
        # init data queue
        data = []
        def jaccard_similarity(x,y):
            intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
            union_cardinality = len(set.union(*[set(x), set(y)]))
            return intersection_cardinality/float(union_cardinality)
        def rank(feature):

            dl = 0.265
            dr = 0.515
            nblocked = np.asarray(blocked)
            nfeature = np.asarray(feature)
            rank = 0
            for b in nblocked:
                distance = jaccard_similarity(nfeature, b)
                if distance >= dl and distance <= dr:
                    rank += 1

            return rank
        
        for i, item in enumerate(d):
            data.append(item)
            
        # init data queue
        features = []
        for i, item in enumerate(f):
            features.append(item)
        candidates_d = []
        candidates_f = []
        while True:
            r = randrange(len(data) - k)
            for i in range(r, r + k):
                candidates_d.append(data.pop(r))
                candidates_f.append(features.pop(r))
            if len(blocked) == 0:
            #if True:
                r = randrange(k)
                test_case = candidates_d.pop(r)
                feature = candidates_f.pop(r)
            else:
                maximum = 0
                index = 0
                for i, item in enumerate(candidates_f):
                    md = rank(item)
                    #print(md)
                    if md > maximum:
                        maximum = md
                        index = i
                test_case = candidates_d.pop(index)
                feature = candidates_f.pop(index)
            for i, item in enumerate(candidates_f):
                data.append(candidates_d.pop(0))
                features.append(candidates_f.pop(0))
            #print(test_case)
            if test_payload(test_case):
                break
            blocked.append(feature)
            print(str(p) + ":" + str(t + 1) + ":" + str(len(blocked)))
        
        results.append(len(blocked))
        print(str(p) + ":" + str(t + 1) + ":" + str(len(blocked)))
        np.save(name +".npy", results)
    return results
    


with concurrent.futures.ThreadPoolExecutor() as executor:
    for i in range(0, 1):
        executor.submit(foo, f, d, i, "xssart_nx_cookie")

   
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        