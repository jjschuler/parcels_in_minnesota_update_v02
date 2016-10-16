from parcels_base_classes import countyEtlParams

class countyEtl(countyEtlParams):

    '''Class per county with unique parameters defined.'''
    def __init__(self):
        self.county_name = 'Cook'
        self.cty_fips = r'31'
        self.county_id = r'031'
        self.cty_abbr = r'COOK'
        self.mngeo_web_id = r'Cook 031'
        self.sourceZipFile = r'COOK_parcels.zip'
        self.sourcePolygons = r'CookCountyTaxParcels.shp'
        self.PIN_exists.fieldTransferList = ['PARCELNBR']
        self.BLDG_NUM_exists.fieldTransferList = ['HOUSE_NBR']
        self.BLDG_NUM_exists.transferType = ''
        self.PREFIX_DIR_exists.fieldTransferList = []
        self.PREFIX_DIR_exists.transferType = ''
        self.PREFIXTYPE_exists.fieldTransferList = []
        self.PREFIXTYPE_exists.transferType = ''
        self.STREETNAME_exists.fieldTransferList = []
        self.STREETNAME_exists.transferType = ''
        self.STREETTYPE_exists.fieldTransferList = []
        self.STREETTYPE_exists.transferType = ''
        self.SUFFIX_DIR_exists.fieldTransferList = []
        self.SUFFIX_DIR_exists.transferType = ''
        self.UNIT_INFO_exists.fieldTransferList = []
        self.UNIT_INFO_exists.transferType = ''
        self.CITY_exists.fieldTransferList = []
        self.CITY_exists.transferType = ''
        self.CITY_USPS_exists.fieldTransferList = []
        self.CITY_USPS_exists.transferType = ''
        self.ZIP_exists.fieldTransferList = []
        self.ZIP_exists.transferType = ''
        self.ZIP4_exists.fieldTransferList = []
        self.ZIP4_exists.transferType = ''
        self.PLAT_NAME_exists.fieldTransferList = ['PLDESC']
        self.PLAT_NAME_exists.transferType = ''
        self.BLOCK_exists.fieldTransferList = ['BLOCKNBR']
        self.BLOCK_exists.transferType = ''
        self.LOT_exists.fieldTransferList = ['LOTNBR']
        self.LOT_exists.transferType = ''
        self.ACRES_POLY_exists.fieldTransferList = ['Calculated']
        self.ACRES_DEED_exists.fieldTransferList = ['DEEDEDACRE']
        self.USE1_DESC_exists.fieldTransferList = ['ACCLDS1']
        self.USE1_DESC_exists.transferType = ''
        self.USE2_DESC_exists.fieldTransferList = ['ACCLDS2']
        self.USE2_DESC_exists.transferType = ''
        self.USE3_DESC_exists.fieldTransferList = ['ACCLDS3']
        self.USE3_DESC_exists.transferType = ''
        self.USE4_DESC_exists.fieldTransferList = []
        self.USE4_DESC_exists.transferType = ''
        self.MULTI_USES_exists.fieldTransferList = []
        self.MULTI_USES_exists.transferType = ''
        self.LANDMARK_exists.fieldTransferList = []
        self.LANDMARK_exists.transferType = ''
        self.OWNER_NAME_exists.fieldTransferList = ['OWNNAME']
        self.OWNER_NAME_exists.transferType = ''
        self.OWNER_MORE_exists.fieldTransferList = []
        self.OWNER_MORE_exists.transferType = ''
        self.OWN_ADD_L1_exists.fieldTransferList = ['OWNADR1']
        self.OWN_ADD_L1_exists.transferType = ''
        self.OWN_ADD_L2_exists.fieldTransferList = ['OWNADR2']
        self.OWN_ADD_L2_exists.transferType = ''
        self.OWN_ADD_L3_exists.fieldTransferList = ['OWNADR3']
        self.OWN_ADD_L3_exists.transferType = ''
        self.OWN_ADD_L4_exists.fieldTransferList = ['OWNADR4', 'OWNZIP5']
        self.OWN_ADD_L4_exists.transferType = 'concatTruncateTwoFields'
        self.TAX_NAME_exists.fieldTransferList = ['TAXNAME']
        self.TAX_NAME_exists.transferType = ''
        self.TAX_ADD_L1_exists.fieldTransferList = ['TAXADR1']
        self.TAX_ADD_L1_exists.transferType = ''
        self.TAX_ADD_L2_exists.fieldTransferList = ['TAXADR2']
        self.TAX_ADD_L2_exists.transferType = ''
        self.TAX_ADD_L3_exists.fieldTransferList = ['TAXADR3']
        self.TAX_ADD_L3_exists.transferType = ''
        self.TAX_ADD_L4_exists.fieldTransferList = ['TAXADR4', 'TAXZIP5']
        self.TAX_ADD_L4_exists.transferType = 'concatTruncateTwoFields'
        self.OWNERSHIP_exists.fieldTransferList = ['OWNTYPE']
        self.OWNERSHIP_exists.transferType = ''
        self.HOMESTEAD_exists.fieldTransferList = []
        self.HOMESTEAD_exists.transferType = ''
        self.TAX_YEAR_exists.fieldTransferList = ['TAXYEAR']
        self.MARKET_YEAR_exists.fieldTransferList = []
        self.EMV_LAND_exists.fieldTransferList = ['LANDEST']
        self.EMV_BLDG_exists.fieldTransferList = ['BUILDING']
        self.EMV_TOTAL_exists.fieldTransferList = []
        self.TAX_CAPAC_exists.fieldTransferList = []
        self.TOTAL_TAX_exists.fieldTransferList = []
        self.SPEC_ASSES_exists.fieldTransferList = []
        self.TAX_EXEMPT_exists.fieldTransferList = []
        self.TAX_EXEMPT_exists.transferType = ''
        self.XUSE1_DESC_exists.fieldTransferList = []
        self.XUSE1_DESC_exists.transferType = ''
        self.XUSE2_DESC_exists.fieldTransferList = []
        self.XUSE2_DESC_exists.transferType = ''
        self.XUSE3_DESC_exists.fieldTransferList = []
        self.XUSE3_DESC_exists.transferType = ''
        self.XUSE4_DESC_exists.fieldTransferList = []
        self.XUSE4_DESC_exists.transferType = ''
        self.DWELL_TYPE_exists.fieldTransferList = []
        self.DWELL_TYPE_exists.transferType = ''
        self.HOME_STYLE_exists.fieldTransferList = []
        self.HOME_STYLE_exists.transferType = ''
        self.FIN_SQ_FT_exists.fieldTransferList = []
        self.GARAGE_exists.fieldTransferList = []
        self.GARAGE_exists.transferType = ''
        self.GARAGESQFT_exists.fieldTransferList = []
        self.BASEMENT_exists.fieldTransferList = []
        self.BASEMENT_exists.transferType = ''
        self.HEATING_exists.fieldTransferList = []
        self.HEATING_exists.transferType = ''
        self.COOLING_exists.fieldTransferList = []
        self.COOLING_exists.transferType = ''
        self.YEAR_BUILT_exists.fieldTransferList = []
        self.NUM_UNITS_exists.fieldTransferList = []
        self.SALE_DATE_exists.fieldTransferList = []
        self.SALE_DATE_exists.transferType = 'Date'
        self.SALE_VALUE_exists.fieldTransferList = []
        self.SCHOOL_DST_exists.fieldTransferList = []
        self.SCHOOL_DST_exists.transferType = ''
        self.WSHD_DIST_exists.fieldTransferList = []
        self.WSHD_DIST_exists.transferType = ''
        self.GREEN_ACRE_exists.fieldTransferList = []
        self.GREEN_ACRE_exists.transferType = ''
        self.OPEN_SPACE_exists.fieldTransferList = []
        self.OPEN_SPACE_exists.transferType = ''
        self.AG_PRESERV_exists.fieldTransferList = []
        self.AG_PRESERV_exists.transferType = ''
        self.AGPRE_ENRD_exists.fieldTransferList = []
        self.AGPRE_ENRD_exists.transferType = 'Date'
        self.AGPRE_EXPD_exists.fieldTransferList = []
        self.AGPRE_EXPD_exists.transferType = 'Date'
        self.PARC_CODE_exists.fieldTransferList = []
        self.SECTION_exists.fieldTransferList = ['SEC']
        self.TOWNSHIP_exists.fieldTransferList = ['TWP']
        self.RANGE_exists.fieldTransferList = ['RGE']
        self.RANGE_DIR_exists.fieldTransferList = ['DIR']
        self.LEGAL_DESC_exists.fieldTransferList = ['DSDESC']
        self.LEGAL_DESC_exists.transferType = ''
        self.EDIT_DATE_exists.fieldTransferList = []
        self.EDIT_DATE_exists.transferType = 'Date'
        self.EXPORT_DATE_exists.fieldTransferList = []
        self.EXPORT_DATE_exists.transferType = 'Date'
        self.ORIG_PIN_exists.fieldTransferList = ['PARCELNBR']
        self.ORIG_PIN_exists.transferType = ''

    def returnCountyBase(self):
        return county_name
