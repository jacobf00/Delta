from dynamixel_sdk import * # Uses Dynamixel SDK library
from common.lock_print import *
class servo:

    def __init__(self,Dynamixel_ID:int) -> None:
        # Factory default ID of all DYNAMIXEL is 1
        self.DXL_ID = Dynamixel_ID
        self.enableTorque()

    def setId(self,dxl_id:int):
        self.setControlTableValue1Byte(servo.ADDR_ID,dxl_id)
        self.DXL_ID = dxl_id

    def reboot(self):
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = servo.packetHandler.reboot(servo.portHandler, self.DXL_ID)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % servo.packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] reboot Succeeded\n" % self.DXL_ID)




    #********* DYNAMIXEL Model definition *********
    #***** (Use only one definition at a time) *****
    MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430
    # MY_DXL = 'MX_SERIES'    # MX series with 2.0 firmware update.
    # MY_DXL = 'PRO_SERIES'   # H54, H42, M54, M42, L54, L42
    # MY_DXL = 'PRO_A_SERIES' # PRO series with (A) firmware update.
    # MY_DXL = 'P_SERIES'     # PH54, PH42, PM54
    # MY_DXL = 'XL320'        # [WARNING] Operating Voltage : 7.4V


    # Control table address
    if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
        ADDR_TORQUE_ENABLE          = 64
        ADDR_GOAL_POSITION          = 116
        ADDR_PRESENT_POSITION       = 132
        ADDR_GOAL_VELOCITY          = 104
        LEN_GOAL_POSITION           = 4         # Data Byte Length
        LEN_PRESENT_POSITION        = 4         # Data Byte Length
        ADDR_ID                     = 7
        DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
        DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
        BAUDRATE                    = 57600
    elif MY_DXL == 'PRO_SERIES':
        ADDR_TORQUE_ENABLE          = 562       # Control table address is different in DYNAMIXEL model
        ADDR_GOAL_POSITION          = 596
        ADDR_PRESENT_POSITION       = 611
        DXL_MINIMUM_POSITION_VALUE  = -150000   # Refer to the Minimum Position Limit of product eManual
        DXL_MAXIMUM_POSITION_VALUE  = 150000    # Refer to the Maximum Position Limit of product eManual
        BAUDRATE                    = 57600
    elif MY_DXL == 'P_SERIES' or MY_DXL == 'PRO_A_SERIES':
        ADDR_TORQUE_ENABLE          = 512        # Control table address is different in DYNAMIXEL model
        ADDR_GOAL_POSITION          = 564
        ADDR_PRESENT_POSITION       = 580
        DXL_MINIMUM_POSITION_VALUE  = -150000   # Refer to the Minimum Position Limit of product eManual
        DXL_MAXIMUM_POSITION_VALUE  = 150000    # Refer to the Maximum Position Limit of product eManual
        BAUDRATE                    = 57600
    elif MY_DXL == 'XL320':
        ADDR_TORQUE_ENABLE          = 24
        ADDR_GOAL_POSITION          = 30
        ADDR_PRESENT_POSITION       = 37
        DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the CW Angle Limit of product eManual
        DXL_MAXIMUM_POSITION_VALUE  = 1023      # Refer to the CCW Angle Limit of product eManual
        BAUDRATE                    = 1000000   # Default Baudrate of XL-320 is 1Mbps

    # DYNAMIXEL Protocol Version (1.0 / 2.0)
    # https://emanual.robotis.com/docs/en/dxl/protocol2/
    PROTOCOL_VERSION            = 2.0


    # Use the actual port assigned to the U2D2.
    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    DEVICENAME                  = '/dev/ttyUSB0'

    TORQUE_ENABLE               = 1     # Value for enabling the torque
    TORQUE_DISABLE              = 0     # Value for disabling the torque
    DXL_MOVING_STATUS_THRESHOLD = 10    # Dynamixel moving status threshold
    GOAL_VELOCITY               = 800



    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():
        lprint("Succeeded to open the port")
    else:
        lprint("Failed to open the port")
        lprint("Press any key to terminate...")
        quit()


    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        lprint("Succeeded to change the baudrate")
    else:
        lprint("Failed to change the baudrate")
        lprint("Press any key to terminate...")
        quit()

    syncReader = GroupSyncRead(port=portHandler,ph=packetHandler,start_address=ADDR_PRESENT_POSITION,data_length=LEN_PRESENT_POSITION)
    groupBulkWrite = GroupBulkWrite(portHandler, packetHandler)

    @staticmethod
    def bulkWritePositions(pos1:int,pos2:int,pos3:int) -> None:
        positions = (pos1,pos2,pos3)
        ids = range(1,4)
        for id in ids:
            index = id-1
            param_goal_position = [DXL_LOBYTE(DXL_LOWORD(positions[index])), DXL_HIBYTE(DXL_LOWORD(positions[index])), DXL_LOBYTE(DXL_HIWORD(positions[index])), DXL_HIBYTE(DXL_HIWORD(positions[index]))]

            # Add Dynamixel#1 goal position value to the Bulkwrite parameter storage
            dxl_addparam_result = servo.groupBulkWrite.addParam(id, servo.ADDR_GOAL_POSITION, servo.LEN_GOAL_POSITION, param_goal_position)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupBulkWrite addparam failed" % id)
                quit()
        # Bulkwrite goal positions
        dxl_comm_result = servo.groupBulkWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
        servo.groupBulkWrite.clearParam()

    @staticmethod
    def syncReadPositions(servoIdStart:int=1,servoIdEnd:int=3):
        ids = range(servoIdStart,servoIdEnd+1)
        for id in ids:
            isProtocol2 = servo.syncReader.addParam(id)
            if not isProtocol2:
                lprint(f"DXL Id {id} could not be added to syndRead")
                return None
        servo.syncReader.txRxPacket()
        pos1 = servo.syncReader.getData(ids[0],servo.ADDR_PRESENT_POSITION,servo.LEN_PRESENT_POSITION)
        pos2 = servo.syncReader.getData(ids[1],servo.ADDR_PRESENT_POSITION,servo.LEN_PRESENT_POSITION)
        pos3 = servo.syncReader.getData(ids[2],servo.ADDR_PRESENT_POSITION,servo.LEN_PRESENT_POSITION)
        servo.syncReader.clearParam()
        return (pos1,pos2,pos3)



    def setGoalVelocity(self,velocity:int):
        self.setControlTableValue4Byte(servo.ADDR_GOAL_VELOCITY,velocity)

    def readCurrentPosition(self) -> int:
        return self.readControlTableValue(servo.ADDR_PRESENT_POSITION)


    def setControlTableValue1Byte(self,address:int,value:int): 
        dxl_comm_result, dxl_error = servo.packetHandler.write1ByteTxRx(servo.portHandler, self.DXL_ID, address, value)
        if dxl_comm_result != COMM_SUCCESS:
            lprint("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            lprint("%s" % servo.packetHandler.getRxPacketError(dxl_error))
        else:
            lprint("Control table value changed successfully")

    def setControlTableValue4Byte(self,address:int,value:int): 
        dxl_comm_result, dxl_error = servo.packetHandler.write4ByteTxRx(servo.portHandler, self.DXL_ID, address, value)
        if dxl_comm_result != COMM_SUCCESS:
            lprint("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            lprint("%s" % servo.packetHandler.getRxPacketError(dxl_error))
        else:
            lprint("Control table value changed successfully")

    def readControlTableValue(self,address:int,) -> int:
        if (servo.MY_DXL == 'XL320'): # XL320 uses 2 byte Position Data, Check the size of data in your DYNAMIXEL's control table
            tableValue, dxl_comm_result, dxl_error = servo.packetHandler.read2ByteTxRx(servo.portHandler, self.DXL_ID, address)
        else:
            tableValue, dxl_comm_result, dxl_error = servo.packetHandler.read4ByteTxRx(servo.portHandler, self.DXL_ID, address)
        if dxl_comm_result != COMM_SUCCESS:
            lprint("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            lprint("%s" % servo.packetHandler.getRxPacketError(dxl_error))
        return tableValue

    def enableTorque(self):
        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = servo.packetHandler.write1ByteTxRx(servo.portHandler, self.DXL_ID, servo.ADDR_TORQUE_ENABLE, servo.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            lprint("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            lprint("%s" % servo.packetHandler.getRxPacketError(dxl_error))
        else:
            lprint(f"Dynamixel {self.DXL_ID} has been successfully connected")

    def disableTorque(self):
        # Disable Dynamixel Torque
        dxl_comm_result, dxl_error = servo.packetHandler.write1ByteTxRx(servo.portHandler, self.DXL_ID, servo.ADDR_TORQUE_ENABLE, servo.TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            lprint("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            lprint("%s" % servo.packetHandler.getRxPacketError(dxl_error))
        else:
            lprint("Dynamixel torque has been successfully disabled")

    def setPosition(self,goalPosition):

        if goalPosition < servo.DXL_MINIMUM_POSITION_VALUE or goalPosition > servo.DXL_MAXIMUM_POSITION_VALUE:
            lprint("goal position is out of range")
        else:

            dxl_goal_position = goalPosition         # Goal position

            # Write goal position
            if (servo.MY_DXL == 'XL320'): # XL320 uses 2 byte Position Data, Check the size of data in your DYNAMIXEL's control table
                dxl_comm_result, dxl_error = servo.packetHandler.write2ByteTxRx(servo.portHandler, self.DXL_ID, servo.ADDR_GOAL_POSITION, dxl_goal_position)
            else:
                dxl_comm_result, dxl_error = servo.packetHandler.write4ByteTxRx(servo.portHandler, self.DXL_ID, servo.ADDR_GOAL_POSITION, dxl_goal_position)
            if dxl_comm_result != COMM_SUCCESS:
                lprint("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                lprint("%s" % servo.packetHandler.getRxPacketError(dxl_error))

            # while 1:
            #     # Read present position
            #     if (servo.MY_DXL == 'XL320'): # XL320 uses 2 byte Position Data, Check the size of data in your DYNAMIXEL's control table
            #         dxl_present_position, dxl_comm_result, dxl_error = servo.packetHandler.read2ByteTxRx(servo.portHandler, self.DXL_ID, servo.ADDR_PRESENT_POSITION)
            #     else:
            #         dxl_present_position, dxl_comm_result, dxl_error = servo.packetHandler.read4ByteTxRx(servo.portHandler, self.DXL_ID, servo.ADDR_PRESENT_POSITION)
            #     if dxl_comm_result != COMM_SUCCESS:
            #         lprint("%s" % servo.packetHandler.getTxRxResult(dxl_comm_result))
            #     elif dxl_error != 0:
            #         lprint("%s" % servo.packetHandler.getRxPacketError(dxl_error))

            #     #lprint("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (self.DXL_ID, dxl_goal_position, dxl_present_position))

            #     if not abs(dxl_goal_position - dxl_present_position) > servo.DXL_MOVING_STATUS_THRESHOLD:
            #         break
