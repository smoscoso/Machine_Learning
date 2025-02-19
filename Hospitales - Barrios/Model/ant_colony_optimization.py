import numpy as np
import random
from config import NUM_ITERACIONES, TASA_EVAPORACION

class AntColonyOptimization:
    def __init__(self, n, num_hospitals):
        """
        n: Tamaño de la cuadrícula (n x n)
        num_hospitals: Número de hospitales a distribuir
        """
        self.n = n
        self.num_hospitals = num_hospitals
        self.grid = np.zeros((n, n), dtype=int)
    
    def evaluate_distribution(self, grid):
        """
        Evalúa la calidad de la distribución calculando la distancia promedio mínima 
        desde cada celda a algún hospital.
        """
        hospitals = np.argwhere((grid > 0) & (grid <= self.num_hospitals))
        if len(hospitals) == 0:
            return float('inf')
        total_distance = 0
        for i in range(self.n):
            for j in range(self.n):
                total_distance += min(np.linalg.norm([i, j] - h) for h in hospitals)
        return total_distance / (self.n * self.n)
    
    def optimize(self, progress_callback=None):
        """
        Ejecuta el algoritmo y retorna la cuadrícula resultante con la mejor distribución.
        Si se proporciona progress_callback(iteracion, total), se llama en cada iteración.
        """
        pheromones = np.ones((self.n, self.n))
        best_grid = None
        best_score = float('inf')
        positions = [(i, j) for i in range(self.n) for j in range(self.n)]
        
        for iteration in range(NUM_ITERACIONES):
            grid = np.zeros((self.n, self.n), dtype=int)
            probabilities = pheromones.flatten() / pheromones.sum()
            selected = random.choices(positions, weights=probabilities, k=self.num_hospitals)
            for idx, (i, j) in enumerate(selected, 1):
                grid[i, j] = idx
            score = self.evaluate_distribution(grid)
            if score < best_score:
                best_score = score
                best_grid = grid.copy()
            # Actualizar feromonas
            pheromones *= TASA_EVAPORACION
            for i, j in zip(*np.where(grid > 0)):
                if score > 0:
                    pheromones[i, j] += 1 / score
            
            # Notificar progreso
            if progress_callback:
                progress_callback(iteration + 1, NUM_ITERACIONES)
        
        self.grid = best_grid
        return self.grid
