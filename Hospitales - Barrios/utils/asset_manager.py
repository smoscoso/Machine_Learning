# utils/asset_manager.py

from PIL import Image, ImageTk

class AssetManager:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        
        # Ajustar el factor de escalado para que las imágenes no queden muy grandes
        scaling_factor = 0.7  # Porcentaje del tamaño de la celda
        desired_size = int(cell_size * scaling_factor)
        
        # Cargar y redimensionar la imagen del hospital
        hospital_img = Image.open("assets/hospital.png")
        hospital_img = hospital_img.resize((desired_size, desired_size), Image.Resampling.LANCZOS)
        self.hospital_image = ImageTk.PhotoImage(hospital_img)
        
        # Cargar y redimensionar la imagen del barrio
        neighborhood_img = Image.open("assets/neighborhood.png")
        neighborhood_img = neighborhood_img.resize((desired_size, desired_size), Image.Resampling.LANCZOS)
        self.neighborhood_image = ImageTk.PhotoImage(neighborhood_img)
