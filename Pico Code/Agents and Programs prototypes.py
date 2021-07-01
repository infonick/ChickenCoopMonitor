def agentHeatProgram(percepts):
    (perceptStates, actuatorStates) = percepts
    
    insideTempSensorName = ""
    outsideTempSensorName = ""
#     systemTempSensorName = ""
    actuatorName = ""

    haveInsideTempReading = False
    haveOutsideTempReading = False
#     haveSystemTempReading = False

    if actuatorStates[actuatorName] == 1:
        actuatorOn = True
    else:
        actuatorOn = False
    
    turnActuatorOn = actuatorOn

    if insideTempSensorName in perceptStates.keys():
        haveInsideTempReading = perceptStates[insideTempSensorName] is not None
    if outsideTempSensorName in perceptStates.keys():
        haveOutsideTempReading = perceptStates[outsideTempSensorName] is not None
#    if systemTempSensorName in perceptStates.keys():
#        haveSystemTempReading = perceptStates[systemTempSensorName] is not None
    
    if haveInsideTempReading:
        coldInside = perceptStates[insideTempSensorName] <= self.goals['insideTempMin']
        warmInside = perceptStates[insideTempSensorName] >= self.goals['insideTempMax']
        mildInside = perceptStates[insideTempSensorName] >= ((self.goals['insideTempMax'] +
                                                                  self.goals['insideTempMin'])/2)
    if haveOutsideTempReading:
        coldOutside = perceptStates[outsideTempSensorName] <= self.goals['outsideTempMin']
        warmOutside = perceptStates[outsideTempSensorName] >= self.goals['outsideTempMax']
        mildOutside = perceptStates[outsideTempSensorName] >= self.goals['insideTempMin']
#     if haveSystemTempReading:
#         coldSystem = perceptStates[systemTempSensorName] <= self.goals['systemTempMin']
#         coldSystem = perceptStates[systemTempSensorName] >= self.goals['systemTempMax']
    
#     if haveInsideTempReading and haveOutsideTempReading:
#         if coldOutside and not mildInside:
#             turnActuatorOn = True
#         elif
#             
#         elif coldInside
#             turnActuatorOn = True
#         elif warmInside
#             turnActuatorOn = False
    
    if haveInsideTempReading:
        if coldInside:
            turnActuatorOn = True
        elif warmInside
            turnActuatorOn = False

#     elif haveOutsideTempReading:
#         if coldOutside:
#             turnActuatorOn = True
#         elif mildOutside:
#             turnActuatorOn = False

#     elif haveSystemTempReading:
#         if coldSystem:
#             turnActuatorOn = True
#         elif warmSystem:
#             turnActuatorOn = False
    
    if actuatorOn == turnActuatorOn:
        return None
    elif turnActuatorOn:
        return [(actuatorStates[actuatorName].setState, 1)]
    else:
        return [(actuatorStates[actuatorName].setState, 0)]


goals = {'insideTempMin':3,
         'insideTempMax':6
         'outsideTempMin':-2
         'outsideTempMax':3}



def OLDagentProgram(percepts):
    (perceptStates, actuatorStates) = percepts
    
    all_actions = {}
    
    for key in validActuators.keys():
        keyOn = key + 'On'
        all_actions[keyOn]  = (actuators[key],1)
        keyOff = key + 'Off'
        all_actions[keyOff] = (actuators[key],0)
    
    possible_actions = list(all_actions.keys())
    actionsTaken = []
    
    for key in validPercepts.keys():
        if key in percepts.keys():
            validPercepts[key] = percepts[key].getState()
        
    for key in validActuators.keys():
        if key in actuators.keys():
            validActuators[key] = actuators[key].getState()
    
    for key in validActuators.keys(): 
        if validActuators[key] == 1:
            act = key + 'On'
            possible_actions.remove(act)
        elif validActuators[key] == 0:
            act = key + 'Off'
            possible_actions.remove(act)
    
    

    for act in possible_actions:
        actionsTaken.append(all_actions[act])
    
    if len(actionsTaken) == 0:
        return None
    else:
        return actionsTaken