import numpy as np
import pytest
from oscillations import primary_oscillation
from pchipinterpolation import plot_pchip_interpolation
from akimainterpolation import plot_akima_interpolation
from linearinterpolation import plot_linear_interpolation
from liner_size import acoustic_liner

def test_primary_oscillation_trends():
    # Test inputs
    mdot = 1.5
    OF_ratio = 6
    P_c = 1500000
    L = 0.36
    R = 302.3
    T_av = 2700
    D_min = np.array([0.045, 0.05, 0.08])

    # Calculate frequencies
    freqs = primary_oscillation(mdot, OF_ratio, P_c, L, R, T_av, D_min)

    assert len(freqs) == len(D_min), "Output length must match input diameter length."
    # Frequency should decrease as port diameter increases (since mass flux G_0 decreases)
    assert freqs[0] > freqs[1], "Frequencies must decrease as diameter increases."
    assert freqs[1] > freqs[2], "Frequencies must decrease as diameter increases."

def test_interpolations_at_knots():
    # Set up experimental data points
    D_fuelgrain = np.array([0.045, 0.05, 0.083])
    solaris_freqs = np.array([884.77, 612.97, 222.66])

    # Fit models
    linear_model = plot_linear_interpolation(D_fuelgrain, solaris_freqs)
    pchip_model = plot_pchip_interpolation(D_fuelgrain, solaris_freqs)
    akima_model = plot_akima_interpolation(D_fuelgrain, solaris_freqs)

    # Interpolation must perfectly pass through experimental data knots
    for i, d in enumerate(D_fuelgrain):
        assert np.isclose(linear_model(d), solaris_freqs[i]), f"Linear interp failed at d={d}"
        assert np.isclose(pchip_model(d), solaris_freqs[i]), f"PCHIP interp failed at d={d}"
        assert np.isclose(akima_model(d), solaris_freqs[i]), f"Akima interp failed at d={d}"

def test_acoustic_liner_dimensions():
    # Setup dummy arrays for frequencies
    freqs_pchip = np.array([400.0, 395.0, 390.0])
    freqs_linear = np.array([402.0, 396.0, 391.0])
    R = 302.3
    target_freq, best_diameter_m, best_freq = acoustic_liner(freqs_pchip, freqs_linear, R)

    # Verify target frequency is calculated and positive
    assert target_freq > 0, "Target frequency must be positive."
    # Verify that the returned optimal neck diameter is within physically realistic bounds for a physical injector/liner cavity (e.g. between 1mm and 50mm)
    assert best_diameter_m is not None, "Optimal diameter should not be None."
    assert 0.001 <= best_diameter_m <= 0.050, f"Calculated liner hole diameter {best_diameter_m*1000:.2f} mm is outside acceptable 1-50 mm limits."
    # Verify the resonance frequency matches well with the target
    assert np.isclose(best_freq, target_freq, rtol=0.1), "Resonance frequency must be close to target frequency."
