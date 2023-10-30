## Requirements:
Python 3.8 or greater
Numpy, Matplotlib, Astropy, tqdm, configparser, scipy, os

## Introduction:
In this step, we perform foreground removal of the data cube by applying a 4 component Principal Component Analysis (PCA) [Irfan & Bull. MNRAS, 2021].
This kind of analysis only uses frequency information and their correlation, losing the spatial information of the image.

The original data cube is $8\times 8$ degrees FoV, but in order to limit the noise, only the central $4 \times 4$ degrees are meant to be used for the power spectrum computation. For that reason, only this central part will be used as an input for the PCA cleaning step.

This step is implemented in the jupyter notebook PCA_data_SDC3.ipynb.
## Description of the algorithm:
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

## Foreground removal step:
Subtracting the 4-component PCA image to the original image, the residual would be the underlying 21 cm signal. In order to reduce the otherwise dominant noise, we decide to perform a Gaussian smoothing which have shown a better result when computing the 2d power spectrum.

The output of this step is a frequency-binned cube, in which the full frequency range of 90 MHz is divided into 15 MHz intervals required for the power spectrum estimation.
