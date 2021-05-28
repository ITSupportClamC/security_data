# coding=utf-8
# 
import logging
from cerberus import SchemaError
from datetime import datetime
from security_data.constants import Constants
from security_data.utils.error_handling import (NoDataClearingInProuctionModeError,
											DataStoreNotYetInitializeError)
from security_data.utils.database import DBConn
from security_data.utils.validator import AppValidatorFactory
from security_data.services.security_base_services import SecurityBaseServices
from security_data.services.futures_services import FuturesServices
from security_data.services.fixed_deposit_services import FixedDepositServices
from security_data.services.fx_forward_services import FxForwardServices
from security_data.services.otc_counter_party_services import OtcCounterPartyServices
from security_data.services.security_attribute_services import SecurityAttributeServices

#-- serivce and DB connection shall be stateless so it is safe to have a singleton
#db = DBConn.get_db()
#repo_master_services = RepoMasterServices(db)
#repo_transaction_services = RepoTransactionServices(db)
#repo_transaction_history_services = RepoTransactionHistoryServices(db)

class AppController:

	logger = None
	dbmode = None
	security_base_services = None
	futures_services = None
	otc_counter_party_services = None
	fixed_deposit_services = None
	fx_forward_services = None
	security_attribute_services = None

	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.dbmode = None

	def initialize_datastore(self, mode):
		if (mode == "production"):
			self.dbmode = Constants.DBMODE_PRODUCTION
			self.logger.info("Change datastore mode to DBMODE_PRODUCTION")
		elif (mode == "uat"):
			self.dbmode = Constants.DBMODE_UAT
			self.logger.info("Change datastore mode to DBMODE_UAT")
		else:
			self.dbmode = Constants.DBMODE_TEST
			self.logger.info("Change datastore mode to DBMODE_TEST")
		db = DBConn.get_db(self.dbmode)
		self.security_base_services = SecurityBaseServices(db)
		self.futures_services = FuturesServices(db)
		self.otc_counter_party_services = OtcCounterPartyServices(db)
		self.fixed_deposit_services = FixedDepositServices(db, self.otc_counter_party_services)
		self.fx_forward_services = FxForwardServices(db, self.otc_counter_party_services)
		self.security_attribute_services = SecurityAttributeServices(db)
		return 0

	def clear_security_data(self):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		print(self.dbmode)
		if self.dbmode == Constants.DBMODE_PRODUCTION:
			error_message = "clearRepoData can only run under DBMODE_TEST mode"
			self.logger.warn(error_message)
			raise NoDataClearingInProuctionModeError(error_message)
		else:
			self.logger.warn("clear data in security_base table")
			self.security_base_services.delete_all()
			self.logger.warn("clear data in futures table")
			self.futures_services.delete_all()
			self.logger.debug("clear data in fixed_deposit table")
			self.fixed_deposit_services.delete_all()
			self.logger.debug("clear data in fx_forward table")
			self.fx_forward_services.delete_all()
			self.logger.debug("clear data in otc_counter_party table")
			self.otc_counter_party_services.delete_all()
			self.logger.debug("clear data in security_attribute table")
			self.security_attribute_services.delete_all()
			return 0
	
	def get_security_basic_info(self, geneva_id):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		params = {
			"geneva_id" : geneva_id
		}
		v = AppValidatorFactory().get_validator("get_security_basic_info")
		#-- validate input fields
		if not v.validate(params):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- get the first value from the dictionary and return
		security_base_l = self.security_base_services.query(params)
		security_base = {}
		if len(security_base_l) > 0:
			security_base = security_base_l[0]
		return security_base

	def add_security_basic_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("add_security_basic_info")
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- 1. add timestamp with curent date time
		now = datetime.now()
		security_info["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
		#-- create data model
		self.security_base_services.create(security_info)
		return 0

	def update_security_basic_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("update_security_basic_info")
		#-- validate input fields
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- 1. add timestamp with curent date time
		now = datetime.now()
		security_info["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
		#-- create data model
		self.security_base_services.update(security_info)
		return 0
	
	def get_futures_info(self, ticker):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		params = {
			"ticker" : ticker
		}
		v = AppValidatorFactory().get_validator("get_futures_info")
		#-- validate input fields
		if not v.validate(params):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- get the first value from the dictionary and return
		futures_l = self.futures_services.query(params)
		futures = {}
		if len(futures_l) > 0:
			futures = futures_l[0]
		return futures

	def add_futures_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("add_futures_info")
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- 1. add timestamp with curent date time
		now = datetime.now()
		security_info["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
		#-- create data model
		self.futures_services.create(security_info)
		return 0

	def update_futures_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("update_futures_info")
		#-- validate input fields
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- 1. add timestamp with curent date time
		now = datetime.now()
		security_info["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S")
		#-- create data model
		self.futures_services.update(security_info)
		return 0
	
	def get_fixed_deposit_info(self, geneva_id):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		params = {
			"geneva_id" : geneva_id
		}
		v = AppValidatorFactory().get_validator("get_fixed_deposit_info")
		#-- validate input fields
		if not v.validate(params):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- get the first value from the dictionary and return
		fixed_deposit_l = self.fixed_deposit_services.query(params)
		fixed_deposit = {}
		if len(fixed_deposit_l) > 0:
			fixed_deposit = fixed_deposit_l[0]
		return fixed_deposit

	def add_fixed_deposit_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("add_fixed_deposit_info")
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no data parsing need
		#-- create data model
		#-- reuse the security_info
		self.fixed_deposit_services.create(security_info)
		return 0

	def update_fixed_deposit_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("update_fixed_deposit_info")
		#-- validate input fields
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no data parsing need
		#-- create data model
		#-- reuse the security_info
		self.fixed_deposit_services.update(security_info)
		return 0
	
	def get_fx_forward_info(self, factset_id):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		params = {
			"factset_id" : factset_id
		}
		v = AppValidatorFactory().get_validator("get_fx_forward_info")
		#-- validate input fields
		if not v.validate(params):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- get the first value from the dictionary and return
		fx_forward_l = self.fx_forward_services.query(params)
		fx_forward = {}
		if len(fx_forward_l) > 0:
			fx_forward = fx_forward_l[0]
		return fx_forward

	def add_fx_forward_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("add_fx_forward_info")
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no data parsing need
		#-- create data model
		#-- reuse the security_info
		self.fx_forward_services.create(security_info)
		return 0

	def update_fx_forward_info(self, security_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("update_fx_forward_info")
		#-- validate input fields
		if not v.validate(security_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no data parsing need
		#-- create data model
		#-- reuse the security_info
		self.fx_forward_services.update(security_info)
		return 0
	
	def get_all_counter_party_info(self):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		#-- no input parameter
		#-- no input validation needs
		#-- return list of counter party
		otc_counter_party_l = self.otc_counter_party_services.query()
		return otc_counter_party_l

	def add_counter_party_info(self, counter_party_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("add_counter_party_info")
		if not v.validate(counter_party_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no data parsing need
		#-- create data model
		#-- reuse the counter_party_info
		self.otc_counter_party_services.create(counter_party_info)
		return 0

	def update_counter_party_info(self, counter_party_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("update_counter_party_info")
		#-- validate input fields
		if not v.validate(counter_party_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no data parsing need
		#-- create data model
		#-- reuse the counter_party_info
		self.otc_counter_party_services.update(counter_party_info)
		return 0
	
	def get_security_attribute(self, security_id_type, security_id):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		params = {
			"security_id_type" : security_id_type,
			"security_id" : security_id
		}
		v = AppValidatorFactory().get_validator("get_security_attribute")
		#-- validate input fields
		if not v.validate(params):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- get the first value from the dictionary and return
		security_attribute_l = self.security_attribute_services.query(params)
		security_attribute = {}
		if len(security_attribute_l) > 0:
			security_attribute = security_attribute_l[0]
		return security_attribute

	def add_security_attribute(self, security_attribute_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("add_security_attribute")
		if not v.validate(security_attribute_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no parsing need
		#-- create data model
		#-- reuse the security_attribute
		self.security_attribute_services.create(security_attribute_info)
		return 0

	def update_security_attribute(self, security_attribute_info):
		if self.dbmode is None:
			raise DataStoreNotYetInitializeError("Plase call initializeDatastore to initialize datastore")
		v = AppValidatorFactory().get_validator("update_security_attribute")
		#-- validate input fields
		if not v.validate(security_attribute_info):
			message = "Input validation error. Details: " + str(v.errors)
			self.logger.error(message)
			raise ValueError(message)
		#-- data parsing
		#-- no parsing need
		#-- create data model
		#-- reuse the counter_party_info
		self.security_attribute_services.update(security_attribute_info)
		return 0