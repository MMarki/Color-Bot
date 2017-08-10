import tweepy
import secrets
import random
import re
import string
import colorsys
import collections
from math import sqrt, sin, cos, ceil

import randomcolor

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():	
	auth = tweepy.OAuthHandler(secrets.C_KEY, secrets.C_SECRET)  
	auth.set_access_token(secrets.A_TOKEN, secrets.A_TOKEN_SECRET)  
	api = tweepy.API(auth)

	colorFailure = "I didn't see a color, so I made you this: "

	#colorArray = makeRandomColorPalette()
	#status = convertColorsToStatus(colorArray)

	#Open player_status file
	f_status = open('/home/pi/Desktop/ColorBot/status.txt', 'r+')

	#Player status file setup
	topMentionId = f_status.readline()
	topMentionId = int(topMentionId.rstrip('\n'))

	mentions = api.mentions_timeline(since_id=topMentionId, count=200)

	for mention in mentions:
		print mention.id
		print mention.text
		userColor = getUserColor(mention.text)
		if (userColor == colorFailure):
			colorArray = makeRandomColorPalette()
			status = '@' + mention.user.screen_name + colorFailure + '\n' + convertColorsToStatus(colorArray)
		else:
			colorArray = getColorHarmony(userColor)
			status = '@' + mention.user.screen_name + '\n' + convertColorsToStatus(colorArray)

                topMentionId = storeMentionId(mention.id, topMentionId,f_status)

		#Print and Send Tweet
		makeAndSaveImage(colorArray)
		printAndSendTweet(status, api, mention.id)

	f_status.close()
	
################################################################################################
#print the tweet
def printAndSendTweet(inStatus, inAPI, inMentionId):
	
	printTweet(inStatus)
	inAPI.update_with_media("/home/pi/Desktop/ColorBot/palette.png",inStatus, in_reply_to_status_id=inMentionId)

def printTweet(tweet): 
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
	fig.savefig('/home/pi/Desktop/ColorBot/palette.png', dpi=90)

def getColorHarmony(inColor):
	
	harmonyChoice = random.randrange(0,12)

	if (harmonyChoice == 0 or harmonyChoice == 1):
		newrandColorArray = getAnalogousHarmony(inColor,0.2)
	elif (harmonyChoice == 2):
		newrandColorArray = getMonochromaticHarmony(inColor,0.1, 0.25)
	elif (harmonyChoice == 3):
		newrandColorArray = goldenRatio(inColor)
	elif (harmonyChoice == 4 or harmonyChoice == 5):
		newrandColorArray = getModTriadicHarmony(inColor,0.8)
	elif (harmonyChoice == 6 or harmonyChoice == 7):
		newrandColorArray = getPentadicHarmony(inColor, 0.1)
	elif (harmonyChoice == 8 or harmonyChoice == 9):
		newrandColorArray = getSplitTetradicHarmony(inColor, 0.05)
	else: #10 or 11
		newrandColorArray = getModPentadicHarmony(inColor)

	return newrandColorArray

def getUserColor(userText):

	colors = re.findall('[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]',userText)
	if isEmpty(colors):
		colors = re.findall('[0-9A-F][0-9A-F][0-9A-F]',userText)
		if isEmpty(colors):
			newColors = findColorWords(userText)
			if isEmpty(colors):
				return "I didn't see a color, so I made you this: "
			else:
				returnText = newColors
		else:
			returnText = '#' + doubleString(colors[0])
	else:
		returnText = '#' + colors[0]

	if (len(returnText) == 7):
		return returnText
	else:
		return "I didn't see a color, so I made you this: "

def isEmpty(colorList):

        if (colorList is None):
                return True
        if (len(colorList) < 1):
                return True
        return False

def makeRandomColorPalette():
	#Create Random Color Array
	randColor = randomcolor.RandomColor()
	randColorArray = randColor.generate(hue="random", count=1)
	colorArray = getColorHarmony(lightenColor(randColorArray[0]))
	
	return colorArray

def lightenColor(inColor):
	if inColor[1] < '4':
		inColor[1] = '4'
	if inColor[3] < '4':
		inColor[1] = '4'
	if inColor[5] < '4':
		inColor[1] = '4'
	
	return inColor


def findColorWords(inString):
	recognizedColors = collections.OrderedDict()

        recognizedColors['chrome'] = '#B7BAC1'
        recognizedColors['lilac'] = '#B666D2'
        recognizedColors['slate'] = '#9098A3'
        recognizedColors['steel'] = '#8CA2A3'
        recognizedColors['indigo'] = '#141951'
        recognizedColors['turquoise'] = '#42F2F7'
        recognizedColors['mauve'] = '#DAB6FC'
        recognizedColors['hot pink'] = '#FC4CFF'
        recognizedColors['chartreuse'] = '#CFCE74'
        recognizedColors['cornflower blue'] = '#659CEF'
        recognizedColors['light orange'] = '#FFA14F'
        recognizedColors['blood orange'] = '#E7341D'
        recognizedColors['ivory'] = '#FEFAEF'
        recognizedColors['nude'] = '#F1D5BF'
        recognizedColors['sand'] = '#ECDFCC'
        recognizedColors['beige'] = '#D5B795'
        recognizedColors['mocha'] = '#987E6D'
        recognizedColors['taupe'] = '#A08A7F'
        recognizedColors['camel'] = '#A87D5B'
        recognizedColors['dark orange'] = '#FF6500'
        recognizedColors['dark red'] = '#990000'
        recognizedColors['light red'] = '#FF4242'
        recognizedColors['dark green'] = '#005600'
        recognizedColors['light green'] = '#19E519'
        recognizedColors['lime green'] = '#00FF00'
        recognizedColors['dark blue'] = '#000095'
        recognizedColors['light blue'] = '#3F7FFF' 
        recognizedColors['dark yellow'] = '#D1BC34'
        recognizedColors['gold'] = '#D1BC34'
        recognizedColors['light yellow'] = '#FFF950'
        recognizedColors['orange'] = '#FF851B'
        recognizedColors['cyan'] = '#2DFDFF'
        recognizedColors['magenta'] = '#FF00FF'
        recognizedColors['silver'] = '#C0C0C0'
        recognizedColors['purple'] = '#800080'
        recognizedColors['fuchsia'] = '#FF00FF'
        recognizedColors['pink'] = '#FF70B2'
        recognizedColors['brown'] = '#68422E'	
        recognizedColors['navy'] = '#000080'
        recognizedColors['blue'] = '#0074D9'	
        recognizedColors['teal'] = '#39CCCC'
        recognizedColors['aqua'] = '#00FFFF'	
        recognizedColors['green'] = '#008000'
        recognizedColors['lime'] = '#00FF00'	
        recognizedColors['olive'] = '#3D9970'
        recognizedColors['yellow'] = '#FFFF00'
        recognizedColors['maroon'] = '#85144b'
        recognizedColors['red'] = '#FF0000'
        recognizedColors['grey'] = '#AAAAAA'
        recognizedColors['gray'] = '#AAAAAA'
        recognizedColors['white'] = '#FFFFFF'
        recognizedColors['black'] = '#000000'

	for key in recognizedColors:
		if (key in inString): return recognizedColors[key]

	return 

def doubleString(inString):
    return ''.join([x*2 for x in inString])

def storeMentionId(inMentionId, inTopMentionId,inFile):
	if (inMentionId > inTopMentionId):
		inFile.seek(0)
		inFile.write(str(inMentionId) + '\n')
		return inMentionId
	else:
		return inTopMentionId

##############################
#RGB Color -> 5 Offset Golden Ratio RGB Colors
def goldenRatio(inBaseColor):

	inColor = fixHueless(inBaseColor)

	baseColorTuple = colorsys.rgb_to_hsv(redHex2Fraction(inColor), greenHex2Fraction(inColor), blueHex2Fraction(inColor))

	color = [0] * 5
	color[0] = inBaseColor

	hue = baseColorTuple[0]
	sat = baseColorTuple[1]
	value = baseColorTuple[2]

	for i in range(1,5):
		colorTuple = colorsys.hsv_to_rgb((hue + (0.0618033988749895 * i)) % 1, sat, value)
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

	inColor = fixHueless(inBaseColor)
	#hls tuple
	baseColorTuple = colorsys.rgb_to_hsv(redHex2Fraction(inColor), greenHex2Fraction(inColor), blueHex2Fraction(inColor))

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

#RGB Color -> 5 Pentadic RGB Colors
def getPentadicHarmony(inBaseColor, hueVariation):
	oneFifth = 0.2

	inColor = fixHueless(inBaseColor)
	#hls tuple
	baseColorTuple = colorsys.rgb_to_hsv(redHex2Fraction(inColor), greenHex2Fraction(inColor), blueHex2Fraction(inColor))

	color = [0] * 5
	color[0] = inBaseColor

	hue = baseColorTuple[0]
	sat = baseColorTuple[1]
	value = baseColorTuple[2]

	for i in range(1,5):
		colorTuple = colorsys.hsv_to_rgb((hue + (oneFifth * i)) % 1, sat, value)
		color[i] = fractions2Hex(colorTuple[0],colorTuple[1],colorTuple[2])

	#new hues, same sats and value
	return color

#RBG Color -> 5 Analogous RGB Colors
def getAnalogousHarmony(inBaseColor, hueVariation):
	
	inColor = fixHueless(inBaseColor)
	#hls tuple
	baseColorTuple = colorsys.rgb_to_hls(redHex2Fraction(inColor), greenHex2Fraction(inColor), blueHex2Fraction(inColor))

	color1 = inBaseColor

	hue = baseColorTuple[0]
	lum = baseColorTuple[1]
	sat = baseColorTuple[2]

	#rgb tuples
	colorTuple2 = colorsys.hls_to_rgb(hue + float(hueVariation)/2, lum, sat)
	colorTuple3 = colorsys.hls_to_rgb(hue + float(hueVariation), lum, sat)
	colorTuple4 = colorsys.hls_to_rgb(hue - float(hueVariation)/2, lum, sat)
	colorTuple5 = colorsys.hls_to_rgb(hue - float(hueVariation), lum, sat)

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

#RBG Color -> 5 split tetradic RGB Colors
def getSplitTetradicHarmony(inBaseColor, hueVariation):
	compAngle = 0.5

	inColor = fixHueless(inBaseColor)

	#hls tuple
	baseColorTuple = colorsys.rgb_to_hls(redHex2Fraction(inColor), greenHex2Fraction(inColor), blueHex2Fraction(inColor))

	color1 = inBaseColor

	hue = baseColorTuple[0]
	lum = baseColorTuple[1]
	sat = baseColorTuple[2]

	#rgb tuples
	colorTuple2 = colorsys.hls_to_rgb((hue - float(hueVariation)) % 1, lum, sat)
	colorTuple3 = colorsys.hls_to_rgb((hue + float(hueVariation)) % 1, lum, sat)
	colorTuple4 = colorsys.hls_to_rgb((hue + compAngle - float(hueVariation)) % 1, lum, sat)
	colorTuple5 = colorsys.hls_to_rgb((hue + compAngle + float(hueVariation)) % 1, lum, sat)

	retArray = [0] * 5

	#RBG Hex
	retArray[0] = fractions2Hex(colorTuple2[0],colorTuple2[1],colorTuple2[2])
	retArray[1] = color1
	retArray[2] = fractions2Hex(colorTuple3[0],colorTuple3[1],colorTuple3[2])
	retArray[3] = fractions2Hex(colorTuple4[0],colorTuple4[1],colorTuple4[2])
	retArray[4] = fractions2Hex(colorTuple5[0],colorTuple5[1],colorTuple5[2])

	return retArray

#RBG Color -> 5 Monochromatic RGB Colors
def getMonochromaticHarmony(inBaseColor, lumVariation, satVariation):
	
	inColor = fixHueless(inBaseColor)

	#hls tuple
	baseColorTuple = colorsys.rgb_to_hls(redHex2Fraction(inColor), greenHex2Fraction(inColor), blueHex2Fraction(inColor))

	color1 = inBaseColor

	hue = baseColorTuple[0]
	lum = baseColorTuple[1]
	sat = baseColorTuple[2]

	#rgb tuples
	colorTuple2 = colorsys.hls_to_rgb(hue, (lum - lumVariation) % 1, (sat - satVariation) % 1)
	colorTuple3 = colorsys.hls_to_rgb(hue, (lum + lumVariation) % 1, (sat - satVariation) % 1)
	colorTuple4 = colorsys.hls_to_rgb(hue, (lum - lumVariation) % 1, (sat + satVariation) % 1)
	colorTuple5 = colorsys.hls_to_rgb(hue, (lum + lumVariation) % 1, (sat + satVariation) % 1)

	retArray = [0] * 5

	#RBG Hex
	retArray[0] = color1
	retArray[1] = fractions2Hex(colorTuple2[0],colorTuple2[1],colorTuple2[2])
	retArray[2] = fractions2Hex(colorTuple3[0],colorTuple3[1],colorTuple3[2])
	retArray[3] = fractions2Hex(colorTuple4[0],colorTuple4[1],colorTuple4[2])
	retArray[4] = fractions2Hex(colorTuple5[0],colorTuple5[1],colorTuple5[2])

	return retArray

def getModPentadicHarmony(inBaseColor):
	retArray = [0] * 5

	offsetAngle = getHueOffsetArray()

	inColor = fixHueless(inBaseColor)

	baseColorTuple = colorsys.rgb_to_hls(redHex2Fraction(inColor), greenHex2Fraction(inColor), blueHex2Fraction(inColor))

	color1 = inBaseColor

	hue = baseColorTuple[0]
	lum = baseColorTuple[1]
	sat = baseColorTuple[2]

	retArray = [0] * 5

	#RBG Hex
	retArray[0] = color1

	for index in range(1,5):
		colorTuple = colorsys.hls_to_rgb((hue + offsetAngle[index]) % 1, lum, sat)
		retArray[index] = fractions2Hex(colorTuple[0],colorTuple[1],colorTuple[2])

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

def getHueOffsetArray():
	arrayNumber = random.randrange(0,5)
	hueArray0 = [0, 0.31944444444, 0.43055555555, 0.56944444444, 0.68055555555]
	hueArray1 = [0, 0.11111111111, 0.25, 0.36111111111, 0.68055555555]
	hueArray2 = [0, 0.13888888888, 0.25, 0.56944444444, 0.88888888888]
	hueArray3 = [0, 0.11111111111, 0.43055555555, 0.75, 0.86111111111]
	hueArray4 = [0, 0.31944444444, 0.63888888888, 0.75, 0.88888888888]

	if (arrayNumber == 0):
		retArray = list(hueArray0)
	elif (arrayNumber == 1):
		retArray = list(hueArray1)
	elif (arrayNumber == 2):
		retArray = list(hueArray2)
	elif (arrayNumber == 3):
		retArray = list(hueArray3)
	else:
		retArray = list(hueArray4)

	return retArray

def getHex(inValue):
	retVal = hex(int(ceil(inValue)))[2:]
	if len(retVal) == 1:
		retVal ='0' + retVal
	return retVal

def checkIfHueless(inColor):
	inColor = inColor[1:len(inColor)+1]
	firstValue = inColor[1]
	for char in inColor:
		if char != firstValue:
			return False

	return True

def fixHueless(inColor):
	if checkIfHueless(inColor):
		inColor = inColor[1:len(inColor)+1]
		newColorList = list(inColor)
		newColorList[getNewIndex()] = newLetter(inColor)
		newColor = ''.join(newColorList)
		return newColor
	else:
		return inColor

def getNewIndex():
	newIndexIndex = random.randint(0,2)
	switcher = {
			0: 1,
			1: 3,
			2: 5
		}

	newIndex = switcher.get(newIndexIndex,0)

	return newIndex

def newLetter(inColorNoHash):
	currentLetter = inColorNoHash[0]
	newLetter = '8'
	switcher = {
			0: '0',
			1: '1',
			2: '2',
			3: '3',
			4: '4',
			5: '5',
			6: '6',
			7: '7',
			8: '8',
			9: '9',
			10: 'A',
			11: 'B',
			12: 'C',
			13: 'D',
			14: 'E',
			15: 'F'
		}
	
	while(1):
		newLetterIndex = random.randint(0,15)

		newLetter = switcher.get(newLetterIndex,'8')
		if newLetter != currentLetter:
			break

	return newLetter

######################################################
if __name__ == "__main__":
	main()
