import Interface

"""
Downmark Plus

Description:
A lightweight, GUI approach toward converting HTML to plaintext.
Primarily intended to be used with email documents, webpage content
can lead to unpredictable results.

Usage:
Copy the HTML to be converted onto the clipboard, and paste it into
the topmost text box.  Click the 'Generate Text' button to begin the
conversion.  The plaintext result will appear in the lower textbox.
Click the 'Copy all' button to copy the result to the clipboard.

Runtime issues can be reported via the 'Report an issue' button, which
will send an email to the maintainers*.  Reports will include:
    - Submitter's name
    - Submission date
    - Description of the issue
    - Provided input
    - Generated output
    
* - Email addresses/passwords are not included in the source distribution, 
    for obvious reasons.  If you wish to use the email functionality yourself, 
    fill in the blanks!
   
"""

__author__ = "Christopher Escue"
__version__ = "1.0.1"
__maintainer__ = "Christopher Escue"
__email__ = "cescue@mail.csuchico.edu"
__status__ = "Production"

Interface.initInterface()
