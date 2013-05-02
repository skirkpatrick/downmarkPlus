#Libraries used to acquire and read images
from PIL import Image
from StringIO import StringIO
import urllib2

class Converter: 

    #Palette of characters with which to draw, from most visible to least visible
    palette = 'MNHQ$OC?7>!:-;.'

    #Convert image from pixels to Ascii characters, returns array of chars
    def process(self, image):
        art = []
        pixels = list(image.getdata())
        for value in pixels:
            #Since max value is 255, each pixel will have a value of 0-10,
            #in correspondence with the pallete.
            i = value / 25
            art.append(self.palette[i])
        return art

    #Returns a formatted string of ascii art from the provided URL.
    #The algorithm used is a derivative of an an open-source script
    #which can be found here:
    #https://gist.github.com/aeter/359182

    def genArt(self, url, threshold):
        imgSource = urllib2.urlopen(url).read()
        img = Image.open(StringIO(imgSource))	
             
        #Store original height/width of image
        width, height = img.size
        print "Width: " + str(width) + " Height " + str(height)
        #Calculate new height based on new width (arbitrary)
        w = 100
        h = int((height * w) / width)

        #Resize image and convert to grayscale, accordingly
        grayscale = img.resize((w, h)).convert("L")

        processedImage = self.process(grayscale)
        processedImage = ''.join(ch for ch in processedImage)
        finalArt = ""
        
        for i in range(0, len(processedImage)):
            finalArt += processedImage[i]
            if i % w == 0 and i != 0:
                finalArt += "\n"

        #Determine whether or not the occurence of each palette character
        #is too high to render a valid image
        ret = True
        for i in range(0, len(self.palette)):
            if finalArt.count(self.palette[i]) > (threshold * .01 * len(finalArt)):
                print "Count: " + str(finalArt.count(self.palette[i]))
                print "Threshold: " + str(threshold * .01 * len(finalArt))
                ret = False

        if ret == True:
            return finalArt
        else:
            return ""