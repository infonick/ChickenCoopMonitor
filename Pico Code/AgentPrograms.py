import AiLib

def setupHeatAgent(sensorDict, actuatorDict):
    heatAgent = AiLib.Agent(heatAgentProgram, heatAgentGoals)
    s = []
    a = []
    for n in heatAgentSensors:
        s.append(sensorDict[n])
    for n in heatAgentActuators:
        a.append(actuatorDict[n])
    
    return AiLib.Environment(heatAgent, s, a)



heatAgentGoals = {'insideTempMin':24.5,
                  'insideTempMax':25}

heatAgentSensors = ['Temp&RH_1',
                    'Temp&RH_2']

heatAgentActuators = ['Relay4']



def heatAgentProgram(percepts, goals):
    (perceptStates, actuatorStates) = percepts
    
    insideTempSensorName = "Temp&RH_1"
    actuatorName = "Relay4"

    haveInsideTempReading = False

    if actuatorStates[actuatorName] == 1:
        actuatorOn = True
    else:
        actuatorOn = False
    
    turnActuatorOn = actuatorOn

    if insideTempSensorName in perceptStates.keys():
        haveInsideTempReading = perceptStates[insideTempSensorName] is not None
    
    if haveInsideTempReading:
        coldInside = perceptStates[insideTempSensorName]['temp'] <= goals['insideTempMin']
        warmInside = perceptStates[insideTempSensorName]['temp'] >= goals['insideTempMax']
        mildInside = perceptStates[insideTempSensorName]['temp'] >= ((goals['insideTempMax'] +
                                                                  goals['insideTempMin'])/2)
    
    if haveInsideTempReading:
        if coldInside:
            turnActuatorOn = True
        elif warmInside:
            turnActuatorOn = False

    
    if actuatorOn == turnActuatorOn:
        return None
    elif turnActuatorOn:
        return [(actuatorName, 1)]
    else:
        return [(actuatorName, 0)]






