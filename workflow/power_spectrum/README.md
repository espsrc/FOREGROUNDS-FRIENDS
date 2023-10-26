# Power Spectrum estimation
This part of the workflow takes care of the estimation of the power spectrum (PS) and its errors, complying with the submission format of the challange. 
The notebook *PS estimation with ps_eor.ipynb* provides a detailed description of the method, while *ps_estimation.ipynb* implements it for the images produced in previous steps. 
The configuration file *ps_config.ini* is used to input parameters in *ps_estimation.ipynb*.

The notebook *processing.ipynb* as been used to prepare the dataset for the power spectrum estimation. It is not necessary to run it every time a power spectrum has to be estimated. Must be run the first time and when new data from the polynomial fit method has been obtained, changing the configuration file.<br>
On one hand, it can be used to divide the full data cubes into the required frequency bins.
On the other hand, it can be used to transform the result of the polynomial fit method, which are 2D images, into cubes with the required frequency bins.<br>
To choose the first option, the *path* parameter in the configuration file must be "general", where the *general* parameter is the full cube we want to divide.
For the second option, *general* is the path to the file the method has been applied on (will be used to create the header) and *path* is the path to the 2D images.

## Input and output
### PS estimation
The input files required for the estimation of the PS are the FITS images of the dataset and of the PSF, along with the configuration file.<br>
The FITS files must have the next format: *path+prefix+*_{freq1}*MHz-*{freq2}*MHz.fits*, where _freq1_ and _freq2_ are the lower and upper limits of the frequency bins. E.g. *results/data/simulation_106.0MHz-121.0MHz.fits*.

The output files are a file with the PS and another one with its errors, for each frequency bin. E.g. *OurTeam_106.0MHz-121.0MHz.data* and *OurTeam_106.0MHz-121.0MHz_errors.data*.

### Processing
The input files for the processing step can be: any FITS file that has to be divided into frequency bins; or various 2D FITS files with the format *path+prefix_{number}.fits*, where *number* are integers from 0 to the number of files. E.g. *results/polyfit_result_0.fits*

The output files are data cubes with the required frequency bins in the format needed for the PS estimation, like e.g. *results/polyfit_result_106.0MHz-121.0MHz.fits*.

## How to use
1. Update *process_config.ini* and run *processing.ipynb*. Optional, only mandatory the first time or with new results from the polynomial fit method.
2. Update *ps_config.ini* and run *ps_estimation.ipynb*.

## Configuration files
The parameters to introduce in the configuration files are the following:

### ps_config.ini
- **path**
  - **image** = string with the path to the image files (*path+prefix*)
  - **psf** = string with the path to the psf files (*path+prefix*)
  - **save** = path of directory to save the results
  - **team** = name of the team; for the SDC3 submission format
- **params**
  - **min_b** = minimum baseline in wavelengths
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
  - **H0** = Hubble's constant in km/s/Mpc
  - **Om0** = Omega baryons; density of non-relativistic matter in units of the critical density

### process_config.ini
- **path**
  - **path** = path to the 2D images to combine into frequency bins (only *path+prefix*; for polynomial fit) or "general" (without quotes) to divide a full cube into frequency bins.
  - **general** = path to the cube to use as reference (for polynomial fit) or path to the cube to divide in frequency bins
  - **save** = path of directory to save the output files
- **params**
  - **min_freq** = minimum frequency in MHz
  - **max_freq** = maximum frequency in MHz
  - **nbins_freq** = number of frequency bins
