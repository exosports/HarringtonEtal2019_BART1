#! /bin/sh

# Author: Michael Himes
# Accompanies paper:
# Harrington et al. 2019, 
# "An Open-Source Bayesian Atmospheric Radiative Transfer (BART) Code: 
# 1. Design, Tests, and Application to Exoplanet HD 189733 b"
# This file should be acquired as part of the compendium associated with the 
# paper. It contains the commands necessary to reproduce the published results.
# The following commands assume they are executed in a terminal at the 
# top-level directory of the compendium. This script is long and not fully 
# tested, so there may be bugs.

### Do not run this entire script in one go! ###

# That will take quite some time to complete.
# Instead, it is provided to show how someone could reproduce the published 
# work.
# If you wish to reproduce the work, ensure you have >45GB of free space 
# available, as many large files are downloaded/created/copied. Also be 
# prepared to wait a long time for some parts of this. Creating the TLI 
# files takes ~hour, computing an opacity table takes ~1 day, and running 
# BART takes ~3 days on an average 8-core modern CPU. Less cores = more time.
# BART runs *require* at least 3 cores, to ensure that the Bayesian sampler 
# is accurate; see ter Braak & Vrugt (2008) for more details.


### Begin ###

# Run BARTTest
cd BARTTest_v0.3
make all
make synthretrievals
make hd189
make retrievalplots

# Back to top-level dir
cd ..

# Run the scripts
cd scripts
./makeplots.py
./credregion.py > credregion.txt
./ess.py > ess.txt


