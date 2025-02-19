# utils/renderer.py

import tkinter as tk
from utils.asset_manager import AssetManager

class Renderer:
    def __init__(self, canvas, grid, cell_size, num_hospitals):
        """
        canvas: Objeto Canvas de Tkinter donde se dibuja la cuadrícula.
        grid: Matriz (NumPy array) con la distribución actual.
        cell_size: Tamaño en píxeles de cada celda.
        num_hospitals: Número de hospitales para diferenciar elementos.
        """
        self.canvas = canvas
        self.grid = grid
        self.cell_size = cell_size
        self.num_hospitals = num_hospitals
        self.asset_manager = AssetManager(cell_size)
        self.hospital_img = self.asset_manager.hospital_image
        self.neighborhood_img = self.asset_manager.neighborhood_image
    
    def draw_grid(self):
        """
        Dibuja la cuadrícula completa. 
        Para cada celda:
          - Si está vacía, dibuja un rectángulo con color blanco.
          - Si contiene un hospital (valor 1 a num_hospitals), dibuja la imagen y el texto "Hospital (n)".
          - Si contiene un barrio (valor > num_hospitals), dibuja la imagen y el texto "Barrio (n)".
        """
        self.canvas.delete("all")
        n = self.grid.shape[0]
        line_color = "#dddddd"  # Color suave para la cuadrícula
        font_family = ("Helvetica", 9)
        
        for i in range(n):
            for j in range(n):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                value = self.grid[i, j]
                
                # Dibujar fondo de la celda
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ffffff", outline=line_color)
                
                if value == 0:
                    # Celda vacía (sin imagen ni texto)
                    continue
                elif 1 <= value <= self.num_hospitals:
                    # Celda de hospital
                    x_center = x1 + self.cell_size // 2
                    y_center = y1 + (self.hospital_img.height() // 2) + 5
                    self.canvas.create_image(x_center, y_center, image=self.hospital_img)
                    
                    # Texto debajo de la imagen
                    text_y = y_center + (self.hospital_img.height() // 2) + 10
                    self.canvas.create_text(x_center, text_y,
                                            text=f"Hospital ({int(value)})",
                                            font=font_family, fill="#333333")
                else:
                    # Celda de barrio
                    barrio_num = int(value - self.num_hospitals)
                    x_center = x1 + self.cell_size // 2
                    y_center = y1 + (self.neighborhood_img.height() // 2) + 5
                    self.canvas.create_image(x_center, y_center, image=self.neighborhood_img)
                    
                    # Texto debajo de la imagen
                    text_y = y_center + (self.neighborhood_img.height() // 2) + 10
                    self.canvas.create_text(x_center, text_y,
                                            text=f"Barrio ({barrio_num})",
                                            font=font_family, fill="#333333")
        
        # Dibujar líneas finales de la cuadrícula (verticales y horizontales)
        for i in range(n + 1):
            self.canvas.create_line(0, i * self.cell_size, n * self.cell_size, i * self.cell_size, fill=line_color)
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, n * self.cell_size, fill=line_color)
    
    def update_grid(self, new_grid):
        """
        Actualiza la cuadrícula y la redibuja.
        """
        self.grid = new_grid
        self.draw_grid()
