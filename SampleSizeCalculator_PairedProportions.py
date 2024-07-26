import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define constants
alpha = 0.05
beta = 0.20
P1 = 0.73
correlation = 0.5
Z_alpha = norm.ppf(1 - alpha / 2)
Z_beta = norm.ppf(1 - beta)

# Function to calculate the standard deviation of the difference
def calculate_sigma_d(P1, P2, correlation):
    return np.sqrt(P1 * (1 - P1) + P2 * (1 - P2) - 2 * correlation * np.sqrt(P1 * (1 - P1) * P2 * (1 - P2)))

# Function to calculate the required sample size, plus extra *2 factor to calculate exact amount of experiments
def calculate_sample_size(P1, P2, correlation, Z_alpha, Z_beta):
    delta = P2 - P1
    sigma_d = calculate_sigma_d(P1, P2, correlation)
    n = (( (Z_alpha + Z_beta) / (delta / sigma_d) ) ** 2)*2
    return np.ceil(n)  # Round up to the next whole number

# Define range of P2 values to investigate
P2_values = np.linspace(0.73, 0.99, 100)
sample_sizes = [calculate_sample_size(P1, P2, correlation, Z_alpha, Z_beta) for P2 in P2_values]

# Define y-tick values manually
y_ticks = [1, 10, 100, 1000, 10000, 100000]

# Find P2 values corresponding to n = 200, 100, 50
n_values = [200, 100, 50]
P2_values_for_n = []

for n in n_values:
    # Find the P2 value closest to the target n value
    closest_P2 = None
    smallest_diff = float('inf')
    for P2, size in zip(P2_values, sample_sizes):
        diff = abs(size - n)
        if diff < smallest_diff:
            smallest_diff = diff
            closest_P2 = P2
    P2_values_for_n.append(closest_P2)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(P2_values, sample_sizes, marker='o', linestyle='-')
plt.title('Required Sample Size for Different Kakarla 1 Proportions in AR group')
plt.xlabel('Augmented Reality Kakarla 1 proportion (P2)')
plt.ylabel('Required Sample Size (n)')
plt.grid(True, which="both", ls="--")

# Set y-axis to logarithmic scale and manually set y-tick values
plt.yscale('log')
plt.yticks(y_ticks, [str(y_tick) for y_tick in y_ticks])

# Indicate specific points with a red cross and add proportion text
for P2, n in zip(P2_values_for_n, n_values):
    plt.scatter(P2, n, color='red', marker='x', s=100)
    plt.text(P2, n, f'  n={n}\n  P2={P2:.2f}', color='red', fontsize=12)

# Indicate proportion of control group
plt.axvline(x=0.73, color='green', linestyle='--', label="Freehand Kakarla 1 proportion")

# Add x-axis label for P1 proportion
plt.text(0.727, 1000, 'Freehand Kakarla 1 proportion (P1): 0.73', color='green', fontsize=10, va='center', ha='center', rotation = 90)

plt.show()
