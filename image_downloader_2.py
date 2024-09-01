
import requests
import bz2
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage import exposure

path_git = "/mnt/c/Users/Chemito/Documents/GitHub/astroinfo-tools"
path_astro = "/mnt/c/Users/Chemito/Desktop/astrostuff"

# Define URLs for FITS files
fits_urls = [
    f"https://data.sdss.org/sas/dr16/eboss/photoObj/frames/301/1000/6/frame-r-001000-6-00{28 + i}.fits.bz2" for i in range(3) #TODO: Lo cambie a 3 para testear mas rapido, cambiar a 50
]

# Function to download and decompress FITS files
def download_fits(url, filename):
    response = requests.get(url)
    compressed_filename = filename + '.bz2'
    with open(compressed_filename, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {compressed_filename}")
    
    # Decompress the file
    with bz2.BZ2File(compressed_filename, 'rb') as compressed_file:
        with open(filename, 'wb') as decompressed_file:
            decompressed_file.write(compressed_file.read())
    print(f"Decompressed {filename}")

# Download and decompress the FITS files
for i, url in enumerate(fits_urls):
    download_fits(url, f"img_new/image_{i+1}.fits")

# Open, apply Gaussian filter, and save FITS files

### Imágenes generadas ahora quedan en carpetas (Deben existir para que funcione)  ##
### Resalta estrellas en distinto color (rojo) ###

for i in range(len(fits_urls)):
    try:
        with fits.open(f"img_new/image_{i+1}.fits") as hdul:
            hdul.info()
            image_data = hdul[0].data
            
            # Apply Gaussian filter
            filtered_image_data = gaussian_filter(image_data, sigma=2)
            
            # Save the filtered image with a more noticeable color map
            plt.figure()
            plt.imshow(filtered_image_data, cmap='hot')  # Cambiar cmap para hacer que las estrellas sean más notorias
            plt.colorbar()  # Agregar una barra de color para referencia
            plt.savefig(f"img_filter_new/filtered_image_{i+1}.png")  # Guardar la imagen filtrada como PNG
            plt.close()  # Cerrar la figura para liberar memoria
            print(f"Saved filtered_image_{i+1}.png")
    except OSError as e:
        print(f"Error opening image_{i+1}.fits: {e}")