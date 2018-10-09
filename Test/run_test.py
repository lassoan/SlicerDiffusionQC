#!/usr/bin/env python-real

import numpy as np
# import pandas as pd
import os, sys, tempfile
import nrrd

eps = 2.2204e-16

SCRIPTDIR= os.path.abspath(os.path.dirname(__file__))
REFDIR= os.path.join(SCRIPTDIR, 'Baseline')

# diffusionQC is added to python search directory
from diffusionqclib.gradient_process import process


def load_results(directory, prefix):

    # csv= pd.read_csv(os.path.join(directory, prefix+'_QC.csv'))
    csv = np.load(os.path.join(directory, prefix + '_QC.npy'))
    qc  = np.load(os.path.join(directory, prefix + '_QC.npy'))
    kl  = np.load(os.path.join(directory, prefix + '_KLdiv.npy'))
    con = np.load(os.path.join(directory, prefix + '_confidence.npy'))
    dwi = nrrd.read(os.path.join(directory, prefix+'_modified.nrrd'))[0]

    return (csv, qc, kl, con, dwi)


def main():
    import subprocess
    subprocess.check_call(['git', 'lfs', 'pull', '--exclude='], cwd=REFDIR, )

    cases= ['SiemensTrio-Syngo2004A-1']

    for case in cases:
        tmpdir = tempfile.mkdtemp()
        print(tmpdir)

        # run test case
        process(os.path.join(REFDIR, case+'.nrrd'), outDir=tmpdir) 


        # load reference results
        csv, qc, kl, con, dwi = load_results(REFDIR, case)
        # load obtained results
        csv_test, qc_test, kl_test, con_test, dwi_test = load_results(tmpdir, case)

        failed= 0
        # for attr in 'csv qc kl con dwi'.split(' '):
        for attr in 'csv qc kl con dwi'.split(' '):
            print(attr, ' test')
            if (eval(attr) - eval(attr+'_test')).sum()>eps:
                failed+=1
                print('{} : {} test failed'.format(case, attr))


    if not failed:
        print('All tests passed')


if __name__== '__main__':
    main()
