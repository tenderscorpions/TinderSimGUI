# TinderSimGUI

Download the TinderSimGUI folder, and inside it add an empty folder called Profiles

Python Stuff
Install python wheel (pip install wheel)
Install python mysql (pip install pymysql)
Install python qt5 [find a tutorial on how to install qt4 for your environment]

Environment Stuff
Install mysql and mysql workbench
Set up the database server
Open TinderSimDB.mwb file in mysql workbench and use the forward engineer function to create the database with empty tables
Create the following folders in your location of choice:
     TinderSimGUI/Images/Women
     TinderSimGUI/Profiles
Download the Men folder and place it in the following location:
     TinderSimGUI/Images
Download the images you wish to rate and place them in the below location:
     TinderSimGUI/Images/Women
Look at the file path in the PopulateDB.py and modify it to reflect your absolute path
The TinderSimGUI folder should have the DBCreation.odt, PopulateDB.py, TinderSimDB.mwb, and TinderSimGUI.py files
In terminal, navigate into the TinderSimGUI folder and run:
     python3 PopulateDB.py
Then to rate images, run:
     python3 TinderSimGUI.py
Once you start, you must finish rating.
If you mess up, just delete the folder in the Profiles folder.  And if you are capable, empty the USER_SELECTION table.
