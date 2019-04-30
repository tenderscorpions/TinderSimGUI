import pymysql
pymysql.install_as_MySQLdb()
#from subprocess import *
#import sys
import os

# Open DB connection
db = pymysql.connect('localhost', 'root', 'password', 'TinderSimDB')
# Prepare a cursor object using cursor() method
cursor = db.cursor()

#pipe = Popen(("pwd"),shell=True,stdout=PIPE).stdout
#output = pipe.read().rstrip().decode("utf-8")
#print(output)

imageDir = '/Users/AlwynLopez/Documents/TechField/TinderSimGUI/Images/'
genderDirs = os.listdir(imageDir)
for dir in genderDirs:
    if dir == "Men":
        gender = "Male"
        genderDir = imageDir + dir + "/"
        genderImageList = os.listdir(genderDir)
        for image in genderImageList:
            #print(image)
            name = image.split('.')[0]
            print(name)
            absImgFPath = genderDir + image
            #print(absImgFPath)
            sql = "INSERT INTO USER(NAME, GENDER, GENDER_PREF, IMAGE_FILE_PATH) " \
                  "VALUES " \
                  "('%s', '%s', '%s', '%s')" %\
                  (name, gender, "Female", absImgFPath)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Commit changes in the db
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
    if dir == "Women":
        gender = "Female"
        genderDir = imageDir + dir + "/"
        genderImageList = os.listdir(genderDir)
        for image in genderImageList:
            #print(image)
            name = image.split('.')[0]
            print(name)
            absImgFPath = genderDir + image
            #print(absImgFPath)
            sql = "INSERT INTO USER(NAME, GENDER, GENDER_PREF, IMAGE_FILE_PATH) " \
                  "VALUES " \
                  "('%s', '%s', '%s', '%s')" % \
                  (name, gender, "Male", absImgFPath)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Commit changes in the db
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
db.close()
