# **EXCM-Python**
## EMCX "smart motor" Driver used with a Festo EXCM

![image](https://user-images.githubusercontent.com/71296226/146245408-a2cb202a-7c28-4657-962c-d6fb2600f2d7.png) 


# Documentation
* [Motor](Docs/PD2C_CANopen_Technical-Manual_V2.0.1.pdf)
* [EXCM Assembly](https://www.festo.com/net/SupportPortal/Files/448653/YXMx_assembly_adjustment_cabling.pdf)

# Pin Assignment

![CANMOTORPINASSIGN](https://user-images.githubusercontent.com/71296226/146244913-4d718cba-84ef-4920-8d67-20355c463699.PNG)

# Hardware Set Up
* Connect 24V to pins A1 and A3, and ground pins A2 and A4
* Pins A6 and A7 are CAN high and low respectively
* The dip switch (S1) is the bus termination resistor switch (120 ohm)
* For most cases this switch will be left in the off position, closer to the motor
* The rotary switch on the bottom of the motor selects the Node-ID and default baudrate
* If errors occur, attempt power cycling the motor and CAN bus line

![CANMOTORROTARYSWITCH](https://user-images.githubusercontent.com/71296226/146244932-f043a585-3e10-4e49-bc2e-ab54d717b97c.PNG)

# Software Set Up
* Some Linux based systems can only work at up to 500 kbps, but the default motor baudrate is 1 mbps so you may need to change this value using an interface such as Busmaster (CAN to USB?)
* To change the Baudrate the rotary switch must be at 8 or above
* On start up, the motor is in closed loop mode with encoders
* Download the PD2_C.py motor driver and objectDict.py files which allow you to get and set the object registers needed for homing, velocity mode, and positioning mode
* The firware version may not support position/velocity units, in this case use position/velocity encoder resolution

# Main Modes
* Profile Positioning Mode:
    * setMode(1): sets the Mode of Operation (6060) to value 1
    * Control Word: Bit 4 = starts travel command, Bit 5 = travel command immediately executed, Bit 6 = 0 is absolute and 1 is relative position, Bit 8 = Halt, Bit 9 = speed is not changed until first target
    * Status Word: Bit 10: last target reached, Bit 11 = limit exceeded, Bit 12 = new set-point acknowledgement, Bit 13 = following error
    * Travel command initiated with bit 4 after target position is set
* Velocity Mode:
    * setMode(2): sets the mode to value 2
    * Control Word: Bit 8 = halt
    * Status Word: Bit 11 = limit exceeded
    * Initiated when target velocity is set and motor is changed to enable operation state
* Homing mode:
    * setmode(6): sets the mode to value 6
    * Control Word: Bit 4 = referencing performed until reference position reached
    * Status Word: See Table Below
    * Initiated when setHomingMethod(-1) is called to set the homing method to "Homing on Block", and bit 5 is set on the control word (0x1F)

![CANMOTORHOMINGSTATUS](https://user-images.githubusercontent.com/71296226/146244974-a0fdb176-1ac4-4f60-aeda-6a08cac6b834.PNG)

# States
![CANMOTORSTATESDIAGRAM](https://user-images.githubusercontent.com/71296226/146245001-a2d95e8a-ca75-481a-9eb2-2ce9ab288255.PNG)
![CANMOTORSTATESCW](https://user-images.githubusercontent.com/71296226/146245008-22bc3638-36c8-4ee2-b670-97fae8129cbc.PNG)
![CANMOTORSTATESSW](https://user-images.githubusercontent.com/71296226/146245017-dee8afa3-e4f0-4f98-a2c2-3fe88545eef1.PNG)

## Control Word
* Bits 0 to 9:
    * Switched On (SO)
    * Enable Voltage (EV)
    * Quick Stop (QS)
    * Enable Operation (EO)
    * Operation Mode Specific (OMS) [3 bits]
    * Fault Reset (FR)
    * Halt
    * Operation Mode Specific (OMS) [1 bit]

## Status Word
* Bits 0 to 15:
    * Ready To Switch On (RTSO)
    * Switched On (SO)
    * Operation Enabled (OE)
    * Fault
    * Voltage Enabled (VE)
    * Quick Stop (QS)
    * Switched on Disabled (SOD)
    * Warning (WARN)
    * Synchronization (SYNC)
    * Remote (REM)
    * Target Reached (TARG)
    * Internal Limit Active (ILA)
    * Operation Mode Specific (OMS) [2 bits]
    * N/A = Bit 14
    * Closed Loop Active (CLA)

# Driver
* The objectDict.py file stores the object register index, datatype, and signed/unsigned information for each of the objects used.
* The PD2_C.py file reads and write over CAN to set and get information from the motor. 
* The functions are split into general functions, position related, velocity related, and homging related.
* The helper functions and set/get object functions are below the imports

# Contributors
|Name                 | Email                         | GitHub         |
| ------------        | -------------------------     | -------------- |
| Jared Raines        | raines.j@northeastern.edu     | @rainesjared   |
| Justin Hynes-Bruell | justin.hynes-bruell@festo.com | @jhynes94      |
