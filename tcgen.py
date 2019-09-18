#!/bin/python3

from mapGenerator import generateMap
from homework3 import executeAlgorithm
import numpy as np
from sys import exit
from PIL import Image, ImageDraw

algorithms = [
    "BFS",
    "A*",
    "UCS"
]

paramlist = []

numTestCases = int(input("[+] Enter number of test cases: "))
maxWidth = int(input("[+] Enter maximum width of map: "))
maxHeight = int(input("[+] Enter maximum height of map: "))

for i in range(numTestCases):
    algor = np.random.choice(algorithms)
    width = np.random.randint(2, maxWidth)
    height = np.random.randint(2, maxHeight)
    maxHeightDifference = np.random.randint(5,20)
    numberTargets = np.random.randint(1, min(width, height) // 2 + 1)
    deviation = int(np.random.normal(maxHeightDifference, maxHeightDifference / 4))
    baseLine = np.random.randint(500)

    params = {
        "algorithm": algor,
        "width": width,
        "height": height,
        "max_height_diff": maxHeightDifference,
        "target_count": numberTargets,
        "deviation": deviation,
        "baseline": baseLine
    }
    paramlist.append(params)
    fileName = "input_gen_{}".format(i+1)
    result = generateMap(params, fileName)
    if not result:
        print("[x] Step {} failed".format(i+1))
    else:
        print("[i] Test case {} created".format(fileName))


colors = [
    (255, 255, 0, 128),
    (255, 0, 255, 128),
    (0, 255, 255, 128),
    (128, 128, 128, 128),
]


for i in range(numTestCases):
    result, solution = executeAlgorithm("input_gen_{}".format(i+1))
    print("[i] Test case for input_gen_{} completed with result {}".format(i+1, "pass" if result else "fail"))
    if solution is not None:
        im = Image.open("input_gen_{}.png".format(i+1))
        widthPerLoc = 1920 // paramlist[i]["width"]
        heightPerLoc = 1080 // paramlist[i]["height"]
        draw = ImageDraw.Draw(im)
        for j in range(len(solution)):
            s = solution[j]
            linepoints = []
            chunks = s.split(" ")
            for c in chunks:
                nums = [int(x) for x in c.split(",")]
                nums[0] = nums[0]*widthPerLoc + widthPerLoc // 2 + 3*j
                nums[1] = nums[1]*heightPerLoc + heightPerLoc // 2 + 3*j
                linepoints.append((nums[0], nums[1]))
            draw.line(linepoints, fill=colors[j % len(colors)], width=4, joint="curve")
            draw.point(linepoints, fill=colors[j % len(colors)])
        im.save("./output_gen_{}.png".format(i+1))
    

print("[i] Paths for successful outputs have been traced.")

                