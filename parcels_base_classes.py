#-------------------------------------------------------------------------------
# Name:        parcels_base_classes.py
# Purpose:     Classes for parcels_in_minnesota_update.py
#
# Authors:     Jeff Reinhart
#
# Created:     10/01/2016
#-------------------------------------------------------------------------------

import os, datetime, arcpy

class userObject(object):
    '''Class for user specific settings.'''
    def __init__(self):
        self.wkspGdb = r'D:\JR_Work\Parcels\parcels.gdb'
        self.sourcePath = r'D:\JR_Work\Parcels\Source'


class countyEtlParams(object):
    '''ETL parameters for downloading, extracting, projecting, and copying
    county parcel data to the statewide schema.
    '''

    county_name = ''
    cty_fips = ''
    county_id = ''
    cty_abbr = ''
    mngeo_web_id = ''
    sourceZipFile = ''
    sourcePolygons = ''
    sourceOwnershipZipFile = ''
    sourceOwnershipTable = ''
    joinInField = ''
    joinJoinField = ''

    PIN_fieldList = []
    PIN_fieldLength = 25
    PIN_transferType = 'statewidePin'

    BLDG_NUM_fieldList = []
    BLDG_NUM_fieldLength = 10
    BLDG_NUM_transferType = 'defaultTransfer'

    PREFIX_DIR_fieldList = []
    PREFIX_DIR_fieldLength = 2
    PREFIX_DIR_transferType = 'defaultTransfer'

    PREFIXTYPE_fieldList = []
    PREFIXTYPE_fieldLength = 6
    PREFIXTYPE_transferType = 'defaultTransfer'

    STREETNAME_fieldList = []
    STREETNAME_fieldLength = 40
    STREETNAME_transferType = 'defaultTransfer'

    STREETTYPE_fieldList = []
    STREETTYPE_fieldLength = 4
    STREETTYPE_transferType = 'defaultTransfer'

    SUFFIX_DIR_fieldList = []
    SUFFIX_DIR_fieldLength = 2
    SUFFIX_DIR_transferType = 'defaultTransfer'

    UNIT_INFO_fieldList = []
    UNIT_INFO_fieldLength = 12
    UNIT_INFO_transferType = 'defaultTransfer'

    CITY_fieldList = []
    CITY_fieldLength = 30
    CITY_transferType = 'defaultTransfer'

    CITY_USPS_fieldList = []
    CITY_USPS_fieldLength = 30
    CITY_USPS_transferType = 'defaultTransfer'

    ZIP_fieldList = []
    ZIP_fieldLength = 5
    ZIP_transferType = 'defaultTransfer'

    ZIP4_fieldList = []
    ZIP4_fieldLength = 4
    ZIP4_transferType = 'defaultTransfer'

    PLAT_NAME_fieldList = []
    PLAT_NAME_fieldLength = 50
    PLAT_NAME_transferType = 'defaultTransfer'

    BLOCK_fieldList = []
    BLOCK_fieldLength = 5
    BLOCK_transferType = 'defaultTransfer'

    LOT_fieldList = []
    LOT_fieldLength = 5
    LOT_transferType = 'defaultTransfer'

    ACRES_POLY_fieldList = []
    ACRES_POLY_fieldLength = 0
    ACRES_POLY_transferType = 'ToDouble'

    ACRES_DEED_fieldList = []
    ACRES_DEED_fieldLength = 0
    ACRES_DEED_transferType = 'ToDouble'

    USE1_DESC_fieldList = []
    USE1_DESC_fieldLength = 100
    USE1_DESC_transferType = 'defaultTransfer'

    USE2_DESC_fieldList = []
    USE2_DESC_fieldLength = 100
    USE2_DESC_transferType = 'defaultTransfer'

    USE3_DESC_fieldList = []
    USE3_DESC_fieldLength = 100
    USE3_DESC_transferType = 'defaultTransfer'

    USE4_DESC_fieldList = []
    USE4_DESC_fieldLength = 100
    USE4_DESC_transferType = 'defaultTransfer'

    MULTI_USES_fieldList = []
    MULTI_USES_fieldLength = 1
    MULTI_USES_transferType = 'defaultTransfer'

    LANDMARK_fieldList = []
    LANDMARK_fieldLength = 100
    LANDMARK_transferType = 'defaultTransfer'

    OWNER_NAME_fieldList = []
    OWNER_NAME_fieldLength = 100
    OWNER_NAME_transferType = 'defaultTransfer'

    OWNER_MORE_fieldList = []
    OWNER_MORE_fieldLength = 100
    OWNER_MORE_transferType = 'defaultTransfer'

    OWN_ADD_L1_fieldList = []
    OWN_ADD_L1_fieldLength = 100
    OWN_ADD_L1_transferType = 'defaultTransfer'

    OWN_ADD_L2_fieldList = []
    OWN_ADD_L2_fieldLength = 100
    OWN_ADD_L2_transferType = 'defaultTransfer'

    OWN_ADD_L3_fieldList = []
    OWN_ADD_L3_fieldLength = 100
    OWN_ADD_L3_transferType = 'defaultTransfer'

    OWN_ADD_L4_fieldList = []
    OWN_ADD_L4_fieldLength = 100
    OWN_ADD_L4_transferType = 'defaultTransfer'

    TAX_NAME_fieldList = []
    TAX_NAME_fieldLength = 100
    TAX_NAME_transferType = 'defaultTransfer'

    TAX_ADD_L1_fieldList = []
    TAX_ADD_L1_fieldLength = 100
    TAX_ADD_L1_transferType = 'defaultTransfer'

    TAX_ADD_L2_fieldList = []
    TAX_ADD_L2_fieldLength = 100
    TAX_ADD_L2_transferType = 'defaultTransfer'

    TAX_ADD_L3_fieldList = []
    TAX_ADD_L3_fieldLength = 100
    TAX_ADD_L3_transferType = 'defaultTransfer'

    TAX_ADD_L4_fieldList = []
    TAX_ADD_L4_fieldLength = 100
    TAX_ADD_L4_transferType = 'defaultTransfer'

    OWNERSHIP_fieldList = []
    OWNERSHIP_fieldLength = 5
    OWNERSHIP_transferType = 'defaultTransfer'

    HOMESTEAD_fieldList = []
    HOMESTEAD_fieldLength = 1
    HOMESTEAD_transferType = 'defaultTransfer'

    TAX_YEAR_fieldList = []
    TAX_YEAR_fieldLength = 2
    TAX_YEAR_transferType = 'ToSmallInteger'

    MARKET_YEAR_fieldList = []
    MARKET_YEAR_fieldLength = 2
    MARKET_YEAR_transferType = 'ToSmallInteger'

    EMV_LAND_fieldList = []
    EMV_LAND_fieldLength = 0
    EMV_LAND_transferType = 'ToInteger'

    EMV_BLDG_fieldList = []
    EMV_BLDG_fieldLength = 0
    EMV_BLDG_transferType = 'ToInteger'

    EMV_TOTAL_fieldList = []
    EMV_TOTAL_fieldLength = 0
    EMV_TOTAL_transferType = 'ToInteger'

    TAX_CAPAC_fieldList = []
    TAX_CAPAC_fieldLength = 0
    TAX_CAPAC_transferType = 'ToInteger'

    TOTAL_TAX_fieldList = []
    TOTAL_TAX_fieldLength = 0
    TOTAL_TAX_transferType = 'ToInteger'

    SPEC_ASSES_fieldList = []
    SPEC_ASSES_fieldLength = 0
    SPEC_ASSES_transferType = 'ToInteger'

    TAX_EXEMPT_fieldList = []
    TAX_EXEMPT_fieldLength = 1
    TAX_EXEMPT_transferType = 'defaultTransfer'

    XUSE1_DESC_fieldList = []
    XUSE1_DESC_fieldLength = 100
    XUSE1_DESC_transferType = 'defaultTransfer'

    XUSE2_DESC_fieldList = []
    XUSE2_DESC_fieldLength = 100
    XUSE2_DESC_transferType = 'defaultTransfer'

    XUSE3_DESC_fieldList = []
    XUSE3_DESC_fieldLength = 100
    XUSE3_DESC_transferType = 'defaultTransfer'

    XUSE4_DESC_fieldList = []
    XUSE4_DESC_fieldLength = 100
    XUSE4_DESC_transferType = 'defaultTransfer'

    DWELL_TYPE_fieldList = []
    DWELL_TYPE_fieldLength = 30
    DWELL_TYPE_transferType = 'defaultTransfer'

    HOME_STYLE_fieldList = []
    HOME_STYLE_fieldLength = 30
    HOME_STYLE_transferType = 'defaultTransfer'

    FIN_SQ_FT_fieldList = []
    FIN_SQ_FT_fieldLength = 0
    FIN_SQ_FT_transferType = 'ToInteger'

    GARAGE_fieldList = []
    GARAGE_fieldLength = 1
    GARAGE_transferType = 'defaultTransfer'

    GARAGESQFT_fieldList = []
    GARAGESQFT_fieldLength = 0
    GARAGESQFT_transferType = 'ToInteger'

    BASEMENT_fieldList = []
    BASEMENT_fieldLength = 1
    BASEMENT_transferType = 'defaultTransfer'

    HEATING_fieldList = []
    HEATING_fieldLength = 30
    HEATING_transferType = 'defaultTransfer'

    COOLING_fieldList = []
    COOLING_fieldLength = 30
    COOLING_transferType = 'defaultTransfer'

    YEAR_BUILT_fieldList = []
    YEAR_BUILT_fieldLength = 0
    YEAR_BUILT_transferType = 'ToSmallInteger'

    NUM_UNITS_fieldList = []
    NUM_UNITS_fieldLength = 0
    NUM_UNITS_transferType = 'ToInteger'

    SALE_DATE_fieldList = []
    SALE_DATE_fieldLength = 0
    SALE_DATE_transferType = 'defaultTransfer'

    SALE_VALUE_fieldList = []
    SALE_VALUE_fieldLength = 0
    SALE_VALUE_transferType = 'ToInteger'

    SCHOOL_DST_fieldList = []
    SCHOOL_DST_fieldLength = 10
    SCHOOL_DST_transferType = 'defaultTransfer'

    WSHD_DIST_fieldList = []
    WSHD_DIST_fieldLength = 50
    WSHD_DIST_transferType = 'defaultTransfer'

    GREEN_ACRE_fieldList = []
    GREEN_ACRE_fieldLength = 1
    GREEN_ACRE_transferType = 'defaultTransfer'

    OPEN_SPACE_fieldList = []
    OPEN_SPACE_fieldLength = 1
    OPEN_SPACE_transferType = 'defaultTransfer'

    AG_PRESERV_fieldList = []
    AG_PRESERV_fieldLength = 1
    AG_PRESERV_transferType = 'defaultTransfer'

    AGPRE_ENRD_fieldList = []
    AGPRE_ENRD_fieldLength = 0
    AGPRE_ENRD_transferType = 'defaultTransfer'

    AGPRE_EXPD_fieldList = []
    AGPRE_EXPD_fieldLength = 0
    AGPRE_EXPD_transferType = 'defaultTransfer'

    PARC_CODE_fieldList = []
    PARC_CODE_fieldLength = 0
    PARC_CODE_transferType = 'ToSmallInteger'

    SECTION_fieldList = []
    SECTION_fieldLength = 0
    SECTION_transferType = 'ToSmallInteger'

    TOWNSHIP_fieldList = []
    TOWNSHIP_fieldLength = 0
    TOWNSHIP_transferType = 'ToSmallInteger'

    RANGE_fieldList = []
    RANGE_fieldLength = 0
    RANGE_transferType = 'ToSmallInteger'

    RANGE_DIR_fieldList = []
    RANGE_DIR_fieldLength = 0
    RANGE_DIR_transferType = 'ToSmallInteger'

    LEGAL_DESC_fieldList = []
    LEGAL_DESC_fieldLength = 256
    LEGAL_DESC_transferType = 'defaultTransfer'

    EDIT_DATE_fieldList = []
    EDIT_DATE_fieldLength = 0
    EDIT_DATE_transferType = 'defaultTransfer'

    EXPORT_DATE_fieldList = []
    EXPORT_DATE_fieldLength = 0
    EXPORT_DATE_transferType = 'defaultTransfer'

    ORIG_PIN_fieldList = []
    ORIG_PIN_fieldLength = 25
    ORIG_PIN_transferType = 'defaultTransfer'