import time
from airsim_wrapper import *

"""
Common-sense:

Tasks:
Take off please.
    
Fly 20 meters up.
    
Fly 30 meters forward.
    
Fly 10 meters to leftwards.
    
Fly to the solar panel. Remember to keep a 30-meter distance on the Z axis.
    
Great! Fly to a turbine (1), keep a 15m distance on the X axis.
    
Excellent. Now, fly to the turbine 2 and keep a 20m distance on the X-axis.
    
As a final task, I want you to hover 5 meters above the car.
    
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

    # Fly 20 meters up
    pose = aw.get_drone_position()
    aw.fly_to([pose[0], pose[1], pose[2] + 20])
    time.sleep(3)

    # Fly 30 meters forward
    pose = aw.get_drone_position()
    aw.fly_to([pose[0] + 30, pose[1], pose[2]])  
    time.sleep(3)

    # Fly 10 meters to the leftwards
    pose = aw.get_drone_position()
    aw.fly_to([pose[0], pose[1] - 10, pose[2]])
    time.sleep(3)

    # Fly to solar panels, keep 30 meters distance on the Z axis
    solarpanels_position = aw.get_position("solarpanels")
    aw.fly_to([solarpanels_position[0], solarpanels_position[1], solarpanels_position[2] + 30])
    time.sleep(3)
    
    # Fly to turbine1, keep 15m distance on the X axis
    turbine1_position = aw.get_position("turbine1")
    aw.fly_to([turbine1_position[0] - 15, turbine1_position[1], turbine1_position[2]])
    time.sleep(3)

    # Fly to turbine2, keep 20m distance on the X axis
    turbine2_position = aw.get_position("turbine2")
    aw.fly_to([turbine2_position[0] - 20, turbine2_position[1], turbine2_position[2]])
    time.sleep(3)

    # Hover 5 meters above the car
    car_position = aw.get_position("car")
    aw.fly_to([car_position[0], car_position[1], car_position[2] + 5])
    time.sleep(0.5)

    print("Done.")
    aw.client.stopRecording()       
    aw.client.enableApiControl(False)


if __name__ == '__main__':
    main()
