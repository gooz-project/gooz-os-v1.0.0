# Gooz Project for ESP32
The Gooz project acts as an operating system and aims at a Linux experience for microcontrollers. It includes many features such as general microcontroller usage, package management system and IoT based operations.

## Basics
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
