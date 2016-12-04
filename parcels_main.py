#-------------------------------------------------------------------------------
# Name:        parcels_main.py
# Purpose:     Control script for package.
#
# Authors:     Jeff Reinhart, Jessica Schuler
#
# Created:     2016-10-16
# Updated:     2016-12-04
#-------------------------------------------------------------------------------

def main():
    import arcpy, os, sys, datetime, traceback
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
    # to False if already dowloaded, extracted, and projected to wkspGdb or if
    # downloading/extracting but not projecting to wkspGdb/running transfer.
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
        [True, 'aitk', 'MN Geo'],
        [False, 'anok', 'MN Geo'], # completed both in individual and metr
        [False, 'beck', 'MN Geo'],
        [True, 'belt', 'MN Geo'],
        [True, 'bent', 'MN Geo'],
        [True, 'bigs', 'MN Geo'],
        [True, 'blue', 'MN Geo'],
        [True, 'brow', 'MN Geo'],
        [True, 'carl', 'MN Geo'],
        [False, 'carv', 'MN Geo'], # completed in metr
        [False, 'cass', 'MN Geo'],
        [False, 'chip', 'MN Geo'],
        [True, 'chis', 'MN Geo'],
        [True, 'clay', 'MN Geo'],
        [True, 'clea', 'MN Geo'],
        [True, 'cook', 'MN Geo'],
        [False, 'cott', 'MN Geo'],
        [True, 'crow', 'MN Geo'],
        [False, 'dako', 'MN Geo'], # completed in metr
        [True, 'dodg', 'MN Geo'],
        [True, 'doug', 'MN Geo'],
        [True, 'fari', 'MN Geo'],
        [True, 'fill', 'MN Geo'],
        [True, 'free', 'MN Geo'],
        [True, 'good', 'MN Geo'],
        [True, 'gran', 'MN Geo'],
        [False, 'henn', 'MN Geo'], # completed both in individual and metr
        [True, 'hous', 'MN Geo'],
        [True, 'hubb', 'MN Geo'],
        [True, 'isan', 'MN Geo'],
        [True, 'itas', 'MN Geo'],
        [True, 'jack', 'MN Geo'],
        [False, 'kana', 'MN Geo'],
        [True, 'kand', 'MN Geo'],
        [True, 'kitt', 'MN Geo'],
        [True, 'kooc', 'MN Geo'],
        [True, 'lacq', 'MN Geo'],
        [True, 'lake', 'MN Geo'],
        [False, 'lesu', 'MN Geo'],
        [True, 'linc', 'MN Geo'],
        [True, 'lotw', 'MN Geo'],
        [True, 'lyon', 'MN Geo'],
        [False, 'mahn', 'MN Geo'],
        [True, 'mars', 'MN Geo'],
        [True, 'mart', 'MN Geo'],
        [False, 'mcle', 'MN Geo'],
        [True, 'meek', 'MN Geo'],
        [True, 'mill', 'MN Geo'],
        [True, 'morr', 'MN Geo'],
        [True, 'mowe', 'MN Geo'],
        [True, 'murr', 'MN Geo'],
        [True, 'nico', 'MN Geo'],
        [True, 'nobl', 'MN Geo'],
        [True, 'norm', 'MN Geo'],
        [True, 'olms', 'MN Geo'],
        [True, 'otte', 'MN Geo'],
        [True, 'penn', 'MN Geo'],
        [True, 'pine', 'MN Geo'],
        [True, 'pipe', 'MN Geo'],
        [True, 'polk', 'MN Geo'],
        [True, 'pope', 'MN Geo'],
        [False, 'rams', 'MN Geo'], # completed both in individual and metr
        [False, 'redl', 'MN Geo'],
        [True, 'redw', 'MN Geo'],
        [True, 'renv', 'MN Geo'],
        [True, 'rice', 'MN Geo'],
        [True, 'rock', 'MN Geo'],
        [False, 'rose', 'MN Geo'],
        [False, 'scot', 'MN Geo'], # completed in metr
        [False, 'sher', 'MN Geo'],
        [True, 'sibl', 'MN Geo'],
        [False, 'stlo', 'MN Geo'],
        [True, 'stea', 'MN Geo'],
        [False, 'stee', 'MN Geo'],
        [False, 'stev', 'MN Geo'],
        [False, 'swif', 'MN Geo'],
        [True, 'todd', 'MN Geo'],
        [False, 'trav', 'MN Geo'],
        [False, 'waba', 'MN Geo'],
        [True, 'wade', 'MN Geo'],
        [False, 'wase', 'MN Geo'],
        [False, 'wash', 'MN Geo'], # completed in metr
        [False, 'wato', 'MN Geo'],
        [True, 'wilk', 'MN Geo'],
        [True, 'wino', 'MN Geo'],
        [True, 'wrig', 'MN Geo'],
        [True, 'yell', 'MN Geo'],
        [True, 'metr', 'MN Geospatial Commons']
        ]

    # check that metr isn't doubling up on metro counties
    if countyRunList[87][0]:
        if countyRunList[1][0] or \
           countyRunList[9][0] or \
           countyRunList[18][0] or \
           countyRunList[26][0] or \
           countyRunList[61][0] or \
           countyRunList[68][0] or \
           countyRunList[81][0]:
            print "Current countyRunList would result in duplicate parcels in"+\
                  " one or more metro counties. Set metr to False or"+\
                  " anok, carv, dako, henn, rams, scot, and wash to False."
            sys.exit()

    # run counties
    for runParams in countyRunList:
        if runParams[0]:
            print "Running for {0}".format(runParams[1])

            '''If updating code and need to get autofill for class attributes,
            then comment next two lines in and following two lines out.
            Switch back before run.'''
##            import properties_aitk
##            cObj = properties_aitk.createCountyObj()
            propertiesCountyModule = __import__("properties_"+runParams[1])
            cObj = propertiesCountyModule.createCountyObj()

            # download and extract data
            if ftp_OR_local == "ftp":
                try:
                    pProcess.downloadExtract(
                        username,
                        password,
                        sourcePath,
                        cObj.sourceZipFile,
                        cObj.cty_abbr,
                        runParams[2])
                except:
                    pProcess.writeToErrorLog(
                        cObj.county_name,
                        "Download and extract sys",
                        "",
                        "",
                        sys.exc_info()[0],
                        traceback.format_exc().splitlines())
                    errorOccured = True
                    continue

            # convert to projected feature class and join if needed
            if project_to_wkspgdb:
                try:
                    # handling for metr or individual county
                    if isinstance(cObj.cty_abbr, (list)):
                        runList = zip(
                            cObj.sourcePolygons,
                            cObj.cty_abbr,
                            cObj.sourceOwnershipTable,
                            cObj.joinInField,
                            cObj.joinJoinField)
                        for ctyParams in runList:
                            inSpatial = os.path.join(sourcePath, 'METR',
                                                     ctyParams[0])
                            pProcess.projectJoin(
                                sourcePath,
                                wkspGdb,
                                inSpatial,
                                ctyParams[1],
                                ctyParams[2],
                                ctyParams[3],
                                ctyParams[4])
                    else:
                        inSpatial = os.path.join(sourcePath, cObj.cty_abbr,
                                                 cObj.sourcePolygons)
                        pProcess.projectJoin(
                            sourcePath,
                            wkspGdb,
                            inSpatial,
                            cObj.cty_abbr,
                            cObj.sourceOwnershipTable,
                            cObj.joinInField,
                            cObj.joinJoinField)
                except arcpy.ExecuteError:
                    # catches esri errors
                    pProcess.writeToErrorLog(
                        cObj.county_name,
                        "Copy or project feature class arcpy",
                        "",
                        "",
                        arcpy.GetMessages(2),
                        "")
                    errorOccured = True
                    continue
                except:
                    # catches anything else
                    pProcess.writeToErrorLog(
                        cObj.county_name,
                        "Copy or project feature class sys",
                        "",
                        "",
                        sys.exc_info()[0],
                        traceback.format_exc().splitlines())
                    errorOccured = True
                    continue

            # transfer and load to parcels_in_minnesota
            if run_transfer:
                try:
                    # set target feature dataset
                    outMnFc = os.path.join(wkspGdb, "parcels_in_minnesota")
                    # handling for metr or individual county
                    if isinstance(cObj.cty_abbr, (list)):
                        runList = zip(
                            cObj.county_name,
                            cObj.cty_abbr,
                            cObj.county_id)
                        for ctyParams in runList:
                            print "Writing {0} ".format(ctyParams[0])+\
                                  "to parcels_in_minnesota..."
                            inFc = os.path.join(wkspGdb, ctyParams[1])
                            pProcess.runTransfer(
                                inFc,
                                outMnFc,
                                cObj,
                                ctyParams[2])
                    # counties
                    else:
                        print "Writing {0} ".format(cObj.county_name)+\
                              "to parcels_in_minnesota..."
                        inFc = os.path.join(wkspGdb, cObj.cty_abbr)
                        pProcess.runTransfer(inFc,
                            outMnFc,
                            cObj,
                            cObj.county_id)

                except arcpy.ExecuteError:
                    # catches esri errors
                    pProcess.writeToErrorLog(
                        cObj.county_name,
                        "Map fields county prep arcpy",
                        "",
                        "",
                        arcpy.GetMessages(2),
                        "")
                    errorOccured = True
                    continue
                except:
                    # catches anything else
                    pProcess.writeToErrorLog(
                        cObj.county_name,
                        "Map fields county prep sys",
                        "",
                        "",
                        sys.exc_info()[1],
                        traceback.format_exc().splitlines())
                    errorOccured = True
                    continue

        else:
            print "Not running for {0}".format(runParams[1])
            pass
    # end run counties

    # timer
    endTime = datetime.datetime.now()
    print "Runtime: {0}".format(endTime-startTime)

    # notification on errors
    if errorOccured:
        print "Completed, but with errors, check error_log.txt and above prints"
    else:
        print "Completed, no errors"

if __name__ == '__main__':
    main()