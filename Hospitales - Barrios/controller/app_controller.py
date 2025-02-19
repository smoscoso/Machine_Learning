import threading
from utils.input_validator import InputValidator
from Model.ant_colony_optimization import AntColonyOptimization
from Model.hospital_distributor import HospitalDistributor
from utils.renderer import Renderer
from config import CELL_SIZE

class AppController:
    def __init__(self, view):
        self.view = view
        # Asignar comandos a los botones de la vista
        self.view.start_button.config(command=self.initialize_simulation)
        self.view.reset_button.config(command=self.reset)
        self.renderer = None
    
    def initialize_simulation(self):
        grid_size, neighborhoods, hospitals = self.view.get_input_values()
        valid, msg = InputValidator.validate_grid_inputs(grid_size, neighborhoods, hospitals)
        if not valid:
            self.view.display_error(msg)
            return
        n = int(grid_size)
        num_neighborhoods = int(neighborhoods)
        num_hospitals = int(hospitals)
        
        self.view.setup_simulation_area(n)
        self.view.set_progress(0)
        
        def run_simulation():
            # Callback para actualizar la barra de progreso
            def progress_callback(iteration, total):
                progress = int((iteration / total) * 100)
                self.view.root.after(0, lambda: self.view.set_progress(progress))
            
            ant_algo = AntColonyOptimization(n, num_hospitals)
            grid_result = ant_algo.optimize(progress_callback=progress_callback)
            
            # Inicializar Renderer para dibujar la cuadrícula
            renderer = Renderer(self.view.canvas, grid_result, CELL_SIZE, num_hospitals)
            self.renderer = renderer
            self.view.root.after(0, renderer.draw_grid)
            
            distributor = HospitalDistributor(grid_result, num_hospitals)
            updated_grid, assignments = distributor.distribute_neighborhoods(num_neighborhoods)
            self.view.root.after(0, lambda: self.renderer.update_grid(updated_grid))
            self.view.root.after(0, lambda: self.view.update_assignments(assignments))
            self.view.root.after(0, lambda: self.view.set_progress(100))
        
        thread = threading.Thread(target=run_simulation)
        thread.start()
    
    def reset(self):
        self.view.reset()
        self.renderer = None