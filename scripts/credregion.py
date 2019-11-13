#! /usr/bin/env python

import sys, os
import numpy as np
import scipy.stats as stats
import scipy.interpolate as si


def load_data(output, burnin, uniform):
    """
    output  : string. Path to MC3 output.npy file.
    burnin  : int. Number of burn-in iterations.
    uniform : array-like. If not None, set uniform abundances with the 
                          specified values for each species.
    """
    # Load and stack results, excluding burn-in
    allparams = np.load(output)
    posterior = allparams[0, :, burnin:]
    for c in np.arange(1, allparams.shape[0]):
        posterior = np.hstack((posterior, allparams[c, :, burnin:]))

    # Shift by initial abundances if uniform, so that plots are log(abundance)
    for n in range(len(uniform)):
        if uniform[n] is not None:
            posterior[-len(uniform)+n] += np.log10(uniform[n])

    return posterior


def credregion(posterior, percentile=[0.6827, 0.9545, 0.9973], 
               lims=(None,None), numpts=100):
    """
    posterior: see load_data()
    percentile: 1D float ndarray, list, or float.
                The percentile (actually the fraction) of the credible region.
                A value in the range: (0, 1).
    lims: tuple, floats. Minimum and maximum allowed values for posterior. 
                         Should only be used if there are physically-imposed 
                         limits.
    numpts: int. Number of points to use when calculating the PDF.
    """
    # Make sure `percentile` is a list or array
    if type(percentile) == float:
        percentile = np.array([percentile])

    # Compute the posterior's PDF:
    kernel = stats.gaussian_kde(posterior)
    # Use a Gaussian kernel density estimate to trace the PDF:
    # Interpolate-resample over finer grid (because kernel.evaluate
    #  is expensive):
    if lims[0] is not None:
        lo = min(np.amin(posterior), lims[0])
    else:
        lo = np.amin(posterior)
    if lims[1] is not None:
        hi = max(np.amax(posterior), lims[1])
    else:
        hi = np.amax(posterior)
    x    = np.linspace(lo, hi, numpts)
    f    = si.interp1d(x, kernel.evaluate(x))
    xpdf = np.linspace(lo, hi, 100*numpts)
    pdf  = f(xpdf)


    # Sort the PDF in descending order:
    ip = np.argsort(pdf)[::-1]
    # Sorted CDF:
    cdf = np.cumsum(pdf[ip])

    # List to hold boundaries of CRs
    # List is used because a given CR may be multiple disconnected regions
    CRlo = []
    CRhi = []
    # Find boundary for each specified percentile
    for i in range(len(percentile)):
        # Indices of the highest posterior density:
        iHPD = np.where(cdf >= percentile[i]*cdf[-1])[0][0]
        # Minimum density in the HPD region:
        HPDmin   = np.amin(pdf[ip][0:iHPD])
        # Find the contiguous areas of the PDF greater than or equal to HPDmin
        HPDbool  = pdf >= HPDmin
        idiff    = np.diff(HPDbool) # True where HPDbool changes T to F or F to T
        iregion, = idiff.nonzero()  # Indexes of Trues. Note , because returns tuple
        # Check boundaries
        if HPDbool[0]:
            iregion = np.insert(iregion, 0, -1) # This -1 is changed to 0 below when 
        if HPDbool[-1]:                       #   correcting start index for regions
            iregion = np.append(iregion, len(HPDbool)-1)
        # Reshape into 2 columns of start/end indices
        iregion.shape = (-1, 2)
        # Add 1 to start of each region due to np.diff() functionality
        iregion[:,0] += 1
        # Store the min and max of each (possibly disconnected) region
        CRlo.append(xpdf[iregion[:,0]])
        CRhi.append(xpdf[iregion[:,1]])

    return pdf, xpdf, CRlo, CRhi


if __name__ == '__main__':
    # Set data paths
    data_dir   = '../BARTTest_v0.3/code-output/01BART/'
    data_files = [data_dir + 's01hjcleariso-ecl/output.npy', 
                  data_dir + 's01hjcleariso-tra/output.npy', 
                  data_dir + 's02hjclearnoinv-ecl/output.npy', 
                  data_dir + 's02hjclearnoinv-tra/output.npy', 
                  data_dir + 's03hjclearinv-ecl/output.npy', 
                  data_dir + 's03hjclearinv-tra/output.npy', 
                  data_dir + 'r01hd189733b/output.npy']

    burnin   = np.array([5000, 5000, 5000, 5000, 5000, 5000, 5000])
    uniform  = np.array([[1e-6, 1e-6, 1e-6, 1e-6, 1e-9], 
                         [1e-6, 1e-6, 1e-6, 1e-6, 1e-9], 
                         [1e-4, 1e-7, 1e-4, 1e-8, 1e-8], 
                         [1e-4, 1e-7, 1e-4, 1e-8, 1e-8], 
                         [1e-5, 1e-7, 1e-4, 1e-8, 1e-8], 
                         [1e-5, 1e-7, 1e-4, 1e-8, 1e-8], 
                         [1e-6, 1e-6, 1e-6, 1e-6]])
    parnames = [['kappa', 'g1', 'g2', 'alpha', 'beta', 
                 'H2O', 'CO2', 'CO', 'CH4', 'NH3'], 
                ['kappa', 'g1', 'g2', 'alpha', 'beta', 'Rp', 
                 'H2O', 'CO2', 'CO', 'CH4', 'NH3'], 
                ['kappa', 'g1', 'g2', 'alpha', 'beta', 
                 'H2O', 'CO2', 'CO', 'CH4', 'NH3'], 
                ['kappa', 'g1', 'g2', 'alpha', 'beta', 'Rp', 
                 'H2O', 'CO2', 'CO', 'CH4', 'NH3'], 
                ['kappa', 'g1', 'g2', 'alpha', 'beta', 
                 'H2O', 'CO2', 'CO', 'CH4', 'NH3'], 
                ['kappa', 'g1', 'g2', 'alpha', 'beta', 'Rp', 
                 'H2O', 'CO2', 'CO', 'CH4', 'NH3'], 
                ['kappa', 'g1', 'g2', 'alpha', 'beta', 
                 'H2O', 'CO2', 'CO', 'CH4']]

    modelnames = ['iso-ecl', 'iso-tra', 'noinv-ecl', 'noinv-tra', 
                  'inv-ecl', 'inv-tra', 'hd189']
    for i in range(len(data_files)):
        # Load the data
        posterior = load_data(data_files[i], burnin[i], uniform[i])
        print(modelnames[i])
        for n in range(posterior.shape[0]):
            # Get credible region
            pdf, xpdf, CRlo, CRhi = credregion(posterior[n])
            # Format it for printing
            creg = [' U '.join(['({:10.4e}, {:10.4e})'.format(CRlo[j][k], 
                                                              CRhi[j][k])
                               for k in range(len(CRlo[j]))])
                    for j in range(len(CRlo))]
            # Print the output
            print("  " + parnames[i][n])
            print("  68.27%: " + str(creg[0]))
            print("  95.45%: " + str(creg[1]))
            print("  99.73%: " + str(creg[2]))
        print("")

    print("Don't forget about your eyes!")


