import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import radon, iradon

# Create a simple 2D object (phantom)
size = 256
x, y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
circle = x <= 0.5

# Compute Radon transform (sinogram)
theta = np.linspace(0., 180., max(circle.shape), endpoint=False)
sinogram = radon(circle, theta=theta)

# Reconstruct using inverse Radon transform
reconstruction = iradon(sinogram, theta=theta, filter_name='ramp')

# Plot
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
ax1.set_title("Original Object")
ax1.imshow(circle, cmap='gray')
ax2.set_title("Sinogram")
ax2.imshow(sinogram, cmap='gray', aspect='auto')
ax3.set_title("Reconstruction")
ax3.imshow(reconstruction, cmap='gray')
plt.show()
