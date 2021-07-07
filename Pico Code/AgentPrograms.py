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



heatAgentGoals = {'insideTempMin':3,
                  'insideTempMax':6}

heatAgentSensors = ['Inside',
                    'Outside']

heatAgentActuators = ['Heat Lamp']



def heatAgentProgram(percepts, goals):
    (perceptStates, actuatorStates) = percepts
    
    insideTempSensorName = "Inside"
    actuatorName = "Heat Lamp"

    haveInsideTempReading = False
    iTemp = None

    if actuatorStates[actuatorName] == 1:
        actuatorOn = True
    else:
        actuatorOn = False
    
    turnActuatorOn = actuatorOn

    if insideTempSensorName in perceptStates.keys():
        haveInsideTempReading = perceptStates[insideTempSensorName] is not None
        iTemp = perceptStates[insideTempSensorName]['Temperature']
    
    if haveInsideTempReading:
        coldInside = iTemp <= goals['insideTempMin']
        warmInside = iTemp >= goals['insideTempMax']
        mildInside = iTemp >= (goals['insideTempMax'] + goals['insideTempMin'])/2
    
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






