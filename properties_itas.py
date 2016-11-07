from parcels_base_classes import countyEtlParams

def createCountyObj():

    countyObj = countyEtlParams()

    countyObj.county_name = 'Itasca'
    countyObj.cty_fips = r'61'
    countyObj.county_id = r'061'
    countyObj.cty_abbr = r'ITAS'
    countyObj.mngeo_web_id = r'Itasca 061'
    countyObj.sourceZipFile = r'ITAS_parcels.zip'
    countyObj.sourcePolygons = r'Itasca_Parcels.shp'
    countyObj.sourceOwnershipZipFile = r''
    countyObj.sourceOwnershipTable = r''
    countyObj.joinInField = r''
    countyObj.joinJoinField = r''
    countyObj.PIN_fieldList = ['PARENTPIN']
    countyObj.BLDG_NUM_fieldList = ['HOUSE_NBR']
    countyObj.BLDG_NUM_transferType = ''
    countyObj.PREFIX_DIR_fieldList = []
    countyObj.PREFIX_DIR_transferType = ''
    countyObj.PREFIXTYPE_fieldList = []
    countyObj.PREFIXTYPE_transferType = ''
    countyObj.STREETNAME_fieldList = []
    countyObj.STREETNAME_transferType = ''
    countyObj.STREETTYPE_fieldList = []
    countyObj.STREETTYPE_transferType = ''
    countyObj.SUFFIX_DIR_fieldList = []
    countyObj.SUFFIX_DIR_transferType = ''
    countyObj.UNIT_INFO_fieldList = []
    countyObj.UNIT_INFO_transferType = ''
    countyObj.CITY_fieldList = []
    countyObj.CITY_transferType = ''
    countyObj.CITY_USPS_fieldList = []
    countyObj.CITY_USPS_transferType = ''
    countyObj.ZIP_fieldList = []
    countyObj.ZIP_transferType = ''
    countyObj.ZIP4_fieldList = []
    countyObj.ZIP4_transferType = ''
    countyObj.PLAT_NAME_fieldList = []
    countyObj.PLAT_NAME_transferType = ''
    countyObj.BLOCK_fieldList = []
    countyObj.BLOCK_transferType = ''
    countyObj.LOT_fieldList = []
    countyObj.LOT_transferType = ''
    countyObj.ACRES_POLY_fieldList = ['Acres']
    countyObj.ACRES_DEED_fieldList = []
    countyObj.USE1_DESC_fieldList = []
    countyObj.USE1_DESC_transferType = ''
    countyObj.USE2_DESC_fieldList = []
    countyObj.USE2_DESC_transferType = ''
    countyObj.USE3_DESC_fieldList = []
    countyObj.USE3_DESC_transferType = ''
    countyObj.USE4_DESC_fieldList = []
    countyObj.USE4_DESC_transferType = ''
    countyObj.MULTI_USES_fieldList = []
    countyObj.MULTI_USES_transferType = ''
    countyObj.LANDMARK_fieldList = []
    countyObj.LANDMARK_transferType = ''
    countyObj.OWNER_NAME_fieldList = []
    countyObj.OWNER_NAME_transferType = ''
    countyObj.OWNER_MORE_fieldList = []
    countyObj.OWNER_MORE_transferType = ''
    countyObj.OWN_ADD_L1_fieldList = []
    countyObj.OWN_ADD_L1_transferType = ''
    countyObj.OWN_ADD_L2_fieldList = []
    countyObj.OWN_ADD_L2_transferType = ''
    countyObj.OWN_ADD_L3_fieldList = []
    countyObj.OWN_ADD_L3_transferType = ''
    countyObj.OWN_ADD_L4_fieldList = []
    countyObj.OWN_ADD_L4_transferType = ''
    countyObj.TAX_NAME_fieldList = ['TAO_NAME']
    countyObj.TAX_NAME_transferType = ''
    countyObj.TAX_ADD_L1_fieldList = ['ADDR_1']
    countyObj.TAX_ADD_L1_transferType = ''
    countyObj.TAX_ADD_L2_fieldList = ['ADDR_2']
    countyObj.TAX_ADD_L2_transferType = ''
    countyObj.TAX_ADD_L3_fieldList = ['ADDR_3']
    countyObj.TAX_ADD_L3_transferType = ''
    countyObj.TAX_ADD_L4_fieldList = ['ADDR_4']
    countyObj.TAX_ADD_L4_transferType = ''
    countyObj.OWNERSHIP_fieldList = []
    countyObj.OWNERSHIP_transferType = ''
    countyObj.HOMESTEAD_fieldList = []
    countyObj.HOMESTEAD_transferType = ''
    countyObj.TAX_YEAR_fieldList = []
    countyObj.MARKET_YEAR_fieldList = []
    countyObj.EMV_LAND_fieldList = ['LAND_EST']
    countyObj.EMV_BLDG_fieldList = ['BUILDING']
    countyObj.EMV_TOTAL_fieldList = ['EMV']
    countyObj.TAX_CAPAC_fieldList = []
    countyObj.TOTAL_TAX_fieldList = []
    countyObj.SPEC_ASSES_fieldList = []
    countyObj.TAX_EXEMPT_fieldList = []
    countyObj.TAX_EXEMPT_transferType = ''
    countyObj.XUSE1_DESC_fieldList = []
    countyObj.XUSE1_DESC_transferType = ''
    countyObj.XUSE2_DESC_fieldList = []
    countyObj.XUSE2_DESC_transferType = ''
    countyObj.XUSE3_DESC_fieldList = []
    countyObj.XUSE3_DESC_transferType = ''
    countyObj.XUSE4_DESC_fieldList = []
    countyObj.XUSE4_DESC_transferType = ''
    countyObj.DWELL_TYPE_fieldList = []
    countyObj.DWELL_TYPE_transferType = ''
    countyObj.HOME_STYLE_fieldList = []
    countyObj.HOME_STYLE_transferType = ''
    countyObj.FIN_SQ_FT_fieldList = []
    countyObj.GARAGE_fieldList = []
    countyObj.GARAGE_transferType = ''
    countyObj.GARAGESQFT_fieldList = []
    countyObj.BASEMENT_fieldList = []
    countyObj.BASEMENT_transferType = ''
    countyObj.HEATING_fieldList = []
    countyObj.HEATING_transferType = ''
    countyObj.COOLING_fieldList = []
    countyObj.COOLING_transferType = ''
    countyObj.YEAR_BUILT_fieldList = []
    countyObj.NUM_UNITS_fieldList = []
    countyObj.SALE_DATE_fieldList = []
    countyObj.SALE_DATE_transferType = 'Date'
    countyObj.SALE_VALUE_fieldList = []
    countyObj.SCHOOL_DST_fieldList = []
    countyObj.SCHOOL_DST_transferType = ''
    countyObj.WSHD_DIST_fieldList = []
    countyObj.WSHD_DIST_transferType = ''
    countyObj.GREEN_ACRE_fieldList = []
    countyObj.GREEN_ACRE_transferType = ''
    countyObj.OPEN_SPACE_fieldList = []
    countyObj.OPEN_SPACE_transferType = ''
    countyObj.AG_PRESERV_fieldList = []
    countyObj.AG_PRESERV_transferType = ''
    countyObj.AGPRE_ENRD_fieldList = []
    countyObj.AGPRE_ENRD_transferType = 'Date'
    countyObj.AGPRE_EXPD_fieldList = []
    countyObj.AGPRE_EXPD_transferType = 'Date'
    countyObj.PARC_CODE_fieldList = []
    countyObj.SECTION_fieldList = ['SECTION']
    countyObj.TOWNSHIP_fieldList = ['TOWNSHIP']
    countyObj.RANGE_fieldList = ['RANGE']
    countyObj.RANGE_DIR_fieldList = []
    countyObj.LEGAL_DESC_fieldList = ['DESCRIP']
    countyObj.LEGAL_DESC_transferType = ''
    countyObj.EDIT_DATE_fieldList = []
    countyObj.EDIT_DATE_transferType = 'Date'
    countyObj.EXPORT_DATE_fieldList = []
    countyObj.EXPORT_DATE_transferType = 'Date'
    countyObj.ORIG_PIN_fieldList = ['PARENTPIN']
    countyObj.ORIG_PIN_transferType = ''

    return countyObj
