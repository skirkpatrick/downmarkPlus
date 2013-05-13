import smtplib
import datetime
import os
from email.mime.text import MIMEText
from Tkinter import *
from HTMLParser import HTMLParser
from Converter import Converter
from StringFormat import StringFormat



#Resultant string is stored as a global variable
#such that it can be modified by HTMLParser handlers
result = ""

#Global storage of previously concatenated data, to prevent
#repeated content
previousContent = ""
previousAlt = ""
previousURL = ""

#Stores most recently parsed URL/IMG information for display
#after the associated plaintext
currURL = ""
currAlt = ""

#Stores source links for IMG tags
images = [];

#Surpression flag to be toggled in the case of certain
#HTML tags (e.g. <HEAD>) to prevent non-content data
#from being copied
suppress = False

#Root widget for interface
root = Tk()
root.wm_title("Downmark Plus")
if os.name == 'nt':
    root.iconbitmap(default='favicon.ico')
else:
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='favicon.gif'))
prompt = Label(root, text="Enter HTML content below.")

#Textbox for HTML input
inHTML = Text()

#Textbox for plaintext output
outText = Text()

#Determines whether or not images will be converted to ascii
#art when text is generated.  Bound to a checkbox.
includeArt = BooleanVar()

#HTML parsing is handled here via inheritance of the
#HTMLParser class
class parse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        c = Converter()

        if tag == "head" or tag == "style":
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
                    if includeArt.get() == True:
                        global result
                        result += c.genArt(attr[1], float(threshold.get()), int(width.get())) + "\n"
            currAlt = alt

        if tag == "li":
            global result
            result += "    -"

        if tag == "br":
            global result
            result += "\n"

        
    def handle_endtag(self, tag):	
        #print "End tag:", tag
        
        if tag == "head" or tag == "style":
            global suppress
            suppress = False
            
        if tag == "a" or tag == "img":
            global result
            global currAlt
            global currURL
            if currAlt != "":
                result += currAlt + '\n'
                currAlt = ""
            if currURL != "":
                result += '\n' + currURL + '\n\n'
                currURL = ""
                
        if tag == "td":
            global result
            result += '\n'

        if tag == "p" or tag == "section" or tag == "aside" or tag == "li":
            global result
            result += '\n'
            
    def handle_comment(self, data):
        #print "Comment:", data
        pass
        
    def handle_data(self, data):
        #print "Data:", data
        data = data.strip()
        global previousContent
        global result
        global suppress
        if len(data) > 0:
            if data[0] == '<':
                #print "Non-text data, discard:" + data
                pass
            else:
                if data != previousContent and suppress == False:
                    result += data + " "
                    previousContent = data

#Dialog for issue reporting
class ReportDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Name", anchor = W).pack()
        self.submitter = Entry(top)
        self.submitter.pack(padx = 5)
        Label(top, text="Description", anchor = W).pack()
        self.description = Text(top)
        self.description.pack(padx = 5)
        submitBtn = Button(top, text = "Submit report", command = self.submit)
        submitBtn.pack(pady = 5)

    #Construct an email and send it via SMTP
    def submit(self):
        text = "DownmarkPlus error submission \n"
        text += "Submitted by " + self.submitter.get() + '\n'
        text += "Submitted at " + str(datetime.datetime.now()) + '\n\n'
        text += "------- Report description -------\n\n"
        text += self.description.get(1.0, END) + "\n\n"
        text += "------- HTML Input ------- \n\n"
        text += inHTML.get(1.0, END) + "\n\n"
        text += "------- Text Output ------- \n\n"
        text += outText.get(1.0, END) + "\n\n"
        
        msg = MIMEText(text)
        msg['Subject'] = "DownmarkPlus Error Report"
        msg['From'] = "put an email here"
        msg['To'] = "put to addrs here"
        msg['cc'] = "put ccs here"

        toaddr = ['toaddr']
        cc = ['cc']
        toaddrs = toaddr + cc

        s = smtplib.SMTP('yourmailprovider', 26)
        try:
            s.login("yourlogin", "yourpassword")
            s.sendmail("youremail", toaddrs, msg.as_string())
        finally:
            s.quit()
        
        #print(text)
        self.top.destroy()



#HTML decoder
unescape = parse.unescape

#Conversion button event handler
def convertHTML():
    sf = StringFormat()
    outText.delete(1.0, END)
    parser = parse()
    toConvert = sf.unescape(inHTML.get(1.0, END))
    parser.feed(toConvert)
    global result
    final = sf.formatLines(result)
    outText.insert(END, final)
    result = ""

#Selection button event handler
def select():
    outText.focus()
    outText.tag_add(SEL, 1.0, END)
    outText.mark_set(INSERT, 1.0)
    outText.see(INSERT)
    text = outText.get("sel.first", "sel.last")
    copy(text)
    return 'break'

#Copies highlighted text to windows clipboard
def copy(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)

def clearAll():
	outText.delete(1.0, END)
	inHTML.delete(1.0, END)

#Submit error report
def submit():
    rd = ReportDialog(root)
    root.wait_window(rd.top)

prompt.pack()
inHTML.pack()

threshHoldLabel = Label(root, text="Enter image threshold")
threshHoldLabel.pack()
threshold = Entry(root, width=4)
threshold.pack()

widthLabel = Label(root, text="Enter image width")
widthLabel.pack()
width = Entry(root, width=4)
width.pack()

incArt = Checkbutton(root, text=" Include Art", variable = includeArt, onvalue=True, offvalue=False)
incArt.pack()

bGenerate = Button(root, text = "Generate Text", width = 15, height = 2, command = convertHTML)
bGenerate.pack()

bClearAll = Button(root, text = "Clear all", width = 15, height = 2, command = clearAll)
bClearAll.pack()

bCopy = Button(root, text = "Copy all", width = 15, height = 2, command = select)
bCopy.pack()

bSubmit = Button(root, text = "Report an issue", width = 15, height = 2, command = submit)
bSubmit.pack()

outText.pack()

root.mainloop()
