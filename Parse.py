#This class was a work-in-progress at the deadline.  It is by 
#no means compelte, but I hope it will be at some point.  This
#file is not currently used by the application.

#HTML parsing library
from HTMLParser import HTMLParser

#Ascii conversion object
from Converter import Converter

previousContent = ""
result = ""
suppress = "" 


#Base HTML parsing is handled here via inheritance of the
#HTMLParser class
class parse(HTMLParser):

    def handle_starttag(self, tag, attrs):
        c = Converter()

        if tag == "head":
            global suppress
            suppress = True

        #Local variables to store content of url and alt args
        url = ""
        alt = ""
    
        if tag == "a":
            global currURL
            for attr in attrs:
                if attr[0] == 'href':
                    if not "mailto" in attr[1]:
                        url = attr[1] 
            currURL = url

        if tag == "img":
            global currAlt
            for attr in attrs:
                if attr[0] == 'alt':
                    alt = attr[1]
                if attr[0] == 'src':
                    global result
                    result += c.GenArt(attr[1]) + "\n"
            currAlt = alt

        if tag == "br":
            global result
            result += "\n"
        
    def handle_endtag(self, tag):	
        #print "End tag:", tag
        
        if tag == "head":
            self.suppress = False
            
        if tag == "a" or tag == "img":
            if currAlt != "":
                global result
                result += currAlt + '\n'
                currAlt = ""
            if currURL != "":
                global result
                result += '\n' + currURL + '\n\n'
                currURL = ""
                
        if tag == "td":
            global result
            result += '\n'
            
    def handle_comment(self, data):
        #print "Comment:", data
        pass
        
    def handle_data(self, data):
        #print "Data:", data
        data = data.strip()
        if len(data) > 0:
            if data[0] == '<':
                #print "Non-text data, discard:" + data
                pass
            else:
                global previousContent
                global suppress
                if data != previousContent and suppress == False:
                    global result
                    global previousContent
                    result += data + " "
                    previousContent = data

    def getResult(self):
        global result
        return result
