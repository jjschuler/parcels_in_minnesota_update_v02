# parcels_in_minnesota_update_v02
Processing spatial parcel data from counties in Minnesota to the statewide parcel feature class schema.

The architecture of this process is intended to be easy to use for the person managing the field mapping. Object-oriented design is used where it made sense at the time, but we make no claims as to the architecture being "correct" object-oriented design. It works and that is what counts. :bowtie:

The script has error handling for each level of the process. Errors are recorded in error_log.txt which is created or appended to in the folder where these modules are stored. If something fails from dataset processing errors down to record level errors, the script will write to the error log and move on.

Prior to running, there are two workspaces that need to be set up:
* a file geodatabase
* a folder

Add the path for the file geodatabase to **parcels_base_classes.py** _**userObject**_ _self.wkspGdb_.

Add the path for the folder to __parcels_base_classes.py__ _**userObject**_ _self.sourcePath_.

A parcels\_in\_minnesota\_template then needs to be added to the geodatabase workspace. A zipped ArcGIS 10.2.2 geodatabase containing the template has been included in this repository. We recommend you unzip this in a different folder if you plan to branch and make contributions to this repository.

The process runs from __parcels_main.py__. You will be prompted for your username and password for a temporary MnGeo web-accessible folder. If you do not have access to this folder, contact your GIS staff.

Next I will describe the structure from the bottom up. The module __parcels_base_classes.py__ contains a class _**countyEtlParams**_. This class sets all of the variables needed for running the ETL process. Attributes with "\*\_exists" are for statewide schema field names where * = FIELD_NAME. The attribute _transferType_ defines what sort of processing needs to be done to load to the statewide schema. If a _transferType_ is standard across all counties, it is set in _**countyEtlParams**_. Otherwise it is set for each county. The attribute _fieldLength_ is used to shorten strings to fit it text fields.

There is a **properties_*.py** module for each county. Each of these modules contains a class _**countyEtl**_, which inherits attributes from **parcels_base_classes._countyEtlParams_**. Attributes that could be potentially updated for each county are set in the _**countyEtl**_ class. If multiple fields are used, there MUST be a _fieldTransfer_ type (more on these when we get to **parcels_main.py**).

The **parcels_county_compile.py** module instantiates each _**countyEtl**_. It is there to keep the clutter down in **parcels_main.py**, which imports **parcels_county_compile._countyCompile_**.

The **parcels_main.py** module has a lot a comments to describe processes. It also relies on functions in **parcels_processing_functions.py** (imported as _pProcess_). Some important code to update when running:
* _append_OR_createnew_ decides whether to create a new statewide schema feature class named parcels\_in\_minnesota or append to an existing one.
* _countyRunList_ determines which counties will run. Set the first item in each sub-list to True or False. The first commit in this repository is set to run all of the counties that had field mapping completed at the time.
* _transferType_ is used to guide how values are mapped and to keep the array for the insertCursor parallel to the searchCursor array. If multiple fields are used in the _fieldTransferList_, the _transferType_ process must increase the counter by the count of fields instead of just by 1.

## Counties
If you work with a county and would like to contribute to the field mapping process, please feel free! If you have some data in a separate table that needs to be joined, this tutorial doesn't cover that (you could join in the data before doing the following or dig deaper into the code to see how to make it happen there. For a layer that has all attributes included, follow these general steps for the quickest route to contributing your field mapping info:
<ol>
<li>Clone the repository.
<li>Fork the repository to your own branch.
<li>In your branch, you will find parcels.gdb.zip. Unzip this and move it to a different folder. This will be your workspace geodatabase. Copy the path for this gdb.
<li>In parcels_base_classes.py, update class UserObject attribute self.wkspGdb to the path you copied in the previous step.
<li>Open your county's properties_*.py file. Look for the self.sourcePolygons attribute. <i>(The script directs to the source geospatial file using a combination of parcels_base_classes.userObject.sourcePath + properties_*.countyEtl.cty_abbr + properties_*.countyEtl.sourcePolygons. This is complex but necessary for the batch process and collaborating across multiple development environments.)</i> <br><br>

If the properties_*.countyEtl.sourcePolygons attribute already has info, that is the file directory structure that you shared with MnGeo (unzipped). Do the following:<br><br>
<ol>
<li>Find where you stored this directory on your computer and copy the directory.
<li>Create a folder named with your four character county abbreviation in all caps (e.g. AITK) and paste the directory you copied in the previous step to this folder.
<li>Copy the path up to the backslash before the county abbreviation (e.g. if the folder you created was <i>C:\Cadastral\Exports\AITK</i> then copy <i>C:\Cadastral\Exports</i>).
<li>In parcels_base_classes.py, update class UserObject attribute self.sourcePath string to the path you copied in the previous step (e.g. line should look like: <i>self.sourcePath = r'C:\Cadastral\Exports'</i>).
</ol>

If the self.sourcePolygons attribute is not filled in, we have not gotten to updating it yet. Do the following:
<ol>
<li>Create a folder where you will put your source county parcel data and name it with your four character county abbreviation in all caps (e.g. AITK).
<li>Copy the path for the folder created in the previous step up to the backslash before the county abbreviation (e.g. if the folder you created is  <i>C:\Cadastral\Exports\AITK</i> then copy <i>C:\Cadastral\Exports</i>).
<li>In parcels_base_classes.py, update class UserObject attribute self.sourcePath to the path you copied in the previous step (e.g. line will look like: <i>self.sourcePath = r'C:\Cadastral\Exports'</i>).
<li>Add your county parcel data to the sourcePath folder. Copy the remainder of the path for the county parcel data layer.
<li>In your county's properties_*.py, update the self.sourcePolygons attribute to the partial path you copied in the previous step (e.g. if the full path to the layer is <i>C:\Cadastral\Exports\AITK\county.gdb\parcel_layer</i> then the line should look like: <i>self.sourcePolygons = r'county.gdb\parcel_layer'</i>).
</ol>
<li>The last step before running is to update your field mapping. In properties_\*.py, in each self.\*\_exists (where \* = statewide schema field name), add a string to the fieldTransferList for the field name of which field in your county's schema matches the statewide schema field (e.g. if your PIN is stored in a field named PRCL_NBR, then <i>properties_*.countyEtl.PIN_exists.fieldTransferList = ['PRCL_NBR']</i>). There is script to handle concatenating multiple fields, but unless you are an experienced Python user, we recommend just mapping to the single best field.
<li>You are nearly ready to run. The process runs from parcels_main.py and there are a few changes to make there. First, update <i>ftp_OR_local = "ftp"</i> to <i>ftp_OR_local = "local"</i>.
<li>In parcels_main.py, within the countyRunList, set all True to False except for your county.
<li>Run the script. Keep an eye on what prints, it will tell you what is happening.
<li>Check your local parcels_in_minnesota_update_v02 folder. If there is an error_log.txt file, then there were errors. You can try to diagnose the errors on your own or send the error_log.txt file to Jeff Reinhart (will try to get to them asap).
<li>If everything worked, you should now have a parcels_in_minnesota layer in your workspace geodatabase (wkspGdb) that contains your county parcel data projected and field mapped to the statewide schema. Share what you have done! Do a pull request for your branch and we will get the updates merged in. Thanks!
</ol>
