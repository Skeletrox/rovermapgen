#!/bin/python3

import png
import numpy as np
from itertools import product
from PIL import Image, ImageDraw, ImageFont

#
# Generates a map given parameters and a file name
#
def generateMap(params, fileName):

    if len(fileName) < 1:
        return False
    
    algor = params.get("algorithm", "BFS")
    width = params.get("width", 7)
    height = params.get("height", 7)
    maxHeightDifference = params.get("max_height_diff", 10)
    numberTargets = params.get("target_count", 3)
    deviation = params.get("deviation", 5)
    baseLine = params.get("baseline", 50)

    roverMap = np.zeros((height, width), dtype=int)

    # Randomly generate the map

    for i in range(height):
        for j in range(width):
            roverMap[i][j] = np.random.normal(baseLine, (deviation + maxHeightDifference) / 3)

    widths = (x for x in range(width))
    heights = (y for y in range(height))
    productWH = [p for p in product(widths, heights)]

    startCoords = productWH[np.random.randint(0, len(productWH))]
    startingX, startingY = startCoords[0], startCoords[1]
    starting = [startingX, startingY]
    productWH.remove(startCoords)

    targets = []

    for i in range(numberTargets):
        currentCoords = productWH[np.random.randint(0, len(productWH))]
        currentX, currentY = currentCoords[0], currentCoords[1]
        targets.append([currentX, currentY])
        productWH.remove(currentCoords)

    with open('./{}.txt'.format(fileName), 'w+') as ipg:
        ipg.write("{}\n".format(algor))
        ipg.write("{} {}\n".format(width, height))
        ipg.write("{} {}\n".format(startingX, startingY))
        ipg.write("{}\n".format(maxHeightDifference))
        ipg.write("{}\n".format(numberTargets))
        for t in targets:
            ipg.write("{} {}\n".format(t[0], t[1]))
        for h in range(height):
            currLine = " ".join(["{}".format(d) for d in roverMap[h]])
            ipg.write("{}\n".format(currLine))


    # Image map creation

    # Get size of each pixel
    # Since the size of the image is say 1024x768
    # The width of each "location" will be 1024 / total number of locations
    # Similarly height
    widthPerLoc = 1920 // width
    heightPerLoc = 1080 // height

    minimumHeight = np.min(roverMap)
    maximumHeight = np.max(roverMap)
    diff = maximumHeight - minimumHeight

    if diff == 0:
        diff = 0.0001

    # We shall create a blue matrix, green for goals and red for starting point
    blueArr = np.array([0, 0, 1, 255])
    greenArr = np.array([0, 1, 0, 255])
    redArr = np.array([1, 0, 0, 255])
    imageMap = []
    for i in range(height):
        currentRow = []
        for j in range(width):
            roverMapVal = roverMap[i][j]
            shadingCoefficient = int((roverMapVal - minimumHeight) / diff * 235) + 10
            heightFactor = np.array([shadingCoefficient, shadingCoefficient, shadingCoefficient, 1])
            currRoverPixel = np.zeros((4), dtype=float)
            if (i, j) == (startingY, startingX):
                currRoverPixel = np.multiply(heightFactor, redArr)
            elif [j, i] in targets:
                currRoverPixel = np.multiply(heightFactor, greenArr)
            else:
                currRoverPixel = np.multiply(blueArr, heightFactor)
            # The current pixel will now be appended to the currentRow
            currentRow.extend([int(x) for x in currRoverPixel.tolist()]*widthPerLoc)
        # Add the current row to the image map
        imageMap.extend([currentRow]*heightPerLoc)
    with open('./{}.png'.format(fileName), 'wb+') as f:
        w = png.Writer(height=len(imageMap), width=len(imageMap[0]) // 4, greyscale=False, alpha=True, background=[0,0,0])
        w.write(f, imageMap)

    base = Image.open("./{}.png".format(fileName)).convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))

    fontSize = int(min(widthPerLoc, heightPerLoc)) // 4
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', fontSize)
    # get a drawing context
    d = ImageDraw.Draw(txt)
    for i in range(height):
        for j in range(width):
            d.text((widthPerLoc*j + widthPerLoc // 4 ,heightPerLoc*i + heightPerLoc // 4), "{}".format(roverMap[i][j]), font=fnt, fill=(255,255,255,255))
    out = Image.alpha_composite(base, txt)

    out.save("./{}.png".format(fileName), "PNG")

    return True



def generateOutputMap(solutions, fileName):
    base = Image.open("./{}.png".format(fileName)).convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))