Insert header

# **EXCM-Python**
## EMCX "smart motor" Driver used with a Festo EXCM

Insert image here

# Documentation
* [Motor](PD2C_CANopen_Technical-Manual_V2.0.1.pdf)
* [EXCM Assembly](https://www.festo.com/net/SupportPortal/Files/448653/YXMx_assembly_adjustment_cabling.pdf)

Insert image here

# Hardware Set Up
* Connect 24V to pins A1 and A3, and ground pins A2 and A4
* Pins A6 and A7 are CAN high and low respectively
* The dip switch (S1) is the bus termination resistor switch (120 ohm)
* For most cases this switch will be left in the off position, closer to the motor
* The rotary switch on the bottom of the motor selects the Node-ID and default baudrate
* If errors occur, attempt power cycling the motor and CAN bus line

Insert image here

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

Insert image here

# States
Insert multiple images here

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







<p align="right">
  <img src="https://user-images.githubusercontent.com/71296226/132049416-fc92dde2-d4fc-4d59-89e9-3aef004c9ee8.png" alt="alt text" width="200" height="30">
</p>

# **VAEM** 8️⃣ 🎮
## **8-Channel Valve Controller**

<p align="center">
  <img src="https://user-images.githubusercontent.com/71296226/135117973-92878832-2fb8-44da-8a9a-5b8161466005.png" alt="alt text" width="400" height="300">
</p>

![GitHub](https://img.shields.io/badge/Festo-Automation-0091dc/?style=for-the-badge&color=0091dc)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/jhynes94/VAEM?include_prereleases)
![GitHub language count](https://img.shields.io/github/languages/count/jhynes94/VAEM)
![GitHub](https://img.shields.io/github/license/jhynes94/VAEM)

* The [Festo](https://www.festo.com/us/en/?fwacid=9c792b0a20f1ab8d&gclid=Cj0KCQjwm9yJBhDTARIsABKIcGb7XGaLbJ-ljqb2bccWRPNZg1aE6mirUx0hWMCG82ycezodZ9I4ZTgaAqOYEALw_wcB) designed valve control module ```VAEM``` makes precise switching of solenoid valves easier than ever in any ```Festo``` systems or dispense applications.
* Up to 8 channels can be parameterised individually.
* A time resolution of only 0.2 ms and the control of the valves via current – not voltage – enable extremely high precision.
* The holding current reduction saves energy and minimizes heat input.
* Communication Protocol: [Modbus TCP/IP](https://en.wikipedia.org/wiki/Modbus#Modbus_TCP_frame_format_(primarily_used_on_Ethernet_networks)).

## Table of Contents

- [About](#about)
- [Links](#links)
- [GUI](#gui)
- [Driver Languages](#driver-languages)
- [Methods](#methods)
- [Diagram](#diagram)
- [Contributors](#contributors)
- [Capabilities](#current-version-capabilities)

## About
* This is an ```open software project``` which provides ```VAEM``` customers and users with a wide array of driver templates in different coding languages to allow for quick and easy adaptability of the ```Festo``` valve control module to any system, project, or environment. Listed below are the current languages provided along with the methods that each driver provides to the user.

## Links
### [:shopping_cart:: Product Page](https://www.festo.com/us/en/a/8088772/?q=VAEM~:festoSortOrderScored)
### [:receipt:: Operating Instructions](https://www.festo.com/net/SupportPortal/Files/716358/VAEM-V-S8EPRS2_operating-instr_2021-10a_8144872g1.pdf)
### [:old_key:: Support Portal](https://www.festo.com/net/en-in_in/SupportPortal/default.aspx?tab=0&q=8088772)
### [:desktop_computer:: GUI](https://www.festo.com/net/en-in_in/SupportPortal/default.aspx?q=8088772&tab=4&s=t#result)

## GUI
<p align="center">
  <img src="https://user-images.githubusercontent.com/71296226/136092356-8481541c-4a9f-4f75-a6a9-5d0b88f3e922.PNG" alt="alt text" width="800" height="700">
</p>

* 🔌 **CONNECT** the VAEM to your PC using an Ethernet cable and click the scan button.
(If the VAEM is found, press the connect button, else your gateway may have to be changed)
* 🕹️ **CONTROL** the eight channels of the VAEM.
* 🔬 **ANALYZE** data including the nominal current versus time.
* ❕ ❕ **STATUSWORD** displays the individual statusword bits and allows for basic read/write operations.
* ℹ️ **SYSTEMINFO** provides firmware and product number information.
* 📶 **ETHERNET** allows the user to change the host IP, port, and timeout.

## Driver Languages
* <img src="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/256/python-icon.png" alt="alt text" width="40" height="40">[  Python](/examples/python)
* <img src="https://images.vexels.com/media/users/3/166401/isolated/lists/b82aa7ac3f736dd78570dd3fa3fa9e24-java-programming-language-icon.png" alt="alt text" width="40" height="40">  [  Java](/examples/java)
* <img src="https://camo.githubusercontent.com/8d56e87edf99e89bfc457cd62462e0b7aae19e6b197b1df5c542d474d8d76f81/68747470733a2f2f646576656c6f7065722e6665646f726170726f6a6563742e6f72672f7374617469632f6c6f676f2f6373686172702e706e67" alt="alt text" width="30" height="30">[  .NET/C#](/examples/c%23)

## Methods
* **:toolbox: configureValves** -
  * ```Purpose:```      Configures the valve opening times of all eight channels, with 0 turning the channel off
  * ```Value Ranges:``` openingTimes >= 0
  * ```Arguments:```    int[8] openingTimes (ms)
  * ```Returns:```      void

* **💧: openValve** -
  * ```Purpose:```      Opens the valves connected to the initialized channels
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void
* **🚪: closeValve** -
  * ```Purpose:```      Closes the valves connected to the initialized channels
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void
  
* **:books: readStatus** -
  * ```Purpose:```      Read the VAEM status, error code, readiness, operating mode, and eight valve status bits (in order)
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void

* **:soap: clearError** -
  * ```Purpose:```      Clears (resets) the error bit on the VAEM
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void

* **:floppy_disk: saveSettings** -
  * ```Purpose:```      Save the current valve configuration upon restart
  * ```Value Ranges:``` NONE
  * ```Arguments:```    void
  * ```Returns:```      void

## Diagram
![festo_vaem_pic](https://user-images.githubusercontent.com/71296226/135151696-b2e39274-deb0-4d43-8371-ba793b44f638.PNG)

## Current Version Capabilities
- [x] Modbus TCP/IP over Ethernet
- [ ] Serial Ascii over RS232
- [x] Open all 8 valve channels
- [x] Close all 8 valve channels
- [x] Read the current device status
- [x] Configure the valves/channels

## Contributors
|Name                 | Email                         | GitHub         |
| ------------        | -------------------------     | -------------- |
| John Alessio        | alessio.j@northeastern.edu    | @jalesssio     |
| Justin Hynes-Bruell | justin.hynes-bruell@festo.com | @jhynes94      |
| Milen Kolev         | milen.kolev@festo.com         | @MKollev       |
| Jared Raines        | raines.j@northeastern.edu     | @rainesjared   |