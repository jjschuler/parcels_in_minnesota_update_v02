#-------------------------------------------------------------------------------
# Name:        parcels_base_classes.py
# Purpose:     Classes for parcels_in_minnesota_update.py
#
# Authors:     Jeff Reinhart
#
# Created:     10/01/2016
#-------------------------------------------------------------------------------

import os, datetime, arcpy
from abc import ABCMeta, abstractmethod

class userObject(object):
    '''Class for user specific settings.'''
    def __init__(self):
        self.wkspGdb = r'D:\JR_Work\Parcels\parcels.gdb'
        self.sourcePath = r'D:\JR_Work\Parcels\Source'


class countyEtlParams(object):
    '''ETL parameters for downloading, extracting, projecting, and copying
    county parcel data to the statewide schema.
    '''

    class fieldTransfer(object):
        '''Class for field transfer items.'''
        def __init__(self):
            self.fieldTransferList = []
            self.fieldLength = 0
            self.transferType = ''

    __metaclass__ = ABCMeta

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

    PIN_exists = fieldTransfer()
    PIN_exists.fieldLength = 25
    PIN_exists.transferType = 'statewidePin'

    BLDG_NUM_exists = fieldTransfer()
    BLDG_NUM_exists.fieldLength = 10
    BLDG_NUM_exists.transferType = ''

    PREFIX_DIR_exists = fieldTransfer()
    PREFIX_DIR_exists.fieldLength = 2
    PREFIX_DIR_exists.transferType = ''

    PREFIXTYPE_exists = fieldTransfer()
    PREFIXTYPE_exists.fieldLength = 6
    PREFIXTYPE_exists.transferType = ''

    STREETNAME_exists = fieldTransfer()
    STREETNAME_exists.fieldLength = 40
    STREETNAME_exists.transferType = ''

    STREETTYPE_exists = fieldTransfer()
    STREETTYPE_exists.fieldLength = 4
    STREETTYPE_exists.transferType = ''

    SUFFIX_DIR_exists = fieldTransfer()
    SUFFIX_DIR_exists.fieldLength = 2
    SUFFIX_DIR_exists.transferType = ''

    UNIT_INFO_exists = fieldTransfer()
    UNIT_INFO_exists.fieldLength = 12
    UNIT_INFO_exists.transferType = ''

    CITY_exists = fieldTransfer()
    CITY_exists.fieldLength = 30
    CITY_exists.transferType = ''

    CITY_USPS_exists = fieldTransfer()
    CITY_USPS_exists.fieldLength = 30
    CITY_USPS_exists.transferType = ''

    ZIP_exists = fieldTransfer()
    ZIP_exists.fieldLength = 5
    ZIP_exists.transferType = ''

    ZIP4_exists = fieldTransfer()
    ZIP4_exists.fieldLength = 4
    ZIP4_exists.transferType = ''

    PLAT_NAME_exists = fieldTransfer()
    PLAT_NAME_exists.fieldLength = 50
    PLAT_NAME_exists.transferType = ''

    BLOCK_exists = fieldTransfer()
    BLOCK_exists.fieldLength = 5
    BLOCK_exists.transferType = ''

    LOT_exists = fieldTransfer()
    LOT_exists.fieldLength = 5
    LOT_exists.transferType = ''

    ACRES_POLY_exists = fieldTransfer()
    ACRES_POLY_exists.fieldLength = 0
    ACRES_POLY_exists.transferType = 'Double'

    ACRES_DEED_exists = fieldTransfer()
    ACRES_DEED_exists.fieldLength = 0
    ACRES_DEED_exists.transferType = 'Double'

    USE1_DESC_exists = fieldTransfer()
    USE1_DESC_exists.fieldLength = 100
    USE1_DESC_exists.transferType = ''

    USE2_DESC_exists = fieldTransfer()
    USE2_DESC_exists.fieldLength = 100
    USE2_DESC_exists.transferType = ''

    USE3_DESC_exists = fieldTransfer()
    USE3_DESC_exists.fieldLength = 100
    USE3_DESC_exists.transferType = ''

    USE4_DESC_exists = fieldTransfer()
    USE4_DESC_exists.fieldLength = 100
    USE4_DESC_exists.transferType = ''

    MULTI_USES_exists = fieldTransfer()
    MULTI_USES_exists.fieldLength = 1
    MULTI_USES_exists.transferType = ''

    LANDMARK_exists = fieldTransfer()
    LANDMARK_exists.fieldLength = 100
    LANDMARK_exists.transferType = ''

    OWNER_NAME_exists = fieldTransfer()
    OWNER_NAME_exists.fieldLength = 100
    OWNER_NAME_exists.transferType = ''

    OWNER_MORE_exists = fieldTransfer()
    OWNER_MORE_exists.fieldLength = 100
    OWNER_MORE_exists.transferType = ''

    OWN_ADD_L1_exists = fieldTransfer()
    OWN_ADD_L1_exists.fieldLength = 100
    OWN_ADD_L1_exists.transferType = ''

    OWN_ADD_L2_exists = fieldTransfer()
    OWN_ADD_L2_exists.fieldLength = 100
    OWN_ADD_L2_exists.transferType = ''

    OWN_ADD_L3_exists = fieldTransfer()
    OWN_ADD_L3_exists.fieldLength = 100
    OWN_ADD_L3_exists.transferType = ''

    OWN_ADD_L4_exists = fieldTransfer()
    OWN_ADD_L4_exists.fieldLength = 100
    OWN_ADD_L4_exists.transferType = ''

    TAX_NAME_exists = fieldTransfer()
    TAX_NAME_exists.fieldLength = 100
    TAX_NAME_exists.transferType = ''

    TAX_ADD_L1_exists = fieldTransfer()
    TAX_ADD_L1_exists.fieldLength = 100
    TAX_ADD_L1_exists.transferType = ''

    TAX_ADD_L2_exists = fieldTransfer()
    TAX_ADD_L2_exists.fieldLength = 100
    TAX_ADD_L2_exists.transferType = ''

    TAX_ADD_L3_exists = fieldTransfer()
    TAX_ADD_L3_exists.fieldLength = 100
    TAX_ADD_L3_exists.transferType = ''

    TAX_ADD_L4_exists = fieldTransfer()
    TAX_ADD_L4_exists.fieldLength = 100
    TAX_ADD_L4_exists.transferType = ''

    OWNERSHIP_exists = fieldTransfer()
    OWNERSHIP_exists.fieldLength = 5
    OWNERSHIP_exists.transferType = ''

    HOMESTEAD_exists = fieldTransfer()
    HOMESTEAD_exists.fieldLength = 1
    HOMESTEAD_exists.transferType = ''

    TAX_YEAR_exists = fieldTransfer()
    TAX_YEAR_exists.fieldLength = 2
    TAX_YEAR_exists.transferType = 'SmallInteger'

    MARKET_YEAR_exists = fieldTransfer()
    MARKET_YEAR_exists.fieldLength = 2
    MARKET_YEAR_exists.transferType = 'SmallInteger'

    EMV_LAND_exists = fieldTransfer()
    EMV_LAND_exists.fieldLength = 0
    EMV_LAND_exists.transferType = 'Integer'

    EMV_BLDG_exists = fieldTransfer()
    EMV_BLDG_exists.fieldLength = 0
    EMV_BLDG_exists.transferType = 'Integer'

    EMV_TOTAL_exists = fieldTransfer()
    EMV_TOTAL_exists.fieldLength = 0
    EMV_TOTAL_exists.transferType = 'Integer'

    TAX_CAPAC_exists = fieldTransfer()
    TAX_CAPAC_exists.fieldLength = 0
    TAX_CAPAC_exists.transferType = 'Integer'

    TOTAL_TAX_exists = fieldTransfer()
    TOTAL_TAX_exists.fieldLength = 0
    TOTAL_TAX_exists.transferType = 'Integer'

    SPEC_ASSES_exists = fieldTransfer()
    SPEC_ASSES_exists.fieldLength = 0
    SPEC_ASSES_exists.transferType = 'Integer'

    TAX_EXEMPT_exists = fieldTransfer()
    TAX_EXEMPT_exists.fieldLength = 1
    TAX_EXEMPT_exists.transferType = ''

    XUSE1_DESC_exists = fieldTransfer()
    XUSE1_DESC_exists.fieldLength = 100
    XUSE1_DESC_exists.transferType = ''

    XUSE2_DESC_exists = fieldTransfer()
    XUSE2_DESC_exists.fieldLength = 100
    XUSE2_DESC_exists.transferType = ''

    XUSE3_DESC_exists = fieldTransfer()
    XUSE3_DESC_exists.fieldLength = 100
    XUSE3_DESC_exists.transferType = ''

    XUSE4_DESC_exists = fieldTransfer()
    XUSE4_DESC_exists.fieldLength = 100
    XUSE4_DESC_exists.transferType = ''

    DWELL_TYPE_exists = fieldTransfer()
    DWELL_TYPE_exists.fieldLength = 30
    DWELL_TYPE_exists.transferType = ''

    HOME_STYLE_exists = fieldTransfer()
    HOME_STYLE_exists.fieldLength = 30
    HOME_STYLE_exists.transferType = ''

    FIN_SQ_FT_exists = fieldTransfer()
    FIN_SQ_FT_exists.fieldLength = 0
    FIN_SQ_FT_exists.transferType = 'Integer'

    GARAGE_exists = fieldTransfer()
    GARAGE_exists.fieldLength = 1
    GARAGE_exists.transferType = ''

    GARAGESQFT_exists = fieldTransfer()
    GARAGESQFT_exists.fieldLength = 0
    GARAGESQFT_exists.transferType = 'Integer'

    BASEMENT_exists = fieldTransfer()
    BASEMENT_exists.fieldLength = 1
    BASEMENT_exists.transferType = ''

    HEATING_exists = fieldTransfer()
    HEATING_exists.fieldLength = 30
    HEATING_exists.transferType = ''

    COOLING_exists = fieldTransfer()
    COOLING_exists.fieldLength = 30
    COOLING_exists.transferType = ''

    YEAR_BUILT_exists = fieldTransfer()
    YEAR_BUILT_exists.fieldLength = 0
    YEAR_BUILT_exists.transferType = 'SmallInteger'

    NUM_UNITS_exists = fieldTransfer()
    NUM_UNITS_exists.fieldLength = 0
    NUM_UNITS_exists.transferType = 'Integer'

    SALE_DATE_exists = fieldTransfer()
    SALE_DATE_exists.fieldLength = 0
    SALE_DATE_exists.transferType = ''

    SALE_VALUE_exists = fieldTransfer()
    SALE_VALUE_exists.fieldLength = 0
    SALE_VALUE_exists.transferType = 'Integer'

    SCHOOL_DST_exists = fieldTransfer()
    SCHOOL_DST_exists.fieldLength = 10
    SCHOOL_DST_exists.transferType = ''

    WSHD_DIST_exists = fieldTransfer()
    WSHD_DIST_exists.fieldLength = 50
    WSHD_DIST_exists.transferType = ''

    GREEN_ACRE_exists = fieldTransfer()
    GREEN_ACRE_exists.fieldLength = 1
    GREEN_ACRE_exists.transferType = ''

    OPEN_SPACE_exists = fieldTransfer()
    OPEN_SPACE_exists.fieldLength = 1
    OPEN_SPACE_exists.transferType = ''

    AG_PRESERV_exists = fieldTransfer()
    AG_PRESERV_exists.fieldLength = 1
    AG_PRESERV_exists.transferType = ''

    AGPRE_ENRD_exists = fieldTransfer()
    AGPRE_ENRD_exists.fieldLength = 0
    AGPRE_ENRD_exists.transferType = ''

    AGPRE_EXPD_exists = fieldTransfer()
    AGPRE_EXPD_exists.fieldLength = 0
    AGPRE_EXPD_exists.transferType = ''

    PARC_CODE_exists = fieldTransfer()
    PARC_CODE_exists.fieldLength = 0
    PARC_CODE_exists.transferType = 'SmallInteger'

    SECTION_exists = fieldTransfer()
    SECTION_exists.fieldLength = 0
    SECTION_exists.transferType = 'SmallInteger'

    TOWNSHIP_exists = fieldTransfer()
    TOWNSHIP_exists.fieldLength = 0
    TOWNSHIP_exists.transferType = 'SmallInteger'

    RANGE_exists = fieldTransfer()
    RANGE_exists.fieldLength = 0
    RANGE_exists.transferType = 'SmallInteger'

    RANGE_DIR_exists = fieldTransfer()
    RANGE_DIR_exists.fieldLength = 0
    RANGE_DIR_exists.transferType = 'SmallInteger'

    LEGAL_DESC_exists = fieldTransfer()
    LEGAL_DESC_exists.fieldLength = 256
    LEGAL_DESC_exists.transferType = ''

    EDIT_DATE_exists = fieldTransfer()
    EDIT_DATE_exists.fieldLength = 0
    EDIT_DATE_exists.transferType = ''

    EXPORT_DATE_exists = fieldTransfer()
    EXPORT_DATE_exists.fieldLength = 0
    EXPORT_DATE_exists.transferType = ''

    ORIG_PIN_exists = fieldTransfer()
    ORIG_PIN_exists.fieldLength = 25
    ORIG_PIN_exists.transferType = ''

    @abstractmethod
    def returnCountyBase(self):
        '''Return the county_name, needed to instantiate this base class'''
        pass