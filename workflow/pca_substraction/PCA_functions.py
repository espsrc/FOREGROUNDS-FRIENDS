########################################################################################
# Functions to perform PCA decomposition of the SKA Data Challenge 3a cube.
# 
# Author: Miguel Ruiz-Granda on behalf of the FOREGROUNDS-FRIENDS team
########################################################################################

import numpy as np

def PCA_eig_decomposition(cube):
    """
    Compute the eigenvectors and eigenvalue decomposition necessary for the 
    Principal Component Analysis.

    :param cube: input data cube.
    :return cube: zero-mean data cube.
    :return mean_cube_2d: the mean of each slice of the cube.
    :return eigvals: the eigenvalues calculated from the covariance matrix.
    :return eigvecs: the eigenvectors calculated from the covariance matrix.
    """
    # Make each slide to have mean zero for both the signal and the full simulations
    mean_cube_2d =  np.mean(cube, axis=1)
    cube -= mean_cube_2d[:, np.newaxis]
    # Compute the covariance matrix
    cov = np.cov(cube) # (Nfreqs x Nfreqs)
    # Do eigendecomposition of covariance matrix
    eigvals, eigvecs = np.linalg.eig(cov)
    # Sort by eigenvalue
    idxs = np.argsort(eigvals)[::-1] # reverse order (biggest eigenvalue first)
    eigvals = eigvals[idxs]
    eigvecs = eigvecs[:,idxs]
    return cube, mean_cube_2d, eigvals, eigvecs

def PCA_solution(nmodes, eigvecs, cube2d, mean_cube2d):
    """
    Function that calculates the first nmodes PCA decomposition and projects them back 
    to the image space. This PCA solution contains in principle the majority of the foregrounds. 

    :param nmodes: number of modes to subtract.
    :param eigvecs: eigenvectors from the PCA decomposition.
    :param cube2d: data cube with dimensions nsamples x Npix**2.
    :param mean_cube2d: mean of each slice of cube2d.
    :return fg_amps: foreground amplitudes in the component space. It has dimensions of
                        Nmodes x Npix x Npix.
    :return fg_field: foreground amplitudes in the image space. It has dimensions of
                        Nfreq x Npix x Npix.
    """
    
    # Construct foreground filter operator by keeping only nmodes eigenmodes
    U_fg = eigvecs[:,:nmodes] # (Nfreqs, Nmodes)
    
    # Calculate foreground amplitudes for each line of sight
    fg_amps = np.dot(U_fg.T, cube2d) # (Nmodes, Npix**2)
    
    # Construct FG field and subtract from input data
    fg_field = np.dot(U_fg, fg_amps) + mean_cube2d[:, np.newaxis] # Operator times amplitudes + mean
    shape1 = (nmodes, int(np.sqrt(cube2d.shape[1])), int(np.sqrt(cube2d.shape[1])))
    shape2 = (int(cube2d.shape[0]), int(np.sqrt(cube2d.shape[1])), int(np.sqrt(cube2d.shape[1])))
    return fg_amps.reshape(shape1), fg_field.reshape(shape2)