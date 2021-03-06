# coding=utf-8
# 
from cerberus import Validator
from cerberus.errors import BasicErrorHandler
from datetime import datetime
import yaml
import re

class AppValidatorFactory:

	def get_validator(self, method_name):
		if method_name == "get_security_basic_info":
			return self._get_get_security_basic_info_validator()
		elif method_name == "add_security_basic_info":
			return self._get_add_security_basic_info_validator()
		elif method_name == "update_security_basic_info":
			return self._get_update_security_basic_info_validator()
		elif method_name == "get_futures_info":
			return self._get_get_futures_info_validator()
		elif method_name == "add_futures_info":
			return self._get_add_futures_info_validator()
		elif method_name == "update_futures_info":
			return self._get_update_futures_info_validator()
		elif method_name == "get_fixed_deposit_info":
			return self._get_get_fixed_deposit_info_validator()
		elif method_name == "add_fixed_deposit_info":
			return self._get_add_fixed_deposit_info_validator()
		elif method_name == "update_fixed_deposit_info":
			return self._get_update_fixed_deposit_info_validator()
		elif method_name == "get_fx_forward_info":
			return self._get_get_fx_forward_info_validator()
		elif method_name == "add_fx_forward_info":
			return self._get_add_fx_forward_info_validator()
		elif method_name == "update_fx_forward_info":
			return self._get_update_fx_forward_info_validator()
		elif method_name == "add_counter_party_info":
			return self._get_add_counter_party_validator()
		elif method_name == "update_counter_party_info":
			return self._get_update_counter_party_info_validator()
		elif method_name == "get_security_attribute":
			return self._get_get_security_attribute_validator()
		elif method_name == "add_security_attribute":
			return self._get_add_security_attribute_validator()
		elif method_name == "update_security_attribute":
			return self._get_add_security_attribute_validator()
		else:
			raise Exception("No validator defined for method_name: " + \
								method_name + \
								". Please check and add back")

	def _get_get_security_basic_info_validator(self):
		#-- note: yaml need to use space not tab for indentation
		schema_text = '''
geneva_id:
  required: true
  empty: false
  type: string
  maxlength: 100
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_add_security_basic_info_validator(self):
		schema_text = '''
geneva_id:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_asset_type:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_investment_type:
  required: true
  empty: false
  type: string
  maxlength: 100
ticker:
  required: true
  empty: false
  type: string
  maxlength: 50
isin:
  required: true
  empty: false
  type: string
  maxlength: 50
bloomberg_id:
  required: true
  empty: false
  type: string
  maxlength: 50
sedol:
  required: true
  empty: false
  type: string
  maxlength: 50
currency:
  required: true
  empty: false
  type: string
  maxlength: 5
is_private:
  required: true
  type: string
  allowed: ['N', 'Y', 'NA']
description:
  required: true
  empty: false
  type: string
  maxlength: 200
exchange_name:
  required: true
  empty: false
  type: string
  maxlength: 100
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_update_security_basic_info_validator(self):
		schema_text = '''
geneva_id:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_asset_type:
  required: false
  empty: false
  type: string
  maxlength: 100
geneva_investment_type:
  required: false
  empty: false
  type: string
  maxlength: 100
ticker:
  required: false
  empty: false
  type: string
  maxlength: 50
isin:
  required: false
  empty: false
  type: string
  maxlength: 50
bloomberg_id:
  required: false
  empty: false
  type: string
  maxlength: 50
sedol:
  required: false
  empty: false
  type: string
  maxlength: 50
currency:
  required: false
  empty: false
  type: string
  maxlength: 5
is_private:
  required: false
  empty: false
  type: string
  allowed: ['N', 'Y', 'NA']
description:
  required: false
  empty: false
  type: string
  maxlength: 200
exchange_name:
  required: false
  empty: false
  type: string
  maxlength: 100
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)


	def _get_get_futures_info_validator(self):
		#-- note: yaml need to use space not tab for indentation
		schema_text = '''
ticker:
  required: true
  empty: false
  type: string
  maxlength: 50
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_add_futures_info_validator(self):
		schema_text = '''
ticker:
  required: true
  empty: false
  type: string
  maxlength: 50
underlying_id:
  required: false
  empty: false
  type: string
  maxlength: 100
contract_size:
  required: false
  check_with: float_format
value_of_1pt:
  required: false
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_update_futures_info_validator(self):
		schema_text = '''
ticker:
  required: true
  empty: false
  type: string
  maxlength: 50
underlying_id:
  required: false
  empty: false
  type: string
  maxlength: 100
contract_size:
  required: false
  check_with: float_format
value_of_1pt:
  required: false
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)


	def _get_get_fixed_deposit_info_validator(self):
		#-- note: yaml need to use space not tab for indentation
		schema_text = '''
geneva_id:
  required: true
  empty: false
  type: string
  maxlength: 50
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_add_fixed_deposit_info_validator(self):
		schema_text = '''
geneva_id:
  required: true
  empty: false
  type: string
  maxlength: 50
factset_id:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_counter_party:
  required: true
  empty: false
  type: string
  maxlength: 100
starting_date:
  required: true
  check_with: yyyy_mm_dd_date_format
maturity_date:
  required: true
  check_with: yyyy_mm_dd_date_format
interest_rate:
  required: true
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_update_fixed_deposit_info_validator(self):
		schema_text = '''
geneva_id:
  required: true
  empty: false
  type: string
  maxlength: 50
factset_id:
  required: false
  empty: false
  type: string
  maxlength: 100
geneva_counter_party:
  required: false
  empty: false
  type: string
  maxlength: 100
starting_date:
  required: false
  check_with: yyyy_mm_dd_date_format
maturity_date:
  required: false
  check_with: yyyy_mm_dd_date_format
interest_rate:
  required: false
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)


	def _get_get_fx_forward_info_validator(self):
		#-- note: yaml need to use space not tab for indentation
		schema_text = '''
factset_id:
  required: true
  empty: false
  type: string
  maxlength: 100
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_add_fx_forward_info_validator(self):
		schema_text = '''
factset_id:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_fx_forward_name:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_counter_party:
  required: true
  empty: false
  type: string
  maxlength: 100
starting_date:
  required: true
  check_with: yyyy_mm_dd_date_format
maturity_date:
  required: true
  check_with: yyyy_mm_dd_date_format
base_currency:
  required: true
  empty: false
  type: string
  maxlength: 5
base_currency_quantity:
  required: true
  check_with: float_format
term_currency:
  required: true
  empty: false
  type: string
  maxlength: 5
term_currency_quantity:
  required: true
  check_with: float_format
forward_rate:
  required: true
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_update_fx_forward_info_validator(self):
		schema_text = '''
factset_id:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_fx_forward_name:
  required: false
  empty: false
  type: string
  maxlength: 100
geneva_counter_party:
  required: false
  empty: false
  type: string
  maxlength: 100
starting_date:
  required: false
  check_with: yyyy_mm_dd_date_format
maturity_date:
  required: false
  check_with: yyyy_mm_dd_date_format
base_currency:
  required: false
  empty: false
  type: string
  maxlength: 5
base_currency_quantity:
  required: false
  check_with: float_format
term_currency:
  required: false
  empty: false
  type: string
  maxlength: 5
term_currency_quantity:
  required: false
  check_with: float_format
forward_rate:
  required: false
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)


	def _get_add_counter_party_validator(self):
		schema_text = '''
geneva_counter_party:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_party_type:
  required: true
  type: string
  allowed: ['Fixed Deposit', 'Repo', 'FX Forward']
geneva_party_name:
  required: false
  empty: true
  type: string
  maxlength: 100
bloomberg_ticker:
  required: false
  empty: true
  type: string
  maxlength: 50
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_update_counter_party_info_validator(self):
		schema_text = '''
geneva_counter_party:
  required: true
  empty: false
  type: string
  maxlength: 100
geneva_party_type:
  required: true
  type: string
  allowed: ['Fixed Deposit', 'Repo', 'FX Forward']
geneva_party_name:
  required: false
  empty: false
  type: string
  maxlength: 100
bloomberg_ticker:
  required: false
  empty: true
  type: string
  maxlength: 50
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)


	def _get_get_security_attribute_validator(self):
		#-- note: yaml need to use space not tab for indentation
		schema_text = '''
security_id_type:
  required: true
  empty: false
  type: string
  maxlength: 100
security_id:
  required: true
  empty: false
  type: string
  maxlength: 100
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_add_security_attribute_validator(self):
		schema_text = '''
security_id_type:
  required: true
  empty: false
  type: string
  allowed: ['Ticker', 'ISIN', 'Bloomberg Id']
security_id:
  required: true
  empty: false
  type: string
  maxlength: 100
gics_sector:
  required: false
  type: string
  maxlength: 100
gics_industry_group:
  required: false
  type: string
  maxlength: 100
industry_sector:
  required: false
  type: string
  maxlength: 100
industry_group:
  required: false
  type: string
  maxlength: 100
bics_sector_level_1:
  required: false
  type: string
  maxlength: 100
bics_industry_group_level_2:
  required: false
  type: string
  maxlength: 100
bics_industry_name_level_3:
  required: false
  type: string
  maxlength: 100
bics_sub_industry_name_level_4:
  required: false
  type: string
  maxlength: 100
parent_symbol:
  required: false
  type: string
  maxlength: 100
parent_symbol_chinese_name:
  required: false
  type: string
  maxlength: 100
parent_symbol_industry_group:
  required: false
  type: string
  maxlength: 100
cast_parent_company_name:
  required: false
  type: string
  maxlength: 100
country_of_risk:
  required: false
  type: string
  maxlength: 100
country_of_issuance:
  required: false
  type: string
  maxlength: 100
sfc_region:
  required: false
  type: string
  maxlength: 100
s_p_issuer_rating:
  required: false
  type: string
  maxlength: 100
moody_s_issuer_rating:
  required: false
  type: string
  maxlength: 100
fitch_s_issuer_rating:
  required: false
  type: string
  maxlength: 100
bond_or_equity_ticker:
  required: false
  type: string
  maxlength: 100
s_p_rating:
  required: false
  type: string
  maxlength: 100
moody_s_rating:
  required: false
  type: string
  maxlength: 100
fitch_rating:
  required: false
  type: string
  maxlength: 100
payment_rank:
  required: false
  type: string
  maxlength: 100
payment_rank_mbs:
  required: false
  type: string
  maxlength: 100
bond_classification:
  required: false
  type: string
  maxlength: 100
local_government_lgfv:
  required: false
  type: string
  maxlength: 100
first_year_default_probability:
  required: false
  check_with: float_format
contingent_capital:
  required: false
  type: string
  maxlength: 100
co_co_bond_trigger:
  required: false
  type: string
  maxlength: 100
capit_type_conti_conv_tri_lvl:
  required: false
  type: string
  maxlength: 100
tier_1_common_equity_ratio:
  required: false
  check_with: float_format
bail_in_capital_indicator:
  required: false
  type: string
  maxlength: 100
tlac_mrel_designation:
  required: false
  type: string
  maxlength: 100
classif_on_chi_state_owned_enterp:
  required: false
  type: string
  maxlength: 100
private_placement_indicator:
  required: false
  type: string
  allowed: ['Y', 'N', '']
trading_volume_90_days:
  required: false
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)

	def _get_update_security_attribute_validator(self):
		schema_text = '''
security_id_type:
  required: true
  empty: false
  type: string
  allowed: ['Ticker', 'ISIN', 'Bloomberg Id']
security_id:
  required: true
  empty: false
  type: string
  maxlength: 100
gics_sector:
  required: false
  type: string
  maxlength: 100
gics_industry_group:
  required: false
  type: string
  maxlength: 100
industry_sector:
  required: false
  type: string
  maxlength: 100
industry_group:
  required: false
  type: string
  maxlength: 100
bics_sector_level_1:
  required: false
  type: string
  maxlength: 100
bics_industry_group_level_2:
  required: false
  type: string
  maxlength: 100
bics_industry_name_level_3:
  required: false
  type: string
  maxlength: 100
bics_sub_industry_name_level_4:
  required: false
  type: string
  maxlength: 100
parent_symbol:
  required: false
  type: string
  maxlength: 100
parent_symbol_chinese_name:
  required: false
  type: string
  maxlength: 100
parent_symbol_industry_group:
  required: false
  type: string
  maxlength: 100
cast_parent_company_name:
  required: false
  type: string
  maxlength: 100
country_of_risk:
  required: false
  type: string
  maxlength: 100
country_of_issuance:
  required: false
  type: string
  maxlength: 100
sfc_region:
  required: false
  type: string
  maxlength: 100
s_p_issuer_rating:
  required: false
  type: string
  maxlength: 100
moody_s_issuer_rating:
  required: false
  type: string
  maxlength: 100
fitch_s_issuer_rating:
  required: false
  type: string
  maxlength: 100
bond_or_equity_ticker:
  required: false
  type: string
  maxlength: 100
s_p_rating:
  required: false
  type: string
  maxlength: 100
moody_s_rating:
  required: false
  type: string
  maxlength: 100
fitch_rating:
  required: false
  type: string
  maxlength: 100
payment_rank:
  required: false
  type: string
  maxlength: 100
payment_rank_mbs:
  required: false
  type: string
  maxlength: 100
bond_classification:
  required: false
  type: string
  maxlength: 100
local_government_lgfv:
  required: false
  type: string
  maxlength: 100
first_year_default_probability:
  required: false
  check_with: float_format
contingent_capital:
  required: false
  type: string
  maxlength: 100
co_co_bond_trigger:
  required: false
  type: string
  maxlength: 100
capit_type_conti_conv_tri_lvl:
  required: false
  type: string
  maxlength: 100
tier_1_common_equity_ratio:
  required: false
  check_with: float_format
bail_in_capital_indicator:
  required: false
  type: string
  maxlength: 100
tlac_mrel_designation:
  required: false
  type: string
  maxlength: 100
classif_on_chi_state_owned_enterp:
  required: false
  type: string
  maxlength: 100
private_placement_indicator:
  required: false
  type: string
  allowed: ['Y', 'N', '']
trading_volume_90_days:
  required: false
  check_with: float_format
'''
		schema = yaml.load(schema_text, Loader=yaml.FullLoader)
		return AppValidator(schema)



class AppValidator(Validator):
	
	#-- comment out as the date in the getRepo() is removed
	def _check_with_yyyy_mm_dd_date_format(self, field, value):
		try:
			datetime.strptime(value, "%Y-%m-%d")
		except ValueError:
			self._error(field, "date format must be in yyyy-mm-dd")

	def _check_with_float_format(self, field, value):
		try:
			val = float(value)
		except ValueError:
			self._error(field, "must be of number type")

