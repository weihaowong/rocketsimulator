from rocket import Rocket
from environment import Environment
from angle import Angle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import sympy as sy


fig, ax = plt.subplots()
rocket_dot, = ax.plot([],[],"go")
trail_line, = ax.plot([],[], "g-", lw=1)
earth_radius = 6378000  # in meters
earth = Circle((0, 0), earth_radius, color='black')  # center at origin
ax.add_patch(earth)
ax.set_xlim(-1.2 * earth_radius, 1.2* earth_radius)
ax.set_ylim(-1.2* earth_radius, 1.2* earth_radius)
ax.set_aspect('equal')
ax.set_xlabel("Horizontal Position (m)")
ax.set_ylabel("Altitude (m)")
ax.set_title("Rocket Launch")
text = ax.text(0.05, 0.95, "", transform=ax.transAxes, fontsize = 10, verticalalignment = "top")

rocket = Rocket(
    mass_empty = 50000,           # kg (dry mass including structure & heat shield)
    fuel_mass = 500000,           # kg
    thrust = 12000000,              # N (6 Raptor engines: 3 sea level, 3 vacuum)
    burn_rate = 2000,               # kg/s (approximate)
    area = 9.0**2 * 3.1416 / 4     # m² (same 9 m diameter)
)

environment = Environment(
    sea_level_air_density = 1.225,
    scale_height = 8500,
    planet_mass = 5.972e24,
    planet_radius = 6378000
)

angle = Angle()

dt = 0.1

trail_x = []
trail_y = []

x_value = 0
rocket_angle = 0
x_increment = 0.3


while True:

    altitude = np.linalg.norm(rocket.position) - environment.planet_radius
    rocket.burn(dt=dt)
    thrust = rocket.thrust_vector()
    drag = environment.calculate_drag_force(drag_coefficient=0.125, area=rocket.area, altitude=altitude, velocity=rocket.velocity)
    environment.calculate_gravity(altitude=altitude)
    gravitational_force = environment.calculate_gravitational_force(altitude=altitude, position=rocket.position, mass=rocket.mass)
    net_force = thrust + drag + gravitational_force
    rocket.update(net_force=net_force, dt=dt)

    if rocket_angle <= 90:
        rocket_angle = angle.angle_function(x_value=x_value)
        rocket.set_angle(angle=np.radians(90+rocket_angle))
        x_value += x_increment
    else:
        rocket.set_angle(angle=np.radians(180))

    speed = np.linalg.norm(rocket.velocity)

    text.set_text(f"Altitude: {altitude}\nSpeed: {speed}\nFuel left: {rocket.fuel_mass}\nThrust: {rocket.thrust}\nDrag: {np.linalg.norm(drag)}")

    x = rocket.position[0]
    y = rocket.position[1]
    rocket_dot.set_data(x, y)

    trail_x.append(x)
    trail_y.append(y)
    trail_line.set_data(trail_x, trail_y)

    plt.pause(0.00000000000000001)
    if altitude < 0:
        break

plt.show()