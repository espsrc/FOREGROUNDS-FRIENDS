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

TBD

## Workflow

The workflow consists of four stages

### create_mask

Describe process [TBD]

### polynomial_fit

This script applies a polynomial fit to the real and imaginary parts of the fast Fourier transform (FFT) of the images, which are in FITS format and have 901 channels (106 MHz to 196 MHz with 0.1MHz channel width) and 2048x2048 pixels each.
It also performs foreground removal and image reconstruction. 

#### Requirements

Python 3.6 or higher
numpy
astropy

#### Usage
python PolyFit.py <input_file> <output_file> <degree> <log>

where:

<input_file> is the name of the FITS file containing the image cube
<output_file> is the name of the FITS file where the reconstructed image cube will be saved
<degree> is the degree of the polynomial to fit to the FFT
<log> is a boolean flag indicating whether to use log-log space (True) or linear space (False) for the polynomial fit

#### Example
python polyfit_fft.py ZW3.image_cube.fits /home/user/ 3 True

This will apply a third-degree polynomial fit to the FFT of each pixel in log-log space, remove the foregrounds, and save the output files to /home/user .

#### Output
The script will generate several temporary files to save RAM memory. These files will be removed at the end.
The script will save each slice of the reconstructed cube to a FITS file into the directory specified by the user.

### pca_substraction

Describe process [TBD]

### power_spectrum

Describe process [TBD]



## File structure

```
.
├── config
│   └── config.yaml
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
    │   └── PCA_real_data.ipynb
    ├── polynomial_fit
    │   ├── PolyFit.py
    │   └── README.md
    └── power_spectrum
        └── PS_estimation_with_ps_eor.ipynb
```

After running the workflow, the results of each step will be stored in the `results` directory.
