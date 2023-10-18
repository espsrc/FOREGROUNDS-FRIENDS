# This is a script to apply a polynomial fit to the real and imaginary parts of the FFT of the images.
# 
# We will follow  these steps:
# 1. Load the file containing the image 
# 2. Make a FFT of the image
# 3. Select a pixel and fit a polynomial to the real and imaginary parts of the FFT of the image for all frequencies
# 4. Repeat step 3 for all pixels
# 5. Remove the fitted foregrounds from the visibilities
# 6. Transform the visibilities back to image space

# Import modules
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import os
from numpy.polynomial.polynomial import polyfit
import sys
import shutil

# The program has four inputs read from the command line: 
# 1) <input_file> is the name of the FITS file containing the image cube
# 2) <output_dir> is the name of the directory where the output files will be saved
# 3) <degree> is the degree of the polynomial to fit to the FFT
# 4) <log> is a boolean flag indicating whether to use log-log space (True) or linear space (False) for the polynomial fit
# An option to choose whether to perform log-log fit or not

# Define a variable to choose whether to perform log-log fit or not
# The variable is numeric, 1 for log-log fit, 0 for no log-log fit
input_file = sys.argv[1] # = "/mnt/sdc3a.MS.0/sdc3dataset/Image/ZW3.msw_image.fits"
output_dir = sys.argv[2] # = "/mnt/scratch/FFTS/" 
deg= int(sys.argv[3]) # = 3
loglog = sys.argv[4]

#  First we load the file containing the image. The file is in FITS format.
# The resolution is 2048x2048 pixels, with each pixel being 16 arcsec in size. The frequency range is 
# 106-196 MHz with a channel width of 0.1 MHz.

npix = 2048
nchan = 901
nu_min = 106 # in MHz
nu_max = 196 # in MHz
channel_width = 0.100 # in MHz
freq_bands = np.arange(nu_min, nu_max+channel_width, channel_width)

# Load the input file
data_msw = fits.getdata(input_file)

# Print the shape of the cube
print(data_msw.shape) #(901, 2048, 2048)

# Define an array to store the visibilities
data_msw_vis = np.zeros((npix, npix), dtype=complex)
real_part_temp = np.zeros((npix, npix))
imag_part_temp = np.zeros((npix, npix))
#Define TEMP_dir to store temporary files
TEMP_dir = os.path.join(output_dir, "TEMP/")
# Create the directory to save the visibilities if it does not exist
if not os.path.exists(TEMP_dir):
    os.makedirs(TEMP_dir)
# Loop over the channels and transform the cube to visibility space
for i in range(nchan):
   #Insert a progress bar using tqdm
    print("Processing channel %d of %d" % (i+1, nchan))
    data_msw_vis = np.fft.fft2(data_msw[i,:,:])
    real_part_temp = np.real(data_msw_vis)
    imag_part_temp = np.imag(data_msw_vis)
    # Save real and imaginary part of the visibility to a numpy file with the number of the channel in the name
    # This step is to save memory, we can not work with the whole cube at once
    output_filename_real = "real_data_vis_"+str(i)+".npy"
    output_filename_imag = "imag_data_vis_"+str(i)+".npy"
    np.save(os.path.join(TEMP_dir, output_filename_real), real_part_temp)
    np.save(os.path.join(TEMP_dir, output_filename_imag), imag_part_temp)

# Delete the image cube to free memory
del data_msw
# Due to memory limitations we analyze first the real part of the visibilities. Later we will repeat the same steps for the imaginary part.
# Define an array to store the visibilities    
real_part = np.zeros((nchan,npix, npix))
#  Loop to load the real part of the visibilities 
for i in range(nchan):
    print("Loading real part of channel %d of %d" % (i+1, nchan))
    output_filename_real = "real_data_vis_"+str(i)+".npy"
    real_part[i,:,:] = np.load(os.path.join(TEMP_dir, output_filename_real))

# Define an array to store the coefficients of the polynomial fit
coefs_real = np.zeros((npix,npix, deg + 1)) # shape (N, deg + 1)

# Fit real part of visibilities separately for each pixel u,v
if loglog:
    print("Performing log-log fit")
    # Define an array to store the log of the real and imaginary parts of the visibilities
    logRealVis = np.zeros(nchan) # shape (N, 900, 900)
    for u in range(npix):
        for v in range(npix):
            # Print a progress message every 1000 pixels to keep track of the progress
            if (u*npix + v + 1) % 1000 == 0:
                print("Fitting pixel %d of %d" % (u*npix + v + 1, npix**2)) 
            # Add constant to the real visibilities to make them positive
            rconst=np.abs(np.min(real_part[:,u,v]))+1
            # Add constants to the real and imaginary visibilities
            logRealVis = np.log(real_part[:,u,v] + rconst)
            # Fit the real part 
            coefs_real[u,v,:] = polyfit(np.log(freq_bands), logRealVis, deg)
            # Remove the fitted foregrounds from the real part of the visibilities and remove back the constants
            real_part[:,u,v] = np.exp(np.log(real_part[:,u,v]+rconst) - np.polyval(coefs_real[u,v][::-1], np.log(freq_bands))) - rconst
else:
    print("Performing linear fit")
    for u in range(npix):
        for v in range(npix):
            if (u*npix + v + 1) % 1000 == 0:
                print("Fitting pixel %d of %d" % (u*npix + v + 1, npix**2))
            # Add constant to the real visibilities to make them positive
            rconst=np.abs(np.min(real_part[:,u,v]))+1
            # Fit the real part 
            coefs_real[u,v,:] = polyfit(freq_bands, real_part[:,u,v], deg)
            # Remove the fitted foregrounds from the real part of the visibilities and remove back the constants
            real_part[:,u,v] = real_part[:,u,v] - np.polyval(coefs_real[u,v][::-1], freq_bands)

#Save each slice of the cube to a npy file
for i in range(nchan):
    print("Saving channel %d of %d" % (i+1, nchan))
    output_filename = "real_part_clean_"+str(i)+".npy"
    np.save(os.path.join(TEMP_dir, output_filename), real_part[i,:,:])

# Delete the array to free memory
del real_part
#################################################################################################
# Now we repeat the same steps for the imaginary part of the visibilities
# Define an array to store the visibilities
imag_part = np.zeros((nchan,npix, npix))
#  Loop to load the real part of the visibilities and store
for i in range(nchan):
    print("Loading imaginary part of channel %d of %d" % (i+1, nchan))
    output_filename_imag = "imag_data_vis_"+str(i)+".npy"
    imag_part[i,:,:] = np.load(os.path.join(TEMP_dir, output_filename_imag))

# Define an array to store the coefficients of the polynomial fit
coefs_imag = np.zeros((npix,npix, deg + 1)) # shape (N, deg + 1)

# Fit imaginary part of visibilities separately for each pixel u,v
if loglog:
    # Define an array to store the log of the real and imaginary parts of the visibilities
    logImagVis = np.zeros(nchan) # shape (N, 900, 900)

    for u in range(npix):
        for v in range(npix):
            if (u*npix + v + 1) % 1000 == 0:
                print("Fitting pixel %d of %d" % (u*npix + v + 1, npix**2))
            # Add constant to the imaginary visibilities to make them positive
            iconst=np.abs(np.min(imag_part[:,u,v]))+1
            # Add constants to the real and imaginary visibilities
            logImagVis = np.log(imag_part[:,u,v] + iconst)
            # Fit the imaginary part 
            coefs_imag[u,v,:] = polyfit(np.log(freq_bands), logImagVis, deg)
            # Remove the fitted foregrounds from the imaginary part of the visibilities and remove back the constants
            imag_part[:,u,v] = np.exp(np.log(imag_part[:,u,v]+iconst) - np.polyval(coefs_imag[u,v][::-1], np.log(freq_bands))) - iconst
else:
    for u in range(npix):
        for v in range(npix):
            if (u*npix + v + 1) % 1000 == 0:
                print("Fitting pixel %d of %d" % (u*npix + v + 1, npix**2))
            # Add constant to the imaginary visibilities to make them positive
            iconst=np.abs(np.min(imag_part[:,u,v]))+1
            # Fit the imaginary part 
            coefs_imag[u,v,:] = polyfit(freq_bands, imag_part[:,u,v], deg)
            # Remove the fitted foregrounds from the imaginary part of the visibilities and remove back the constants
            imag_part[:,u,v] = imag_part[:,u,v] - np.polyval(coefs_imag[u,v][::-1], freq_bands)    

#Save each slice of the cube to a npy file
for i in range(nchan):
    print("Saving channel %d of %d" % (i+1, nchan))  
    output_filename = "imag_part_clean_"+str(i)+".npy"
    np.save(os.path.join(TEMP_dir, output_filename), imag_part[i,:,:])
    
# Delete the array to free memory
del imag_part
#################################################################################################

# Combine the real and imaginary parts to form the complex visibilities
# Load the real and imaginary parts of the visibilities from a numpy file for each channel
# Then combine them to form the complex visibilities and transform them back to image space
# Save each slice of the cube to a fits file

# Load the original image cube
data_msw = fits.getdata(input_file)
# Print the shape of the cube
print(data_msw.shape) #(901, 2048, 2048)

# Save the clean image to a fits file 
for i in range(nchan):
    print("Processing channel %d of %d" % (i+1, nchan))
    output_filename_real = "real_part_clean_"+str(i)+".npy"
    output_filename_imag = "imag_part_clean_"+str(i)+".npy"
    real_part = np.load(os.path.join(TEMP_dir, output_filename_real))
    imag_part = np.load(os.path.join(TEMP_dir, output_filename_imag))
    # Combine the real and imaginary parts to form the complex visibilities
    data_msw_clean_vis = real_part + 1j*imag_part
    # Transform the visibilities back to image space
    data_msw_clean = np.real(np.fft.ifft2(data_msw_clean_vis))
    # Save the clean image to a fits file
    output_filename_fits = "data_clean_"+str(i)+".fits"
    hdu = fits.PrimaryHDU(data_msw_clean)
    hdu.writeto(os.path.join(output_dir, output_filename_fits), overwrite=True)
    
# Delete the files in the TEMP_dir directory
shutil.rmtree(TEMP_dir)
