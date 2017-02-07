import tweepy
import secrets
import random
import string
import re

import randomcolor

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():	
	#Create Random Color Array
	randColor = randomcolor.RandomColor()
	randColorArray = randColor.generate(hue="random", count=5)

	fig = plt.figure(frameon=False)
	fig.set_size_inches(3,3)

	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

	for p in [
	    patches.Rectangle(
	        (0.00, 0.00), 0.2, 1,color=randColorArray[0],
	    ),
	    patches.Rectangle(
	        (0.2, 0.00), 0.2, 1,color=randColorArray[1]
	    ),
	    patches.Rectangle(
	        (0.4, 0.00), 0.2, 1,color=randColorArray[2]
	    ),
	    patches.Rectangle(
	        (0.6, 0.00), 0.2, 1,color=randColorArray[3]
	    ),
	    patches.Rectangle(
	        (0.8, 0.00), 0.2, 1,color=randColorArray[4]
	    ),
	]:
	    ax.add_patch(p)
	fig.savefig('palette.png', dpi=90)  #bbox_inches='tight', pad_inches=0

	auth = tweepy.OAuthHandler(secrets.C_KEY, secrets.C_SECRET)  
	auth.set_access_token(secrets.A_TOKEN, secrets.A_TOKEN_SECRET)  
	api = tweepy.API(auth)

	#Print and Send Tweet
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

######################################################
if __name__ == "__main__":
	main()
