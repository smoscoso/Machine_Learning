# utils/input_validator.py

class InputValidator:
    @staticmethod
    def validate_grid_inputs(grid_size, neighborhoods, hospitals):
        """
        Valida que los parámetros sean enteros y que la suma de barrios y hospitales
        no exceda el número total de celdas de la cuadrícula.
        """
        try:
            n = int(grid_size)
            num_neighborhoods = int(neighborhoods)
            num_hospitals = int(hospitals)
        except ValueError:
            return False, "Todos los parámetros deben ser números enteros."
        if n < 1:
            return False, "El tamaño de la cuadrícula debe ser al menos 1."
        if num_neighborhoods < 1:
            return False, "El número de barrios debe ser al menos 1."
        if num_hospitals < 1:
            return False, "El número de hospitales debe ser al menos 1."
        if num_neighborhoods + num_hospitals > n * n:
            return False, "La suma de barrios y hospitales no puede exceder el número de celdas de la cuadrícula."
        return True, ""
