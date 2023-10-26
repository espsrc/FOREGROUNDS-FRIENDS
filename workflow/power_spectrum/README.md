# Power Spectrum estimation
This part of the workflow takes care of the estimation of the power spectrum (PS) and its errors, complying with the submission format of the challange. 
The notebook *PS estimation with ps_eor.ipynb* provides a detailed description of the method, while *ps_estimation.ipynb* implements it for the images produced in previous steps. 
The configuration file *ps_config.ini* is used to input parameters in *ps_estimation.ipynb*.

## Input and output
The input files required for the estimation of the PS are the FITS images of the dataset and of the PSF, along with the configuration file.<br>
The FITS files must have the next format: *path+prefix+*_{freq1}*MHz-*{freq2}*MHz.fits*, where _freq1_ and _freq2_ are the lower and upper limits of the frequency bins. E.g. *results/data/simulation_106.0MHz-121.0MHz.fits*.

The output files are a file with the PS and another one with its errors, for each frequency bin. E.g. *OurTeam_106.0MHz-121.0MHz.data* and *OurTeam_106.0MHz-121.0MHz_errors.data*.

## Configuration file

The parameters to introduce in the configuration file are the following:
- **path**
  - **image** : string with the path to the image files
  - **psf** : string with the path to the psf files
  - **save** : path of directory to save the results
  - **team** : name of the team; for the SDC3 submission format
- **params**
  - **min_b** : minimum baseline in wavelengths
  - **max_b** = maximum baseline in wavelengths
  - **fov** = field of view in degrees
  - **int_time** = integration time in seconds
  - **tot_time** = total time in seconds
  - **min_freq** = minimum frequency in MHz
  - **max_freq** = maximum frequency in MHz
  - **nbins_freq** = number of frequency bins
  - **nbins_per** = number of bins in k_perpendicular
  - **nbins_par** = number of bins in k_parallel
  - **binmin** = minimum value of k (both parallel and perpendicular)
  - **binmax** = maximum value of k (both parallel and perpendicular)
- **cosmo**
  - **H0** : Hubble's constant in km/s/Mpc
  - **Om0** : Omega baryons; density of non-relativistic matter in units of the critical density
