# Sensor Fault Detection

## Problem Statement

Air Pressure System (APS) is a critical component of heavy duty vehicle that uses compressed air to force piston to break pads, slowing the vehicle down. The benefits of using an APS instead of hydrolic system are the easy availability and long term sustainability of natural air.

This is a Binary Classification problem, in which affirmative class indicates that the failure was caused by certain component of APS, while negative class indicates that the failure was caused by something else.

## Solution: 

In this project, the system in focus is Air Pressure System (APS) which generates pressurized air that are utilized in various functions in a truck such as braking and gear changes. The datasets positive class coresponds to component failure for specific component of APS system. The negative class coresponds to trucks with failure for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

# Tech Stack Used

1. Python
2. FastAPI
3. Machine Learning Algorithm
4. Docker
5. MongoDB

## Deploy using docker

### 1. Build ->
`
docker -t <docker-image-name> . 
`
### 2. Check docker images ->
`
docker images
`
### 3. Run docker image ->
`
docker run -p <host-port>:<container-port> <docker-image>
`

