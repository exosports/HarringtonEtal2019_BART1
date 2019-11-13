Harrington et al. 2019, 
"An Open-Source Bayesian Atmospheric Radiative Transfer (BART) Code: 1. Design, Tests, and Application to Exoplanet HD 189733 b"
----------------------------------------------------------------
This README file describes the layout of the compendium.

If you wish to reproduce the work, ensure you have at least 45 GB of 
free space available, as many large files are downloaded/created/copied. 
Also be prepared to wait a long time for some parts. 
Creating the TLI files can take hours, 
computing an opacity table can take a day, and 
running BART can take days on an average 8-core modern CPU. 
Less cores = more time.
BART runs *require* at least 3 cores, to ensure that the Bayesian sampler 
is accurate; see ter Braak & Vrugt (2008) for more details.
The final section of this document describes the software used.

NOTE: To conserve space, we have not included line lists, and we have deleted TLI and opacity files. 
The posteriors and band-integrated spectra have been compressed as .tar.gz files to further conserve space. 
Commands below will re-create/extract these files.
Beginning from the top-level directory,

```
cd BARTTest_v0.3
tar -zxvf code-output/01BART/r01hd189733b/output.tar.gz -C code-output/01BART/r01hd189733b/
tar -zxvf code-output/01BART/r01hd189733b/band_eclipse.tar.gz -C code-output/01BART/r01hd189733b/
tar -zxvf code-output/01BART/s01hjcleariso-ecl/output.tar.gz -C code-output/01BART/s01hjcleariso-ecl/
tar -zxvf code-output/01BART/s01hjcleariso-ecl/band_eclipse.tar.gz -C code-output/01BART/s01hjcleariso-ecl/
tar -zxvf code-output/01BART/s01hjcleariso-tra/output.tar.gz -C code-output/01BART/s01hjcleariso-tra/
tar -zxvf code-output/01BART/s01hjcleariso-tra/band_eclipse.tar.gz -C code-output/01BART/s01hjcleariso-tra/
tar -zxvf code-output/01BART/s02hjclearnoinv-ecl/output.tar.gz -C code-output/01BART/s02hjclearnoinv-ecl/
tar -zxvf code-output/01BART/s02hjclearnoinv-ecl/band_eclipse.tar.gz -C code-output/01BART/s02hjclearnoinv-ecl/
tar -zxvf code-output/01BART/s02hjclearnoinv-tra/output.tar.gz -C code-output/01BART/s02hjclearnoinv-tra/
tar -zxvf code-output/01BART/s02hjclearnoinv-tra/band_eclipse.tar.gz -C code-output/01BART/s02hjclearnoinv-tra/
tar -zxvf code-output/01BART/s03hjclearinv-ecl/output.tar.gz -C code-output/01BART/s03hjclearinv-ecl/
tar -zxvf code-output/01BART/s03hjclearinv-ecl/band_eclipse.tar.gz -C code-output/01BART/s03hjclearinv-ecl/
tar -zxvf code-output/01BART/s03hjclearinv-tra/output.tar.gz -C code-output/01BART/s03hjclearinv-tra/
tar -zxvf code-output/01BART/s03hjclearinv-tra/band_eclipse.tar.gz -C code-output/01BART/s03hjclearinv-tra/
make bart
make hitran_linelists
make retrieval_tli
make hd189_tli
../BART/BART.py -c tests/s01hjcleariso/iso_emission.brt --justOpacity
../BART/BART.py -c tests/r01hd189733b/HD189733b.brt --justOpacity
cp -a code-output/01BART/s01hjcleariso-ecl/opacity_hjclear.dat code-output/01BART/s01hjcleariso-tra/.
cp -a code-output/01BART/s01hjcleariso-ecl/opacity_hjclear.dat code-output/01BART/s02hjclearnoinv-ecl/.
cp -a code-output/01BART/s01hjcleariso-ecl/opacity_hjclear.dat code-output/01BART/s02hjclearnoinv-tra/.
cp -a code-output/01BART/s01hjcleariso-ecl/opacity_hjclear.dat code-output/01BART/s03hjclearinv-ecl/.
cp -a code-output/01BART/s01hjcleariso-ecl/opacity_hjclear.dat code-output/01BART/s03hjclearinv-tra/.
```

There are 2 files and 3 subdirectories within the compendium, described below.

Files
-----
compendium.sh - Contains the commands necessary to reproduce the work.
README.md     - The file you are currently reading.


Subdirectories
--------------
BARTTest_v0.3 - Contains BARTTest with output for all tests
inputs        - Contains the opacity file for the s01 -- s03 tests.
plots         - Plots produced for the paper, separate from BART/transit
scripts       - Contains scripts used to process output


A more detailed description of each subdirectory:

BARTTest_v0.3
-------------
Contains its own documentation. See BARTTest_v0.3/docs/

Contains all of the output of the tests. See BARTTest_v0.3/code-output/,
which has some results from miniRT, all results from BART/transit, and 
some results from DDART.  Note that the opacity files, TLI files, and 
line lists are not included; downloading/generating them via BARTTest will 
take hours to days, depending on the machine.

There are additional plots/text output created by BARTTest found in 
BARTTest_v0.3/results/, which has some results specific to BART, and 
a general plots directory for comparing the spectra produced by different codes.

plots
-----
- hd189-abun-comp.png -- plot comparing the retrieved abundances for HD 189733 b 
                         reported in the literature

scripts
-------
- credregion.py -- computes the credible regions for marginalized posteriors.
- credregion.txt - output of credregion.py
- ess.py        -- computes the SPEIS, ESS, and posterior accuracy.
- ess.txt       -- output of ess.py
- makeplots.py  -- produces the hd189-abun-comp.png plot.


Software
--------
The final runs were between June and September 2019.

- Ubuntu version: 16.04.6
- GNU Make ver  : 4.1
- MPI    version: 3.2
- mpi4py version: 2.0.0
- SWIG   version: 3.0.8
- Python version: 2.7.12
- Numpy  version: 1.16.2
- Scipy  version: 0.17.0
- Matplotlib ver: 1.5.1

