
def plot_akima_interpolation(D_fuelgrain, solaris_freqs):
    """
    Fits an Akima interpolation model using experimental hotfire data.

    Parameters
    ----------
    D_fuelgrain : array_like
        Experimental fuel grain port diameter values [m].
    solaris_freqs : array_like
        Experimental frequency values [Hz].

    Returns
    -------
    scipy.interpolate.Akima1DInterpolator
        The fitted Akima interpolation model.
    """
    import numpy as np
    from scipy.interpolate import Akima1DInterpolator

    # Sort data points by diameter (X-axis) for valid interpolation mapping
    sort_indices = np.argsort(D_fuelgrain)
    x_sorted = D_fuelgrain[sort_indices]
    y_sorted = solaris_freqs[sort_indices]

    # Apply the Akima interpolation method
    akima_interp = Akima1DInterpolator(x_sorted, y_sorted)

    return akima_interp
