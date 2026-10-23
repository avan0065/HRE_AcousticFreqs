
def plot_pchip_interpolation(D_fuelgrain, solaris_freqs):
    """
    Generates and displays a PCHIP interpolation plot using experimental hotfire data.

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
    import matplotlib.pyplot as plt
    from scipy.interpolate import PchipInterpolator

    # Sort data points by diameter (X-axis) for valid interpolation mapping
    sort_indices = np.argsort(D_fuelgrain)
    x_sorted = D_fuelgrain[sort_indices]
    y_sorted = solaris_freqs[sort_indices]

    # Define fine resolution grid over the data range for smooth curves
    x_fine = np.linspace(x_sorted.min(), x_sorted.max(), 300)

    # Apply the PCHIP interpolation method
    pchip_interp = PchipInterpolator(x_sorted, y_sorted)
    y_pchip = pchip_interp(x_fine)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.scatter(D_fuelgrain, solaris_freqs, color='black', s=60, zorder=5, label='Experimental Hotfire Points')
    plt.plot(x_fine, y_pchip, color='darkorange', linewidth=2.5, label='PCHIP Interpolation')

    plt.title('Interpolation Trends of Solaris Mk2 Hotfire Experimental Data')
    plt.xlabel('Fuel Grain Port Diameter (d) [m]')
    plt.ylabel('Frequency (f) [Hz]')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.show()

    return pchip_interp
