# Delta
Code for controlling fob delta robot
common folder contains all code relevant for controlling robot and communicating with server and servos.  
main.py is only responsible for creating delta and communication objects and starting threads.  
setup.py is unnecessary and is only used to make the modules globally accessible on system.  
delta.py contains most of the code for controlling the robot and math necessary for calculating movements.  
servo_service.py is used by delta.py to create servo objects and communicate with servos.  
comm.py is used to communicate with server and execute actions received from server.  
config.py contains initialized global variables/functions.  
points.py is a class that can generate tray points based on input parameters and can shift the point field as well.  
motion.py contains methods for movement including the trays program which generates and points using points.py and loops goes through them.
home.py can be ran from putty and just homes the robot.  
  
Only important files in data folder is key.key which is needed for encryption and runtime.log which will show how the robot is operating. LOOK FOR WARNINGS.  
  
Nothing important in dev, this is used for testing.  
  
WHEN INSTALLING ROBOT:  
Points will likely not be in the right orientation, make sure to mount robot directly in the center of the trays to have the points line up, if this is not possible you will have to use the pfShift method to shift the points to where you need them. Make sure z0 level is accurate, and if the calibration point on the first bottle is accurate, it should shift the rest of the points to where they need to be.  MAKE SURE TRAYS ARE ORIENTED STRAIGHT AND ARE LEVEL. If the orientation of the points is off by 90 degrees, switch length/width and xpoints/ypoints parameters in code and it should fix it.