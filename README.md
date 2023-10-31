# FOREGROUNDS-FRIENDS
## The SKA data challenge 3a

The SKA Data Challenge 3a - Epoch of Reionisation is described in the [SDC3a page](https://sdc3.skao.int/overview).

The FOREGROUNDS-FRIENDS team is lead by Diego Herranz (IFCA). More details to come.

## Reproducibility
The FOREGROUNDS-FRIENDS team participates with the [Reproducibility Badge in mind](https://sdc3.skao.int/reproducibility-badges) with the aim of making this solution open, reproducible and reusable. 

## Installation

To deploy this project, first you need to install conda, download the pipeline from Github and install the environment.

### 1. Get conda

You don't need to run this if you already have a working `conda` installation. If you don't have `conda` follow the steps below to install it in the local directory `conda-install`. We will use the light-weight version `miniconda`. We also install `mamba`, which is a very fast dependency solver for conda. 

```bash
 curl --output Miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
 bash Miniconda.sh -b -p conda-install
 source conda-install/etc/profile.d/conda.sh
 conda install mamba --channel conda-forge --yes
```


### 2. Get the pipeline and install the dependencies

```bash
git clone https://github.com/espsrc/FOREGROUNDS-FRIENDS.git
cd 
mamba env create -f environment.yml
conda activate snakemake
```

If you have created the environemnt already, simply activate it by running the last command.

### 3. Execute the workflow

The workflow consist of three main steps. The first step is the creation of a point source mask which it is optional as we are only using it for visualization purposes. In the second step we use two independent foreground removal algorithms to obtain the 21 cm signal. The first one is a polynomial fit in the visibilities and the second one is a PCA cleaning in the image. The best algorithm seems to be the PCA cleaning, so this is the one used to generate the cleaned images used for the power spectrum estimation. Last, we estimate the 2d power spectrum with their error bars for each of the six frequency bins in the appropiate format for submission.

## Workflow

The workflow consists of three main stages:

### 1. create_mask (optional)

Describe process [TBD]

### 2.1. polynomial_fit

This step is an alternative to pca_subtraction.
This script applies a polynomial fit to the real and imaginary parts of the fast Fourier transform (FFT) of the images, which are in FITS format and have 901 channels (106 MHz to 196 MHz with 0.1MHz channel width) and 2048x2048 pixels each.
It also performs foreground removal and image reconstruction. 

#### Requirements

Python 3.6 or higher

numpy

astropy

#### Usage
Usage
```bash
python PolyFit.py <input_file> <output_file> <degree> <log>
```
where:

`<input_file>` is the name of the FITS file containing the image cube

`<output_file>` is the name of the FITS file where the reconstructed image cube will be saved

`<degree>` is the degree of the polynomial to fit to the FFT

`<log>` is a boolean flag indicating whether to use log-log space (True) or linear space (False) for the polynomial fit

#### Example
```bash
python Polyfit.py ZW3.image_cube.fits /home/user/results/ 3 True
```

This will apply a third-degree polynomial fit to the FFT of each pixel in log-log space, remove the foregrounds, and save the output files to /home/user .

#### Output
The script will generate several temporary files to save RAM memory. These files will be removed at the end.
The script will save each slice of the reconstructed cube to a FITS file into the directory specified by the user. 
Output filenames follow the pattern `data_clean_i.fits`, where `i` represents the channel number and ranges from 1 to 901.

### 2.2. pca_substraction

In this step, we perform foreground removal of the data cube by applying a 4 component Principal Component Analysis (PCA) [Irfan & Bull. MNRAS, 2021].
This kind of analysis only uses frequency information and their correlation, losing the spatial information of the image.

The original data cube is $8\times 8$ degrees FoV, but in order to limit the noise, only the central $4 \times 4$ degrees are meant to be used for the power spectrum computation. For that reason, only this central part will be used as an input for the PCA cleaning step.

This step is implemented in the jupyter notebook PCA_data_SDC3.ipynb.
#### Description of the algorithm
The PCA algorithm works as follows.

1. Converts the 3-dimensional data cube of dimensions $N_{\text{freq}}\times N_{pix}\times N_{pix}$ in a 2-dimensional array of dimensions $N_{\text{freq}}\times N_{pix}^2$ using a method called reshaping. $N_{\text{freq}}$ is the number of frequencies in the cube (equal to 901) and $N_{pix}$ is the number of pixel in the $x/y$ axis (equal to 900). From now on, this reshaped 2d data set will be referred to as $D$.
2. Removes the mean for each slide, $\overline{D}$, i.e. making it mean zero. As an abuse of notation, we will call the mean-subtracted data $D$ as well.
3. Computes the $N_{\text{freq}}\times N_{\text{freq}}$ frequency covariance matrix, $C$, and performs a eigenvalue and eigenvector decomposition,
    $$A= V^{-1}CV,$$
where the $A$ is a diagonal matrix of eigenvalues of $C$ and $V$ contains $N_{\text{freq}}$ column vectors which represent the eigenvectors of the matrix $C$.
4. The eigenvalues and eigenvectors are sorted by decreasing order, from major to minor contribution to the variance of the image,
    $$A, V \longmapsto \widetilde{A}, \widetilde{V}.$$
5. We decide to keep only the first four components ($ncomp=4$), because our simulations have shown that this is the number which leads to the smallest reconstruction error. For that purpose, we define the following matrix,
    $$W = \widetilde{V}[:, :ncomp]\in \mathbb{R}^{N_{\text{freq}}\times ncomp}.$$
6. Finally, we project to the component space (with only four components) and then back to the image space, which contains almost all the foregrounds. The four component PCA image is named $F$ and it is corrected by the mean of the original data in order to get an unbiased result:
    $$F = WW^TD + \overline{D}.$$

#### Foreground removal step
Subtracting the 4-component PCA image to the original image, the residual would be the underlying 21 cm signal. In order to reduce the otherwise dominant noise, we decide to perform a Gaussian smoothing which have shown a better result when computing the 2d power spectrum.

The output of this step is a frequency-binned cube, in which the full frequency range of 90 MHz is divided into 15 MHz intervals required for the power spectrum estimation.

### 3. power_spectrum

The power spectrum allows us to study the distribution of fluctuations of the EoR signal at different scales (spatial or spectral). The HI signal from the EoR evolves with the frequency, i.e. with the redshift; yet, it can be considered isotropic at small frequency bins. Instrumental and foreground effects also evolve with the frequency but cannot be considered isotropic. For this reason, the cylindrical 2D power spectrum is used to analyse and correct line of sight effects while the spherical power spectrum is used for clean EoR signal. For more information see e.g. [1,2,3,4,5]

This step estimates the cylindrical power spectrum and its errors from 3D FITS images using the ps_eor python package (https://gitlab.com/flomertens/ps_eor). It takes as input the FITS files produced in the previous step, either using the polynomial fit or the PCA substaction method, and the PSF of the original image. The output are various text files with the power spectra and errors, following the submission format of the SDC3. A detailed description of the process followed in this step is given in the folder "workflow/power_spectrum". That folder, appart from the notebook for the PS estimation, includes another notebook to transform the images into the required format.

[1] Nithyanandan Thyagarajan et al 2013 ApJ 776 6<br>
[2] Giri, Sambit K., "Tomographic studies of the 21-cm signal during reionization: Going beyond the power spectrum", 978-91-7797-611-0<br>
[3] Zhaoting Chen, Emma Chapman, Laura Wolz, Aishrila Mazumder, Detecting the H i power spectrum in the post-reionization Universe with SKA-Low, Monthly Notices of the Royal Astronomical Society, Volume 524, Issue 3, September 2023, Pages 3724–3740, https://doi.org/10.1093/mnras/stad2102<br>
[4]  Joshua S. Dillon et al 2014 Phys. Rev. D 89, 023002<br>
[5] Liu, A. and Tegmark, M., “A method for 21 cm power spectrum estimation in the presence of foregrounds”, <i>Physical Review D</i>, vol. 83, no. 10, 2011. doi:10.1103/PhysRevD.83.103006.<br>

## File structure

```
.
├── config
│   └── config.yaml
│   └── configfile_data_PCA.ini
├── environment.yml
├── env_pseor.yml
├── LICENSE
├── README.md
└── workflow
    ├── create_mask
    │   ├── config
    │   │   ├── default.conv
    │   │   ├── default.nnw
    │   │   ├── default.param
    │   │   ├── default.psf
    │   │   ├── default.sex
    │   │   ├── gauss_4.0_7x7.conv
    │   │   └── mexhat_2.0_7x7.conv
    │   ├── mask.ipynb
    │   ├── pipeline.ipynb
    │   └── README.md
    ├── pca_substraction
    │   └── PCA_data_SDC3.ipynb
    │   └── PCA_functions.py
    │   └── README.md
    ├── polynomial_fit
    │   ├── PolyFit.py
    │   └── README.md
    └── power_spectrum
        └── PS_estimation_with_ps_eor.ipynb
```

After running the workflow, the results of each step will be stored in the `results` directory.
