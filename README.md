# parcels_in_minnesota_update_v02
Processing spatial parcel data from counties in Minnesota to the statewide parcel feature class schema.

The architecture of this process is intended to be easy to use for the person managing the field mapping. That is why it was organized with a file for each county's field mapping settings.

The script has error handling for each level of the process. Errors are recorded in error_log.txt which is created or appended to in the root folder of this project. If something fails from dataset processing errors down to errors with individual records, the script will write to the error log and continue. OBJECTID values are logged for errors from individual records so you can find the issue with the record.

## Basic Setup
Prior to running, there are two workspaces that need to be set up:
<ul>
<li>a file geodatabase
<li>a folder
</ul>

To set up your environment:

1. Create a file geodatabase or use the geodatabase in the included parcels.gdb.zip (is version ArcGIS 10.2.2). It is recommended to put this geodatabase in a different folder if you plan to branch and contribute to this repository.

2. A feature class named parcels_in_minnesota_template then needs to be added to the geodatabase workspace (included in parcels.gdb.zip).

3. Add the path for the file geodatabase to **parcels_base_classes.py** `userObject self.wkspGdb`.

4. Create a folder to store source data that will be downloaded.

5. Add the path for the folder to **parcels_base_classes.py** `userObject self.sourcePath`.

The process runs from **parcels_main.py**. When you run the script, you will be prompted for your username and password for a temporary MnGeo web-accessible folder. If you do not have access to this folder, contact your GIS staff.

This is the structure from the bottom up. The module **parcels_base_classes.py** contains a class `countyEtlParams`. This class contains all of the variables that may be needed for running the ETL process. Attributes with `*_fieldList` are for statewide schema field names where * = FIELD_NAME. The attribute `*_transferType` for each field defines what sort of processing needs to be done to load to the statewide schema. If a `*_transferType` is standard across all counties, it is set in the `countyEtlParams` class. Otherwise it is set for each county. The attribute `*_fieldLength` for each field is used to shorten strings to fit it text fields.

There is a **properties_*.py** module for each county. Each of these modules contains a function `createCountyObj`, which creates a `parcels_base_classes.countyEtlParams` object. Attributes that could be potentially updated for each county are set in the  `createCountyObj` function. If multiple fields are used, there MUST be a `*_transferType` (more on these when we get to **parcels_main.py**).

The **parcels_main.py** module has a lot a comments to describe processes. It also relies on functions in **parcels_processing_functions.py** (imported as `pProcess`). Some important code to update when running:
* `append_OR_createnew` determines whether to create a new statewide schema feature class named parcels\_in\_minnesota or append to an existing one.
* `ftp_OR_local` determines whether to download the source files to your source folder or to use your local source files that are already downloaded to your source folder.
* `project_to_wkspgdb` determines whether to copy/project a feature class for the county from your source folder to your workspace geodatabase or to use the existing feature class that you already copied/projected (feature class gets named with county abbreviation).
* `run_transfer` determines whether or not to extract from the workspace geodatabase feature class and load to the statewide schema.
* `countyRunList` determines which counties will run. Set the first item in each sub-list to `True` or `False`. The list will be kept up to date for all counties that have been completed as script updates are committed.
* Functions for transfering different value types to the statewide schema included in **parcels_processing_functions.py** must be named to match `_transferType` strings in **properties_*.py** or in **parcels_base_classes.py** `countyEtlParams`.

## Counties
If you work with a county and would like to contribute to the field mapping process, please feel free! If you have some data in a separate table that needs to be joined, this tutorial doesn't cover that (you could join in the data before doing the following or dig deaper into the code to see how to make it happen there. For a layer that has all attributes included, follow these general steps for the quickest route to contributing your field mapping info:
<ol>
<li>Clone the repository.
<li>Fork the repository to your own branch.
<li>In your branch, you will find parcels.gdb.zip. Unzip this and move it to a different folder. This will be your workspace geodatabase. Copy the path for this gdb.
<li>In parcels_base_classes.py, update class UserObject attribute self.wkspGdb to the path you copied in the previous step.
<li>Open your county's properties_*.py file. Look for the countyObj.sourcePolygons attribute. <i>(The script directs to the source geospatial file using a combination of parcels_base_classes.userObject.sourcePath + properties_*.countyObj.cty_abbr + properties_*.countyObj.sourcePolygons. This is complex but necessary for the batch process and collaborating across multiple development environments.)</i> <br><br>

If the properties_*.countyObj.sourcePolygons attribute already has info, that is the file directory structure that you shared with MnGeo (unzipped). Do the following:<br><br>
<ol>
<li>Find where you stored this directory on your computer and copy the directory.
<li>Create a folder named with your four character county abbreviation in all caps (e.g. AITK) and paste the directory you copied in the previous step to this folder.
<li>Copy the path up to the backslash before the county abbreviation (e.g. if the folder you created was <i>C:\Cadastral\Exports\AITK</i> then copy <i>C:\Cadastral\Exports</i>).
<li>In parcels_base_classes.py, update class UserObject attribute self.sourcePath string to the path you copied in the previous step (e.g. line should look like: <i>self.sourcePath = r'C:\Cadastral\Exports'</i>).
</ol>

If the countyObj.sourcePolygons attribute is not filled in, we have not gotten to updating it yet. Do the following:
<ol>
<li>Create a folder where you will put your source county parcel data and name it with your four character county abbreviation in all caps (e.g. AITK).
<li>Copy the path for the folder created in the previous step up to the backslash before the county abbreviation (e.g. if the folder you created is  <i>C:\Cadastral\Exports\AITK</i> then copy <i>C:\Cadastral\Exports</i>).
<li>In parcels_base_classes.py, update class UserObject attribute self.sourcePath to the path you copied in the previous step (e.g. line will look like: <i>self.sourcePath = r'C:\Cadastral\Exports'</i>).
<li>Add your county parcel data to the sourcePath folder. Copy the remainder of the path for the county parcel data layer.
<li>In your county's properties_*.py, update the countyObj.sourcePolygons attribute to the partial path you copied in the previous step (e.g. if the full path to the layer is <i>C:\Cadastral\Exports\AITK\county.gdb\parcel_layer</i> then the line should look like: <i>countyObj.sourcePolygons = r'county.gdb\parcel_layer'</i>).
</ol>
<li>The last step before running is to update your field mapping. In properties_\*.py, in each \*_fieldList (where \* = statewide schema field name), add a string to the list for the field name of which field in your county's schema matches the statewide schema field (e.g. if your PIN is stored in a field named PRCL_NBR, then <i>countyObj.PIN_fieldList = ['PRCL_NBR']</i>). There is script to handle concatenating multiple fields, but unless you are an experienced Python user, we recommend just mapping to the single best field.
<li>You are nearly ready to run. The process runs from parcels_main.py and there are a few changes to make there. First, update <i>ftp_OR_local = "ftp"</i> to <i>ftp_OR_local = "local"</i>.
<li>In parcels_main.py, within the countyRunList, set all True to False except for your county.
<li>Run the script. Keep an eye on what prints, it will tell you what is happening.
<li>Check your local parcels_in_minnesota_update_v02 folder. If there is an error_log.txt file, then there were errors. You can try to diagnose the errors on your own or send the error_log.txt file to Jeff Reinhart (will try to get to them asap).
<li>If everything worked, you should now have a parcels_in_minnesota layer in your workspace geodatabase (wkspGdb) that contains your county parcel data projected and field mapped to the statewide schema. Share what you have done! Do a pull request for your branch and we will get the updates merged in. Thanks!
</ol>
