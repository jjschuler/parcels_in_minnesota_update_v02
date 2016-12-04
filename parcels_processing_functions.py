#-------------------------------------------------------------------------------
# Name:        parcels_processing_functions.py
# Purpose:     Supporting processing functions for ETL.
#
# Author:      Jeff Reinhart
#
# Created:     2016-10-01
# Updated:     2016-12-04
#-------------------------------------------------------------------------------

import arcpy, datetime, os, urllib2, zipfile, sys, traceback

def writeToErrorLog(countyName, currentProcess, objectid,
                    field, error, tracebackMessage):
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
               "TRACEBACK: {0}\n".format(tracebackMessage)+\
               "<end>\n\n"

    # Write log entry
    with open(errorLog,'a+') as f:
        f.write(logEntry)

def templateSetup(append_OR_createnew, wkspGdb):
    '''Creates new parcels_in_minnesota feature dataset copied from
    parcels_in_minnesota_template if "createnew", handles if no feature dataset
    to append to if "append".'''
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

def downloadExtract(username, password, sourcePath,
                    sourceZipFile, ctyAbbrIn, site):
    '''Downloads zipped data set from either Mn Geo site or MN Geospatial
    Commons site, extracts downloaded zip file to source folder.'''
    # handle if metro or single county
    if isinstance(ctyAbbrIn, (list)):
        ctyAbbr = 'METR'
    else:
        ctyAbbr = ctyAbbrIn
    print "Downloading and extracting for {0}...".format(ctyAbbr)

    # handle which site
    if site == 'MN Geo':
        url = "http://geoint.lmic.state.mn.us/parcels/"
        # connection to MnGeo site
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, username, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        try:
            opener.open(url)
        except urllib2.HTTPError as e:
            print e.reason
            sys.exit()
        urllib2.install_opener(opener)
    elif site == 'MN Geospatial Commons':
        url = "ftp://ftp.gisdata.mn.gov/pub/gdrs/data/"+\
              "pub/us_mn_state_metrogis/plan_regonal_parcels_2015/"
    else:
        print "Invalid string for site parameter, "+\
              "use either MN Geo or MN Geospatial Commons."
        sys.exit()

    # download from URL
    sourceUrl = url + sourceZipFile
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

def projectJoin(sourcePath, wkspGdb, inSpatial, ctyAbbr,
                sourceOwnershipTable, joinInField, joinJoinField):
    '''Projects county dataset to workspace geodatabase. If there is a table to
    join in other attributes, joins table and then does projection. Will
    overwrite existing feature dataset if exists.'''
    # spatial reference object for projection
    outCoordsObj = arcpy.SpatialReference("NAD 1983 UTM Zone 15N")
    # output path for parcel feature class
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

def buildCursorLists(cObj):
    # Lists for search cursor and insert cursor.
    fieldsInsert = ['SHAPE@']
    fieldsSearch = ['SHAPE@']

    '''Build field lists dynamically for search cursor that will get values from
    input county data and for insert cursor that will write to statewide
    schema.'''
    for attr in iter(sorted(dir(cObj))):
        if attr[-10:] == "_fieldList":
            # get fieldTransferList
            fieldTransferList = getattr(cObj, attr)
            if len(fieldTransferList) > 0:
                # append field names to statewide schema InsertCursor field list
                fieldsInsert.append(attr[:-10])
                # append field names to county schema SearchCursor field list
                for field in fieldTransferList:
                    fieldsSearch.append(field)

    '''Fields and values not derived from input data to be added at end of
    fieldsInsert after building list from dictionary.'''
    fieldsInsert.append('COUNTY_ID')

    '''Fields to add at end of fieldsSearch because they are not used in
    transfer.'''
    fieldsSearch.append('OBJECTID')

    return [fieldsInsert, fieldsSearch]

def statewidePin(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name.

    Concatenates county id and PIN.'''
    if valueList[0] is None:
        pinVal = ''
    else:
        pinVal = valueList[0]
    newPin = countyId + "-" + str(pinVal)
    return newPin[:fieldLength]

def concatTruncateTwoFields(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Concatenates two fields and truncate, handle null values and non utf-8
    characters.'''
    if valueList[0] is not None and valueList[1] is None:
        if isinstance(valueList[0], (int, long, float, complex)):
            concatValue = str(valueList[0])
        elif any(ord(char) > 126 for char in valueList[0]):
            concatValue = valueList[0].encode('utf-8', 'ignore')
        else:
            concatValue = str(valueList[0])
    elif valueList[0] is not None and valueList[1] is not None:
        if isinstance(valueList[0], (int, long, float, complex)):
            concatValue1 = str(valueList[0])
        elif any(ord(char) > 126 for char in valueList[0]):
            concatValue1 = valueList[0].encode('utf-8', 'ignore')
        else:
            concatValue1 = str(valueList[0])
        if isinstance(valueList[1], (int, long, float, complex)):
            concatValue2 = str(valueList[1])
        elif any(ord(char) > 126 for char in valueList[1]):
            concatValue2 = valueList[1].encode('utf-8', 'ignore')
        else:
            concatValue2 = str(valueList[1])
        concatValue = concatValue1 + " " + concatValue2
    else:
        concatValue = ''
    # set as string and clear leading/trailing spaces
    concatValueStrip = str(concatValue).strip()
    return concatValueStrip[:fieldLength]

def concatTruncateLastAddrLine(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Handles address last line as city, state zip - blank if any are null in
    row.'''
    if valueList[0] is None or valueList[1] is None or valueList[2] is None or \
       valueList[0] == '' or valueList[1] == '' or valueList[2] == '':
        addrLastLineValue = ''
    else:
        addrLastLineValue = "{0}, {1} {2}".format(
            str(valueList[0]),
            str(valueList[1]),
            str(valueList[2]))
    # set as string and clear leading/trailing spaces
    return addrLastLineValue[:fieldLength]

def ToYN(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Changes non Y/N valuse to Y/N.'''
    if valueList[0] is not None and valueList[0] != '':
        returnVal = 'Y'
    else:
        returnVal = 'N'
    return returnVal

def ToDouble(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Converts all numeric to double.'''
    if isinstance(valueList[0], (int, long, float, complex)):
        returnVal = float(valueList[0])
    else:
        returnVal = 0
    return returnVal

def ToSmallInteger(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Converts all numeric to small integer.'''
    if isinstance(valueList[0], (int, long, float, complex)):
        intVal = int(valueList[0])
        if intVal <= 32767 and intVal >= -32768:
            returnVal = intVal
        else:
            returnVal = 0
    elif isinstance(valueList[0], basestring) and valueList[0].isdigit():
        intVal = int(valueList[0])
        if intVal <= 32767 and intVal >= -32768:
            returnVal = intVal
        else:
            returnVal = 0
    else:
        returnVal = 0
    return returnVal

def ToInteger(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Converts all numeric to integer.'''
    if isinstance(valueList[0], (int, long, float, complex)):
        returnVal = long(valueList[0])
    elif isinstance(valueList[0], basestring) and valueList[0].isdigit():
        returnVal = long(valueList[0])
    else:
        returnVal = 0
    return returnVal

def ToDate(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Handles nulls for date fields. TODO: add better handling.'''
    if valueList[0] is not None:
        returnVal = valueList[0]
    else:
        returnVal = None
    return returnVal

def LongIntToDate(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Converts integer date value of YYYYMMDD to datetime.'''
    if valueList[0] is not None:
        intString = str(valueList[0])
        dateFix = datetime.datetime(
            int(intString[0:4]),
            int(intString[4:6]),
            int(intString[6:8]))
        returnVal = dateFix
    else:
        returnVal = None
    return returnVal

def LongIntToDateNoDay(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Converts integer date value of YYYYMM to datetime.'''
    if valueList[0] is not None and len(str(valueList[0])) == 6:
        intString = str(valueList[0])
        dateFix = datetime.datetime(int(intString[0:4]), int(intString[4:6]), 1)
        returnVal = dateFix
    else:
        returnVal = None
    return returnVal

def defaultTransfer(valueList, fieldLength, countyId):
    '''Runs if FIELD_transferType string is same as function name. Param
    countyId not needed here, only used in use for statewidePin, but since
    function is called with getattr, included on all transferType functions.

    Default function for transferType, converts different types to string. Most
    fields in target schema are Text. Truncates based on field length.'''
    # If none then append an empty string
    if valueList[0] is None:
        returnVal = ''
    # If a number cast to unicode
    elif isinstance(valueList[0], (int, long, float, complex)):
        value = unicode(valueList[0])
        returnVal = value[:fieldLength]
        # If has any odd characters
    elif any(ord(char) > 126 for char in valueList[0]):
        # Otherwise just write over using utf-8 so special characters will pass
        value = valueList[0].encode('utf-8', 'ignore')
        returnVal = value[:fieldLength]
    # If a string:
    elif isinstance(valueList[0], (basestring)):
        value = unicode(valueList[0])
        returnVal = value[:fieldLength]
    else:
        # Otherwise just write over using utf-8 so special characters will pass
        value = valueList[0].encode('utf-8', 'ignore')
        returnVal = value[:fieldLength]
    return returnVal

def runTransfer(inFc, outMnFc, cObj, countyId):
    '''Runs transfer/load process.

    Note: Can only use cObj for field control attributes, lists in
    properties_metr.py for non field control attributes are not handled in this
    function except in writeToErrorLog (which will just write the list as a
    string.

    If updating code and need to get autofill for class attributes,
    uncomment next two lines. Comment back out before run.'''
##    import properties_aitk
##    cObj = properties_aitk.createCountyObj()

    # lists for search cursor and insert cursor
    cursorLists = buildCursorLists(cObj)
    fieldsInsert = cursorLists[0]
    fieldsSearch = cursorLists[1]

    # create insert cursor
    icur = arcpy.da.InsertCursor(outMnFc, fieldsInsert)

    # for each row in county data
    with arcpy.da.SearchCursor(inFc, fieldsSearch) as scur:
        for srow in scur:
            # objectid for row based error handling
            objectId = srow[-1]
            try:
                # field values that will be written with insert cursor,
                # starts with shape
                fieldValues = [srow[0]]
                counter = 1

                # skip shape and COUNTY_ID, gather field values for other fields
                for field in fieldsInsert[1:-1]:
                    # get processing information for field
                    fieldTransferList = getattr(cObj, field+'_fieldList')
                    fieldLength = getattr(cObj, field+'_fieldLength')
                    transferType = getattr(cObj, field+'_transferType')
                    # set up list of values to pass to transferType function
                    # longest list is 3 as of 2016-12-04, but set to handle up
                    # to five
                    fieldsCount = len(fieldTransferList)
                    if fieldsCount == 1:
                        valList = [srow[counter]]
                    if fieldsCount == 2:
                        valList = [srow[counter], srow[counter+1]]
                    if fieldsCount == 3:
                        valList = [srow[counter], srow[counter+1],
                                   srow[counter+2]]
                    if fieldsCount == 4:
                        valList = [srow[counter], srow[counter+1],
                                   srow[counter+2], srow[counter+3]]
                    if fieldsCount == 5:
                        valList = [srow[counter], srow[counter+1],
                                   srow[counter+2], srow[counter+3],
                                   srow[counter+4]]
                    # add new value to fieldValues based on transferType
                    thisModule = sys.modules[__name__]
                    transferMethod = getattr(thisModule, transferType)
                    cleanVal = transferMethod(valList, fieldLength, countyId)
                    fieldValues.append(cleanVal)
                    # increment counter based on number of fields to keep
                    # fieldsInsert and fieldsSearch parallel
                    counter += fieldsCount

                # add extra values to insert set
                fieldValues.append(countyId)
                # insert to parcels_in_minnesota
                icur.insertRow(fieldValues)

            except arcpy.ExecuteError:
                # catches esri errors for rows:
                writeToErrorLog(
                    cObj.county_name,
                    "Map fields row arcpy",
                    "OBJECTID = "+str(objectId),
                    field,
                    arcpy.GetMessages(2),
                    "")
                errorOccured = True
                continue
            except:
                # catches anything else
                writeToErrorLog(
                    cObj.county_name,
                    "Map fields row sys",
                    "OBJECTID = "+str(objectId),
                    field,
                    sys.exc_info()[1],
                    traceback.format_exc().splitlines())
                errorOccured = True
                continue

    # delete insert cursor
    del icur