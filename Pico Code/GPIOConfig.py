#{'pinNum': , 'pinMode': , 'name':'', 'gpioInType':'down', 'irq':'none', 'driver':'none', 'convFactorADC':None}
#pinNum, pinMode, name=None, gpioInType='down', irq='none', driver='none', convFactorADC=None

#     __sensorPinModes = ['gpio-in', 'adc-in']
#     __irqTypes = ['none', 'rising', 'falling', 'all']
#     __sensorDrivers = ['none', 'dht22']

sensors = [{'pinNum':  8, 'pinMode':'gpio-in', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None, 'name':'Man Door 1'},
           {'pinNum':  9, 'pinMode':'gpio-in', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None, 'name':'Man Door 2'},
           {'pinNum': 10, 'pinMode':'gpio-in', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None, 'name':'Man Door 3'},
           {'pinNum': 11, 'pinMode':'gpio-in', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None, 'name':'Egg Box Door'},
           {'pinNum': 12, 'pinMode':'gpio-in', 'gpioInType':'down', 'irq':'all', 'driver':'slidingdoor', 'convFactorADC':None, 'name':'Chicken Door'},
         # Pin 13 is automatically used in conjuction with Pin 12 to provide a sliding door with two sensors
         # {'pinNum': 13, 'pinMode':'gpio-in', 'gpioInType':'down', 'irq':'all', 'driver':'none', 'convFactorADC':None, 'name':'Door6'},
           {'pinNum': 14, 'pinMode':'gpio-in', 'gpioInType':'up', 'irq':'none', 'driver':'dht22', 'convFactorADC':None, 'name':'Outside'},
           {'pinNum': 15, 'pinMode':'gpio-in', 'gpioInType':'up', 'irq':'none', 'driver':'dht22', 'convFactorADC':None, 'name':'Inside'}]




#{'pinNum':, 'name': '', 'gpioOutInitValue': 0 , 'reverseStates': False }
#pinNum, name=None, gpioOutInitValue=0, reverseStates = False
    
actuators = [{'pinNum': 6, 'gpioOutInitValue': 0, 'reverseStates': False, 'name': 'AlertLED'},
             {'pinNum': 7, 'gpioOutInitValue': 0, 'reverseStates': False, 'name': 'Doorkeeper'},
             {'pinNum':16, 'gpioOutInitValue': 0, 'reverseStates': True , 'name': 'Heat Lamp'},
             {'pinNum':17, 'gpioOutInitValue': 0, 'reverseStates': True , 'name': 'Ventilation Fan' },
             {'pinNum':18, 'gpioOutInitValue': 0, 'reverseStates': True , 'name': 'Relay2' },
             {'pinNum':19, 'gpioOutInitValue': 0, 'reverseStates': True , 'name': 'Relay1' },
             {'pinNum':22, 'gpioOutInitValue': 0, 'reverseStates': False, 'name': 'ZeroReset' }]