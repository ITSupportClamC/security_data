from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base(name='BaseModel')

class SecurityAttribute(BaseModel):
	__tablename__ = "security_attributes"
	id = Column(Integer, primary_key=True)
	security_id_type = Column(String(100))
	security_id = Column(String(100))
	gics_sector = Column(String(100))
	gics_industry_group = Column(String(100))
	industry_sector = Column(String(100))
	industry_group = Column(String(100))
	bics_sector_level_1 = Column(String(100))
	bics_industry_group_level_2 = Column(String(100))
	bics_industry_name_level_3 = Column(String(100))
	bics_sub_industry_name_level_4 = Column(String(100))
	parent_symbol = Column(String(100))
	parent_symbol_chinese_name = Column(String(100))
	parent_symbol_industry_group = Column(String(100))
	cast_parent_company_name = Column(String(100))
	country_of_risk = Column(String(100))
	country_of_issuance = Column(String(100))
	sfc_region = Column(String(100))
	s_p_issuer_rating = Column(String(100))
	moody_s_issuer_rating = Column(String(100))
	fitch_s_issuer_rating = Column(String(100))
	bond_or_equity_ticker = Column(String(100))
	s_p_rating = Column(String(100))
	moody_s_rating = Column(String(100))
	fitch_rating = Column(String(100))
	payment_rank = Column(String(100))
	payment_rank_mbs = Column(String(100))
	bond_classification = Column(String(100))
	local_government_lgfv = Column(String(100))
	first_year_default_probability = Column(Numeric(asdecimal=False))
	contingent_capital = Column(String(100))
	co_co_bond_trigger = Column(String(100))
	capit_type_conti_conv_tri_lvl = Column(String(100))
	tier_1_common_equity_ratio = Column(Numeric(asdecimal=False))
	bail_in_capital_indicator = Column(String(100))
	tlac_mrel_designation = Column(String(100))
	classif_on_chi_state_owned_enterp = Column(String(100))
	private_placement_indicator = Column(String(100))
	trading_volume_90_days = Column(Numeric(asdecimal=False))
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	created_by = Column(Integer)
	updated_by = Column(Integer)

	def __init__(self, \
				security_id_type, \
				security_id, \
				gics_sector=None, \
				gics_industry_group=None, \
				industry_sector=None, \
				industry_group=None, \
				bics_sector_level_1=None, \
				bics_industry_group_level_2=None, \
				bics_industry_name_level_3=None, \
				bics_sub_industry_name_level_4=None, \
				parent_symbol=None, \
				parent_symbol_chinese_name=None, \
				parent_symbol_industry_group=None, \
				cast_parent_company_name=None, \
				country_of_risk=None, \
				country_of_issuance=None, \
				sfc_region=None, \
				s_p_issuer_rating=None, \
				moody_s_issuer_rating=None, \
				fitch_s_issuer_rating=None, \
				bond_or_equity_ticker=None, \
				s_p_rating=None, \
				moody_s_rating=None, \
				fitch_rating=None, \
				payment_rank=None, \
				payment_rank_mbs=None, \
				bond_classification=None, \
				local_government_lgfv=None, \
				first_year_default_probability=None, \
				contingent_capital=None, \
				co_co_bond_trigger=None, \
				capit_type_conti_conv_tri_lvl=None, \
				tier_1_common_equity_ratio=None, \
				bail_in_capital_indicator=None, \
				tlac_mrel_designation=None, \
				classif_on_chi_state_owned_enterp=None, \
				private_placement_indicator=None, \
				trading_volume_90_days=None):
		self.security_id_type = security_id_type
		self.security_id = security_id
		self.gics_sector = gics_sector
		self.gics_industry_group = gics_industry_group
		self.industry_sector = industry_sector
		self.industry_group = industry_group
		self.bics_sector_level_1 = bics_sector_level_1
		self.bics_industry_group_level_2 = bics_industry_group_level_2
		self.bics_industry_name_level_3 = bics_industry_name_level_3
		self.bics_sub_industry_name_level_4 = bics_sub_industry_name_level_4
		self.parent_symbol = parent_symbol
		self.parent_symbol_chinese_name = parent_symbol_chinese_name
		self.parent_symbol_industry_group = parent_symbol_industry_group
		self.cast_parent_company_name = cast_parent_company_name
		self.country_of_risk = country_of_risk
		self.country_of_issuance = country_of_issuance
		self.sfc_region = sfc_region
		self.s_p_issuer_rating = s_p_issuer_rating
		self.moody_s_issuer_rating = moody_s_issuer_rating
		self.fitch_s_issuer_rating = fitch_s_issuer_rating
		self.bond_or_equity_ticker = bond_or_equity_ticker
		self.s_p_rating = s_p_rating
		self.moody_s_rating = moody_s_rating
		self.fitch_rating = fitch_rating
		self.payment_rank = payment_rank
		self.payment_rank_mbs = payment_rank_mbs
		self.bond_classification = bond_classification
		self.local_government_lgfv = local_government_lgfv
		self.first_year_default_probability = first_year_default_probability
		self.contingent_capital = contingent_capital
		self.co_co_bond_trigger = co_co_bond_trigger
		self.capit_type_conti_conv_tri_lvl = capit_type_conti_conv_tri_lvl
		self.tier_1_common_equity_ratio = tier_1_common_equity_ratio
		self.bail_in_capital_indicator = bail_in_capital_indicator
		self.tlac_mrel_designation = tlac_mrel_designation
		self.classif_on_chi_state_owned_enterp = classif_on_chi_state_owned_enterp
		self.private_placement_indicator = private_placement_indicator
		self.trading_volume_90_days = trading_volume_90_days

	def __repr__(self):
		res = {}
		columns = [m.key for m in model.__table__.columns]
		for column in columns:
			res[column] = getattr(model, column)
		return res
