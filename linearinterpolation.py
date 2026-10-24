
def plot_linear_interpolation(D_fuelgrain, solaris_freqs):
    """
    Fits a linear interpolation model using experimental hotfire data.

    Parameters
    ----------
    D_fuelgrain : array_like
        Experimental fuel grain port diameter values [m].
    solaris_freqs : array_like
        Experimental frequency values [Hz].

    Returns
    -------
    scipy.interpolate.interp1d
        The fitted linear interpolation model.
    """
    import numpy as np
    from scipy.interpolate import interp1d

    # Sort data points by diameter (X-axis) for valid interpolation mapping
    sort_indices = np.argsort(D_fuelgrain)
    x_sorted = D_fuelgrain[sort_indices]
    y_sorted = solaris_freqs[sort_indices]

    # Apply the PCHIP interpolation method
    linear_interp = interp1d(x_sorted, y_sorted)

    return linear_interp
