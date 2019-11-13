#! /usr/bin/env python

import sys
import numpy as np
import scipy.interpolate as si
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FormatStrFormatter
sys.path.append("../../BART/modules/transit/scripts/")
import readtransit as rt

plt.ion()


def compspec(fspec1, fspec2, outname, outdir='../results/plots/', 
             geo='eclipse'):
    """
    This function produces a plot comparing two spectra for the forward 
    tests (f##).

    Inputs
    ------
    fspec1 : string. Path to specturm text file.
    fspec2 : string. Path to spectrum text file.
    outname: string. Savename of plot. The code names for `fspec1` and `fspec2` 
                     will be added to the beginning of this.
    """
    # Load spectra
    wlength1, flux1 = rt.readspectrum(fspec1, 0)
    wlength2, flux2 = rt.readspectrum(fspec2, 0)

    # Add code names to `outname`
    cname1  = fspec1.split('/')
    cname1  = cname1[cname1.index('code-output')+1][2:]
    cname2  = fspec2.split('/')
    cname2  = cname2[cname2.index('code-output')+1][2:]
    outname = cname1 + '_' + cname2 + '_' + outname

    # Make plot
    fig0 = plt.figure(0, (8,5))
    plt.clf()
    frame1 = fig0.add_axes((.14, .3, .8, .65))

    plt.xlabel(u"Wavelength  (\u03bcm)")
    if geo == 'transit':
        plt.ylabel("Modulation  (%)") 
    else:
        plt.ylabel("Flux (erg s$^{-1}$ cm$^{-1}$)")

    frame1.set_xticklabels([])
    frame1.yaxis.set_label_coords(-0.1, 0.5)
    plt.plot(wlength1, flux1, label=cname1)
    plt.plot(wlength2, flux2, label=cname2)
    yticks = frame1.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    plt.legend(loc='best')

    frame2 = fig0.add_axes((.14, .1, .8, .2))
    
    # Residuals, in units of %
    if np.all(wlength1!=wlength2):
        print("Wavelength arrays do not match.")
        print("Interpolating " + fspec2 + " to the grid of " + fspec1)
        fint  = si.interp1d(wlength2, flux2, bounds_error=False, fill_value=0)
        flux2 = fint(wlength1)
    resid = (flux1 - flux2) / np.max(np.concatenate((flux1, flux2))) * 100

    plt.plot(wlength1, resid, "k", linestyle = ":")
    plt.ylabel('Residuals (%)')
    plt.xlabel(u"Wavelength  (\u00b5m)")
    frame2.yaxis.set_major_locator(MaxNLocator(nbins = '5', prune='upper'))

    plt.savefig(outdir+outname)
    plt.close()


def comparison(transit, rhd, geo, atm, outdir=None, titles=False):
    """
    This function produces a plot of Transit and RHD (or other RT code) spectra 
    for the comparison tests (c##).

    Inputs
    ------
    transit: string. path/to/file for transit spectrum data.
    rhd    : string. path/to/file for RHD (or other RT code) spectrum data.
    geo    : string. Viewing geometry. 'eclipse' or 'transit'
    atm    : string. Atmosphere's PT profile. 'iso', 'inv', or 'noi'
    outdir : string. path/to/output. Default is execution directory
    titles : bool.   Determines whether to include titles on plots or not.

    Revisions
    ---------
    2017-10-16  mhimes          Initial implementation.
    2018-02-03  raechel         Improved plotting, added residuals subplot.
    2019-04-01  mhimes          Merged into BARTTest.
    """
    # Load transit data
    wlength, flux = rt.readspectrum(transit, 0)

    # Load RHD data
    data  = open(rhd, "r")
    lines = data.readlines()

    if geo == 'eclipse':
        lines = lines[3:]
        
        wlengthb = np.zeros(len(lines), dtype=float)
        fluxb    = np.zeros(len(lines), dtype=float)
        
        for i in range(len(lines)):
            line = lines[i].split()
            wlengthb[i] = float(line[1])
            fluxb[i]    = float(line[2]) * 2.998e10
    elif geo == 'transit':
        lines = lines[3:]
        
        wlengthb = np.zeros(len(lines), dtype=float)
        fluxb    = np.zeros(len(lines), dtype=float)
        
        for i in range(len(lines)):
            line = lines[i].split()
            wlengthb[i] = float(line[1])
            fluxb[i]    = float(line[2]) / 100

    # Resample code1 to code2's sampling
    # Use a linear interpolation! Splines can cause values smaller/bigger than 
    # the known mix and max values
    rep    = si.interp1d(wlength, flux)
    resamp = rep(wlengthb)
    # Set plot title and file output name
    if geo == 'transit':
        if atm == 'inv':
            titlenm = "inverted Transmission"
            filenm  = "inverted_transmission_comp.png"
        elif atm == 'iso':
            titlenm = "Isothermal Transmission"
            filenm  = "Isothermal_transmission_comp.png"
        elif atm == 'noi':
            titlenm = "Non-inverted Transmission"
            filenm  = "noninverted_transmission_comp.png"
        else:
            print("Wrong `atm` specification. Use 'inv', 'iso', or 'noi'.\n")
    elif geo == 'eclipse':
        if atm == 'inv':
            titlenm = "inverted Emission"
            filenm  = "inverted_emission_comp.png"
        elif atm == 'iso':
            titlenm = "Isothermal Emission"
            filenm  = "Isothermal_emission_comp.png"
        elif atm == 'noi':
            titlenm = "Non-inverted Emission"
            filenm  = "noninverted_emission_comp.png"
        else:
            print("Wrong `atm` specification. Use 'inv', 'iso', or 'noi'.\n")
    else:
        print("Wrong `geo` specification. Use 'transit' or 'eclipse'.\n")
        sys.exit()
    # Add code names to `filenm`
    cname1 = transit.split('/')
    cname1 = cname1[cname1.index('code-output')+1][2:]
    cname2 = rhd.split('/')
    cname2 = cname2[cname2.index('code-output')+1][2:]
    filenm = cname1 + '_' + cname2 + '_' + filenm
    
    # Plot it
    fig0 = plt.figure(0, (8,5))
    plt.clf()
    frame1 = fig0.add_axes((.14, .3, .8, .65))
    if titles==True:
        plt.title(titlenm)

    if geo == 'transit':
        flux   = 100*flux   # convert to %
        fluxb  = 100*fluxb
        resamp = 100*resamp
    if geo == 'eclipse':
        if atm == 'iso':
            plt.plot(wlength,  flux,   "lightblue", 
                     label=cname1 + ' - high resolution', linewidth = 10.0)
            plt.plot(wlengthb, resamp, "royalblue", 
                     label=cname1 + ' - resampled to ' + cname2)
            plt.plot(wlengthb, fluxb,  "firebrick", label=cname2)
        else:
            plt.plot(wlength,  flux,   "lightblue", 
                     label=cname1 + ' - high resolution')
            plt.plot(wlengthb, resamp, "royalblue", 
                     label=cname1 + ' - resampled to ' + cname2)
            plt.plot(wlengthb, fluxb,  "firebrick", label=cname2)
    else:
        plt.plot(wlength,  flux,   "lightblue", 
                 label=cname1 + ' - high resolution')
        plt.plot(wlengthb, resamp, "royalblue", 
                 label=cname1 + ' - resampled to ' + cname2)
        plt.plot(wlengthb, fluxb,  "firebrick", label=cname2)


    plt.xlabel(u"Wavelength  (\u03bcm)")
    if geo == 'transit':
        plt.ylabel("Modulation  (%)") 
    else:
        plt.ylabel("Flux (erg s$^{-1}$ cm$^{-1}$)")

    #plot black body curves
    h  = 6.62607004e-27     # erg*s
    c  = 2.9979245800e10    # cm/s
    k  = 1.38064852e-16     # erg/K

    # Set min and max temperatures for plotting
    if atm == 'inv':
        T1 =  968.60        # K
        T2 =  1243.05       # K
    elif atm == 'iso':
        T1 =  1100.0               
        T2 =  1100.0
    elif atm == 'noi':
        T1 =  882.93
        T2 =  1408.70

    w   = np.linspace(10000./11.0, 10000./1.000, 10000)   # cm^-1
    
    # Blackbody associated with min/max temperature
    a   = np.pi * 2 * h * (c**2) * (w**3)    
    b1  = (h*c*w) / (k*T1)
    Bb1 = a / (np.exp(b1) - 1.0)
  
    b2  = (h*c*w) / (k*T2)
    Bb2 = a / (np.exp(b2) - 1.0)
    
    l   = 10000. / w
    
    T1s = str(T1)+' K'
    T2s = str(T2)+' K'
    
    if geo == 'eclipse':
        frame1.set_ylim(0, max(Bb2)+5000)
        if T1 != T2:
            plt.plot(l, Bb1, "r", linestyle =':', 
                     label="Blackbody at "+T1s, linewidth = 2.0)
            plt.plot(l, Bb2, "b"        , linestyle =':', 
                     label="Blackbody at "+T2s, linewidth = 2.0)
        else:
            plt.plot(l, Bb1, "k"        , linestyle =':', 
                     label="Blackbody at "+T2s, linewidth = 2.0)
        plt.legend(loc='upper left', prop={'size':8})
    elif geo == 'transit':
        plt.legend(loc='lower right', prop={'size':8})

    frame1.set_xscale('log')
    frame1.set_xlim(1, 11.0)
    frame1.set_xticklabels([])
    frame1.yaxis.set_label_coords(-0.1, 0.5)
    # Set y axis limits
    if geo == 'transit':
        frame1.set_ylim(np.amin(flux)*0.99, np.amax(flux)*1.01)
        frame1.yaxis.set_major_locator(MaxNLocator(nbins='6', prune='lower'))
    else:
        frame1.set_ylim(np.amin(Bb1)*0.9,  np.amax(Bb2)*1.1)


    frame2 = fig0.add_axes((.14, .1, .8, .2))
    
    #residual plots
    resid = np.zeros(len(lines), dtype=float)
    # Residuals, in units of %
    resid = (resamp - fluxb) / np.max(np.concatenate((resamp, fluxb))) * 100

    plt.plot(wlengthb, resid, "k", linestyle = ":")
    plt.ylabel('Residuals (%)')
    plt.xlabel(u"Wavelength  (\u00b5m)")

    frame2.set_xscale('log')
    frame2.set_xlim(0, 11.0)

    frame2.set_ylim(np.amin(resid) - 0.2*np.abs(np.amin(resid)), 
                    np.amax(resid) + 0.2*np.abs(np.amax(resid)))
    
    frame2.set_xticklabels([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    frame2.yaxis.set_major_locator(MaxNLocator(nbins = '5', prune='upper'))
    if(geo == 'eclipse') and (atm == 'iso'):
        frame2.yaxis.get_major_ticks()[-1].label1.set_visible(False)
    frame2.xaxis.set_major_locator(plt.MultipleLocator(1))

    frame2.yaxis.set_label_coords(-0.1, 0.5)

    if(geo == 'eclipse') and (atm == 'iso'):
        frame3 = fig0.add_axes((.57, .38, .25, .25))
        frame3.set_ylim(23000, 24000)
        frame3.set_xscale('log')
        frame3.set_xlim(3.5, 6.5)
        frame3.set_xticklabels([4, 4.5, 5, 5.5, 6])
        frame3.xaxis.set_major_locator(plt.MultipleLocator(1))
        plt.plot(wlength,  flux,   "lightblue", linewidth = 10.0)
        plt.plot(wlengthb, resamp, "royalblue", linewidth = 2.0)
        plt.plot(wlengthb, fluxb,  "firebrick", linewidth = 2.0)
        plt.plot(l, Bb1, "k", linestyle = ':',  linewidth = 4.0)

    if outdir!=None:
        plt.savefig(outdir+filenm)
    else:
        plt.savefig(filenm)
    plt.close()


if __name__ == "__main__":
    """
    Produce the plots using the above function
    """
    # f01 -- f06, no f05
    compspec('../code-output/00miniRT/f01oneline/oneline.dat', 
             '../code-output/01BART/f01oneline/oneline_emission_spectrum.dat', 
             'oneline_emission.png')

    compspec('../code-output/00miniRT/f02fewline/fewline.dat', 
             '../code-output/01BART/f02fewline/fewline_emission_spectrum.dat', 
             'fewline_emission.png')

    compspec('../code-output/00miniRT/f03multiline/multiline.dat', 
             '../code-output/01BART/f03multiline/' + \
                                      'multiline_emission_spectrum.dat', 
             'multiline_emission.png')

    compspec('../code-output/00miniRT/f04broadening/broadening.dat', 
             '../code-output/01BART/f04broadening/' + \
                                      'broadening_emission_spectrum.dat', 
             'broadening_emission.png')

    compspec('../code-output/00miniRT/f06blending/blending.dat', 
             '../code-output/01BART/f06blending/' + \
                                      'blending_emission_spectrum.dat', 
             'blending_emission.png')
    # c01 -- c03
    comparison('../code-output/01BART/c03hjclearinv/' + \
             'inv_emission_spectrum.dat', 
             '../code-output/02DDART/full_inv_emission.dat', 
             'eclipse', 'inv', 
             '../results/plots/')

    comparison('../code-output/01BART/c01hjcleariso/' + \
             'iso_emission_spectrum.dat', 
             '../code-output/02DDART/full_iso_emission.dat', 
             'eclipse', 'iso', 
             '../results/plots/')

    comparison('../code-output/01BART/c02hjclearnoinv/' + \
             'noinv_emission_spectrum.dat', 
             '../code-output/02DDART/full_noinv_emission.dat', 
             'eclipse', 'noi', 
             '../results/plots/')

    comparison('../code-output/01BART/c03hjclearinv/' + \
             'inv_transmission_spectrum.dat', 
             '../code-output/02DDART/full_inv_transit.dat', 
             'transit', 'inv', 
             '../results/plots/')

    comparison('../code-output/01BART/c01hjcleariso/' + \
             'iso_transmission_spectrum.dat', 
             '../code-output/02DDART/full_iso_transit.dat', 
             'transit', 'iso', 
             '../results/plots/')

    comparison('../code-output/01BART/c02hjclearnoinv/' + \
             'noinv_transmission_spectrum.dat', 
             '../code-output/02DDART/full_noinv_transit.dat', 
             'transit', 'noi', 
             '../results/plots/')


