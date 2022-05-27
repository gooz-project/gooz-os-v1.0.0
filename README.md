# Gooz Project for ESP32
The Gooz project acts as an operating system and aims at a Linux experience for microcontrollers. It includes many features such as general microcontroller usage, package management system and IoT based operations.

# Basics
Basic GOOZ commands to use operating system like Linux

### list Command

```bash
>>> list
```

- Lists available functions that user can use.

### help Command

```bash
>>> help
---OUTPUT---
ls
pwd
cd
rm
rmdir
cat
clear
echo
touch
mkdir
mv
cp
list
INFO:For more information about commands -> help [COMMAND]
```

- Shows some fundamental commands that can be used by user as seen in the example.
    
    ```bash
    >>> help pwd
    ---OUTPUT---
    INFO:Usage -> pwd
    INFO:prints the current working directory
    ```
    
    - Helps about a specific command as seen in the example.

### history Command

```bash
>>> history 
```

- Shows past commands used by user.

### clear Command

```bash
>>> clear
```

- Clears the terminal screen.

### delay Command

```bash
delay [TIME]
```

- Delays all programs as much as `[TIME]` seconds.

### reset Command

```bash
>>> reset
```

- Resets the system.

### shutdown Command

```bash
>>> shutdown
```

- Shuts the system.

# System Configuration

System default settings and configurations of GoozOS.

## Show Configs

```bash
conf show #Show all configs of GoozOS
conf show [CONFIG_PATH] #Show the config value in given [CONFIG_PATH]

conf show system
>>>{'machine': 'ESP32', 'version': '0.0.1'}

conf show system/machine
>>> ESP32
```

- `[CONFIG_PATH]` can refer to a single configuration or multiple configurations
- Configurations format is JSON

## Changing Configurations

```bash
>>> conf change [CONFIG_PATH] [NEW_VALUE] 
# Change the value of the variable at [CONFIG_PATH] as [NEW_VALUE]

>>> conf change user/password 1234
The value which refers to "user/password" successfully changed as "1234"
```

- Changing configurations does not support multiple changes. That means the `[CONFIG_PATH]` must refer to a single configuration.
- System configuration does not support adding new configuration. If you need new key-value type data you can use Environment Variables.

# Environment Variables

Environment variables of GoozOS

## Environent Variable Format

- Variables are stored in etc/env/env_variables.txt
- Environment variables have fallowing format in etc/env/env_variables.txt

<aside>
📎 exampleKey=example variable value
message=Hello Gooz!
defGpio=pin var gpio --name myPin --pin 2 --type OUT
pinConfig=--name myPin --pin 2 --type OUT

</aside>

- Variable key must be one word, it can not contain special characters such as ‘=’ but it can contain ‘_’ character.
- Variable value supports multiple word and special characters except ‘=’ and python default escape characters

## What is Environment Variable

- Environment variable can store value and can be called anywhere in the system.
- If GoozEngine sees `$[VARIABLE_KEY]` in any command it will change it to `[VARIABLE_KEY]`

## Variable Monitoring

```bash
>>> env # Show all saved environment variables
>>> env [VARIABLE_KEY] # Show environment variable named [VARIABLE_KEY]
```

- Also, `echo` command can be used to print any variable value

```bash
>>> echo $[VARIABLE_KEY] # Show environment variable named [VARIABLE_KEY]
```

- `echo` command prints everything written after it. It supports environment variables too.

## Adding and Changing Variables

```bash
>>> export [VARIABLE_KEY]=[VARIABLE_VALUE]

>>> export message=Hello Gooz! 
#It will add environment variable in etc/env/env_variables.txt
```

The following way can also be used for adding or changing variable

```bash
>>> $[VARIABLE_KEY] = [VARIABLE_VALUE]

>>> $message = Hello Gooz!
#It will add environment variable in etc/env/env_variables.txt
```

- If the key named `[VARIABLE_KEY]` already exist, the value is changed to `[VARIABLE_VALUE]`
- If there is no key named `[VARIABLE_KEY]`, the value named `[VARIABLE_VALUE]` will be created.

## Variable Removing

```bash
>>> unset [VARIABLE_KEY] # Delete the variable named [VARIABLE_KEY]

>>> unset message # Delete the variable named 'message'
```

## Example Usage

```bash
>>> export pinConfig=--name myPin --pin 2 --type OUT
---OUTPUT---
INFO:The variable added successfully: pinConfig=--name myPin --pin 2 --type OUT

>>> env pinConfig
---OUTPUT---
--name myPin --pin 2 --type OUT

>>> pin var gpio $pinConfig

INFO:The var pin named new successfully registered
---OUTPUT---
{'--pin': '2', '--type': 'OUT', 'pinType': 'gpio', '--name': 'myPin'}

>>> pin gpio write myPin 1 
```

# GPIO
Commands for GPIO pins

## GPIO Help

```python
>>> pin gpio help  # Gives general information about gpio

>>> pin gpio help [COMMAND_NAME] # Gives information about gpio [COMMAND_NAME] command

>>> pin gpio help write
---OUTPUT---
INFO:Usage -> pin gpio write [PIN_NAME] [VALUE]
INFO:[VALUE] can be HIGH (1) or LOW (0)
```

## Pin Registering

```bash
>>> pin var gpio –-name [PIN_NAME] --pin [PIN_NUMBER] --type [GPIO_TYPE]
# Creates new gpio pin named [PIN_NAME]

>>> pin var gpio --name myPin --pin 2 --type OUT
```

- `[PIN_NAME]` must be unique and it does not support special characters except ‘_’
- `[PIN_NUMBER]` can be any gpio pin number.
- `[GPIO_TYPE]` can be OUT, IN, ALT, OPENDRAIN or ALTOPENDRAIN

## Registered Pin Commands

---

### Update

```bash
>>> pin gpio update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]
# Updates the [VALUE_TO_CHANGE] value of the gpio pin named [PIN_NAME] to [NEW_VALUE]

>>> pin gpio update myPin --pin 3
```

- Pin update command supports multiple value changes.
    
    ```bash
    >>> pin gpio update myPin --pin 2 --type OUT
    ```
    

### Show

```bash
>>> pin gpio show # Shows all gpio pins

>>> pin gpio show [PARAMETER]:[VALUE_TO_SEARCH_FOR] # Shows specific gpio pins
>>> pin gpio show pin:2 # Shows gpio pins value 2
```

### Delete

```bash
>>> pin gpio delete [PIN_NAME] # Deletes gpio pin named [PIN_NAME]
>>> pin gpio delete myPin 

>>> pin gpio delete all # Deletes all gpio pins
```

## GPIO Pin Usage

---

### Writing GPIO Pin

```bash
>>> pin gpio write [PIN_NAME] [VALUE] # Write value to gpio pin named [PIN_NAME]

>>> pin gpio write myPin HIGH
```

- A gpio pin supports digital voltage (HIGH or LOW) , analog values are not supported.
    - [PWM pins](https://www.notion.so/PWM-254ce7bababe46af94763c7e60461ed4) can be used to writing analog voltage values.
- `[VALUE]` can be HIGH (1) and LOW (0)

### Reading GPIO Pin

```bash
>>> pin gpio read [PIN_NAME] # Read value from gpio pin named [PIN_NAME]

>>> pin gpio read myPin
---OUTPUT---
1
```

# ADC

Commands for Analog to Digital Converter (ADC) pins.

## ADC Info

- Gooz ADC pins read a raw analog value in the range 0-4096.

## ADC Help

```python
>>> pin adc help  # Gives general information about gpio

>>> pin adc help [COMMAND_NAME] # Gives information about gpio [COMMAND_NAME] command

>>> pin adc help read
---OUTPUT---
Info:Usage -> pin adc read [PIN_NAME] [READ_COUNT]
Info:reads value [READ_COUNT] times
```

## Pin Registering

```bash
>>> pin var adc –-name [PIN_NAME] --pin [PIN_NUMBER]
# Create new gpio pin named [PIN_NAME]

>>> pin var adc --name myPin --pin 2
```

- `[PIN_NAME]` must be unique and it does not support special characters except ‘_’
- `[PIN_NUMBER]` can be any adc pin number. Current microcontroller must support this ADC pin.

## Registered Pin Commands

---

### Update

```bash
>>> pin adc update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]
# Update the [VALUE_TO_CHANGE] value of the adc pin named [PIN_NAME] to [NEW_VALUE]

>>> pin adc update myPin --pin 3
```

- Pin update command supports multiple value changes.
    
    ```bash
    >>> pin adc update myPin --pin 2 --type OUT
    ```
    

### Show

```bash
>>> pin adc show # Show all adc pins

>>> pin adc show [PARAMETER]:[VALUE_TO_SEARCH_FOR] # Show specific adc pins
>>> pin adc show pin:2 #Show adc pins value 2
```

### Delete

```bash
>>> pin adc delete [PIN_NAME] # Delete adc pin named [PIN_NAME]
>>> pin adc delete myPin 

>>> pin adc delete all # Delete all adc pins
```

## ADC Pin Usage

---

### Reading ADC Pin

```bash
>>> pin adc read [PIN_NAME] [READ_COUNT] 
# Reads the value [COUNT] times from the adc pin named [PIN_NAME]
```

- `[READ_COUNT]` is not necessary.

```bash
>>> pin adc read myPin
---OUTPUT---
2048
```

### Listening ADC Pin

- Listen command supports many reads from given adc pin.
- Listen command will create a listen thread operation.
    - For stopping, showing current operations and more information please visit thread page

```bash
>>> pin adc listen [PIN_NAME] # Read value from adc pin named [PIN_NAME] every 1 second
>>> pin adc listen myPin
```

- Listen command accepts some parameters
    
    ```bash
    >>> pin adc listen [PIN_NAME] --[PARAMETER_KEY] [PARAMETER_VALUE] 
    ```
    
    - Parameters:
        - --file [FILE_NAME]
            - If this parameter exists, the readed value will be written in the given `[FILE_NAME]`
            - `[FILE_NAME]` format can be directly file name or file name with path
                - listen_values.txt
                - /user_files/listen_values.txt
        - --date [DATE_BOOL]
            - Default value of `[DATE_BOOL]` is `1`
            - `[DATE_BOOL]` can be 1 or 0
            - If `[DATE_BOOL]` 1, the readed value will be written with date
        - --loop [LOOP_COUNT]
            - Default value of `[LOOP_COUNT]` is `-1` that means, it will read until stopped manually.
            - If `[LOOP_COUNT]` is bigger than 0, the number of reads will be the given number.
        - --delay [SLEEP_TIME]
            - Default value of `[SLEEP_TIME]` is `1`
            - `[SLEEP_TIME]` can be any float number.
            - Listen command waits as `[SLEEP_TIME]` (unit = second) between two read operations.
        - --end [END_CHARACTER]
            - Default value of `[END_CHARACTER]` is `“\n”`
            - `[END_CHARACTER]` can be any character
            - Listen command prints given `[END_CHARCTER]` after readed value in files.
        
        ### Example Usage of Listen Command
        
        ```bash
        	>>> pin adc listen myPin --file values.txt --delay 0.5
        ```
        
        - Every `0.5` second the readed value of `myPin` is written to file named `values.txt`
        
# PWM
Commands for PWM pins.

## PWM Help

```bash
>>> pin pwm help
```

- Gives general information about pwm and it’s commands.

```bash
pin pwm help [COMMAND_NAME]
```

- Gives information about specific pwm  `[COMMAND_NAME]`  command.

```bash
>>> pin pwm help write
---OUTPUT---
INFO:Usage -> pin pwm write [PIN_NAME] [PWM_DUTY_CYCLE]
INFO:sets duty cycle from 0 to 1023 with [PWM_DUTY_CYCLE]
```

- Example usage for PWM help command

## Pin Registering

Users must register a pin with a name, pin number and pwm frequency before using the PWM pin.

```bash
pin var pwm --name [PIN_NAME] --pin [PIN_NUMBER] --freq [PWM_FREQUENCY]
```

- About PWM Parameters
    - `[PIN_NAME]` must be unique and it does not support special characters except ‘_’
    - `[PIN_NUMBER]` can be any pwm pins.
    - `[PWM_FREQUENCY]` can set PWM frequency from 1Hz to 40MHz. Default pwm frequency is 5000Hz.

## Registered Pin Commands

### Update

```bash
pin pwm update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]
```

- Updates the  `[VALUE_TO_CHANGE]`  value of the pwm pin named  `[PIN_NAME]`  to  `[NEW_VALUE]`

```bash
>>> pin pwm update my_pin --pin 3
```

- Example usage for updating pwm pins. According to the example, new value of pwm pin number is 3.
    
    ```bash
    >>> pin pwm update my_pin --pin 3 --name my_pwm
    ```
    
    - Example usage of pin update command that also supports multiple value changes

### Show

```bash
>>> pin pwm show
```

- Shows information about all existing pwm pins.

```bash
pin pwm show [PARAMETER]:[VALUE_TO_SEARCH_FOR]
```

- Shows information about a specific pwm pin which is called by user.

```bash
>>> pin pwm show name:my_pwm
```

- Example usage for showing a specific pwm pin

### Delete

```bash
pin pwm delete [PIN_NAME]

pin pwm delete all
```

- Deletes the pwm pin named  `[PIN_NAME]`
- `pin pwm delete all`  command deletes all registered pwm pins.

```bash
>>> pin pwm delete my_pwm
```

- Example usage for deleting a pwm pin

## Usage of PWM Pins

---

### Writing PWM Pin

```bash
pin pwm write [PIN_NAME] [PWM_DUTY_CYCLE]
```

- Writes  `[PWM_DUTY_CYCLE]`  to pwm pin named  `[PIN_NAME]`
- PWM pins support analog voltage values. Digital voltage values are not supported.
    - [GPIO pins](https://www.notion.so/GPIO-d9317a98db78491eaf3cc03fd7a1558b) can be used for writing digital voltage values.
- `[PWM_DUTY_CYCLE]`  sets duty cycle from 0 to 1023 (0v - 3.3v). If duty cycle is 0, pwm pin is at the lowest value which means it is closed.

```bash
>>> pin pwm write my_pwm 512
```

- Example usage for writing a pwm pin named my_pwm

### Closing PWM Pin

```bash
pin pwm close [PIN_NAME]
```

- Turns off the running pwm pin named  `[PIN_NAME]`

# UART

UART ****is a hardware communication protocol that uses asynchronous serial communication with configurable speed.

## Uart Help

```bash
>>> pin uart help  # Gives general information about uart

>>> pin uart help [COMMAND_NAME] # Gives information about uart [COMMAND_NAME] command

>>> pin uart help write
---OUTPUT---
INFO:Usage -> pin gpio write [PIN_NAME] [VALUE]
INFO:sends [TX_DATA] to the [PIN_NAME]
```

## Pin Registering

```bash
>>> pin var uart --name [PIN_NAME] --id [UART_ID] --baud [BAUDRATE]
# Creates new uart pin named [PIN_NAME]

>>> pin var uart --name myPin --id 2 --baud 115200
```

- `[PIN_NAME]` must be unique and it does not support special characters except ‘_’
- `[UART_ID]` have to be 0 ,1 or 2 as below.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6b7b0917-2972-4380-823a-bab205f58831/Untitled.png)
    
- `[BAUDRATE]` is 9600 as default. Also it can be assigned manually.

## Registered Pin Commands

---

### Update

```bash
>>> pin uart update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]
# Updates the [VALUE_TO_CHANGE] value of the uart pin named [PIN_NAME] to [NEW_VALUE]

>>> pin uart update myPin --name myUartPin
```

- Pin update command supports multiple value changes.
    
    ```bash
    >>> pin uart update myPin --name myUartPin --id 1
    ```
    

### Show

```bash
>>> pin uart show  # Shows all uart pins

>>> pin uart show [PARAMETER]:[VALUE_TO_SEARCH_FOR]  # Shows specific uart pins
>>> pin uart show pin:2  # Shows uart pins with a pin value of 2
```

### Delete

```bash
>>> pin uart delete [PIN_NAME] # Deletes uart pin named [PIN_NAME]
>>> pin uart delete myPin 

>>> pin uart delete all # Deletes all uart pins
```

## GPIO Pin Usage

---

### Sending Data from Uart Pin

```bash
>>> pin uart write [PIN_NAME] --data [TX_DATA] # Sends [TX_DATA] to uart pin named [PIN_NAME]

>>> pin uart write myPin --data Hi
>>> pin uart write myPin --data "Hello World!"
```

- [TX_DATA] have to be in double quotes if it is more than one word.

### Reading Data from Uart Pin

```bash
>>> pin uart read [PIN_NAME] # Reads last taken data from uart pin named [PIN_NAME]
>>> pin uart read myPin
```

### Reading Data Continuously from Uart Pin

- Listen command supports many reads from given uart pin.
- Listen command will create a listen thread operation.
    - For stopping, showing current operations and more information please visit thread page

```bash
>>> pin uart listen [PIN_NAME] # Reads value from uart pin named [PIN_NAME] every 1 second
>>> pin uart listen myPin
```

- Listen command accepts some parameters
    
    ```bash
    >>> pin uart listen [PIN_NAME] --[PARAMETER_KEY] [PARAMETER_VALUE] 
    ```
    
    - Parameters:
        - --file [FILE_NAME]
            - If this parameter exists, the readed value will be written in the given `[FILE_NAME]`
            - `[FILE_NAME]` format can be directly file name or file name with path
                - listen_values.txt
                - /user_files/listen_values.txt
        - --date [DATE_BOOL]
            - Default value of `[DATE_BOOL]` is `1`
            - `[DATE_BOOL]` can be 1 or 0
            - If `[DATE_BOOL]` 1, the readed value will be written with date
        - --loop [LOOP_COUNT]
            - Default value of `[LOOP_COUNT]` is `-1` that means, it will read until stopped manually.
            - If `[LOOP_COUNT]` is bigger than 0, the number of reads will be the given number.
        - --delay [SLEEP_TIME]
            - Default value of `[SLEEP_TIME]` is `1`
            - `[SLEEP_TIME]` can be any float number.
            - Listen command waits as `[SLEEP_TIME]` (unit = second) between two read operations.
        - --end [END_CHARACTER]
            - Default value of `[END_CHARACTER]` is `“\n”`
            - `[END_CHARACTER]` can be any character
            - Listen command prints given `[END_CHARACTER]` after readed value in files.
        
        ### Example Usage of Listen Command
        
        ```bash
        	>>> pin uart listen myPin --file values.txt --delay 0.5
        ```
        
        - Every `0.5` second the readed value of `myPin` is written to file named `values.txt`

# I2C

I2C (Inter-Integrated Circuit) is a two wire serial interface.

## I2C Help

```bash
>>> pin i2c help  # Gives general information about i2c

>>> pin i2c help [COMMAND_NAME] # Gives information about i2c [COMMAND_NAME] command

>>> pin i2c help write
---OUTPUT---
INFO:Usage -> pin i2c delete "pin_name"
INFO:sends [TX_DATA] to [PIN_NAME]
```

## Pin Registering

```bash
>>> pin var i2c --name [PIN_NAME] --scl [SCL_PIN] --sda [SDA_PIN] --address [ADDRESS] --baud [BAUDRATE]]
# Creates new i2c pin named [PIN_NAME]

>>> pin var i2c --name myPin --scl 22 --sda 21 --address 0x10 --baud 115200
```

- `[PIN_NAME]` must be unique and it does not support special characters except ‘_’
- `[SCL_PIN]` is serial clock line pin.
- `[SDA_PIN]` is serial data line pin.
- `[ADDRESS]` is address of connected slave device.
- `[BAUDRATE]` is 10000 as default. Also it can be assigned manually.

## Registered Pin Commands

---

### Update

```bash
>>> pin i2c update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE]
# Updates the [VALUE_TO_CHANGE] value of the i2c pin named [PIN_NAME] to [NEW_VALUE]

>>> pin i2c update myPin --name myI2cPin
```

- Pin update command supports multiple value changes.
    
    ```bash
    >>> pin i2c update myPin --scl 5 --sda 4
    ```
    

### Show

```bash
>>> pin i2c show  # Shows all i2c pins

>>> pin i2c show [PARAMETER]:[VALUE_TO_SEARCH_FOR]  # Shows specific i2c pins
>>> pin i2c show pin:2  # Shows i2c pins with a pin value of 2
```

### Delete

```bash
>>> pin i2c delete [PIN_NAME] # Deletes i2c pin named [PIN_NAME]
>>> pin i2c delete myPin 

>>> pin i2c delete all # Deletes all i2c pins
```

## I2C Pin Usage

---

### Sending Data from I2C Pin

```bash
>>> pin i2c write [PIN_NAME] --data [TX_DATA] # Sends [TX_DATA] to i2c pin named [PIN_NAME]

>>> pin i2c write myPin --data Hi
>>> pin i2c write myPin --data "Hello World!"
```

- [TX_DATA] have to be in double quotes if it is more than one word.

### Reading Data from I2C Pin

```bash
>>> pin i2c read [PIN_NAME] --byte [BYTE_SIZE]  # Takes data from [PIN_NAME] in lenght [BYTE_SIZE]

>>> pin i2c read myPin --byte 10
```

### Reading Data Continuously from I2C Pin

```bash
>>> pin i2c listen [PIN_NAME]  # Takes data from [PIN_NAME] continuously in thread
>>> pin i2c listen myPin

>>> pin i2c listen stop  # stops reading message from all i2c pins
```

### Reading Data Continuously from I2C Pin

- Listen command supports many reads from given i2c pin.
- Listen command will create a listen thread operation.
    - For stopping, showing current operations and more information please visit thread page

```bash
>>> pin i2c listen [PIN_NAME] # Reads value from i2c pin named [PIN_NAME] every 1 second
>>> pin i2c listen myPin
```

- Listen command accepts some parameters
    
    ```bash
    >>> pin i2c listen [PIN_NAME] --[PARAMETER_KEY] [PARAMETER_VALUE] 
    ```
    
    - Parameters:
        - --file [FILE_NAME]
            - If this parameter exists, the readed value will be written in the given `[FILE_NAME]`
            - `[FILE_NAME]` format can be directly file name or file name with path
                - listen_values.txt
                - /user_files/listen_values.txt
        - --date [DATE_BOOL]
            - Default value of `[DATE_BOOL]` is `1`
            - `[DATE_BOOL]` can be 1 or 0
            - If `[DATE_BOOL]` 1, the readed value will be written with date
        - --loop [LOOP_COUNT]
            - Default value of `[LOOP_COUNT]` is `-1` that means, it will read until stopped manually.
            - If `[LOOP_COUNT]` is bigger than 0, the number of reads will be the given number.
        - --delay [SLEEP_TIME]
            - Default value of `[SLEEP_TIME]` is `1`
            - `[SLEEP_TIME]` can be any float number.
            - Listen command waits as `[SLEEP_TIME]` (unit = second) between two read operations.
        - --end [END_CHARACTER]
            - Default value of `[END_CHARACTER]` is `“\n”`
            - `[END_CHARACTER]` can be any character
            - Listen command prints given `[END_CHARACTER]` after readed value in files.
        
        ### Example Usage of Listen Command
        
        ```bash
        	>>> pin i2c listen myPin --file values.txt --delay 0.5
        ```
        
        - Every `0.5` second the readed value of `myPin` is written to file named `values.txt`

# SPI

SPI (Serial Peripheral Interface) is a synchronous serial communication interface that supports full-duplex mode where data can be sent and received simultaneously.

## SPI Help

```bash
>>> pin spi help  # Gives general information about spi 

>>> pin spi help [COMMAND_NAME] # Gives information about spi [COMMAND_NAME] command

>>> pin spi help write
---OUTPUT---
INFO:Usage -> pin spi write [PIN_NAME] --data [TX_DATA]
INFO:sends [TX_DATA] to spi pin named [PIN_NAME]
```

## Pin Registering

```bash
>>> pin var spi --name [NAME] --id [SPI_ID] --baud [BAUDRATE] --ss [SLAVE_SELECT_PIN] 
# Creates new spi pin named [PIN_NAME]

>>> pin var spi --name myPin --id 2 --baud 115200 --ss 6
```

- `[PIN_NAME]` must be unique and it does not support special characters except ‘_’
- `[SPI_ID]` have to be 1 or 2 as below.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ee9ab38c-0732-440a-8b6f-3561fbdf72dd/Untitled.png)
    
- `[BAUDRATE]` is 4000000 as default. Also it can be assigned manually.

## Registered Pin Commands

---

### Update

```bash
>>> pin spi update [PIN_NAME] --[VALUE_TO_CHANGE] [NEW_VALUE] 
# Updates the [VALUE_TO_CHANGE] value of the spi pin named [PIN_NAME] to [NEW_VALUE]

>>> pin spi update myPin --name mySPIPin
```

- Pin update command supports multiple value changes.
    
    ```bash
    >>> pin spi update myPin --name mySPIPin --id 1
    ```
    

### Show

```bash
>>> pin spi show # Shows all spi pins

>>> pin spi show [PARAMETER]:[VALUE_TO_SEARCH_FOR]  # Shows specific spi pins
>>> pin spi show pin:2  # Shows spi pins with a pin value of 2
```

### Delete

```bash
>>> pin spi delete [PIN_NAME] # Deletes spi pin named [PIN_NAME]
>>> pin spi delete myPin 

>>> pin spi delete all # Deletes all spi pins
```

## SPI Pin Usage

---

### Sending Data from SPI Pin

```bash
>>> pin spi write [PIN_NAME] --data [TX_DATA] 
# Sends [TX_DATA] to spi pin named [PIN_NAME]

>>> pin spi write myPin --data Hi
>>> pin spi write myPin --data "Hello World!"
```

- [TX_DATA] have to be in double quotes if it is more than one word.

### Reading Data from SPI Pin

```bash
>>> pin spi read [PIN_NAME] --byte [BYTE_SIZE] # reads datas in length of [BYTE_SIZE] from spi pin named [PIN_NAME]
>>> pin spi read myPin --byte 10
```

### Reading Data Continuously from I2C Pin

```bash
>>> pin spi  listen [PIN_NAME]  # Takes data from [PIN_NAME] continuously in thread
>>> pin spi listen myPin

>>> pin spi listen stop  # stops reading message from all spi pins
```

### Reading Data Continuously from I2C Pin

- Listen command supports many reads from given spi pin.
- Listen command will create a listen thread operation.
    - For stopping, showing current operations and more information please visit thread page

```bash
>>> pin spi listen [PIN_NAME] # Reads value from spi pin named [PIN_NAME] every 1 second
>>> pin spi listen myPin
```

- Listen command accepts some parameters
    
    ```bash
    >>> pin spi listen [PIN_NAME] --[PARAMETER_KEY] [PARAMETER_VALUE] 
    ```
    
    - Parameters:
        - --file [FILE_NAME]
            - If this parameter exists, the readed value will be written in the given `[FILE_NAME]`
            - `[FILE_NAME]` format can be directly file name or file name with path
                - listen_values.txt
                - /user_files/listen_values.txt
        - --date [DATE_BOOL]
            - Default value of `[DATE_BOOL]` is `1`
            - `[DATE_BOOL]` can be 1 or 0
            - If `[DATE_BOOL]` 1, the readed value will be written with date
        - --loop [LOOP_COUNT]
            - Default value of `[LOOP_COUNT]` is `-1` that means, it will read until stopped manually.
            - If `[LOOP_COUNT]` is bigger than 0, the number of reads will be the given number.
        - --delay [SLEEP_TIME]
            - Default value of `[SLEEP_TIME]` is `1`
            - `[SLEEP_TIME]` can be any float number.
            - Listen command waits as `[SLEEP_TIME]` (unit = second) between two read operations.
        - --end [END_CHARACTER]
            - Default value of `[END_CHARACTER]` is `“\n”`
            - `[END_CHARACTER]` can be any character
            - Listen command prints given `[END_CHARACTER]` after readed value in files.
        
        ### Example Usage of Listen Command
        
        ```bash
        	>>> pin spi listen myPin --file values.txt --delay 0.5
        ```
        
        - Every `0.5` second the readed value of `myPin` is written to file named `values.txt`

# WiFi

Wifi library helps to connect any hotspot wifis

## Activating & deactivating wifi

```bash
wifi on
wifi off
```

## Finding available wifis

```bash
wifi ls
```

## Connecting wifi

```bash
wifi connect --name [SSID] --password [PASSWORD]
```

## Disconnecting wifi

```bash
wifi disconnect
```

## Active wifi connection status
```bash
wifi status # shows network connection

wifi ifconfig  # shows detailed network connection informations
```

# Tools

## Internal Temperature Sensor

Internal Temperature Sensor module of GoozOS

### Printing CPU Temperature

```bash
>>> cpu_temp
```

- Prints current CPU temperature as degree Celcius.

```bash
>>> cpu_temp -f
```

- Prints current CPU temperature as degree Fahrenheit.

## Internal Hall Sensor

Internal Hall Sensor module of GoozOS

### Printing Magnetic Area Value

```bash
>>> hall
```

- Prints value of current magnetic area.

## RTC

Real Time Clock (RTC) module of GoozOS

### RTC Info

- Built-in RTC module stores time data as tuple format
    - Example Time: `(2022, 4, 14, 3, 10, 8, 16, 797293)`
    - 0 Year, 1 Month, 2 Day of Month, 3 Day of Week, 4 Hour, 5 Minute, 6 Second, 7 miliseconds
    - `pin listen` commands uses RTC when value of `--date` parameter is `1` .

### RTC Commands

```bash
>>> rtc show
---OUTPUT---
(2022, 2, 14, 3, 12, 4, 15, 858697)
```

- Shows current RTC data as tuple.

```bash
>>> rtc autoset
```

- Sets time to current real time.
- Wifi must be connected for `rtc autoset` command.

```bash
>>> rtc set
---OUTPUT---
Please enter 0'th value: [2019]
DEBUG:Date had taken!: (2019)
Please enter 1'th value: [c]
DEBUG:Date had taken!: (4)
.
.
.
```

- Sets RTC manually.
- `rtc set` command will want 7 integer data one by one.
- If the given value equal to `‘c'`, value of current RTC does not change.

## Calculator

Calculator module of GoozOS

### Calculating operations

```bash
calc [OPERATION]
```

- Calculates `[OPERATION]` and prints the result to terminal.

```bash
>>> calc 3+8/2
---OUTPUT---
7
```

- Example usage for calculating operations

```bash
calc [OPERATION] > [VARIABLE]
```

- Calculates `[OPERATION]` and prints the result to env_variables.txt file as `[VARIABLE]`
    - For more informations about variables → [Environment Variables](https://www.notion.so/Environment-Variables-dd0b2e4089314d39be43f74df8c18d2e)

## Usage

Usage module of GoosOS

### Printing RAM and ROM Statuses

```bash
>>> usage
---OUTPUT---
Total ROM Size: 2.0MB
Used ROM Size: 0.359MB
Free ROM Size: 1.641MB
ROM Usage Percentage: 17.95%

Total RAM Size: 108.625KB
Used RAM Size: 46.391KB
Free RAM Size: 62.234KB
RAM Usage Percentage: 42.71%
```

- Prints current RAM and ROM statuses as seen in the example.

Informations about Gooz File System

## Client

Module for the remote terminal access with TCP-IP communication.

### Starting the client

```bash
>>> client start --port [PORT]
```

```bash
>>> client start  # takes default port value as [PORT]
```

- [PORT] can be assigned using “conf change client/port [PORT]” and can be used like above:

```bash
>>> conf change client/auto_start True # starts automatically the client on boot
```

### Closing the client

```bash
>>> client close
```

**Note:** Com-port terminal cannot be used while client is running. If client is closed from remote access terminal, then com-port terminal can be used.

## File Operations

---

### Showing Current Path

```bash
>>> pwd
```

### Showing Files and Directories

```bash
ls

ls [PATH]
```

- Shows files and directories in current directory except hidden ones.
- If  `[PATH]` is entered, shows files and directories in  `[PATH]` except hidden ones.

```bash
ls -a

ls [PATH] -a
```

- Shows files and directories in current directory including hidden ones.
- If  `[PATH]` is entered, shows files and directories in  `[PATH]` including hidden ones.

### Changing Directory

```bash
cd [DIRECTORY]
```

- Goes `[DIRECTORY]` path in the system.

```bash
>>> cd ..
```

- Goes upper directory in the system.

### Creating Directories and Files

```bash
mkdir [DIR_NAME]
>>> mkdir dir1

mkdir /[DIR_NAME]/[DIR_NAME]
>>> mkdir /directory/dir1
```

- Creates an empty directory named `[DIR_NAME]` in current directory or given path `/[DIR_NAME]/[DIR_NAME]`.

```bash
touch [FILE_NAME]
>>> touch file1

touch /[DIR_NAME]/[FILE_NAME]
>>> touch /directory/file1
```

- Creates an empty file named  `[FILE_NAME]` in current directory or given path `/[DIR_NAME]/[FILE_NAME]`.

### Deleting Directories and Files

```bash
rmdir [DIR_NAME]
>>> rmdir dir1

rmdir /[DIR_NAME]/[DIR_NAME]
>>> rmdir /directory/dir1
```

- Deletes the directory recursively named `[DIR_NAME]` in current directory or given path `/[DIR_NAME]/[DIR_NAME]`.

```bash
rm [FILE_NAME]
>>> rm file1

rm /[DIR_NAME]/[FILE_NAME]
>>> rm /directory/file1
```

- Deletes the file named  `[FILE_NAME]`  in current directory or given path `/[DIR_NAME]/[FILE_NAME]`.

### Renaming and Moving Files

```bash
mv [FILE_NAME1] [FILE_NAME2]
```

- Renames `[FILE_NAME1]`  to  `[FILE_NAME2]`

```bash
mv [FILE_NAME1] [FOLDER_NAME] [FILE_NAME2]
```

- Moves  `[FILE_NAME1]` to  `[FOLDER_NAME]` as  `[FILE_NAME2]`

### Copying Files

```bash
cp [FILE_NAME1] [FILE_NAME2]
```

- Copies `[FILE_NAME1]`  to  `[FILE_NAME2]` on the same path.

```bash
cp [FILE_NAME1] [FOLDER_NAME] [FILE_NAME2]
```

- Copies `[FILE_NAME1]` to the bottom of the  `[FOLDER_NAME]`  as  `[FILE_NAME2]`

### Reading Files

```bash
cat [FILE_NAME]
>>> cat file1

cat /[DIR_NAME]/[FILE_NAME]
>>> cat /directory/file1
```

- Reads the file named `[FILE_NAME]` in current directory or given path `/[DIR_NAME]/[FILE_NAME]`.

### Printing Data

```bash
echo [DATA]
```

- Prints  `[DATA]` to terminal.

```bash
>>> echo Hello World!
---OUTPUT---
Hello World!
```

- Example usage for printing data

```bash
echo [DATA] > [FILE_NAME]
```

- Prints `[DATA]` to a newly created  `[FILE_NAME]`

```bash
echo [DATA] >> [FILE_NAME]
```

- Prints `[DATA]`  to an already existing  `[FILE_NAME]`

# Thread

- Thread supports multiple operations in same time.
- Thread tool can be used for running micropython scripts.
- Also, `pin listen` commands are a thread operation.

## Thread Usage

### Thread Show

```bash
>>> thread show # Shows current thread operations and settings
--OUTPUT--
{'ID': 1, '--delay': '0', 'code_file_name': 'blink.py', 'type': 'code'}
```

### Thread Start

```bash
>>> thread start [FILE_NAME] # Run file named [FILE_NAME] in thread
```

- `thread start` command also accepts some parameters
    - Parameters:
        - --delay [SLEEP_TIME]
            - Default value of `[SLEEP_TIME]` is `1`
            - `[SLEEP_TIME]` is can be any float number.
            - `thread start` command waits as `[SLEEP_TIME]` (unit = second) between two run operations.
        - --loop [LOOP_COUNT]
            - Default value of `[LOOP_COUNT]` is `-1` that means, it will run file until stopped manually.
            - If `[LOOP_COUNT]` is bigger than 0, the number of runs will be the given number.

### Thread Stop

```bash
>>> thread stop [THREAD_ID] # Stops thread operation by ID
```

## Thread File Format

- The same named variables in different thread operations causes errors!
    - But, same named functions does not cause errors

## Example Thread Usage

- ledblink.py

```python
def blink():
    from machine import Pin
    import utime
    led = Pin(2,Pin.OUT)
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(1)   
blink()
```

- Imports must be in function

```bash
>>> thread start ledblink.py --delay 0
```

```bash
>>> thread show
---OUTPUT---
{'ID': 1, '--delay': '0',  'code_file_name': 'ledblink.py', 'type': 'code', '--loop':'-1'}
```

```bash
>>> thread stop 1
```

# Package Installer

## Package Install

```bash
pkg install [PACKAGE_NAME]
```

## Package Uninstall

```bash
pkg uninstall [PACKAGE_NAME]
```

## Package Installer Templates

For JSON file

```json
{
    "name" : "tester",
    "codes" : [{"filename":"main.py","code":"def run():\\n    print('Hello from tester')"}],
    "managersnip":"    elif cmd_arr[0] == 'tester':\\n        try:\\n            import app.tester.main\\n            app.tester.main.run()\\n        except:\\n            print('This app is deleted')\\n"
}
```

There are 3 fields for packaging. These are `name`, `codes` and `managersnip` 

Name field includes package name and this name also exists in .json file as a name

Codes field include `.py` files and their codes. Every code have to be written as string format. This format must be same Thonny IDE code styling. So `\t` does not be used.

Gooz Package Installer seperates these files and their codes, after it creates a application folder under `app` folder. The file which is `[pkgmanager.py](http://pkgmanager.py)` manages application orchestration. So, `pkgmanager` must include runner codes. It is provided with managersnip field in JSON file. Managersnip codes have to be like example JSON file.

For new line `\\n` must be used

Every application has any folder when turning on package, because every application contains only `.py` files. Unlimited py files can be used but not contain any folder.

# Goozshell

Goozshell runs Gooz commands in a row.

```bash
# example.py

# pwd
# delay 3
# cpu_temp

>>> goozshell example.py
---OUTPUT---
/  # delays 3 second
48.9 degree Celcius
```

