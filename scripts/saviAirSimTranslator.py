#!/usr/bin/env python

# Created on Wed Feb 19 16:17:21 2020
# @author: Patrick Gavigan

import rospy
import airsim
import threading

from std_msgs.msg import String

def connectToAirSim():
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    return client

def syncPrint(message, sem):
    sem.acquire()
    rospy.loginfo(message)
    sem.release()

def perceptionHandler(client,simulatorSemaphore,consoleSemaphore):
    
    syncPrint("Perception handler launched.", consoleSemaphore)
    pub = rospy.Publisher('perceptions', String, queue_size=10)
    
    rate = rospy.Rate(1) # 1hz

    while not rospy.is_shutdown():
        
        # Get the data
        simulatorSemaphore.acquire()
        imu_data = client.getImuData()
        simulatorSemaphore.release()
        
        # Build the perception
        angularVelocity = "angularVelocity("+str(imu_data.angular_velocity.x_val)+","+str(imu_data.angular_velocity.y_val)+","+str(imu_data.angular_velocity.z_val)+","+str(imu_data.time_stamp)+")"
        linearAcceleration = "linearAcceleration("+str(imu_data.linear_acceleration.x_val)+","+str(imu_data.linear_acceleration.y_val)+","+str(imu_data.linear_acceleration.z_val)+","+str(imu_data.time_stamp)+")"
        orientation = "orientation("+str(imu_data.orientation.w_val)+","+str(imu_data.orientation.x_val)+","+str(imu_data.orientation.y_val)+","+str(imu_data.orientation.z_val)+","+str(imu_data.time_stamp)+")"
        
        #angularVelocity = "angularVelocity(1,1,1,1)"
        #linearAcceleration = "linearAcceleration(1,1,1,1)"
        #orientation = "orientation(1,1,1,1,1)"
        
        perception = angularVelocity + " " + linearAcceleration + " " + orientation
        
        # Publish the perception
        rospy.loginfo(perception)
        pub.publish(perception)
        rate.sleep()

def actionReceiver(data, args):
    (client,simulatorSemaphore,consoleSemaphore) = args

    message = str(rospy.get_caller_id() + 'I heard ' + str(data.data))
    syncPrint(message, consoleSemaphore)
    
    simulatorSemaphore.acquire()
    client.takeoffAsync().join()
    simulatorSemaphore.release()
    
    syncPrint("Takeoff command sent", consoleSemaphore)

def actionHandler(client,simulatorSemaphore,consoleSemaphore):
    syncPrint("Action handler launched", consoleSemaphore)
   
   
    rospy.Subscriber('actions', String, actionReceiver, (client,simulatorSemaphore,consoleSemaphore))

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def saviAirSimTranslator():
    
    rospy.init_node('saviAirSimTranslator', anonymous=True)
    client = connectToAirSim()
    simulatorSemaphore = threading.Semaphore()
    consoleSemaphore = threading.Semaphore()
    
    perceptionThread = threading.Thread(target=perceptionHandler, 
                                        args=(client,simulatorSemaphore,
                                              consoleSemaphore))
    perceptionThread.start()
    
    actionThread = threading.Thread(target=actionHandler,
                                    args=(client,simulatorSemaphore,
                                          consoleSemaphore))
    actionThread.start()
    

if __name__ == '__main__':
    try:
        saviAirSimTranslator()
    except rospy.ROSInterruptException:
        pass
