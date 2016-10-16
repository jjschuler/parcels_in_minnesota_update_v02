#-------------------------------------------------------------------------------
# Name:        parcels_processing_functions.py
# Purpose:     Functions for running ETL that don't need parameters.
#
# Author:      Jeff Reinhart
#
# Created:     10/01/2016
#-------------------------------------------------------------------------------

import arcpy, datetime, os, urllib2, zipfile

def writeToErrorLog(countyName, currentProcess, objectid, field, error, traceback):
    '''Writes to error log for process based and row based errors. Creates or
    appends to error_log.txt in same directory as script.'''

    # Output
    cwd = os.getcwd()
    errorLog = os.path.join(cwd, 'error_log.txt')
    dt = datetime.datetime.now()

    # Build log entry as date, current process, esri error
    logEntry = "DATE: {0}\n".format(dt.strftime("%Y-%m-%d %H:%M:%S"))+\
               "COUNTY: {0}\n".format(countyName)+\
               "PROCESS: {0}\n".format(currentProcess)+\
               "OBJECTID: {0}\n".format(objectid)+\
               "FIELD: {0}\n".format(field)+\
               "ERROR: {0}\n".format(error)+\
               "TRACEBACK: {0}\n".format(traceback)+\
               "<end>\n\n"

    # Write log entry
    with open(errorLog,'a+') as f:
        f.write(logEntry)

def templateSetup(append_OR_createnew, wkspGdb):
    print "Setting up parcels_in_minnesota from template..."
    templateFc = os.path.join(wkspGdb, "parcels_in_minnesota_template")
    outMnFc = os.path.join(wkspGdb, "parcels_in_minnesota")
    # create new or append
    if append_OR_createnew == "createnew":
        # create new feature class from template
        if arcpy.Exists(outMnFc):
            print "Deleting existing {0}...".format(outMnFc)
            arcpy.Delete_management(outMnFc)
        print "Creating new {0}...".format(outMnFc)
        arcpy.CopyFeatures_management(templateFc, outMnFc)
    elif append_OR_createnew == "append":
        # append to existing feature class
        print "Appending to existing {0}...".format(outMnFc)
        if not arcpy.Exists(outMnFc):
            print "{0} does not exist, ending process...".format(outMnFc)
            sys.exit()
    else:
        print "Invalid string for append_OR_createnew, ending process..."
        sys.exit()

def downloadExtract(username, password, sourcePath, sourceZipFile, ctyAbbr):
    mnGeoUrl = "http://geoint.lmic.state.mn.us/parcels/"

    # connection to MnGeo site
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, mnGeoUrl, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    opener.open(mnGeoUrl)
    urllib2.install_opener(opener)

    # download from URL
    sourceUrl = mnGeoUrl + sourceZipFile
    sourceZipFile = os.path.join(sourcePath, sourceZipFile)
    print "Saving {0} to {1}...".format(sourceUrl, sourceZipFile)

    # open the URL
    response = urllib2.urlopen(sourceUrl)

    # write to file
    with open(sourceZipFile, 'wb') as f:
        while True:
            tmp = response.read(1024)
            if not tmp:
                break
            f.write(tmp)

    # extract file
    sourceFilePath = os.path.join(sourcePath, ctyAbbr)
    print "Extracting to {0}...".format(sourceFilePath)
    zipRef = zipfile.ZipFile(sourceZipFile, 'r')
    zipRef.extractall(sourceFilePath)
    zipRef.close()

def projectJoin(sourcePath, wkspGdb, ctyAbbr, sourcePolygons, sourceOwnershipTable, joinInField, joinJoinField):
    # spatial reference object for projection
    outCoordsObj = arcpy.SpatialReference("NAD 1983 UTM Zone 15N")
    # output path for parcel feature class
    inSpatial = os.path.join(sourcePath, ctyAbbr, sourcePolygons)
    outPath = os.path.join(wkspGdb, ctyAbbr)
    tempPath = os.path.join(wkspGdb, "temp")
    print "Creating feature class {0}...".format(outPath)
    # clear in_layer if exists from previous failed run
    if arcpy.Exists("in_layer"):
        arcpy.Delete_management("in_layer")
    # clear tempFc used for join if exists from previous failed run
    if arcpy.Exists(tempPath):
        arcpy.Delete_management(tempPath)
    # set up dataset
    print "Creating layer..."
    inLayer = arcpy.MakeFeatureLayer_management(inSpatial, "in_layer")
    # join if needed
    if sourceOwnershipTable != '':
        # if xslx, import table to wkspGdb, else set joinTable path
        if sourceOwnershipTable[-4:] == 'xlsx':
            inXlsx = os.path.join(sourcePath, ctyAbbr, sourceOwnershipTable)
            outTablePath = os.path.join(wkspGdb, ctyAbbr+"_t")
            # delete if exists
            if arcpy.Exists(outTablePath):
                arcpy.Delete_management(outTablePath)
            # excel to table
            arcpy.ExcelToTable_conversion(inXlsx, outTablePath)
            joinTable = outTablePath
        else:
            joinTable = os.path.join(sourcePath, ctyAbbr, sourceOwnershipTable)
        print "Adding join..."
        inField = joinInField
        joinField = joinJoinField
        arcpy.AddJoin_management(inLayer, inField, joinTable, joinField)
        print "Copying joined features..."
        tempFc = arcpy.CopyFeatures_management(inLayer, tempPath)
        # reset inlayer to copied features
        arcpy.Delete_management("in_layer")
        inLayer = arcpy.MakeFeatureLayer_management(tempFc, "in_layer")
    # delete if exists
    if arcpy.Exists(outPath):
        arcpy.Delete_management(outPath)
    # project
    print "Projecting..."
    outFc = arcpy.Project_management(inLayer, outPath, outCoordsObj)
    # delete layer
    arcpy.Delete_management("in_layer")
    # delete tempFc used for join if needed
    if arcpy.Exists(tempPath):
        arcpy.Delete_management(tempPath)

