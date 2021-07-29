# ChickenCoopMonitor
A microcontroller and interface to provide a variety of sensor readings of a chicken coop environment (such as the internal temperature) and automatically actuate coop systems (such as a heat lamp).
  
<br>

## Folders
 - **Docs:** installation and user manual (includes wiring diagrams)  
 - **Pico Code:** code for a Raspberry Pi Pico  
 - **Zero Code:** code for a Raspberry Pi Zero W  
  
<br>

## Clone the Repository
Use 

```
git clone --recurse-submodules https://github.com/infonick/ChickenCoopMonitor.git
```

or 

```
git clone https://github.com/infonick/ChickenCoopMonitor.git
cd ChickenCoopMonitor
git submodule update --init
```
  
<br> 
<br> 

```
               . .
              /|/|/\
            /V ____/
           /  /vvvv‘-._
          /  /vvvvvvvvv‘.                     ,.
         /   | ,-. \vvvvv‘                 .-`/
        / _, / ‘-’  \vvvvv\             _.’../
       ,OOooooo      |vvvvv\          ./...::\
      oOOOOO°°EE    /vvvvvvV\       ./....:::/
     °°   EE/EEEE--’vvvvvvvVV\    _/.....:::|
          \E\EEE/vvvvvvvvvVVVV\ -‘.::::::...\
            |vvvvvvvvvvvVVVVVVV\:............\
            |vvvvvvvvvvvvvvVVVVV\:...........:‘.
           |vvvvvvvvvVVVVVVVVVVVV\:::.......::.‘.
           |vvvvvvvvvVVVVVVVVVVVVV`.:::.........‘.
           |vvvvvvvVVVVVVVVVVVVVVVVV`.:..........|
          .’vvvvvvVVVVVVVVVVVVVVVVVVVVV‘.........\
         /VVVvvvvVVVVVVVVVVVVVVVVVVVVVVv‘........|
        /VVVVVvvvvvvvvvvvvvVVVVVVVVVVVVvvvV‘.::../
       /VVVVVvvvvvvvvvvvvvvvvvvvvVVVVVvvvvVVV‘.-`
     /VVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvVVVVVV\
    .VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvVVVVVVV\
    |VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvVVVVVVV\
    |VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvVVVVVVVV\
    |VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvVVVVVVv\
    |VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvVVVVvvv\
    ‘VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvVVvvvv\
     .VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\
      \VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\
       \VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\
        \VVVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\
         \VVVVVVvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\
          \VVVVvvvvvvvVVVVVVVVVVVVVVVvvvvvvvvvv\
           \VVvvvvvvVVVVVVVVVVVVVVVVVVVVVVvvvvv\
            \vvvvvvvVVVVVVVVVVVVVVVVVVVVVvvvvvv\
              \vvvvVVVVVVVVVVVVVVVVVVVVVVVvvvv\
                \VVVVVVVVVVVVVVVVVVVVVVVVVVVV\
                 ‘VVVVVVVVVVVVVVVVVVVVVVVVV.’
                     `’’VVVVVVVVVVVVVVVV,’
                    _.HHH\VVVVVVVVVVV/
                 .HHH’’  HH\VVVVVVVV/
                         HH |HH/
                         H/ /HH
                         V .HH/
                         _,/HH\
                         __.’HHHHH|
                  HHHHHHHHHHHH\
                        /HHHHHH\
                       HH/    \HH.
                     .’H/        ‘-‘
                    ==’
```
