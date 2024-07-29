import time
from airsim_wrapper import *

"""
Long context capturing:

Tasks:
I want you to perform multiple tasks in an order, one by one. Take off, fly up 30 meters, and fly 20 meters forward. Rotate the drone 180 degrees and then, fly 20 meters forward to return your original position.
    
Excellent, I want to inspect the car from three different points on the X axis. You can inspect the car from the front, back, and right side from 20 meters away on the X-axis. After examining the car from a point, wait three seconds and move to the next point. Finally set yaw to zero.

Great! I want you to fly to the turbine 1 until 15m distance on the X axis in the negative direction, and reach an altitude of 50 meters. Remember that you are on the front side of the turbine right now. Right after that, lower your altitude to 30 meters and fly to the next turbine until 15-meter distance in the negative direction, and reach an altitude of 50 meters again.
    
Let's inspect this turbine, perform the following tasks in an order, one by one. I want you to move backwards 15 meters on the X axis, wait for 3 seconds and fly back to your first position. After that you'll repeat the process for the backside of the turbine in the following instructions. You should fly 10 meters rightwards, 30 meters forward, 10 meters leftwards and then set yaw to zero to inspect the turbine from the backside. Finally move 10 meters forward, and wait for 3 seconds.
 
Amazing! As a final task, lower your altitude to 25 meters to not to hit the wheel of the turbine and then land the drone 10 meters away from the car on the X-axis.
    
!exit
"""

def main():
    print("Initializing AirSim...")
    aw = AirSimWrapper()

    # Recording trajectory
    aw.client.startRecording()

    # Take off and fly up 30 meters and fly 20 meters forward. 
    # Rotate the drone 180 degrees and then, fly 20 meters back to return your original position.
    # Finally rotate the drone 180 degrees again.
    aw.takeoff()
    pose = aw.get_drone_position()
    aw.fly_to([pose[0], pose[1], pose[2] + 30])
    pose = aw.get_drone_position()
    aw.fly_to([pose[0] + 20, pose[1], pose[2]])
    yaw = aw.get_yaw()
    aw.set_yaw(yaw + 180)
    aw.fly_to([pose[0], pose[1], pose[2]])
    yaw = aw.get_yaw()
    aw.set_yaw(0)
    time.sleep(3)
    
    # Inspect the car from three different points on the X axis. 
    # Inspect the car from the front, back, and right side from 20 meters away on the X-axis.
    car_position = aw.get_position("car")
    aw.fly_to([car_position[0] + 20, car_position[1], car_position[2]])
    time.sleep(3)
    aw.fly_to([car_position[0] - 20, car_position[1], car_position[2]])
    time.sleep(3)
    aw.fly_to([car_position[0], car_position[1] + 20, car_position[2]])
    time.sleep(3)
    aw.set_yaw(0)
    time.sleep(3)

    # Fly to the turbine1, keep 15m distance on the X axis and reach an altitude of 50 meters. 
    # Right after that, lower your altitude by 35 meters to nat to hit the turning wheels of the turbine and fly to the next turbine, keep 20 meters distance like you just did and reach an altitude of 50 meters again.
    turbine1_position = aw.get_position("turbine1")
    aw.fly_to([turbine1_position[0] - 15, turbine1_position[1], 50])
    aw.fly_to([turbine1_position[0] - 15, turbine1_position[1], 15])
    
    turbine2_position = aw.get_position("turbine2")
    aw.fly_to([turbine2_position[0] - 20, turbine2_position[1], 50])
    time.sleep(3)

    # Let's inspect this turbine. 
    # Fly backwards 15 meters, wait for 3 seconds and fly back to your first position.
    # After that repeat the process for the backside of the turbine.
    # You can fly 10 meters rightwards, 30 meters forward, 10 meters leftwards and then set yaw to zero to inspect the turbine from the backside.
    # Finally fly 10 meters backwards, wait for 3 seconds.
    # Fly 15 meters backwards
    pose = aw.get_drone_position()
    aw.fly_to([pose[0] - 15, pose[1], pose[2]])
    time.sleep(3)

    # Fly back to your first position
    aw.fly_to([pose[0], pose[1], pose[2]])
    pose = aw.get_drone_position()

    # Fly 10 meters rightwards
    aw.fly_to([pose[0], pose[1] + 10, pose[2]])
    pose = aw.get_drone_position()

    # Fly 30 meters forward
    aw.fly_to([pose[0] + 30, pose[1], pose[2]])
    pose = aw.get_drone_position()
    
    # Fly 10 meters leftwards
    aw.fly_to([pose[0], pose[1] - 10, pose[2]])

    # Fly 10 meters forward
    pose = aw.get_drone_position()
    aw.fly_to([pose[0] + 15, pose[1], pose[2]])
    aw.set_yaw(180)
    time.sleep(3)
    
    # Amazing! As a final task, lower your altitude to 25 meters to not to hit the wheel of the turbine and then land the drone 10 meters away from the car on the X-axis.
    pose = aw.get_drone_position()
    aw.fly_to([pose[0], pose[1], 25])
    car_position = aw.get_position("car")
    aw.fly_to([car_position[0], car_position[1] + 10, car_position[2] + 5])
    aw.land()
    time.sleep(3)
    
    print("Done.")
    aw.client.stopRecording()       
    aw.client.enableApiControl(False)


if __name__ == '__main__':
    main()
