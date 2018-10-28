#! /bin/env python
import os
nbins=20
theta=[(.14+i*2.86/nbins,.14+(i+1)*2.86/nbins) for i in range(nbins)]

for n,t in theta:
    os.system("python letsroll.py {0} {1} &".format(n,t))
