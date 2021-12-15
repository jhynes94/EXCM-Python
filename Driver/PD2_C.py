import can
from objectDict import eds
import struct

DataSize = {
    "8" : 0x2F,
    "16": 0x2B,
    "24": 0x27,
    "32": 0x23
}


def formatData(obj, value):
    if (not obj["signed"]) and value < 0:
        raise ValueError("Unsigned value cannot be negative")
    int_to_bytes = struct.Struct('<I').pack
    return int_to_bytes(value & 0xFFFFFFFF)


def receiveData(obj, subindex):
    byteTwo = obj["index"] >> 8
    byteOne = obj["index"] & 0xFF
    return [0x40, byteOne, byteTwo, subindex, 0x00, 0x00, 0x00, 0x00]


def sendData(obj, value, subindex):
    byteTwo = obj["index"] >> 8
    byteOne = obj["index"] & 0xFF
    sizeByte = DataSize[obj["datatype"]]
    data = formatData(obj, value)
    return [sizeByte, byteOne, byteTwo, subindex, data[0], data[1], data[2], data[3]]


class PD2_C:
    # Constructor
    def __init__(self, motorID=8):
        self.connection = can.interface.Bus(channel='can0', bustype='socketcan')
        self.__default_motor = motorID
        self.__CanId = motorID + 0x600

    # Object Access
    def getMotorID(self):
        return self.__default_motor

    def getObject(self, obj, subindex=0):
        rd = receiveData(obj, subindex)
        msg = can.Message(arbitration_id=self.__CanId, data=rd, extended_id=False)
        print(msg)

        self.connection.send(msg)
        # msg = self.connection.recv(10)
        while(msg.arbitration_id != (self.__default_motor + 0x580) or msg.data[2] != rd[2] or msg.data[1] != rd[1]):
            msg = self.connection.recv(10)
        print (msg)
        return ((msg.data[7] << 24) | (msg.data[6] << 16) | (msg.data[5] << 8) | (msg.data[4]))

    def setObject(self, obj, value, subindex=0):
        msg = can.Message(arbitration_id=self.__CanId, data=sendData(obj, value, subindex),
                          extended_id=False)
        # print(msg)
        self.connection.send(msg)

########################################################################################################################
    # Objects

    def startOperation(self):
        self.setObject(eds["ControlWord"], 0x1F)

    def startMotor(self):
        self.setObject(eds["ControlWord"], 0x6)
        self.setObject(eds["ControlWord"], 0x7)
        self.setObject(eds["ControlWord"], 0xF)

    def halt(self):
        self.setObject(eds["ControlWord"], 0x6)

    # Bits:
    # 0 = Switched On, 1 = Enable Voltage, 2 = Quick Stop, 3 = Enable Operation,
    # 4, 5, 6 = Operation Mode Specific, 7 = Fault Reset, 8 = Halt, 9 = OMS
    def setControlWord(self, val):
        self.setObject(eds["ControlWord"], val)

    def getControlWord(self):
        return self.getObject(eds["ControlWord"])

    def getStatusWord(self):
        return self.getObject(eds["StatusWord"])

    # 1 = Profile Position, 2 = Velocity, 3 = Profile Velocity, 6 = Homing
    def setMode(self, mode):
        self.setObject(eds["ModeOfOperation"], mode)

    def getMode(self):
        return self.getObject(eds["ModeDisplay"])

    def stateShutdown(self):
        self.setObject(eds["ControlWord"], 6)

    def stateSwitchOn(self):
        self.setObject(eds["ControlWord"], 7)

    def stateDisableVoltage(self):
        self.setObject(eds["ControlWord"], 0)

    def stateQuickStop(self):
        self.setObject(eds["ControlWord"], 2)

    def stateDisableOperation(self):
        self.setObject(eds["ControlWord"], 7)

    def stateEnableOperation(self):
        self.setObject(eds["ControlWord"], 0xF)

    def stateEnableAfterQuickStop(self):
        self.setObject(eds["ControlWord"], 0xF)

    def setPolarity(self, pol):
        self.setObject(eds["Polarity"], pol)

    def getMinVelocity(self):
        return self.getObject(eds["MinMaxVelocity"], 1)

    def setMinVelocity(self, velocity):
        self.setObject(eds["MinMaxVelocity"], velocity, 1)

    def getMaxVelocity(self):
        return self.getObject(eds["MinMaxVelocity"], 2)

    def setMaxVelocity(self, velocity):
        self.setObject(eds["MinMaxVelocity"], velocity, 2)

    def getMaxAcceleration(self):
        return self.getObject(eds["MaxAcceleration"])

    def setMaxAcceleration(self, acceleration):
        self.setObject(eds["MaxAcceleration"], acceleration)

    def getMaxDeceleration(self):
        return self.getObject(eds["MaxDeceleration"])

    def setMaxDeceleration(self, velocity):
        return self.setObject(eds["MaxDeceleration"], velocity)

    def getErrorFlags(self):
        self.getObject(eds["ErrorNumber"])

    # POSITION

    def getTargetPosition(self):
        return self.getObject(eds["TargetPosition"])

    def setTargetPosition(self, position):
        self.setObject(eds["TargetPosition"], position)

    def moveTo(self, position, velocity=None):
        if velocity:
            self.setMaxVelocity(velocity)
        # self.connection.move(0, self.__default_motor, position)
        self.setTargetPosition(position)

    def moveBy(self, difference, velocity=None):
        position = difference + self.getActualPosition()
        self.moveTo(position, velocity)
        return position

    def getActualPosition(self):
        return self.getObject(eds["ActualPosition"])

    #  Bit 9 | Bit 5
    # -------|-------
    #    X   |   1     Move immediately
    #    0   |   0     Complete target before new point
    #    1   |   0     Pass through current target
    def setTravelOption(self, nine, five):
        self.setObject(eds["ControlWord"], nine, 9)
        self.setObject(eds["ControlWord"], five, 5)

    def getTravelOption(self):
        return {self.getObject(eds["ControlWord"], 9),
                self.getObject(eds["ControlWord"], 5)}

    # Returns encoder increments @ subindex 1 and
    # motor revolutions @ subindex 2
    def getPositionEncoderResolution(self):
        increments = self.getObject(eds["PositionEncoderResolution"], 1)
        revs = self.getObject(eds["PositionEncoderResolution"], 2)
        return {increments, revs}

    def setPositionEncoderResolution(self, increments, revs):
        self.setObject(eds["PositionEncoderResolution"], increments, 1)
        self.setObject(eds["PositionEncoderResolution"], revs, 2)

    def getPositionUnits(self):
        return self.getObject(eds["PositionUnits"])

    # Bits 16 to 23 = position unit
    # Bits 24 to 31 = exponent of power of ten
    # (0xFD01) = millimeters
    def setPositionUnits(self, units):
        self.setObject(eds["PositionUnits"], units)

    # Returns motor revolutions and shaft revolutions
    def getGearRatio(self):
        return {self.getObject(eds["GearRatio"], 1), self.getObject(eds["GearRatio"], 2)}

    def setGearRatio(self, motorRevs, shaftRevs):
        self.setObject(eds["GearRatio"], motorRevs, 1)
        self.setObject(eds["GearRatio"], shaftRevs, 2)

    # VELOCITY

    def getTargetVelocity(self):
        return self.getObject(eds["TargetVelocity"])

    def setTargetVelocity(self, velocity):
        self.setObject(eds["TargetVelocity"], velocity)

    def getActualVelocity(self):
        return self.getObject(eds["ActualVelocity"])

    def rotate(self, velocity):
        self.setTargetVelocity(velocity)

    def stop(self):
        self.rotate(0)

    # Returns encoder increments per second @ subindex 1 and
    # motor revolutions per second @ subindex 2
    def getVelocityEncoderResolution(self):
        increments = self.getObject(eds["VelocityEncoderResolution"], 1)
        revs = self.getObject(eds["VelocityEncoderResolution"], 2)
        return {increments, revs}

    def setVelocityEncoderResolution(self, increments, revs):
        self.setObject(eds["VelocityEncoderResolution"], increments, 1)
        self.setObject(eds["VelocityEncoderResolution"], revs, 2)

    def getVelocityUnits(self):
        return self.getObject(eds["VelocityUnits"])

    # Bits 8 to 15 = time unit
    # Bits 16 to 23 = position unit
    # Bits 24 to 31 = exponent of power of ten
    def setVelocityUnits(self, units):
        self.setObject(eds["VelocityUnits"], units)

    # Returns feed and shaft revolutions
    def getFeedConstant(self):
        return {self.getObject(eds["FeedConstant"], 1), self.getObject(eds["FeedConstant"], 2)}

    def setFeedConstant(self, feed, shaftRevs):
        self.setObject(eds["FeedConstant"], feed, 1)
        self.setObject(eds["FeedConstant"], shaftRevs, 2)

    # HOMING

    # 0 = performed
    # 1 = interrupted or not started
    # 4 = performed since last start (target not reached)
    # 5 = completed
    # 8 = error and motor still turning
    # 9 = error and motor at standstill
    def getHomingStatus(self):
        sw = self.getObject(eds["StatusWord"])
        sw = (sw >> 8 & 0xFF)
        return (sw & 52) >> 2

    def getHomingOffset(self):
        return self.getObject(eds["HomingOffset"])

    def setHomingOffset(self, offset):
        self.setObject(eds["HomingOffset"], offset)

    def getHomingMethod(self):
        return self.getObject(eds["HomingMethod"])

    def setHomingMethod(self, method):
        self.setObject(eds["HomingMethod"], method)

    def getHomingSpeed(self):
        return self.getObject(eds["HomingSpeed"])

    # Subindex 1 = To Switch, Subindex 2 = To Zero
    def setHomingSpeed(self, speed):
        self.setObject(eds["HomingSpeed"], speed)

    def getBlockDetection(self):
        return self.getObject(eds["BlockDetection"])

    def setBlockDetectionCurrent(self, current):
        self.setObject(eds["BlockDetection"], current, 1)

    def setBlockDetectionTime(self, period):
        self.setObject(eds["BlockDetection"], period, 2)

    def getHomingAcceleration(self):
        return self.getObject(eds["HomingAccel"])

    def setHomingAcceleration(self, accel):
        self.setObject(eds["HomingAccel"], accel)

    def getMaxMotorSpeed(self):
        return self.getObject(eds["MaxMotorSpeed"])

    def SetMaxMotorSpeed(self, speed):
        self.setObject(eds["MaxMotorSpeed"], speed)
