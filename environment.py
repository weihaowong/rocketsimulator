import numpy as np

class Environment:
    def __init__(self, sea_level_air_density, scale_height, planet_mass, planet_radius):
        self.sea_level_air_density = sea_level_air_density
        self.scale_height = scale_height
        self.planet_mass = planet_mass
        self.planet_radius = planet_radius

    def calculate_drag_force(self, drag_coefficient, area, altitude, velocity):
        rho = self.sea_level_air_density * np.exp(-(altitude)/self.scale_height)
        v = np.linalg.norm(velocity)
        if v == 0:
            direction = np.array([0,0])
        else:
            direction = -velocity/v

        drag_magnitude = 1/2 * rho * v*v * drag_coefficient * area
        drag = drag_magnitude * direction
        return drag
    
    def calculate_gravity(self, altitude):
        g = (6.6743e-11 * self.planet_mass) / (self.planet_radius + altitude)**2
        return g
    
    def calculate_gravitational_force(self, altitude, position, mass):
        gravitational_magnitude = mass * self.calculate_gravity(altitude) #magnitude
        displacement_from_center = np.linalg.norm(position)
        direction = -position / displacement_from_center
        gravitational_force = gravitational_magnitude * direction
        return gravitational_force





