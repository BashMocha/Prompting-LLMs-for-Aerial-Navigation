import time
from airsim_wrapper import *

"""
Logical reasoning:

Tasks:
Take off please.
    
Fly 30 meters up.
    
Now I want you to draw a circle with 45 meters radius, you can use the math.cos() and math.sin() functions to calculate the points of the circle. Remember that the drone has a width of 2 meters.
    
!exit
"""

def main():
    print("Initializing AirSim...")
    aw = AirSimWrapper()

    # Recording trajectory
    aw.client.startRecording()

    # Take off
    aw.takeoff()
    time.sleep(3)

    # Fly 30 meters up
    pose = aw.get_drone_position()
    aw.fly_to([pose[0], pose[1], pose[2] + 30])
    time.sleep(3)

    # Draw a circle with 45 meters radius
    circle_points = []
    center = aw.get_drone_position()
    for i in range(0, 360, 1):
        x = center[0] + 51 * math.cos(math.radians(i))
        y = center[1] - 51 * math.sin(math.radians(i))
        z = center[2]
        circle_points.append([x, y, z])
    aw.fly_path(circle_points)
    time.sleep(3)
    
    print("Done.")
    aw.client.stopRecording()       
    aw.client.enableApiControl(False)


if __name__ == '__main__':
    main()
