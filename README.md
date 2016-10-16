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

The process runs from __parcels_main.py__. You will be prompted for your username and password for the MnGeo parcel data site (http://geoint.lmic.state.mn.us/parcels/).

Next I will describe the structure from the bottom up. The module __parcels_base_classes.py__ contains a class _**countyEtlParams**_. This class sets all of the variables needed for running the ETL process. Attributes with "\*\_exists" are for statewide schema field names where * = FIELD_NAME. The attribute _transferType_ defines what sort of processing needs to be done to load to the statewide schema. If a _transferType_ is standard across all counties, it is set in _**countyEtlParams**_. Otherwise it is set for each county. The attribute _fieldLength_ is used to shorten strings to fit it text fields.

There is a **properties_*.py** module for each county. Each of these modules contains a class _**countyEtl**_, which inherits attributes from **parcels_base_classes._countyEtlParams_**. Attributes that could be potentially updated for each county are set in the _**countyEtl**_ class. If multiple fields are used, there MUST be a _fieldTransfer_ type (more on these when we get to **parcels_main.py**).

The **parcels_county_compile.py** module instantiates each _**countyEtl**_. It is there to keep the clutter down in **parcels_main.py**, which imports **parcels_county_compile._countyCompile_**.

The **parcels_main.py** module has a lot a comments to describe processes. It also relies on functions in **parcels_processing_functions.py** (imported as _pProcess_). Some important code to update when running:
* _append_OR_createnew_ decides whether to create a new statewide schema feature class named parcels\_in\_minnesota or append to an existing one.
* _countyRunList_ determines which counties will run. Set the first item in each sub-list to True or False. The first commit in this repository is set to run all of the counties that had field mapping completed at the time.
* _transferType_ is used to guide how values are mapped and to keep the array for the insertCursor parallel to the searchCursor array. If multiple fields are used in the _fieldTransferList_, the _transferType_ process must increase the counter by the count of fields instead of just by 1.
