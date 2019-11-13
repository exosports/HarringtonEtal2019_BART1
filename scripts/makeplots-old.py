#! /usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

plt.ion()

xlo =  -1.5
xhi =   7.0
ylo = -14.5
yhi =   0

mollabels = np.array(['H$_2$O', 'CH$_4$', 'CO', 'CO$_2$'])
mols      = np.arange(8, step=2)

bartvallo = np.array([-1.9, -11.7, -6.6, -2.5])
bartvalhi = np.array([-0.8,  -5.5, -0.5, -1.5])

bartvallo = 1 - bartvallo/ylo
bartvalhi = 1 - bartvalhi/ylo

taurexval = np.array([-4.978, -6.768, -2.689, -4.204])
taurexunc = np.array([ 0.602,  0.487,  0.769,  0.488])

chimeraval = np.array([-3.053,         -4.703,         -1.740,         -2.542])
chimeraunc = np.array([[0.419, 0.160], [0.298, 0.082], [2.821, 0.227], [0.347, 0.114]])

leeval = np.array([-3.174,         -6.721,       -2.538,     -2.699])
leeunc = np.array([[1.349, 1.174], [100, 2.721], [100, 100], [1.125, 1.176]])

lineval = np.array([-3.924,         -8.010,         -1.939,         -2.472])
lineunc = np.array([[0.351, 0.351], [6.000, 6.000], [0.504, 0.500], [0.300, 0.300]])

madhulo = np.array([-5.0, -100, -4.0, -1.156])
madhuhi = np.array([-3.0, -5.2, -2.0, -1.154])

madhulo = 1 - madhulo/ylo
madhuhi = 1 - madhuhi/ylo

swainlo = np.array([-5.0, -100, -4.0,   -7.0])
swainhi = np.array([-4.0, -5.0,    -3.523, -6.0])

swainlo = 1 - swainlo/ylo
swainhi = 1 - swainhi/ylo

plt.xlim(xlo, xhi)
plt.ylim(ylo, yhi)

plt.errorbar(mols+0.1, taurexval,  yerr=taurexunc, 
             label='Tau-REx', fmt='o')
plt.errorbar(mols+0.2, chimeraval, yerr=[chimeraunc[:,0], chimeraunc[:,1]], 
             label='CHIMERA', fmt='o')
plt.errorbar(mols+0.3, leeval,     yerr=[leeunc[:,0], leeunc[:,1]],
             label='Lee et al. 2012', fmt='o')
plt.errorbar(mols+0.4, lineval,    yerr=[lineunc[:,0], lineunc[:,1]],
             label='Line et al. 2012', fmt='o')

for i in range(len(mols)):
    plt.axvline(x=mols[i]+0.0, ymin=bartvallo[i], ymax=bartvalhi[i], 
                color='gold', label='BART')
    if i<3:
        plt.axvline(x=mols[i]+0.5, ymin=madhulo[i], ymax=madhuhi[i], 
                    color='magenta', label='Madhusudhan & \nSeager 2009')
    else:
        plt.scatter(x=mols[i]+0.5, y=-1.155, color='magenta')
    plt.axvline(x=mols[i]+0.6, ymin=swainlo[i], ymax=swainhi[i], color='cyan', 
                label='Swain et al. 2009')
    if i==0:
        # This is very hacky and poor coding practice 
        # but I just want this plot to be done
        handles, labels = plt.gca().get_legend_handles_labels()
        handles = [handles[0], handles[3], handles[4], handles[5], handles[6], \
                   handles[1], handles[2]]
        labels  = [labels[0],  labels[3],  labels[4],  labels[5],  labels[6], \
                   labels[1],  labels[2]]
        plt.legend(handles, labels, loc='lower left', prop={'size': 13})

plt.ylim(-14, 0)
plt.ylabel('Log Abundance')
locs, labels = plt.xticks()
plt.xticks(mols, mollabels)
plt.savefig('../plots/hd189-abun-comp.png')
plt.close()

