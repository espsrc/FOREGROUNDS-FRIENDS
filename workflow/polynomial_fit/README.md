Polynomial fit to FFT of images

This script applies a polynomial fit to the real and imaginary parts of the fast Fourier transform (FFT) of the images, which are in FITS format and have 901 channels (106 MHz to 196 MHz with 0.1 MHz channel width) and 2048x2048 pixels each. It also performs foreground removal and image reconstruction.

Requirements

Python 3.6 or higher
numpy
astropy

Usage

python PolyFit.py <input_file> <output_file> <degree> <log>

where:

<input_file> is the name of the FITS file containing the image cube
<output_file> is the name of the FITS file where the reconstructed image cube will be saved
<degree> is the degree of the polynomial to fit to the FFT
<log> is a boolean flag indicating whether to use log-log space (True) or linear space (False) for the polynomial fit

Example

python polyfit_fft.py ZW3.image_cube.fits /home/user/ 3 True

This will apply a third-degree polynomial fit to the FFT of each pixel in log-log space, remove the foregrounds, and save the output files to /home/user .

Output

The script will generate several temporary files to save RAM memory. These files will be removed at the end.
The script will save each slice of the reconstructed cube to a FITS file into the directory specified by the user.
