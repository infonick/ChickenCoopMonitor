#{'pinNum': , 'pinMode': , 'name':'', 'gpioInType':'down', 'irq':'none', 'driver':'none', 'convFactorADC':None}
#pinNum, pinMode, name=None, gpioInType='down', irq='none', driver='none', convFactorADC=None

#     __sensorPinModes = ['gpio-in', 'adc-in']
#     __irqTypes = ['none', 'rising', 'falling', 'all']
#     __sensorDrivers = ['none', 'dht22']

sensors = [{'pinNum':  8, 'pinMode':'gpio-in', 'name':'Door1', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None},
           {'pinNum':  9, 'pinMode':'gpio-in', 'name':'Door2', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None},
           {'pinNum': 10, 'pinMode':'gpio-in', 'name':'Door3', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None},
           {'pinNum': 11, 'pinMode':'gpio-in', 'name':'Door4', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None},
           {'pinNum': 12, 'pinMode':'gpio-in', 'name':'ChickenDoor', 'gpioInType':'down', 'irq':'all', 'driver':'slidingdoor', 'convFactorADC':None},
              # Pin 13 is automatically used in conjuction with Pin 12 to provide a sliding door with two sensors
              # {'pinNum': 13, 'pinMode':'gpio-in', 'name':'Door6', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None},
           {'pinNum': 14, 'pinMode':'gpio-in', 'name':'Temp&RH_1', 'gpioInType':'up', 'irq':'none', 'driver':'dht22', 'convFactorADC':None},
           {'pinNum': 15, 'pinMode':'gpio-in', 'name':'Temp&RH_2', 'gpioInType':'up', 'irq':'none', 'driver':'dht22', 'convFactorADC':None}]




#{'pinNum':, 'name': '', 'gpioOutInitValue': 0 , 'reverseStates': False }
#pinNum, name=None, gpioOutInitValue=0, reverseStates = False
    
actuators = [{'pinNum': 6, 'name': 'AlertLED', 'gpioOutInitValue': 0, 'reverseStates': False},
             {'pinNum': 7, 'name': 'Doorkeeper', 'gpioOutInitValue': 0, 'reverseStates': False},
             {'pinNum':16, 'name': 'Relay4', 'gpioOutInitValue': 0 , 'reverseStates': True },
             {'pinNum':17, 'name': 'Relay3', 'gpioOutInitValue': 0 , 'reverseStates': True },
             {'pinNum':18, 'name': 'Relay2', 'gpioOutInitValue': 0 , 'reverseStates': True },
             {'pinNum':19, 'name': 'Relay1', 'gpioOutInitValue': 0 , 'reverseStates': True },
             {'pinNum':22, 'name': 'ZeroReset', 'gpioOutInitValue': 0 , 'reverseStates': False }]