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

