from rocket import Rocket
from environment import Environment
from angle import Angle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

#setting values for our rockets and environment

first_stage = Rocket(
    mass_empty = 3000+200+3385,           # kg
    fuel_mass = 30150,           # kg
    thrust = 318000,             # N
    burn_rate = 178.3,           # kg/s (approx: fuel_mass / burn_time)
    area = 1.68                  # m^2 (approx diameter of 1.68 m)
)

# Falcon 1 Second Stage
second_stage = Rocket(
    mass_empty = 200,            # kg
    fuel_mass = 3385,            # kg
    thrust = 31000,              # N
    burn_rate = 11.28,           # kg/s (approx: fuel_mass / burn_time)
    area = 1.68                  # m^2 (same diameter as first stage)
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

separation_altitude = 0

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

    #gravity turn method
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
        #start second stage with initialization
        if len(second_stage_positions) == 0:
            separation_altitude = ((np.linalg.norm((first_stage.position)) - environment.planet_radius) / 1000)
            second_stage.position = first_stage.position.copy()
            second_stage.velocity = first_stage.velocity.copy()
            second_stage.set_angle(angle=np.radians(175))

        altitude2 = np.linalg.norm(second_stage.position) - environment.planet_radius
        
        speed = np.linalg.norm(second_stage.velocity)

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

        second_stage_apogee = max(second_stage_altitudes)

    time_elapsed += dt

    if time_elapsed > 6000 or altitude2 < 0:
        break

first_stage_positions = np.array(first_stage_positions)
x1 = first_stage_positions[:, 0]
y1 = first_stage_positions[:, 1]

second_stage_positions = np.array(second_stage_positions)
x2 = second_stage_positions[:, 0]
y2 = second_stage_positions[:, 1]

###trajectory plot
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


###telemetry plot
time1 = [i * dt for i in range(len(first_stage_altitudes))]
time2 = [i * dt for i in range(len(second_stage_altitudes))]
time3 = [i * dt for i in range(len(first_stage_speeds))]
time4 = [i * dt for i in range(len(second_stage_speeds))]

fig, axs = plt.subplots(3, 2, figsize=(12, 10))

axs[0,0].plot(time1, first_stage_altitudes)
axs[0,0].set_title("First Stage Altitude vs Time")
axs[0,0].set_xlabel("Time (s)")
axs[0,0].set_ylabel("Altitude (km)")

axs[0,1].plot(time2, second_stage_altitudes)
axs[0,1].set_title("Second Stage Altitude vs Time")
axs[0,1].set_xlabel("Time (s)")
axs[0,1].set_ylabel("Altitude (km)")

axs[1,0].plot(time3, first_stage_speeds)
axs[1,0].set_title("First Stage Speed vs Time")
axs[1,0].set_xlabel("Time (s)")
axs[1,0].set_ylabel("Speed (ms^-1)")

axs[1,1].plot(time4, second_stage_speeds)
axs[1,1].set_title("Second Stage Speed vs Time")
axs[1,1].set_xlabel("Time (s)")
axs[1,1].set_ylabel("Speed (ms^-1)")

axs[2, 0].axis('off')
axs[2, 1].axis('off')

telemetry1 =  f"""
First Stage:
Apogee: {max(first_stage_altitudes)} km
Max Speed: {max(first_stage_speeds)} ms-1
Separation Altitude: {separation_altitude} km"""

telemetry2 = f"""
Second Stage:
Apogee: {max(second_stage_altitudes)} km
Perigee: {min(second_stage_altitudes)} km
Max Speed: {max(second_stage_speeds)} ms-1
Average Speed: {(sum(second_stage_speeds) / len(second_stage_speeds))} ms-1"""

axs[2, 0].text(0.01, 1.0, telemetry1, fontsize=10, va='top', ha='left', linespacing=1.4, wrap=True)
axs[2, 1].text(0.01, 1.0, telemetry2, fontsize=10, va='top', ha='left', linespacing=1.4, wrap=True)

plt.tight_layout()
plt.show()
