import tweepy
import secrets
import random
import string
import colorsys
from math import sqrt, sin, cos, ceil

import randomcolor

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():	
	#Create Random Color Array
	randColor = randomcolor.RandomColor()
	randColorArray = randColor.generate(hue="random", count=5)

	#Print and Send Tweet
	newrandColorArray = getAnalogousHarmony(randColorArray[0],0.2)

	makeAndSaveImage(newrandColorArray)
	
	#randColorArray[3] = RandomMix(randColorArray[0], randColorArray[1], randColorArray[2],3)
	#randColorArray[4] = RandomMix(randColorArray[0], randColorArray[1], randColorArray[2],3)

	auth = tweepy.OAuthHandler(secrets.C_KEY, secrets.C_SECRET)  
	auth.set_access_token(secrets.A_TOKEN, secrets.A_TOKEN_SECRET)  
	api = tweepy.API(auth)

	status = convertColorsToStatus(newrandColorArray)
	print_tweet(status)
	api.update_with_media("./palette.png",status)

	
################################################################################################
#send the tweet
def print_tweet(tweet): 
	print tweet

def removeHash(colorString):
	return colorString.replace('#','')

def convertColorsToStatus(colorArray):
	return removeHash(colorArray[0]).upper() + '\n' + removeHash(colorArray[1]).upper() + '\n' + removeHash(colorArray[2]).upper() + '\n' + removeHash(colorArray[3]).upper() + '\n' + removeHash(colorArray[4]).upper()

def makeAndSaveImage(colorArray):
	fig = plt.figure(frameon=False)
	fig.set_size_inches(3,3)

	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

	for p in [
	    patches.Rectangle(
	        (0.00, 0.00), 0.2, 1,color=colorArray[0],
	    ),
	    patches.Rectangle(
	        (0.2, 0.00), 0.2, 1,color=colorArray[1]
	    ),
	    patches.Rectangle(
	        (0.4, 0.00), 0.2, 1,color=colorArray[2]
	    ),
	    patches.Rectangle(
	        (0.6, 0.00), 0.2, 1,color=colorArray[3]
	    ),
	    patches.Rectangle(
	        (0.8, 0.00), 0.2, 1,color=colorArray[4]
	    ),
	]:
	    ax.add_patch(p)
	fig.savefig('palette.png', dpi=90)  #bbox_inches='tight', pad_inches=0
##############################
#Takes 3 Hex RBG Colors -> Returns 5 Hex RGB Colors
def RandomMix(color1, color2, color3, greyControl):
	#color1 ex: #00FFAA

	randomIndex = random.randint(1,3)

	if (randomIndex == 1):
		mixRatio1 = random.random() * greyControl 
	else: 
		mixRatio1 = random.random() 

	if (randomIndex == 2):
		mixRatio2 = random.random() * greyControl 
	else: 
		mixRatio2 = random.random() 

	if (randomIndex == 3):
		mixRatio3 = random.random() * greyControl 
	else: 
		mixRatio3 = random.random() 

	sumTotal = mixRatio1 + mixRatio2 + mixRatio3;

	mixRatio1 = mixRatio1 / sumTotal
	mixRatio2 = mixRatio2 / sumTotal
	mixRatio3 = mixRatio3 / sumTotal

	colorStringR = str(mixRatio1 * getRed(color1) + mixRatio2 * getRed(color2) + mixRatio3 * getRed(color3))
	colorStringG = str(mixRatio1 * getGreen(color1) + mixRatio2 * getGreen(color2) + mixRatio3 * getGreen(color3))
	colorStringB =  str(mixRatio1 * getBlue(color1) + mixRatio2 * getBlue(color2) + mixRatio3 * getBlue(color3))

	return '#'+hex(int(float(colorStringR)))[2:] + hex(int(float(colorStringG)))[2:] + hex(int(float(colorStringB)))[2:]
	print hex(int(float(colorStringR)))
	print hex(int(float(colorStringG)))
	print hex(int(float(colorStringB)))

#HSV Color -> 5 Modified Triadic RGB Colors
def getModTriadicHarmony(hue, sat, value, deltaParam):
	oneThird = 0.3333
	h1 = hue
	h2s = (h1 + oneThird)
	h3s = (h2s + oneThird)

	#need to even out h2s and h3s

	delta = 0.06*deltaParam
	h2 = (h2s - delta)
	h3 = (h2s + delta)
	h4 = (h3s - delta)
	h5 = (h3s + delta)

	#rgb tuples
	colorTuple1 = colorsys.hsv_to_rgb(h1, sat, value)
	colorTuple2 = colorsys.hsv_to_rgb(h2, sat, value)
	colorTuple3 = colorsys.hsv_to_rgb(h3, sat, value)
	colorTuple4 = colorsys.hsv_to_rgb(h4 ,sat, value)
	colorTuple5 = colorsys.hsv_to_rgb(h5, sat, value)

	#Hex Colors
	color1 = fractions2Hex(colorTuple1[0],colorTuple1[1],colorTuple1[2])
	color2 = fractions2Hex(colorTuple2[0],colorTuple2[1],colorTuple2[2])
	color3 = fractions2Hex(colorTuple3[0],colorTuple3[1],colorTuple3[2])
	color4 = fractions2Hex(colorTuple4[0],colorTuple4[1],colorTuple4[2])
	color5 = fractions2Hex(colorTuple5[0],colorTuple5[1],colorTuple5[2])

	retArray = [0] * 5

	#new hues, same sats and value
	retArray[0] = color1
	retArray[1] = color2
	retArray[2] = color2
	retArray[3] = color4
	retArray[4] = color5

	return retArray

#RBG Color -> 5 Analogous RGB Colors
def getAnalogousHarmony(inBaseColor, hueVariation):
	#hls tuple
	baseColorTuple = colorsys.rgb_to_hls(redHex2Fraction(inBaseColor), greenHex2Fraction(inBaseColor), blueHex2Fraction(inBaseColor))

	color1 = inBaseColor

	#rgb tuples
	colorTuple2 = colorsys.hls_to_rgb(baseColorTuple[0] + float(hueVariation)/2, baseColorTuple[1], baseColorTuple[2])
	colorTuple3 = colorsys.hls_to_rgb(baseColorTuple[0] + float(hueVariation), baseColorTuple[1], baseColorTuple[2])
	colorTuple4 = colorsys.hls_to_rgb(baseColorTuple[0] - float(hueVariation)/2, baseColorTuple[1], baseColorTuple[2])
	colorTuple5 = colorsys.hls_to_rgb(baseColorTuple[0] - float(hueVariation), baseColorTuple[1], baseColorTuple[2])

	color2 = fractions2Hex(colorTuple2[0],colorTuple2[1],colorTuple2[2])
	color3 = fractions2Hex(colorTuple3[0],colorTuple3[1],colorTuple3[2])
	color4 = fractions2Hex(colorTuple4[0],colorTuple4[1],colorTuple4[2])
	color5 = fractions2Hex(colorTuple5[0],colorTuple5[1],colorTuple5[2])

	retArray = [0] * 5

	retArray[0] = color3
	retArray[1] = color2
	retArray[2] = color1
	retArray[3] = color4
	retArray[4] = color5

	return retArray

#Hex Color -> RBG Integer Values
def getRed(inColor):
	inColor = inColor[1:len(inColor)+1]
	return int(inColor[0:2], 16)

def getGreen(inColor):
	inColor = inColor[1:len(inColor)+1]
	return int(inColor[2:4], 16)

def getBlue(inColor):
	inColor = inColor[1:len(inColor)+1]
	return int(inColor[4:6], 16)

#Hex Color -> Fraction between 0 and 1
def redHex2Fraction(inColor):
	return float(getRed(inColor))/255

def greenHex2Fraction(inColor):
	return float(getGreen(inColor))/255

def blueHex2Fraction(inColor):
	return float(getBlue(inColor))/255

#Fraction between 0 and 1 -> Hex Color
def fractions2Hex(firstFraction, secondFraction, thirdFraction):
	return '#' + getHex(firstFraction*255) + getHex(secondFraction*255)+ getHex(thirdFraction*255)

def getHex(inValue):
	retVal = hex(int(ceil(inValue)))[2:]
	if len(retVal) == 1:
		retVal ='0' + retVal
	return retVal

######################################################
if __name__ == "__main__":
	main()
