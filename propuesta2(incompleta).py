import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, filters
from skimage.transform import resize
from skimage.util import random_noise


# Imagen
img = io.imread("satelite.png")

if img.shape[2] == 4:
    img = img[:,:,:3]

img = color.rgb2gray(img)
img = resize(img,(128,128))

noisy = random_noise(img, mode='gaussian', var=0.01)
Y = noisy.copy()

# Parametros

lambda_data = 4.0
lambda_smooth = 0.8
iterations = 10

h, w = Y.shape

# valores posibles de pixel
values = np.linspace(0, 1, 256)

# Gibbs Sampling
for it in range(iterations):

    for i in range(1, h-1):
        for j in range(1, w-1):
 
            energies = []

            for v in values:
                data_term = lambda_data*(v - noisy[i, j])**2
                neighbors = [
                    Y[i-1, j],
                    Y[i+1, j],
                    Y[i, j-1],
                    Y[i, j+1],
                    Y[i-1, j-1],
                    Y[i-1, j+1],
                    Y[i+1, j-1],
                    Y[i+1, j+1]
                ]

                smooth_term = sum((v-n)**2 for n in neighbors)
                smooth_term *= lambda_smooth

                E = data_term + smooth_term
                energies.append(E)

            energies = np.array(energies)
            probs = np.exp(-energies)
            probs /= probs.sum()
            Y[i, j] = np.random.choice(values, p=probs)

    print("Iteración:", it)


threshold = filters.threshold_otsu(Y)

segmentation = Y > threshold

reconstructed = Y

##############################################################################

plt.figure(figsize=(14, 4))

plt.subplot(1, 4, 1)
plt.title("Imagen original")
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1, 4,  2)
plt.title("Imagen con ruido")
plt.imshow(noisy, cmap='gray')
plt.axis('off')

plt.subplot(1, 4, 3)
plt.title("Reconstrucción (MRF)")
plt.imshow(reconstructed, cmap='gray')
plt.axis('off')

plt.subplot(1, 4, 4)
plt.title("Segmentación")
plt.imshow(segmentation, cmap='gray')
plt.axis('off')

plt.show()