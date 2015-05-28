from array import array
from samples import *

#Configurable file, choose the components, the variable to plot, and a string for cuts

# Binning
pt_bins = [0,20,40,60,80,100,120,140,150,300]
num_pt_bins = len(pt_bins)-1

eta_bins = [-2.7, -1.479, 1.479, 2.7]
num_eta_bins = len(eta_bins)-1

# Samples that are used
mc_samples = [GGH, VBF, TTH]
