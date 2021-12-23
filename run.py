#!/usr/bin/python3

import numpy as np
import json
import os 
import argparse
from astropy.io import fits
from ccdproc import process

def parse_args():
    """Parses command line arguments.

    Parameters:
        nothing

    Returns:
        args : argparse.Namespace object
            An argparse object containing all of the added arguments.

    Outputs:
        nothing
    """

    #Create help string:
    rpath_help = 'Path to rawfile.'
    # Add arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('--rpath', '-rpath', dest = 'rpath', action = 'store',
                        type = str, required = True, help = rpath_help)
    
    #Create help string:
    bpath_help = 'Path to superbias.'
    # Add arguments:
    
    parser.add_argument('--bpath', '-bpath', dest = 'bpath', action = 'store',
                        type = str, required = True, help = bpath_help)

    #Create help string:
    dpath_help = 'Path to superdark.'
    # Add arguments:
    
    parser.add_argument('--dpath', '-dpath', dest = 'dpath', action = 'store',
                        type = str, required = True, help = dpath_help)

    #Create help string:
    fpath_help = 'Path to superflat.'
    # Add arguments:
    
    parser.add_argument('--fpath', '-fpath', dest = 'fpath', action = 'store',
                        type = str, required = True, help = fpath_help)
    
    #Create help string:
    crpath_help = 'Path to the CR file.'
    # Add arguments:
    
    parser.add_argument('--crpath', '-crpath', dest = 'crpath', action = 'store',
                        type = str,help = crpath_help)

    #Create help string:
    opath_help = 'Path to output.'
    # Add arguments:
    
    parser.add_argument('--opath', '-opath', dest = 'opath', action = 'store',
                        type = str, help = opath_help)


    # Parse args:
    args = parser.parse_args()

    return args

def make_config(biaspath, darkpath, flatpath, conffile, currentpath):

    reffiles={'BPIXTAB':'N/A',
              'CCDTAB':currentpath+'/Ref/csst_ccd.fits',
              'OSCNTAB':currentpath+'/Ref/x1_osc.fits',
              'BIASFILE':'N/A',
              'DARKFILE':'N/A',
              'FLSHFILE':'N/A',
              'PFLTFILE':'N/A'}
    reffiles['BIASFILE'] = biaspath
    reffiles['DARKFILE'] = darkpath
    reffiles['PFLTFILE'] = flatpath

    with open(conffile,'w+') as f:
        json.dump(reffiles, f)
    
if __name__ == '__main__':

    args = parse_args()

    rawfile = args.rpath
    
    _path = os.path.dirname(os.path.abspath(__file__))
    #_py_abspath = os.path.abspath(__file__)#/app/run.py
    conffile = _path+ '/Conf/conf.json'

    make_config(args.bpath, args.dpath, args.fpath, conffile, currentpath=_path)

    if args.opath:
        outputpath = args.opath
    else:
        outputpath = None

    if args.crpath:
        crfile = args.crpath
        crimg = fits.getdata(crfile)
        bpmap = np.where(crimg!=0, 8, 0).astype(np.uint16)
    else:
        bpmap = None

    if os.path.isfile(conffile):
        rd = process.pipeline(filename= rawfile, 
                                refconf = conffile,
                                noScan=True,
                                mask=bpmap,
                                outputpath=outputpath,
                                normfl = False, 
                                writetofits = True,
                                DQInit = True,
                                BiasCorr = True,
                                ToElectron=True,
                                BlevCorr=False,
                                DarkCorr = True,
                                FlatCorr = True,
                                ToCPS=True)
 
