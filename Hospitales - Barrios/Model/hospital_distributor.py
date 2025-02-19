# model/hospital_distributor.py

import random

class HospitalDistributor:
    def __init__(self, grid, num_hospitals):
        """
        grid: Matriz (NumPy array) con la distribución de hospitales.
        num_hospitals: Número de hospitales (valores 1 a num_hospitals en la grid).
        """
        self.grid = grid
        self.n = grid.shape[0]
        self.num_hospitals = num_hospitals
        self.assignments = {}  # Diccionario: {número_barrio: número_hospital}
    
    def distribute_neighborhoods(self, num_neighborhoods):
        """
        Distribuye 'num_neighborhoods' barrios alrededor de los hospitales.
        Retorna la cuadrícula actualizada y el diccionario de asignaciones.
        """
        neighborhood_count = 1
        hospitals = [(i, j) for i in range(self.n) 
                           for j in range(self.n)
                           if 0 < self.grid[i, j] <= self.num_hospitals]
        for _ in range(num_neighborhoods):
            if not hospitals:
                break
            hi, hj = random.choice(hospitals)
            hospital_num = self.grid[hi, hj]
            # Buscar celdas vecinas libres (incluyendo diagonales)
            neighbors = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = hi + di, hj + dj
                    if 0 <= ni < self.n and 0 <= nj < self.n and self.grid[ni, nj] == 0:
                        neighbors.append((ni, nj))
            if neighbors:
                ni, nj = random.choice(neighbors)
                self.grid[ni, nj] = self.num_hospitals + neighborhood_count
                self.assignments[neighborhood_count] = hospital_num
                neighborhood_count += 1
        return self.grid, self.assignments
