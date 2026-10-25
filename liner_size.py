
def acoustic_liner(freqs_pchip, freqs_linear, R, T_av):
    """
    Determines the optimal neck diameter for an acoustic liner cavity to target 
    the average frequency calculated from interpolation models.

    Parameters
    ----------
    freqs_pchip : array-like
        Interpolated frequency data array using the PCHIP method [Hz].
    freqs_linear : array-like
        Interpolated frequency data array using the Linear method [Hz].
    R : float
        Specific gas constant of the chamber mixture [J/(kg*K)].
    T_av : float
        Average combustion temperature [K].

    Returns
    -------
    best_diameter_m : float
        The optimal hole/neck diameter matching the target frequency [m].
    best_freq : float
        The calculated resonance frequency at the optimal diameter [Hz].
    """
    import numpy as np
    import math

    # Design target and parameters
    target_freq = np.mean([freqs_pchip.mean(), freqs_linear.mean()])
    c_gas = np.sqrt(1.18 * R * T_av)
    depth = 0.01 # depth of back cavity (between chamber wall and liner) [m]
    t_liner = 0.003 # thickness of liner [m]
    p_liner = 0.08 # porosity of the liner

    # Define the search range for hole diameters
    neck_diameters_mm = np.linspace(1.0, 10.0, 100)

    best_diameter_m = None
    best_freq = None
    min_deviation = float('inf')

    print(f"Optimal neck diameter to target: {target_freq:.2f} Hz\n")

    for d_mm in neck_diameters_mm:
        d_m = d_mm / 1000.0 # hole diameter in metres
        t_e = t_liner + 0.85 * d_m
        f_res = (c_gas / (2 * math.pi)) * np.sqrt(p_liner / (t_e * depth))

        deviation = abs(f_res - target_freq)
        if deviation < min_deviation:
            min_deviation = deviation
            best_diameter_m = d_m
            best_freq = f_res

    return best_diameter_m, best_freq
