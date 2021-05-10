# # coding=utf-8
# # 

import logging
import logging.config
from datetime import datetime
from os.path import abspath, dirname, join
import unittest2
from security_data.constants import Constants
from security_data.data import (initialize_datastore,
							clear_security_data,
							get_security_basic_info, 
							add_security_basic_info,
							update_security_basic_info,
							get_futures_info, 
							add_futures_info,
							update_futures_info,
							get_fixed_deposit_info, 
							add_fixed_deposit_info,
							update_fixed_deposit_info)
from security_data.models.security_base import SecurityBase
from security_data.models.futures import Futures
from security_data.models.fixed_deposit import FixedDeposit
from security_data.utils.database import DBConn
from security_data.utils.error_handling import (NoDataClearingInProuctionModeError,
                                            SecurityBaseAlreadyExistError,
                                            SecurityBaseNotExistError,
                                            FuturesAlreadyExistError,
                                            FuturesNotExistError,
                                            FixedDepositAlreadyExistError,
                                            FixedDepositNotExistError)
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

getCurrentDirectory = lambda : \
	dirname(abspath(__file__))

class TestFactSetData(unittest2.TestCase):

	unittest_dbmode = Constants.DBMODE_UAT

	def __init__(self, *args, **kwargs):
		super(TestFactSetData, self).__init__(*args, **kwargs)

	def setUp(self):
		#-- when fileConfig is being called, it will remove all the loggers created
		#-- when importing AppControllers.py when importing file security_data
		#-- added disable_existing_loggers=False to prevent this
		logging.config.fileConfig( join(getCurrentDirectory(), "..", "logging_config.ini"),
									defaults={'date':datetime.now().date().strftime('%Y-%m-%d')},
									disable_existing_loggers=False
								)
		initialize_datastore("uat")
		clear_security_data()

	def test_initialize_datastore(self):
		#-- test run without error throw
		self.assertEqual(0, initialize_datastore("production"))
		#self.assertEqual(0, initialize_datastore("test"))
		self.assertEqual(0, initialize_datastore("uat"))

	def test_clear_security_data(self):
		#-- test if NoDataClearingInProuctionModeError raise under production mode
		initialize_datastore("production")
		with self.assertRaises(NoDataClearingInProuctionModeError):
			clear_security_data()
		initialize_datastore("uat")
		clear_security_data()
		session = sessionmaker(bind=DBConn.get_db(self.unittest_dbmode))()
		self.assertEqual(0, session.query(func.count(SecurityBase.id)).scalar())
		self.assertEqual(0, session.query(func.count(Futures.id)).scalar())
		self.assertEqual(0, session.query(func.count(FixedDeposit.id)).scalar())

	def test_add_security_basic_info(self):
		#-- 1. normal creation
		security_info = self._get_test_security_base()
		self.assertEqual(add_security_basic_info(security_info), 0)
		#-- 2. test duplicated security insert raise SecurityBaseAlreadyExistError
		security_info = self._get_test_security_base()
		with self.assertRaises(SecurityBaseAlreadyExistError):
			add_security_basic_info(security_info)
		#-- 3. test missing value in the field Geneva Id, Geneva Asset Type, Geneva Investment Type
		#--    when adding security base
		#-- 3.1 missing Geneva Id
		security_info = self._get_test_security_base()
		security_info["geneva_id"] = ""
		with self.assertRaises(ValueError):
			add_security_basic_info(security_info)
		#-- 3.2 missing Geneva Asset Type
		security_info = self._get_test_security_base()
		security_info["geneva_asset_type"] = ""
		with self.assertRaises(ValueError):
			add_security_basic_info(security_info)
		#-- 3.1 missing Geneva Investment Type
		security_info = self._get_test_security_base()
		security_info["geneva_investment_type"] = ""
		with self.assertRaises(ValueError):
			add_security_basic_info(security_info)
		#-- 3.1 all field are required and non-empty, use description as sample
		security_info = self._get_test_security_base()
		security_info["description"] = ""
		with self.assertRaises(ValueError):
			add_security_basic_info(security_info)

	def test_get_security_basic_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_security_base()
		add_security_basic_info(security_info)
		security_info = self._get_test_security_base2()
		add_security_basic_info(security_info)
		#-- 1. normal get by geneva_id and verify the result
		d = get_security_basic_info("701 HK")
		self.assertEqual(d["geneva_id"], "701 HK")
		self.assertEqual(d["geneva_asset_type"], "Equities")
		self.assertEqual(d["geneva_investment_type"], "Common Stock")
		self.assertEqual(d["ticker"], "701 HK Equity")
		self.assertEqual(d["isin"], "BMG2237T1009")
		self.assertEqual(d["bloomberg_id"], "BBG12345678")
		self.assertEqual(d["sedol"], "TEST123")
		self.assertEqual(d["currency"], "HKD")
		self.assertEqual(d["is_private"], "N")
		self.assertEqual(d["description"], "CNT Group Limited 中文")
		self.assertEqual(d["exchange_name"], "HKEX")
		#-- 2. no result return
		self.assertEqual(get_security_basic_info("702 HK"), {})
		#-- 3. missing input
		with self.assertRaises(ValueError):
			get_security_basic_info("")

	def test_update_security_basic_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_security_base()
		add_security_basic_info(security_info)
		security_info = self._get_test_security_base2()
		add_security_basic_info(security_info)
		#-- 1. normal update succeeded
		security_info = {
			"geneva_id" : "700 HK",
			"isin" : "XS1234567890",
			"is_private" : "Y"
		}
		self.assertEqual(update_security_basic_info(security_info), 0)
		d = get_security_basic_info("700 HK")
		#-- verify only the updated fields get updated
		self.assertEqual(d["geneva_id"], "700 HK")
		self.assertEqual(d["geneva_asset_type"], "Equities")
		self.assertEqual(d["geneva_investment_type"], "Common Stock")
		self.assertEqual(d["ticker"], "700 HK Equity")
		self.assertEqual(d["isin"], "XS1234567890")
		self.assertEqual(d["bloomberg_id"], "BBG000BJ35N5")
		self.assertEqual(d["sedol"], "BMMV2K8")
		self.assertEqual(d["currency"], "HKD")
		self.assertEqual(d["is_private"], "Y")
		self.assertEqual(d["description"], "Tencent Holdings 中文")
		self.assertEqual(d["exchange_name"], "HKEX")
		#-- 2. test invalid input 
		#-- 2.1 is_private value
		security_info = {
			"geneva_id" : "700 HK",
			"is_private" : "XXX"
		}
		with self.assertRaises(ValueError):
			update_security_basic_info(security_info)
		#-- 2.2 geneva_id not exist
		security_info = {
			"geneva_id" : "700 HKXX",
			"is_private" : "Y"
		}
		with self.assertRaises(SecurityBaseNotExistError):
			update_security_basic_info(security_info)
		#-- 2.3 submit empty update field
		security_info = {
			"geneva_id" : "700 HK",
			"description" : ""
		}
		with self.assertRaises(ValueError):
			update_security_basic_info(security_info)

	def _get_test_security_base(self):
		security_info = {
			"geneva_id" : "700 HK",
			"geneva_asset_type" : "Equities",
			"geneva_investment_type" : "Common Stock",
			"ticker" : "700 HK Equity",
			"isin" : "KYG875721634",
			"bloomberg_id" : "BBG000BJ35N5",
			"sedol" : "BMMV2K8",
			"currency" : "HKD",
			"is_private" : "N",
			"description" : "Tencent Holdings 中文",
			"exchange_name" : "HKEX"
		}
		return security_info
		
	def _get_test_security_base2(self):
		security_info = {
			"geneva_id" : "701 HK",
			"geneva_asset_type" : "Equities",
			"geneva_investment_type" : "Common Stock",
			"ticker" : "701 HK Equity",
			"isin" : "BMG2237T1009",
			"bloomberg_id" : "BBG12345678",
			"sedol" : "TEST123",
			"currency" : "HKD",
			"is_private" : "N",
			"description" : "CNT Group Limited 中文",
			"exchange_name" : "HKEX"
		}
		return security_info

	#-- testcase for futures
	def test_add_futures_info(self):
		#-- 1. normal creation
		security_info = self._get_test_futures()
		self.assertEqual(add_futures_info(security_info), 0)
		#-- 2. test duplicated future insert raise FuturesAlreadyExistError
		security_info = self._get_test_futures()
		with self.assertRaises(FuturesAlreadyExistError):
			add_futures_info(security_info)
		#-- 3. test missing value in the field ticker
		#--    when adding security base
		#-- 3.1 empty ticker
		security_info = self._get_test_futures()
		security_info["ticker"] = ""
		with self.assertRaises(ValueError):
			add_futures_info(security_info)
		#-- 3.2 missing ticker
		security_info = {
			"underlying_id" : "US 10yr 6%",
			"contract_size" : "100000",
			"value_of_1pt" : "1000"
		}
		with self.assertRaises(ValueError):
			add_futures_info(security_info)
		#-- 3.2 missing an attribute such as underlying_id
		security_info = {
			"ticker" : "TYM1 Comdty",
			"contract_size" : "100000",
			"value_of_1pt" : "1000"
		}
		#-- 3.2 empty attribute such as value_of_1pt
		security_info = self._get_test_futures()
		security_info["value_of_1pt"] = ""
		with self.assertRaises(ValueError):
			add_futures_info(security_info)

	def test_get_futures_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_futures()
		add_futures_info(security_info)
		security_info = self._get_test_futures2()
		add_futures_info(security_info)
		#-- 1. normal get by geneva_id and verify the result
		d = get_futures_info("TYM1 Comdty 2")
		self.assertEqual(d["ticker"], "TYM1 Comdty 2")
		self.assertEqual(d["underlying_id"], "US 10yr 6.5%")
		self.assertEqual(d["contract_size"], 200000)
		self.assertEqual(d["value_of_1pt"], 2000)
		#-- 2. no result return
		self.assertEqual(get_futures_info("TYM1 Comdty 3"), {})
		#-- 3. missing input
		with self.assertRaises(ValueError):
			get_futures_info("")

	def test_update_futures_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_futures()
		add_futures_info(security_info)
		security_info = self._get_test_futures2()
		add_futures_info(security_info)
		#-- 1. normal update succeeded
		security_info = {
			"ticker" : "TYM1 Comdty",
			"underlying_id" : "testing 123",
			"contract_size" : 400000.1,
			"value_of_1pt" : 10.15
		}
		self.assertEqual(update_futures_info(security_info), 0)
		d = get_futures_info("TYM1 Comdty")
		#-- verify only the updated fields get updated
		self.assertEqual(d["ticker"], "TYM1 Comdty")
		self.assertEqual(d["underlying_id"], "testing 123")
		self.assertEqual(d["contract_size"], 400000.1)
		self.assertEqual(d["value_of_1pt"], 10.15)
		#-- 2. test invalid input 
		#-- 2.1 string vlaue for contract_size
		security_info = {
			"ticker" : "TYM1 Comdty",
			"contract_size" : "wrong input"
		}
		with self.assertRaises(ValueError):
			update_futures_info(security_info)
		#-- 2.2 ticker not exist
		security_info = {
			"ticker" : "TYM1 Comdty Not Exist",
			"contract_size" : 10000
		}
		with self.assertRaises(FuturesNotExistError):
			update_futures_info(security_info)
		#-- 2.3 submit empty update field
		security_info = {
			"ticker" : "TYM1 Comdty",
			"underlying_id" : ""
		}
		with self.assertRaises(ValueError):
			update_futures_info(security_info)

	def _get_test_futures(self):
		security_info = {
			"ticker" : "TYM1 Comdty",
			"underlying_id" : "US 10yr 6%",
			"contract_size" : "100000",
			"value_of_1pt" : "1000"
		}
		return security_info
		
	def _get_test_futures2(self):
		security_info = {
			"ticker" : "TYM1 Comdty 2",
			"underlying_id" : "US 10yr 6.5%",
			"contract_size" : "200000",
			"value_of_1pt" : "2000"
		}
		return security_info

	#-- testcase for fixed deposit
	def test_add_fixed_deposit_info(self):
		#-- 1. normal creation
		security_info = self._get_test_fixed_deposit()
		self.assertEqual(add_fixed_deposit_info(security_info), 0)
		#-- 2. test duplicated future insert raise FixedDepositAlreadyExistError
		security_info = self._get_test_fixed_deposit()
		with self.assertRaises(FixedDepositAlreadyExistError):
			add_fixed_deposit_info(security_info)
		#-- 3. test missing value in the field ticker
		#--    when adding security base
		#-- 3.1 empty ticker
		security_info = self._get_test_fixed_deposit()
		security_info["geneva_id"] = ""
		with self.assertRaises(ValueError):
			add_fixed_deposit_info(security_info)
		#-- 3.2 missing geneva_id
		security_info = {
			"factset_id" : "IB_Fixed_Deposit_0_pt_651_07082021",
			"geneva_counter_party" : "IB",
			"starting_date" : "2021-01-08",
			"maturity_date" : "2021-07-08",
			"interest_rate" : 0.75
		}
		with self.assertRaises(ValueError):
			add_fixed_deposit_info(security_info)
		#-- 3.2 missing an attribute such as factset_id
		security_info = {
			"geneva_id" : "IB Fixed Deposit 0.651 07/08/2021",
			"geneva_counter_party" : "IB",
			"starting_date" : "2021-01-08",
			"maturity_date" : "2021-07-08",
			"interest_rate" : 0.75
		}
		#-- 3.2 empty attribute such as geneva_counter_party
		security_info = self._get_test_fixed_deposit()
		security_info["geneva_counter_party"] = ""
		with self.assertRaises(ValueError):
			add_fixed_deposit_info(security_info)

	def test_get_fixed_deposit_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_fixed_deposit()
		add_fixed_deposit_info(security_info)
		security_info = self._get_test_fixed_deposit2()
		add_fixed_deposit_info(security_info)
		#-- 1. normal get by geneva_id and verify the result
		d = get_fixed_deposit_info("IB Fixed Deposit 0.651 07/08/2021")
		self.assertEqual(d["geneva_id"], "IB Fixed Deposit 0.651 07/08/2021")
		self.assertEqual(d["factset_id"], "IB_Fixed_Deposit_0_pt_651_07082021")
		self.assertEqual(d["geneva_counter_party"],  "IB")
		self.assertEqual(d["starting_date"],  "2021-01-08")
		self.assertEqual(d["maturity_date"], "2021-07-08")
		self.assertEqual(d["interest_rate"], 0.75)
		#-- 2. no result return
		self.assertEqual(get_fixed_deposit_info("TYM1 Comdty 3"), {})
		#-- 3. missing input
		with self.assertRaises(ValueError):
			get_fixed_deposit_info("")

	def test_update_fixed_deposit_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_fixed_deposit()
		add_fixed_deposit_info(security_info)
		security_info = self._get_test_fixed_deposit2()
		add_fixed_deposit_info(security_info)
		#-- 1. normal update succeeded
		security_info = {
			"geneva_id" : "IB Fixed Deposit 0.555 01/01/2021",
			"factset_id" : "test1",
			"geneva_counter_party" : "test2",
			"starting_date" : "2021-03-01",
			"maturity_date" : "2021-03-31",
			"interest_rate" : 0.111
		}
		self.assertEqual(update_fixed_deposit_info(security_info), 0)
		d = get_fixed_deposit_info("IB Fixed Deposit 0.555 01/01/2021")
		#-- verify only the updated fields get updated
		self.assertEqual(d["geneva_id"], "IB Fixed Deposit 0.555 01/01/2021")
		self.assertEqual(d["factset_id"], "test1")
		self.assertEqual(d["geneva_counter_party"], "test2")
		self.assertEqual(d["starting_date"], "2021-03-01")
		self.assertEqual(d["maturity_date"], "2021-03-31")
		self.assertEqual(d["interest_rate"], 0.111)
		#-- 2. test invalid input 
		#-- 2.1 string vlaue for interest_rate
		security_info = {
			"geneva_id" :"IB Fixed Deposit 0.555 01/01/2021",
			"interest_rate" : "wrong input"
		}
		with self.assertRaises(ValueError):
			update_fixed_deposit_info(security_info)
		#-- 2.2 geneva_id not exist
		security_info = {
			"geneva_id" :"unknown ticker",
			"interest_rate" : 10.11
		}
		with self.assertRaises(FixedDepositNotExistError):
			update_fixed_deposit_info(security_info)
		#-- 2.3 submit empty update field
		security_info = {
			"ticker" : "IB Fixed Deposit 0.555 01/01/2021",
			"factset_id" : ""
		}
		with self.assertRaises(ValueError):
			update_fixed_deposit_info(security_info)

	def _get_test_fixed_deposit(self):
		security_info = {
			"geneva_id" : "IB Fixed Deposit 0.651 07/08/2021",
			"factset_id" : "IB_Fixed_Deposit_0_pt_651_07082021",
			"geneva_counter_party" : "IB",
			"starting_date" : "2021-01-08",
			"maturity_date" : "2021-07-08",
			"interest_rate" : 0.75
		}
		return security_info
		
	def _get_test_fixed_deposit2(self):
		security_info = {
			"geneva_id" : "IB Fixed Deposit 0.555 01/01/2021",
			"factset_id" : "IB_Fixed_Deposit_0_pt_555_01012021",
			"geneva_counter_party" : "IB",
			"starting_date" : "2021-01-01",
			"maturity_date" : "2021-01-31",
			"interest_rate" : 0.951
		}
		return security_info