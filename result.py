from rocket import Rocket
from environment import Environment
from angle import Angle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

#setting values for our rockets and environment
first_stage = Rocket(
    mass_empty = 25600 + 4000 + 3000,   # kg (first stage dry + second stage dry + fuel)
    fuel_mass = 385000,                 # kg (RP-1 + LOX for first stage)
    thrust = 7607000,                   # N (sea-level thrust from 9 Merlin 1D engines)
    burn_rate = 2500,                   # kg/s (approximate)
    area = 3.66 ** 2 * 3.1416 / 4       # m² (diameter ~3.66 m)
)

second_stage = Rocket(
    mass_empty = 4000,             # kg (dry mass)
    fuel_mass = 6000,             # kg (RP-1 + LOX)
    thrust = 934000,               # N (vacuum thrust from 1 Merlin 1D Vacuum engine)
    burn_rate = 250,               # kg/s (approximate)
    area = 3.66 ** 2 * 3.1416 / 4  # m² (same diameter as first stage)
)

environment = Environment(
    sea_level_air_density = 1.225,
    scale_height = 8500,
    planet_mass = 5.972e24,
    planet_radius = 6378000
)

angle = Angle()

#initializations
dt = 0.1

trail_x = []
trail_y = []

x_value = 0
rocket_angle = 0
x_increment = 0.3

first_stage_positions = []
first_stage_altitudes = []
first_stage_speeds = []
second_stage_positions = []
second_stage_altitudes = []
second_stage_speeds = []

time_elapsed = 0

#main loop for simulation
while True:

    #first stage operation
    altitude = np.linalg.norm(first_stage.position) - environment.planet_radius
    altitude2 = 0

    first_stage.burn(dt=dt)
    thrust = first_stage.thrust_vector()

    drag = environment.calculate_drag_force(drag_coefficient=0.125, area=first_stage.area, altitude=altitude, velocity=first_stage.velocity)
    environment.calculate_gravity(altitude=altitude)
    gravitational_force = environment.calculate_gravitational_force(altitude=altitude, position=first_stage.position, mass=first_stage.mass)
    net_force = thrust + drag + gravitational_force
    first_stage.update(net_force=net_force, dt=dt)

    if rocket_angle <= 90:
        rocket_angle = angle.angle_function(x_value=x_value)
        first_stage.set_angle(angle=np.radians(90+rocket_angle))
        x_value += x_increment
    else:
        first_stage.set_angle(angle=np.radians(180))

    first_stage_positions.append(first_stage.position.copy())
    first_stage_altitudes.append(altitude/1000)
    first_stage_speeds.append(np.linalg.norm(first_stage.velocity))

    #second stage operation
    if first_stage.fuel_mass < 1:
        if len(second_stage_positions) == 0:
            second_stage.position = first_stage.position.copy()
            second_stage.velocity = first_stage.velocity.copy()
            second_stage.set_angle(angle=np.radians(213))

        
        altitude2 = np.linalg.norm(second_stage.position) - environment.planet_radius

        second_stage.burn(dt=dt)
        thrust = second_stage.thrust_vector()

        drag = environment.calculate_drag_force(drag_coefficient=0.125, area=second_stage.area, altitude=altitude2, velocity=second_stage.velocity)
        environment.calculate_gravity(altitude=altitude2)
        gravitational_force = environment.calculate_gravitational_force(altitude=altitude2, position=second_stage.position, mass=second_stage.mass)
        net_force = thrust + drag + gravitational_force
        second_stage.update(net_force=net_force, dt=dt)

        second_stage_positions.append(second_stage.position.copy())
        second_stage_altitudes.append(altitude2/1000)
        second_stage_speeds.append(np.linalg.norm(second_stage.velocity))

    time_elapsed += dt
    if time_elapsed > 10000 or altitude2 < 0:
        break

first_stage_positions = np.array(first_stage_positions)
x1 = first_stage_positions[:, 0]
y1 = first_stage_positions[:, 1]

second_stage_positions = np.array(second_stage_positions)
x2 = second_stage_positions[:, 0]
y2 = second_stage_positions[:, 1]

###main plot of trajectory
plt.figure(figsize=(10, 10))
ax = plt.gca()
earth = Circle((0, 0), environment.planet_radius, color='cyan', zorder=0)
ax.add_patch(earth)

plt.plot(x1, y1, 'r-', label="1st Stage Trajectory", zorder=1)
plt.plot(x2, y2, 'b-', label="2nd Stage Trajectory", zorder=1)

ax.set_aspect('equal')
ax.relim()
ax.autoscale_view()

plt.title("Trajectory")
plt.legend()

###plot for individual properties
time1 = [i * dt for i in range(len(first_stage_altitudes))]
time2 = [i * dt for i in range(len(second_stage_altitudes))]
time3 = [i * dt for i in range(len(first_stage_speeds))]
time4 = [i * dt for i in range(len(second_stage_speeds))]

fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # 3 rows, 1 column

axs[0,0].plot(time1, first_stage_altitudes)
axs[0,0].set_title("First Stage Altitude vs Time")
axs[0,0].set_xlabel("Time (s)")
axs[0,0].set_ylabel("Altitude (m)")

axs[0,1].plot(time2, second_stage_altitudes)
axs[0,1].set_title("Second Stage Altitude vs Time")
axs[0,1].set_xlabel("Time (s)")
axs[0,1].set_ylabel("Altitude (m)")

axs[1,0].plot(time3, first_stage_speeds)
axs[1,0].set_title("First Stage Speed vs Time")
axs[1,0].set_xlabel("Time (s)")
axs[1,0].set_ylabel("Speed (ms^-1)")

axs[1,1].plot(time4, second_stage_speeds)
axs[1,1].set_title("Second Stage Speed vs Time")
axs[1,1].set_xlabel("Time (s)")
axs[1,1].set_ylabel("Speed (ms^-1)")

plt.tight_layout()
plt.show()
