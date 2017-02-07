import tweepy
import secrets
import random
import string
from math import sqrt, sin, cos

import randomcolor

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():	
	#Create Random Color Array
	randColor = randomcolor.RandomColor()
	randColorArray = randColor.generate(hue="random", count=5)

	makeAndSaveImage(randColorArray)

	auth = tweepy.OAuthHandler(secrets.C_KEY, secrets.C_SECRET)  
	auth.set_access_token(secrets.A_TOKEN, secrets.A_TOKEN_SECRET)  
	api = tweepy.API(auth)

	#Print and Send Tweet
	randColorArray[3] = RandomMix(randColorArray[0], randColorArray[1], randColorArray[2],3)
	randColorArray[4] = RandomMix(randColorArray[0], randColorArray[1], randColorArray[2],3)
	
	status = convertColorsToStatus(randColorArray)
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

def RandomMix(color1, color2, color3, greyControl):

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

def getRed(inColor):
	inColor = inColor[1:len(inColor)+1]
	return int(inColor[0:2], 16)

def getGreen(inColor):
	inColor = inColor[1:len(inColor)+1]
	return int(inColor[2:4], 16)

def getBlue(inColor):
	inColor = inColor[1:len(inColor)+1]
	return int(inColor[4:6], 16)

#######################
def getFiveColors(hue, sat, value, delta):
    		oneThird = 52
            h0 = hue
            h1s = (h0 + oneThird) % 1.0
            h2s = (h1s + oneThird) % 1.0
            delta = 0.06*parameter
            h1 = (h1s - delta) % 1.0
            h2 = (h1s + delta) % 1.0
            h3 = (h2s - delta) % 1.0
            h4 = (h2s + delta) % 1.0

            #new hues, same sats and values
######################################################
if __name__ == "__main__":
	main()
