#!/bin/python3
from mapGenerator import generateMap

##
# Mandatory Inputs
##

algor = input("[+] Enter algorithm for search: ")
width = int(input("[+] Enter width of map: "))
height = int(input("[+] Enter height of map: "))
maxHeightDifference = int(input("[+] Enter maximum height difference for the rover to traverse: "))
numberTargets = int(input("[+] Enter number of targets: "))

##
# Additional inputs
##

deviation = int(input("[+] Enter a height deviation to generate noise in the terrain: "))
baseLine = int(input("[+] Provide a baseline height for your map: "))

params = {
    "algorithm": algor,
    "width": width,
    "height": height,
    "max_height_diff": maxHeightDifference,
    "target_count": numberTargets,
    "deviation": deviation,
    "baseline": baseLine
}

fName = generateMap(params, "hello")