import numpy as np

# Input Parameters
# Steel properties
E = 209e9  # Young's Modulus (Pa)
G = E / (2 * (1 + 0.3))  # Shear Modulus (Pa), assuming Poisson's ratio = 0.3
yield_strength = 355e6  # Yield strength (Pa)

# Dimensions of the lifting lug (converted to meters)
a = 75e-3  # Height of the first rectangle (m)
b = 40e-3  # Width of the rectangles (m)
t = 30e-3  # Thickness of the lifting lug (m)
c = 32.5e-3  # Height of the second rectangle (m)

# Load parameters
mass_GCU = 36000  # Mass of GCU (kg)
g = 9.81  # Gravity (m/s^2)
total_load = mass_GCU * g  # Total weight (N)

# Equally distributed load among 6 lugs
lug_load = total_load / 6

# Timoshenko beam parameters
def calc_area(height, width):
    """Calculate the cross-sectional area."""
    return height * width

def calc_moment_of_inertia(height, width):
    """Calculate the moment of inertia for a rectangular section."""
    return (width * height**3) / 12

def calc_shear_coefficient():
    """Shear coefficient for a rectangular cross-section (Timoshenko theory)."""
    return 6 / 5  # Approximate for a rectangle

# Areas
area1 = calc_area(a, t)
area2 = calc_area(c, t)
total_area = area1 + area2

# Moments of inertia
I1 = calc_moment_of_inertia(a, t)
I2 = calc_moment_of_inertia(c, t)

# Shear coefficients
k1 = calc_shear_coefficient()
k2 = calc_shear_coefficient()

# Shear deformation contribution
shear_deflection1 = lug_load * a / (k1 * G * area1)
shear_deflection2 = lug_load * c / (k2 * G * area2)

# Bending deformation contribution
bending_deflection1 = (lug_load * a**3) / (3 * E * I1)
bending_deflection2 = (lug_load * c**3) / (3 * E * I2)

# Total deflection
total_deflection = bending_deflection1 + shear_deflection1 + bending_deflection2 + shear_deflection2

# Maximum von Mises stress in the rectangles
stress1 = lug_load / area1
stress2 = lug_load / area2

# Evaluate stress at the transition between rectangles
# The bending moment at the interface
M_interface = lug_load * a  # Moment at the base of the first rectangle
I_interface = I1  # Approximate moment of inertia at the interface

# Stress at the transition region (maximum bending stress at the interface)
stress_transition = M_interface * (a / 2) / I_interface  # σ = M*y/I

# Combine bending stress and shear stress using von Mises criteria
shear_stress_transition = lug_load / area1
von_mises_transition = np.sqrt(stress_transition**2 + 3 * shear_stress_transition**2)

# Breaking strength with and without safety factor
breaking_strength_no_sf = yield_strength
breaking_strength_with_sf = yield_strength / 5

# Safety checks
is_safe_no_sf = von_mises_transition < breaking_strength_no_sf
is_safe_with_sf = von_mises_transition < breaking_strength_with_sf

# Output Results
print("Results (Timoshenko Beam Theory with Transition Stress):")
print(f"Total Vertical Deflection at the end of the lug: {total_deflection:.6e} m")
print(f"Bending Deflection: {bending_deflection1 + bending_deflection2:.6e} m")
print(f"Shear Deflection: {shear_deflection1 + shear_deflection2:.6e} m")
print(f"Maximum von Mises Stress at Transition: {von_mises_transition:.6e} Pa")
print(f"Breaking Strength (No Safety Factor): {breaking_strength_no_sf:.6e} Pa")
print(f"Breaking Strength (With Safety Factor): {breaking_strength_with_sf:.6e} Pa")
print(f"Is the design safe without safety factor? {'Yes' if is_safe_no_sf else 'No'}")
print(f"Is the design safe with safety factor? {'Yes' if is_safe_with_sf else 'No'}")
