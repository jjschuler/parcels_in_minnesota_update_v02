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

    # county run list as [run county bool, county abbr,
    #                     USA Counties Generalized Name]
    countyRunList = [
        [True, 'aitk', 'MN Geo', 'Aitkin'],
        [False, 'anok', 'MN Geo', 'Anoka'], # completed both in cty and metr
        [False, 'beck', 'MN Geo', 'Becker'],
        [True, 'belt', 'MN Geo', 'Beltrami'],
        [True, 'bent', 'MN Geo', 'Benton'],
        [True, 'bigs', 'MN Geo', 'Big Stone'],
        [True, 'blue', 'MN Geo', 'Blue Earth'],
        [True, 'brow', 'MN Geo', 'Brown'],
        [True, 'carl', 'MN Geo', 'Carlton'],
        [False, 'carv', 'MN Geo', 'Carver'], # completed in metr
        [False, 'cass', 'MN Geo', 'Cass'],
        [False, 'chip', 'MN Geo', 'Chippewa'],
        [True, 'chis', 'MN Geo', 'Chisago'],
        [True, 'clay', 'MN Geo', 'Clay'],
        [True, 'clea', 'MN Geo', 'Clearwater'],
        [True, 'cook', 'MN Geo', 'Cook'],
        [False, 'cott', 'MN Geo', 'Cottonwood'],
        [True, 'crow', 'MN Geo', 'Crow Wing'],
        [False, 'dako', 'MN Geo', 'Dakota'], # completed in metr
        [True, 'dodg', 'MN Geo', 'Dodge'],
        [True, 'doug', 'MN Geo', 'Douglas'],
        [True, 'fari', 'MN Geo', 'Faribault'],
        [True, 'fill', 'MN Geo', 'Fillmore'],
        [True, 'free', 'MN Geo', 'Freeborn'],
        [True, 'good', 'MN Geo', 'Goodhue'],
        [True, 'gran', 'MN Geo', 'Grant'],
        [False, 'henn', 'MN Geo', 'Hennepin'], # completed both in cty and metr
        [True, 'hous', 'MN Geo', 'Houston'],
        [True, 'hubb', 'MN Geo', 'Hubbard'],
        [True, 'isan', 'MN Geo', 'Isanti'],
        [True, 'itas', 'MN Geo', 'Itasca'],
        [True, 'jack', 'MN Geo', 'Jackson'],
        [False, 'kana', 'MN Geo', 'Kanabec'],
        [True, 'kand', 'MN Geo', 'Kandiyohi'],
        [True, 'kitt', 'MN Geo', 'Kittson'],
        [True, 'kooc', 'MN Geo', 'Koochiching'],
        [True, 'lacq', 'MN Geo', 'Lac qui Parle'],
        [True, 'lake', 'MN Geo', 'Lake'],
        [False, 'lesu', 'MN Geo', 'Le Sueur'],
        [True, 'linc', 'MN Geo', 'Lincoln'],
        [True, 'lotw', 'MN Geo', 'Lake of the Woods'],
        [True, 'lyon', 'MN Geo', 'Lyon'],
        [False, 'mahn', 'MN Geo', 'Mahnomen'],
        [True, 'mars', 'MN Geo', 'Marshall'],
        [True, 'mart', 'MN Geo', 'Martin'],
        [False, 'mcle', 'MN Geo', 'McLeod'],
        [True, 'meek', 'MN Geo', 'Meeker'],
        [True, 'mill', 'MN Geo', 'Mille Lacs'],
        [True, 'morr', 'MN Geo', 'Morrison'],
        [True, 'mowe', 'MN Geo', 'Mower'],
        [True, 'murr', 'MN Geo', 'Murray'],
        [True, 'nico', 'MN Geo', 'Nicollet'],
        [True, 'nobl', 'MN Geo', 'Nobles'],
        [True, 'norm', 'MN Geo', 'Norman'],
        [True, 'olms', 'MN Geo', 'Olmsted'],
        [True, 'otte', 'MN Geo', 'Otter Tail'],
        [True, 'penn', 'MN Geo', 'Pennington'],
        [True, 'pine', 'MN Geo', 'Pine'],
        [True, 'pipe', 'MN Geo', 'Pipestone'],
        [True, 'polk', 'MN Geo', 'Polk'],
        [True, 'pope', 'MN Geo', 'Pope'],
        [False, 'rams', 'MN Geo', 'Ramsey'], # completed both in cty and metr
        [False, 'redl', 'MN Geo', 'Red Lake'],
        [True, 'redw', 'MN Geo', 'Redwood'],
        [True, 'renv', 'MN Geo', 'Renville'],
        [True, 'rice', 'MN Geo', 'Rice'],
        [True, 'rock', 'MN Geo', 'Rock'],
        [False, 'rose', 'MN Geo', 'Roseau'],
        [False, 'scot', 'MN Geo', 'Scott'], # completed in metr
        [False, 'sher', 'MN Geo', 'Sherburne'],
        [True, 'sibl', 'MN Geo', 'Sibley'],
        [False, 'stlo', 'MN Geo', 'St. Louis'],
        [True, 'stea', 'MN Geo', 'Stearns'],
        [False, 'stee', 'MN Geo', 'Steele'],
        [False, 'stev', 'MN Geo', 'Stevens'],
        [False, 'swif', 'MN Geo', 'Swift'],
        [True, 'todd', 'MN Geo', 'Todd'],
        [False, 'trav', 'MN Geo', 'Traverse'],
        [False, 'waba', 'MN Geo', 'Wabasha'],
        [True, 'wade', 'MN Geo', 'Wadena'],
        [False, 'wase', 'MN Geo', 'Waseca'],
        [False, 'wash', 'MN Geo', 'Washington'], # completed in metr
        [False, 'wato', 'MN Geo', 'Watonwan'],
        [True, 'wilk', 'MN Geo', 'Wilkin'],
        [True, 'wino', 'MN Geo', 'Winona'],
        [True, 'wrig', 'MN Geo', 'Wright'],
        [True, 'yell', 'MN Geo', 'Yellow Medicine'],
        [True, 'metr', 'MN Geospatial Commons', '']
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