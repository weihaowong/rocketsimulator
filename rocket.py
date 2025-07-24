import numpy as np

class Rocket:
    def __init__(self, mass_empty, fuel_mass, thrust, burn_rate, area):
        #values from input 
        self.mass_empty = mass_empty
        self.fuel_mass = fuel_mass
        self.thrust = thrust
        self.burn_rate = burn_rate
        self.area = area

        #internal process values
        self.mass = mass_empty + fuel_mass
        self.position = np.array([0.0, 6378000.0+1.0])  
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.angle = 0.0 #0 means horizontal

    def burn(self, dt):
        if self.fuel_mass > 0:
            #fuel mass decreases as it burns over time, update mass 
            self.fuel_mass -= self.burn_rate * dt
            self.mass = self.mass_empty + self.fuel_mass
        else:
            self.thrust = 0
            self.fuel_mass = 0
    
    def thrust_vector(self):
        #thrust resolution into x and y directions based on angle
        tx = self.thrust * np.cos(self.angle)
        ty = self.thrust * np.sin(self.angle)
        return np.array([tx,ty])
    
    def update(self, net_force, dt):
        #update the acceleration, velocity and position from the net_force (which is calculated in other module) and mass
        self.acceleration = net_force / self.mass
        self.velocity += self.acceleration * dt
        if np.linalg.norm(self.position) - 6378000 < 0:
            self.position = (self.position / np.linalg.norm(self.position)) * 6378000
            self.acceleration = np.array([0.0,0.0])
            self.velocity = np.array([0.0,0.0])
        else:
            self.position += self.velocity * dt

    def set_angle(self, angle):
        #used to set our banking angle
        self.angle = angle

    








