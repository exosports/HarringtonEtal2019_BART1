#! /usr/bin/env python

import sys, os
import numpy as np
from scipy import stats


def convergetest(chains):
    """
    Wrapper for the Gelman & Rubin (1992) convergence test on a MCMC
    chain parameters.
    Parameters
    ----------
    chains : ndarray
        A 3D array of shape (nchains, nparameters, chainlen) containing
        the parameter MCMC chains.
    Returns
    -------
    psrf : ndarray
        The potential scale reduction factors of the chain.  If the
        chain has converged, each value should be close to unity.  If
        they are much greater than 1, the chain has not converged and
        requires more samples.  The order of psrfs in this vector are
        in the order of the free parameters.
    Previous (uncredited) developers
    --------------------------------
    Chris Campo

    Notes
    -----
    Taken from MCcubed's gelman_rubin.py
    """
    # Allocate placeholder for results:
    npars = np.shape(chains)[1]
    psrf  = np.zeros(npars)

    # Calculate psrf for each parameter:
    for i in range(npars):
        psrf[i] = gelmanrubin(chains[:, i, :])

    return psrf


def gelmanrubin(chains):
    """
    Calculate the potential scale reduction factor of the Gelman & Rubin
    convergence test on a fitting parameter
    Parameters
    ----------
    chains: 2D ndarray
       Array containing the chains for a single parameter.  Shape
       must be (nchains, chainlen)

    Notes
    -----
    Taken from MCcubed's gelman_rubin.py
    """
    # Get length of each chain and reshape:
    nchains, chainlen = np.shape(chains)

    # Calculate W (within-chain variance):
    W = np.mean(np.var(chains, axis=1))

    # Calculate B (between-chain variance):
    means = np.mean(chains, axis=1)
    mmean = np.mean(means)
    B     = (chainlen/(nchains-1.0)) * np.sum((means-mmean)**2)

    # Calculate V (posterior marginal variance):
    V = W*((chainlen - 1.0)/chainlen) + B*((nchains + 1.0)/(chainlen*nchains))

    # Calculate potential scale reduction factor (PSRF):
    psrf = np.sqrt(V/W)

    return psrf




def sig(ess, p_est=np.array([0.68269, 0.86639, 0.95450, 0.98758, 0.99730])):
    """
    Computes the 1, 1.5, 2, 2.5, 3 sigma uncertainties given an effective 
    sample size. Assumes flat prior on a credible region, with the mean 
    and standard deviation estimated from the posterior.

    Inputs
    ------
    ess  : int.   Effective sample size.
    p_est: array. Credible regions to estimate uncertainty.

    Revisions
    ---------
    2019-09-13  mhimes            Original implementation.
    """
    return ((1.-p_est)*p_est/(ess+3))**0.5


def ess(output, burnin, step=10000):
    """
    Inputs
    ------
    output: string. Path/to/output.npy file from MCcubed.
    burnin: int.    Number of burned iterations.
    step  : int.    Step size between each GR test calculation

    Notes
    -----
    This code is adapted from Ryan Challener's MCcubed pull request.
    """
    # Load the output, discard burnin
    allparams = np.load(output)
    allparams = allparams[:, :, burnin:]
    totiter   = allparams.shape[-1] * allparams.shape[0]

    # Loop through iterations in steps of `step`
    for i in range(1, int(np.ceil(allparams.shape[-1]/step))):
        psrf = convergetest(allparams[:, :, :i*step])
        if np.all(psrf < 1.01):
            print("All parameters converged to within 1% of unity.")
            print("Iteration:", i*step)
            break

    # Calculate the ESS
    nisamp = np.zeros((allparams.shape[0], allparams.shape[1]))
    for nc in range(allparams.shape[0]):
        k      = 0
        allpac = np.zeros((allparams.shape[1], i*step))
        for p in range(allparams.shape[1]):
            meanapi   = np.mean(     allparams[nc,p,:i*step])
            autocorr  = np.correlate(allparams[nc,p,:i*step]-meanapi,
                                     allparams[nc,p,:i*step]-meanapi, mode='full')
            allpac[k] = autocorr[np.size(autocorr)//2:] / np.max(autocorr)
            
            if np.min(allpac[k]) < 0.01:
                cutoff = np.where(allpac[k] < 0.01)[0][0]
            else:
                cutoff = -1
            nisamp[nc, k]  = 1 + 2 * np.sum(allpac[k,:cutoff])
            k += 1

    return int(np.ceil(np.amax(nisamp))), totiter


if __name__ == '__main__':
    predir = '../BARTTest_v0.3/code-output/01BART/'
    s01ecl = predir + 's01hjcleariso-ecl/output.npy'
    s01tra = predir + 's01hjcleariso-tra/output.npy'
    s02ecl = predir + 's02hjclearnoinv-ecl/output.npy'
    s02tra = predir + 's02hjclearnoinv-tra/output.npy'
    s03ecl = predir + 's03hjclearinv-ecl/output.npy'
    s03tra = predir + 's03hjclearinv-tra/output.npy'
    r01    = predir + 'r01hd189733b/output.npy'
    runs   = [s01ecl, s01tra, s02ecl, s02tra, s03ecl, s03tra, r01]
    p_est  = np.array([0.68269, 0.86639, 0.95450, 0.98758, 0.99730])

    for foo in runs:
        print('')
        print(foo.split('/')[-2])
        speis, totiter = ess(foo, burnin=5000)
        print("  SPEIS:", speis)
        print("  ESS  :", totiter//speis)
        siggy = sig(totiter/speis)
        for i in range(len(p_est)):
            print('  ' + str(p_est[i]) + u"\u00B1" + str(siggy[i]))


