# coding=utf-8
# 
import logging
from security_data.constants import Constants
from security_data.controllers import AppController

#controller supposed to be stateless so it is safe to have a singleton , one for all users 
controller = AppController()

def initialize_datastore(mode):
	"""
	[String] mode ('production' means produciton mode, test mode otherwise)

	side effect: initialize the underlying data store in test or production
	mode.
	"""
	return controller.initialize_datastore(mode)
	


def clear_security_data():
	"""
	Clears all the data in the factset tables including: 
	security_base, futures, fixed_incomes

	Throws NoDataClearingInProuctionModeError if the underlying datastore is
	in production mode.
	"""
	return controller.clear_security_data()



def get_security_basic_info(geneva_investment_id):
	"""
	[String] Geneva investment id => [Dictionary] security info
	"""
	return controller.get_security_basic_info(geneva_investment_id)



def add_security_basic_info(security_info):
	"""
	[Dictionary] security info

	Side effect: add security info to datastore

	Throws: SecurityInfoAlreadyExistError
	"""
	return controller.add_security_basic_info(security_info)



def update_security_basic_info(security_info):
	"""
	[Dictionary] security info

	Side effect: update the security info to datastore

	Throws: SecurityInfoNotExistError
	"""
	return controller.update_security_basic_info(security_info)



def get_futures_info(ticker):
	"""
	[String] Ticker => [Dictionary] security info
	"""
	return controller.get_futures_info(ticker)



def add_futures_info(security_info):
	"""
	[Dictionary] security info

	Side effect: add security info to datastore

	Throws: SecurityInfoAlreadyExistError
	"""
	return controller.add_futures_info(security_info)



def update_futures_info(security_info):
	"""
	[Dictionary] security info

	Side effect: update the security info to datastore

	Throws: SecurityInfoNotExistError
	"""
	return controller.update_futures_info(security_info)

	

def get_fixed_deposit_info(geneva_id):
	"""
	[String] geneva_id => [Dictionary] security info
	"""
	return controller.get_fixed_deposit_info(geneva_id)



def add_fixed_deposit_info(security_info):
	"""
	[Dictionary] security info

	Side effect: add security info to datastore

	Throws: SecurityInfoAlreadyExistError
	"""
	return controller.add_fixed_deposit_info(security_info)



def update_fixed_deposit_info(security_info):
	"""
	[Dictionary] security info

	Side effect: update the security info to datastore

	Throws: SecurityInfoNotExistError
	"""
	return controller.update_fixed_deposit_info(security_info)