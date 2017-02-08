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
	randColorArray = randColor.generate(hue="random", count=1)

	#newrandColorArray = getAnalogousHarmony(randColorArray[0],0.2)
	newrandColorArray = getModTriadicHarmony(randColorArray[0],0.8)
	#newrandColorArray = goldenRatio(randColorArray[0])
	
	#Print and Send Tweet
	makeAndSaveImage(newrandColorArray)

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
	fig.savefig('palette.png', dpi=90)

##############################
#RGB Color -> 5 Offset Golden Ratio RGB Colors
def goldenRatio(inBaseColor):

	baseColorTuple = colorsys.rgb_to_hsv(redHex2Fraction(inBaseColor), greenHex2Fraction(inBaseColor), blueHex2Fraction(inBaseColor))

	color = [0] * 5
	color[0] = inBaseColor

	hue = baseColorTuple[0]
	print hue
	sat = baseColorTuple[1]
	value = baseColorTuple[2]

	for i in range(1,5):
		print (hue + (0.0618033988749895 * i)) % 1
		colorTuple = colorsys.hsv_to_rgb((hue + (0.0618033988749895 * i)) % 1, sat, value);
		color[i] = fractions2Hex(colorTuple[0],colorTuple[1],colorTuple[2])

	return color

#RGB Color -> 3 Triadic RGB Colors
def getTriadicHarmony(inBaseColor):
	oneThird = 0.3333
	#hls tuple
	baseColorTuple = colorsys.rgb_to_hsv(redHex2Fraction(inBaseColor), greenHex2Fraction(inBaseColor), blueHex2Fraction(inBaseColor))

	color1 = inBaseColor

	hue = baseColorTuple[0]
	sat = baseColorTuple[1]
	value = baseColorTuple[2]

	h2 = (hue + oneThird) % 1
	h3 = (h2 + oneThird) % 1

	#rgb tuples
	colorTuple2 = colorsys.hsv_to_rgb(h2, sat, value)
	colorTuple3 = colorsys.hsv_to_rgb(h3, sat, value)

	#RGB Hex Colors
	color2 = fractions2Hex(colorTuple2[0],colorTuple2[1],colorTuple2[2])
	color3 = fractions2Hex(colorTuple3[0],colorTuple3[1],colorTuple3[2])

	retArray = [0] * 3

	#new hues, same sats and value
	retArray[0] = color1
	retArray[1] = color2
	retArray[2] = color3

	return retArray

#RGB Color -> 5 Modified Triadic RGB Colors
def getModTriadicHarmony(inBaseColor, hueVariation):
	oneThird = 0.3333
	#hls tuple
	baseColorTuple = colorsys.rgb_to_hsv(redHex2Fraction(inBaseColor), greenHex2Fraction(inBaseColor), blueHex2Fraction(inBaseColor))

	retArray = [0] * 5
	retArray[0] = inBaseColor

	hue = baseColorTuple[0]
	sat = baseColorTuple[1]
	value = baseColorTuple[2]

	h2s = (hue + oneThird) % 1
	h3s = (h2s + oneThird) % 1

	delta = 0.06*hueVariation
	h2 = (h2s - delta) % 1
	h3 = (h2s + delta) % 1
	h4 = (h3s - delta) % 1
	h5 = (h3s + delta) % 1

	#rgb tuples
	colorTuple2 = colorsys.hsv_to_rgb(h2, sat, value)
	colorTuple3 = colorsys.hsv_to_rgb(h3, sat, value)
	colorTuple4 = colorsys.hsv_to_rgb(h4 ,sat, value)
	colorTuple5 = colorsys.hsv_to_rgb(h5, sat, value)

	#RGB Hex Colors
	retArray[1] = fractions2Hex(colorTuple2[0],colorTuple2[1],colorTuple2[2])
	retArray[2] = fractions2Hex(colorTuple3[0],colorTuple3[1],colorTuple3[2])
	retArray[3] = fractions2Hex(colorTuple4[0],colorTuple4[1],colorTuple4[2])
	retArray[4] = fractions2Hex(colorTuple5[0],colorTuple5[1],colorTuple5[2])

	#new hues, same sats and value
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

	#RBG Hex
	color2 = fractions2Hex(colorTuple2[0],colorTuple2[1],colorTuple2[2])
	color3 = fractions2Hex(colorTuple3[0],colorTuple3[1],colorTuple3[2])
	color4 = fractions2Hex(colorTuple4[0],colorTuple4[1],colorTuple4[2])
	color5 = fractions2Hex(colorTuple5[0],colorTuple5[1],colorTuple5[2])

	retArray = [0] * 5

	#Order by Hue
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
