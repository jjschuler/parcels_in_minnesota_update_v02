#-------------------------------------------------------------------------------
# Name:        parcels_main.py
# Purpose:     Processes county parcel data from MnGeo WAF site all the way
#              through to a statewide layer. Requires ArcGIS 10.2.2 or higher.
#
# Authors:     Jeff Reinhart, Jessica Schuler
#
# Created:     2016-10-16
# Updated:     2016-11-06
#-------------------------------------------------------------------------------

def main():
    import arcpy, os, sys, datetime, traceback, unicodedata
    from parcels_base_classes import userObject
    import parcels_processing_functions as pProcess

    #---------------------------------------------------------------------------
    # Append or create new parcels_in_minnesota feature class. Update string as
    # "append" or "createnew".
    #---------------------------------------------------------------------------
    append_OR_createnew = "createnew"

    #---------------------------------------------------------------------------
    # Run based on local dataset or download/extract first. Update string as
    # "ftp" or "local".
    #---------------------------------------------------------------------------
    ftp_OR_local = "ftp"

    #---------------------------------------------------------------------------
    # Whether to run the projection to the workspace geodatabse. Update boolean
    # to False if already dowloaded, extracted, and projected to wkspGdb. Should
    # have ftp_OR_local set to "local" if setting project_to_wkspgbd to False.
    #---------------------------------------------------------------------------
    project_to_wkspgdb = True

    #---------------------------------------------------------------------------
    # Whether to transfer from the county schema to the statewide schema. May
    # just want to download and project/join before running the transfer.
    #---------------------------------------------------------------------------
    run_transfer = True

    # get username and password
    if ftp_OR_local == "ftp":
        username = raw_input("Username: ")
        password = raw_input("Password: ")

    # timer and error flag
    startTime = datetime.datetime.now()
    print "Started: {0}".format(startTime)
    errorOccured = False

    # variables from user object
    userObj = userObject()
    sourcePath = userObj.sourcePath
    wkspGdb = userObj.wkspGdb

    # set up feature class for statewide schema
    pProcess.templateSetup(append_OR_createnew, wkspGdb)

    # county run list as [run county bool, county abbr]
    countyRunList = [
        [True, 'aitk'],
        [True, 'anok'],
        [False, 'beck'],
        [True, 'belt'],
        [True, 'bent'],
        [True, 'bigs'],
        [True, 'blue'],
        [True, 'brow'],
        [True, 'carl'],
        [False, 'carv'],
        [False, 'cass'],
        [False, 'chip'],
        [True, 'chis'],
        [True, 'clay'],
        [True, 'clea'],
        [True, 'cook'],
        [False, 'cott'],
        [True, 'crow'],
        [False, 'dako'],
        [True, 'dodg'],
        [True, 'doug'],
        [True, 'fari'],
        [True, 'fill'],
        [True, 'free'],
        [True, 'good'],
        [True, 'gran'],
        [True, 'henn'],
        [True, 'hous'],
        [True, 'hubb'],
        [True, 'isan'],
        [True, 'itas'],
        [True, 'jack'],
        [False, 'kana'],
        [True, 'kand'],
        [True, 'kitt'],
        [True, 'kooc'],
        [True, 'lacq'],
        [True, 'lake'],
        [False, 'lesu'],
        [False, 'linc'],
        [True, 'lotw'],
        [False, 'lyon'],
        [False, 'mahn'],
        [False, 'mars'],
        [False, 'mart'],
        [False, 'mcle'],
        [False, 'meek'],
        [False, 'mill'],
        [False, 'morr'],
        [False, 'mowe'],
        [False, 'murr'],
        [False, 'nico'],
        [False, 'nobl'],
        [False, 'norm'],
        [False, 'olms'],
        [False, 'otte'],
        [False, 'penn'],
        [False, 'pine'],
        [False, 'pipe'],
        [False, 'polk'],
        [False, 'pope'],
        [False, 'rams'],
        [False, 'redl'],
        [False, 'redw'],
        [False, 'renv'],
        [False, 'rice'],
        [False, 'rock'],
        [False, 'rose'],
        [False, 'scot'],
        [False, 'sher'],
        [False, 'sibl'],
        [False, 'stlo'],
        [False, 'stea'],
        [False, 'stee'],
        [False, 'stev'],
        [False, 'swif'],
        [False, 'todd'],
        [False, 'trav'],
        [False, 'waba'],
        [False, 'wade'],
        [False, 'wase'],
        [False, 'wash'],
        [False, 'wato'],
        [False, 'wilk'],
        [False, 'wino'],
        [False, 'wrig'],
        [False, 'yell']
        ]

    # run counties
    for runPair in countyRunList:
        if runPair[0]:
            print "Running for {0}".format(runPair[1])

            '''If updating code and need to get autofill for class attributes,
            then comment next two lines in and following two lines out.
            Switch back before run.'''
##            import properties_aitk
##            cObj = properties_aitk.createCountyObj()
            propertiesCountyModule = __import__("properties_"+runPair[1])
            cObj = propertiesCountyModule.createCountyObj()

            # download and extract data
            if ftp_OR_local == "ftp":
                try:
                    pProcess.downloadExtract(username, password, sourcePath, cObj.sourceZipFile, cObj.cty_abbr)
                except:
                    pProcess.writeToErrorLog(cObj.county_name, "Download and extract sys", "", "", sys.exc_info()[0], traceback.format_exc().splitlines())
                    errorOccured = True
                    continue

            # convert to projected feature class and join if needed
            if project_to_wkspgdb:
                try:
                    pProcess.projectJoin(sourcePath, wkspGdb, cObj.cty_abbr, cObj.sourcePolygons, cObj.sourceOwnershipTable, cObj.joinInField, cObj.joinJoinField)
                except arcpy.ExecuteError:
                    # catches esri errors
                    pProcess.writeToErrorLog(cObj.county_name, "Copy or project feature class arcpy", "", "", arcpy.GetMessages(2), "")
                    errorOccured = True
                    continue
                except:
                    # catches anything else
                    pProcess.writeToErrorLog(cObj.county_name,"Copy or project feature class sys", "", "", sys.exc_info()[0], traceback.format_exc().splitlines())
                    errorOccured = True
                    continue

            # transfer and load to parcels_in_minnesota
            if run_transfer:
                try:
                    '''Setup.'''
                    print "Writing {0} to parcels_in_minnesota...".format(cObj.county_name)
                    inFc = os.path.join(wkspGdb, cObj.cty_abbr)
                    # TODO move this global
                    outMnFc = os.path.join(wkspGdb, "parcels_in_minnesota")

                    '''Lists for search cursor, insert cursor, and controlling when one field in
                    the statewide schema comes from multiple fields in a county schema.'''
                    fieldsSearch = ['SHAPE@']
                    fieldsInsert = ['SHAPE@']
                    writeControls = [['Shape',['SHAPE@'], 0]]

                    '''Build field lists dynamically for search cursor that will get values from
                    input county data, for insert cursor that will write to statewide schema, and
                    for row level control that will handle different transfer types and where
                    multiple fields from county data map to one field in statewide schema.'''
                    for attr in iter(sorted(dir(cObj))):
                        if attr[-10:] == "_fieldList":
                            # get fieldTransferList
                            fieldTransferList = getattr(cObj, attr)
                            if len(fieldTransferList) > 0:
                                # append field names to insert cursor that will insert to statewide schema
                                fieldsInsert.append(attr[:-10])
                                # append field names to search cursor that will search county data
                                for field in fieldTransferList:
                                    fieldsSearch.append(field)

                    '''Fields and values not derived from input data to be added at end of
                    fieldsInsert after building list from dictionary.'''
                    fieldsInsert.append('COUNTY_ID')

                    '''Fields to add at end of fieldsSearch because they are not used in transfer.'''
                    fieldsSearch.append('OBJECTID')

                    # create insert cursor
                    icur = arcpy.da.InsertCursor(outMnFc, fieldsInsert)

                    # for each row in county data
                    with arcpy.da.SearchCursor(inFc, fieldsSearch) as scur:
                        for srow in scur:
                            try:
                                # objectid for row based error handling
                                objectId = srow[-1]
                                arcpy.AddMessage(objectId)
                                # field values that will be written with insert cursor, starts with shape
                                fieldValues = [srow[0]]
                                counter = 1
                                # skip shape and COUNTY_ID, build field values for remaining
                                for field in fieldsInsert[1:-1]:
                                    # add remaining values using fieldTransferList, fieldLength, transferType
                                    fieldTransferList = getattr(cObj, field+'_fieldList')
                                    fieldLength = getattr(cObj, field+'_fieldLength')
                                    transferType = getattr(cObj, field+'_transferType')
                                    # begin logic for transfer type, defaults to string that
                                    # is truncated if needed
                                    if transferType == 'statewidePin':
                                        # concat original pin and county id
                                        if srow[counter] is None:
                                            pinVal = ''
                                        else:
                                            pinVal = srow[counter]
                                        newPin = cObj.county_id + "-" + str(pinVal)
                                        fieldValues.append(newPin[:fieldLength])
                                        counter += 1
                                    elif transferType == 'concatTruncateTwoFields':
                                        # concatenate two fields and truncate, handle null values and non utf-8 characters (Houston)
                                        if srow[counter] is not None and srow[counter + 1] is None:
                                            if isinstance(srow[counter], (int, long, float, complex)):
                                                concatValue = str(srow[counter])
                                            elif any(ord(char) > 126 for char in srow[counter]):
                                                concatValue = srow[counter].encode('utf-8', 'ignore')
                                            else:
                                                concatValue = str(srow[counter])
                                        elif srow[counter] is not None and srow[counter + 1] is not None:
                                            if isinstance(srow[counter], (int, long, float, complex)):
                                                concatValue1 = str(srow[counter])
                                            elif any(ord(char) > 126 for char in srow[counter]):
                                                concatValue1 = srow[counter].encode('utf-8', 'ignore')
                                            else:
                                                concatValue1 = str(srow[counter])
                                            if isinstance(srow[counter+1], (int, long, float, complex)):
                                                concatValue2 = str(srow[counter+1])
                                            elif any(ord(char) > 126 for char in srow[counter+1]):
                                                concatValue2 = srow[counter+1].encode('utf-8', 'ignore')
                                            else:
                                                concatValue2 = str(srow[counter+1])
                                            concatValue = concatValue1 + " " + concatValue2
                                        else:
                                            concatValue = ''
                                        # set as string and clear leading/trailing spaces
                                        concatValueStrip = str(concatValue).strip()
                                        fieldValues.append(concatValueStrip[:fieldLength])
                                        counter += 2
                                    elif transferType == 'concatTruncateLastAddrLine':
                                        # handles address last line as city, state zip - blank if any are null in row
                                        if srow[counter] is None or srow[counter + 1] is None or srow[counter + 2] is None or \
                                           srow[counter] == '' or srow[counter + 1] == '' or srow[counter + 2] == '':
                                            addrLastLineValue = ''
                                        else:
                                            addrLastLineValue = "{0}, {1} {2}".format(str(srow[counter]), str(srow[counter + 1]), str(srow[counter + 2]))
                                        # set as string and clear leading/trailing spaces
                                        fieldValues.append(addrLastLineValue[:fieldLength])
                                        counter += 3
                                    elif transferType == 'ToYN':
                                        if srow[counter] is not None and srow[counter] != '':
                                            fieldValues.append('Y')
                                        else:
                                            fieldValues.append('N')
                                        counter += 1
                                    elif transferType == 'Double':
                                        # TODO: for all number types, strip alpha and convert if string, isinstance may not be best route
                                        if isinstance(srow[counter], (int, long, float, complex)):
                                            fieldValues.append(float(srow[counter]))
                                        else:
                                            fieldValues.append(0)
                                        counter += 1
                                    elif transferType == 'SmallInteger':
                                        if isinstance(srow[counter], (int, long, float, complex)):
                                            intVal = int(srow[counter])
                                            if intVal <= 32767 and intVal >= -32768:
                                                fieldValues.append(intVal)
                                            else:
                                                fieldValues.append(0)
                                        elif isinstance(srow[counter], basestring) and srow[counter].isdigit():
                                            intVal = int(srow[counter])
                                            if intVal <= 32767 and intVal >= -32768:
                                                fieldValues.append(intVal)
                                            else:
                                                fieldValues.append(0)
                                        else:
                                            fieldValues.append(0)
                                        counter += 1
                                    elif transferType == 'Integer':
                                        if isinstance(srow[counter], (int, long, float, complex)):
                                            fieldValues.append(long(srow[counter]))
                                        elif isinstance(srow[counter], basestring) and srow[counter].isdigit():
                                            fieldValues.append(long(srow[counter]))
                                        else:
                                            fieldValues.append(0)
                                        counter += 1
                                    elif transferType == 'Date':
                                        # TODO: could use improvement - watch when date field is first transfered
                                        if srow[counter] is not None:
                                            fieldValues.append(srow[counter])
                                        else:
                                            fieldValues.append(None)
                                        counter += 1
                                    elif transferType == 'LongIntToDate':
                                        if srow[counter] is not None:
                                            intString = str(srow[counter])
                                            dateFix = datetime.datetime(int(intString[0:4]), int(intString[4:6]), int(intString[6:8]))
                                            fieldValues.append(dateFix)
                                        else:
                                            fieldValues.append(None)
                                        counter += 1
                                    elif transferType == 'LongIntToDateNoDay':
                                        if srow[counter] is not None and len(str(srow[counter])) == 6:
                                            intString = str(srow[counter])
                                            dateFix = datetime.datetime(int(intString[0:4]), int(intString[4:6]), 1)
                                            fieldValues.append(dateFix)
                                        else:
                                            fieldValues.append(None)
                                        counter += 1
                                    else:
                                        # is a string, so add to list and truncate if needed
                                        # If none then append an empty string
                                        if srow[counter] is None:
                                            fieldValues.append('')
                                        # If a number cast to unicode
                                        elif isinstance(srow[counter], (int, long, float, complex)):
                                            value = unicode(srow[counter])
                                            fieldValues.append(value[:fieldLength])
                                            # If has any odd characters
                                        elif any(ord(char) > 126 for char in srow[counter]):
                                            # Otherwise just write over using utf-8 so special characters will pass
                                            value = srow[counter].encode('utf-8', 'ignore')
                                            fieldValues.append(value[:fieldLength])
                                        # If a string:
                                        elif isinstance(srow[counter], (basestring)):
                                            value = unicode(srow[counter])
                                            fieldValues.append(value[:fieldLength])
                                        else:
                                            # Otherwise just write over using utf-8 so special characters will pass
                                            value = srow[counter].encode('utf-8', 'ignore')
                                            fieldValues.append(value[:fieldLength])
                                        counter += 1
                                # add extra values to insert set
                                fieldValues.append(cObj.county_id)
                                # insert to parcels_in_minnesota
                                icur.insertRow(fieldValues)

                            except arcpy.ExecuteError:
                                # catches esri errors for rows:
                                pProcess.writeToErrorLog(cObj.county_name, "Map fields row arcpy", "OBJECTID = "+str(objectId), field, arcpy.GetMessages(2), "")
                                errorOccured = True
                                continue
                            except:
                                # catches anything else
                                pProcess.writeToErrorLog(cObj.county_name,"Map fields row sys", "OBJECTID = "+str(objectId), field, sys.exc_info()[1], traceback.format_exc().splitlines())
                                errorOccured = True
                                continue

                    # delete insert cursor
                    del icur

                except arcpy.ExecuteError:
                    # catches esri errors
                    pProcess.writeToErrorLog(cObj.county_name, "Map fields county prep arcpy", "", "", arcpy.GetMessages(2), "")
                    errorOccured = True
                    continue
                except:
                    # catches anything else
                    pProcess.writeToErrorLog(cObj.county_name,"Map fields county prep sys", "", "", sys.exc_info()[1], traceback.format_exc().splitlines())
                    errorOccured = True
                    continue

        else:
            print "Not running for {0}".format(runPair[1])
            pass

    # timer
    endTime = datetime.datetime.now()
    print "Runtime: {0}".format(endTime-startTime)

    # notification on errors
    if errorOccured:
        print "Completed, but with errors, check error_log.txt"
    else:
        print "Completed, no errors"

if __name__ == '__main__':
    main()


