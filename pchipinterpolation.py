
def plot_pchip_interpolation(D_fuelgrain, solaris_freqs):
    """
    Fits a PCHIP interpolation model using experimental hotfire data.

    Parameters
    ----------
    D_fuelgrain : array_like
        Experimental fuel grain port diameter values [m].
    solaris_freqs : array_like
        Experimental frequency values [Hz].

    Returns
    -------
    scipy.interpolate.PchipInterpolator
        The fitted PCHIP interpolation model.
    """
    import numpy as np
    from scipy.interpolate import PchipInterpolator

    # Sort data points by diameter (X-axis) for valid interpolation mapping
    sort_indices = np.argsort(D_fuelgrain)
    x_sorted = D_fuelgrain[sort_indices]
    y_sorted = solaris_freqs[sort_indices]

    # Apply the PCHIP interpolation method
    pchip_interp = PchipInterpolator(x_sorted, y_sorted)

    return pchip_interp
