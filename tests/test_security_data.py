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
							update_fixed_deposit_info,
							get_fx_forward_info, 
							add_fx_forward_info,
							update_fx_forward_info,
							get_all_counter_party_info, 
							add_counter_party_info,
							update_counter_party_info,
							get_security_attribute, 
							add_security_attribute,
							update_security_attribute)
from security_data.models.security_base import SecurityBase
from security_data.models.futures import Futures
from security_data.models.fixed_deposit import FixedDeposit
from security_data.models.fx_forward import FxForward
from security_data.models.otc_counter_party import OtcCounterParty
from security_data.models.security_attribute import SecurityAttribute
from security_data.utils.database import DBConn
from security_data.utils.error_handling import (NoDataClearingInProuctionModeError,
                                            SecurityBaseAlreadyExistError,
                                            SecurityBaseNotExistError,
                                            FuturesAlreadyExistError,
                                            FuturesNotExistError,
                                            FixedDepositAlreadyExistError,
                                            FixedDepositNotExistError,
                                            FxForwardAlreadyExistError,
                                            FxForwardNotExistError,
                                            OtcCounterPartyAlreadyExistError,
                                            OtcCounterPartyNotExistError,
                                            SecurityAttributeAlreadyExistError,
                                            SecurityAttributeNotExistError)
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
		self.assertEqual(0, session.query(func.count(FxForward.id)).scalar())
		self.assertEqual(0, session.query(func.count(OtcCounterParty.id)).scalar())
		self.assertEqual(0, session.query(func.count(SecurityAttribute.id)).scalar())

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
		#-- 3. test missing value in the field geneva_id
		#--    when adding fixed deposit
		#-- 3.1 empty geneva_id
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
		#-- 4. test adding fx forward with same counter party
		#--    The system shall allow and skip the duplicated counter party error
		security_info = self._get_test_fixed_deposit2()
		self.assertEqual(add_fixed_deposit_info(security_info), 0)
		count = -1
		#--    verify and suppose only 1 counter party exist
		with DBConn.get_db(self.unittest_dbmode).connect() as con:
			count = con.execute("""
								SELECT count(*)  
								FROM otc_counter_parties
								""").scalar()
			con.close()
		self.assertEqual(count, 1)

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

	#-- testcase for fx forward
	def test_add_fx_forward_info(self):
		#-- 1. normal creation
		security_info = self._get_test_fx_forward()
		self.assertEqual(add_fx_forward_info(security_info), 0)
		#-- 2. test duplicated future insert raise FxForwardAlreadyExistError
		security_info = self._get_test_fx_forward()
		with self.assertRaises(FxForwardAlreadyExistError):
			add_fx_forward_info(security_info)
		#-- 3. test missing value in the field factset_id
		#--    when adding fx forward
		#-- 3.1 empty factset_id
		security_info = self._get_test_fx_forward()
		security_info["factset_id"] = ""
		with self.assertRaises(ValueError):
			add_fx_forward_info(security_info)
		#-- 3.2 missing factset_id
		security_info = {
			"geneva_fx_forward_name" : "CNH per USD @ 6.55 NOMURA - 07/28/2021 40017",
			"geneva_counter_party" : "INST-FI",
			"starting_date" : "2021-04-21",
			"maturity_date" : "2021-05-17",
			"base_currency" : "USD",
			"base_currency_quantity" : 348241.37,
			"term_currency" : "CNH",
			"term_currency_quantity" : 2350000.00,
			"forward_rate" : 6.6051
		}
		with self.assertRaises(ValueError):
			add_fx_forward_info(security_info)
		#-- 3.2 missing an attribute such as geneva_counter_party
		security_info = {
			"factset_id" : "FXForward_1163847",
			"geneva_fx_forward_name" : "CNH per USD @ 6.55 NOMURA - 07/28/2021 40017",
			"starting_date" : "2021-04-21",
			"maturity_date" : "2021-05-17",
			"base_currency" : "USD",
			"base_currency_quantity" : 348241.37,
			"term_currency" : "CNH",
			"term_currency_quantity" : 2350000.00,
			"forward_rate" : 6.6051
		}
		#-- 3.2 empty attribute such as geneva_counter_party
		security_info = self._get_test_fx_forward()
		security_info["geneva_counter_party"] = ""
		with self.assertRaises(ValueError):
			add_fx_forward_info(security_info)
		#-- 4. test adding fx forward with same counter party
		#--    The system shall allow and skip the duplicated counter party error
		security_info = self._get_test_fx_forward3()
		self.assertEqual(add_fx_forward_info(security_info), 0)
		#--    verify and suppose only 1 counter party exist
		count = -1
		with DBConn.get_db(self.unittest_dbmode).connect() as con:
			count = con.execute("""
								SELECT count(*)  
								FROM otc_counter_parties
								""").scalar()
			con.close()
		self.assertEqual(count, 1)

	def test_get_fx_forward_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_fx_forward()
		add_fx_forward_info(security_info)
		security_info = self._get_test_fx_forward2()
		add_fx_forward_info(security_info)
		security_info = self._get_test_fx_forward3()
		add_fx_forward_info(security_info)
		#-- 1. normal get by geneva_id and verify the result
		d = get_fx_forward_info("FXForward_000003")
		self.assertEqual(d["factset_id"], "FXForward_000003")
		self.assertEqual(d["geneva_fx_forward_name"], "CNH per USD @ 5.01 Testing")
		self.assertEqual(d["geneva_counter_party"],  "INST-FI")
		self.assertEqual(d["starting_date"],  "2020-04-21")
		self.assertEqual(d["maturity_date"], "2020-05-17")
		self.assertEqual(d["base_currency"], "USD")
		self.assertEqual(d["base_currency_quantity"], 500000.37)
		self.assertEqual(d["term_currency"], "CNH")
		self.assertEqual(d["term_currency_quantity"], 6000000.01)
		self.assertEqual(d["forward_rate"], 5.01)
		#-- 2. no result return
		self.assertEqual(get_fx_forward_info("FXForward_000004"), {})
		#-- 3. missing input
		with self.assertRaises(ValueError):
			get_fx_forward_info("")

	def test_update_fx_forward_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_fx_forward()
		add_fx_forward_info(security_info)
		security_info = self._get_test_fx_forward2()
		add_fx_forward_info(security_info)
		#-- 1. normal update succeeded
		security_info = {
			"factset_id" : "FXForward_1163847",
			"starting_date" : "2022-04-21",
			"maturity_date" : "2022-05-17",
			"base_currency" : "USDD",
			"base_currency_quantity" : 348241.373,
			"term_currency" : "CNHH",
			"term_currency_quantity" : 2350000.001,
			"forward_rate" : 6.60511
		}
		self.assertEqual(update_fx_forward_info(security_info), 0)
		d = get_fx_forward_info("FXForward_1163847")
		#-- verify only the updated fields get updated
		self.assertEqual(d["factset_id"], "FXForward_1163847")
		self.assertEqual(d["starting_date"], "2022-04-21")
		self.assertEqual(d["maturity_date"], "2022-05-17")
		self.assertEqual(d["base_currency"], "USDD")
		self.assertEqual(d["base_currency_quantity"], 348241.373)
		self.assertEqual(d["term_currency"], "CNHH")
		self.assertEqual(d["term_currency_quantity"], 2350000.001)
		self.assertEqual(d["forward_rate"], 6.60511)
		#-- 2. test invalid input 
		#-- 2.1 string vlaue for forward_rate
		security_info = {
			"factset_id" :"FXForward_1163847",
			"forward_rate" : "wrong input"
		}
		with self.assertRaises(ValueError):
			update_fx_forward_info(security_info)
		#-- 2.2 factset_id not exist
		security_info = {
			"factset_id" :"unknown factset_id",
			"forward_rate" : 10.11
		}
		with self.assertRaises(FxForwardNotExistError):
			update_fx_forward_info(security_info)
		#-- 2.3 submit empty update field
		security_info = {
			"factset_id" : "unknown factset_id",
			"geneva_fx_forward_name" : ""
		}
		with self.assertRaises(ValueError):
			update_fx_forward_info(security_info)

	def _get_test_fx_forward(self):
		security_info = {
			"factset_id" : "FXForward_1163847",
			"geneva_fx_forward_name" : "CNH per USD @ 6.55 NOMURA - 07/28/2021 40017",
			"geneva_counter_party" : "INST-FI",
			"starting_date" : "2021-04-21",
			"maturity_date" : "2021-05-17",
			"base_currency" : "USD",
			"base_currency_quantity" : 348241.37,
			"term_currency" : "CNH",
			"term_currency_quantity" : 2350000.00,
			"forward_rate" : 6.6051
		}
		return security_info
		
	def _get_test_fx_forward2(self):
		security_info = {
			"factset_id" : "FXForward_000002",
			"geneva_fx_forward_name" : "CNH per USD @ 5.01 Testing",
			"geneva_counter_party" : "diff-counter-party",
			"starting_date" : "2020-04-21",
			"maturity_date" : "2020-05-17",
			"base_currency" : "USD",
			"base_currency_quantity" : 500000.37,
			"term_currency" : "CNH",
			"term_currency_quantity" : 6000000.01,
			"forward_rate" : 5.01
		}
		return security_info
		
	def _get_test_fx_forward3(self):
		security_info = {
			"factset_id" : "FXForward_000003",
			"geneva_fx_forward_name" : "CNH per USD @ 5.01 Testing",
			"geneva_counter_party" : "INST-FI",
			"starting_date" : "2020-04-21",
			"maturity_date" : "2020-05-17",
			"base_currency" : "USD",
			"base_currency_quantity" : 500000.37,
			"term_currency" : "CNH",
			"term_currency_quantity" : 6000000.01,
			"forward_rate" : 5.01
		}
		return security_info

	#-- testcase for otc counter party
	def test_add_counter_party_info(self):
		#-- 1. normal creation
		security_info = self._get_test_counter_party()
		self.assertEqual(add_counter_party_info(security_info), 0)
		#-- 2. test duplicated future insert raise FxForwardAlreadyExistError
		security_info = self._get_test_counter_party()
		with self.assertRaises(OtcCounterPartyAlreadyExistError):
			add_counter_party_info(security_info)
		#-- 3. test missing value in the field factset_id
		#--    when adding fx forward
		#-- 3.1 empty geneva_party_type
		security_info = self._get_test_counter_party()
		security_info["geneva_party_type"] = ""
		with self.assertRaises(ValueError):
			add_counter_party_info(security_info)
		#-- 3.2 missing geneva_counter_party
		security_info = {
			"geneva_party_type" : "Repo",
			"geneva_party_name" : "Industrial Bank of China",
			"bloomberg_ticker" : "601166 CH"
		}
		with self.assertRaises(ValueError):
			add_counter_party_info(security_info)
		#-- 3.3 empty an attribute such as geneva_party_name
		security_info = {
			"geneva_counter_party" : "BNP-REPO",
			"geneva_party_type" : "Repo",
			"geneva_party_name" : "",
			"bloomberg_ticker" : "testing ticker"
		}

	def test_get_all_counter_party_info(self):
		#-- preparation by adding 2 securities
		#-- 1. no result return
		self.assertEqual(get_all_counter_party_info(), [])
		security_info = self._get_test_counter_party()
		add_counter_party_info(security_info)
		security_info = self._get_test_counter_party2()
		add_counter_party_info(security_info)
		#-- 2. normal get all counter party and check result
		d = get_all_counter_party_info()
		self.assertEqual(d[0]["geneva_counter_party"], "BNP-REPO")
		self.assertEqual(d[0]["geneva_party_type"], "Repo")
		self.assertEqual(d[0]["geneva_party_name"], "Industrial Bank of China")
		self.assertEqual(d[0]["bloomberg_ticker"], "601166 CH")
		self.assertEqual(d[1]["geneva_counter_party"], "INST-FI")
		self.assertEqual(d[1]["geneva_party_type"], "Fixed Deposit")
		self.assertEqual(d[1]["geneva_party_name"], "test geneva_party_name")
		self.assertEqual(d[1]["bloomberg_ticker"], "test bloomberg_ticker")

	def test_update_counter_party_info(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_counter_party()
		add_counter_party_info(security_info)
		security_info = self._get_test_counter_party2()
		add_counter_party_info(security_info)
		#-- 1. normal update succeeded
		security_info = {
			"geneva_counter_party" : "INST-FI",
			"geneva_party_type" : "Fixed Deposit",
			"geneva_party_name" : "testing 1",
			"bloomberg_ticker" : "testing 2"
		}
		self.assertEqual(update_counter_party_info(security_info), 0)
		d = get_all_counter_party_info()
		#-- verify only the updated fields get updated
		self.assertEqual(d[1]["geneva_counter_party"], "INST-FI")
		self.assertEqual(d[1]["geneva_party_type"], "Fixed Deposit")
		self.assertEqual(d[1]["geneva_party_name"], "testing 1")
		self.assertEqual(d[1]["bloomberg_ticker"], "testing 2")
		#-- 2. test invalid input 
		#-- 2.1 geneva_party_type not match
		security_info = {
			"geneva_counter_party" :"INST-FI",
			"geneva_party_type" : "Repo",
			"geneva_party_name" : "testing 123"
		}
		with self.assertRaises(OtcCounterPartyNotExistError):
			update_counter_party_info(security_info)
		#-- 2.2 geneva_party_type not exist
		security_info = {
			"geneva_counter_party" :"unknown",
			"geneva_party_type" : "Repo",
			"geneva_party_name" : "testing 123"
		}
		with self.assertRaises(OtcCounterPartyNotExistError):
			update_counter_party_info(security_info)

	def _get_test_counter_party(self):
		security_info = {
			"geneva_counter_party" : "BNP-REPO",
			"geneva_party_type" : "Repo",
			"geneva_party_name" : "Industrial Bank of China",
			"bloomberg_ticker" : "601166 CH"
		}
		return security_info
		
	def _get_test_counter_party2(self):
		security_info = {
			"geneva_counter_party" : "INST-FI",
			"geneva_party_type" : "Fixed Deposit",
			"geneva_party_name" : "test geneva_party_name",
			"bloomberg_ticker" : "test bloomberg_ticker"
		}
		return security_info

	#-- testcase for security attribute
	def test_add_security_attribute(self):
		#-- 1. normal creation
		#-- 1.1. normal creation
		security_info = self._get_test_security_attribute()
		self.assertEqual(add_security_attribute(security_info), 0)
		#-- 1.2. only have the required attribute
		security_info = {
			"security_id_type" : "Bloomberg Id",
			"security_id" : "security_id test 1"
		}
		self.assertEqual(add_security_attribute(security_info), 0)
		#-- 1.2. only have the required attribute and some non-required attributes
		security_info = {
			"security_id_type" : "Ticker",
			"security_id" : "security_id test 2",
			"gics_sector" : "gics_sector test 2"
		}
		self.assertEqual(add_security_attribute(security_info), 0)
		#--    verify there are 3 security attribute
		count = -1
		with DBConn.get_db(self.unittest_dbmode).connect() as con:
			count = con.execute("""
								SELECT count(*)  
								FROM security_attributes
								""").scalar()
			con.close()
		self.assertEqual(count, 3)
		#-- 2. test duplicated future insert raise SecurityAttributeAlreadyExistError
		security_info = self._get_test_security_attribute()
		with self.assertRaises(SecurityAttributeAlreadyExistError):
			add_security_attribute(security_info)
		#-- 3. test missing value in the field security_id
		#--    when adding Security Attribute
		#-- 3.1 empty security_id
		security_info = self._get_test_security_attribute()
		security_info["security_id"] = ""
		with self.assertRaises(ValueError):
			add_security_attribute(security_info)
		#-- 3.1 empty security_type_id
		security_info = self._get_test_security_attribute()
		security_info["security_type_id"] = ""
		with self.assertRaises(ValueError):
			add_security_attribute(security_info)
		#-- 3.2 missing security_type_id
		security_info = {
			"security_id" : "Test 1",
			"trading_volume_90_days" : 1000.00
		}
		with self.assertRaises(ValueError):
			add_security_attribute(security_info)
		#-- 3.3 unknown security_type_id
		security_info = {
			"security_type_id" : "Unknown Type",
			"security_id" : "security_id Test 2",
			"trading_volume_90_days" : 10000000.00
		}
		with self.assertRaises(ValueError):
			add_security_attribute(security_info)

	def test_get_security_attribute(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_security_attribute()
		add_security_attribute(security_info)
		security_info = self._get_test_security_attribute2()
		add_security_attribute(security_info)
		#-- 1. normal get by geneva_id and verify the result
		d = get_security_attribute("ISIN", "XS1936784161")
		self.assertEqual(d["security_id_type"], "ISIN")
		self.assertEqual(d["security_id"], "XS1936784161")
		self.assertEqual(d["gics_sector"], "Financials")
		self.assertEqual(d["gics_industry_group"], "Banks")
		self.assertEqual(d["industry_sector"], "Financial")
		self.assertEqual(d["industry_group"], "Banks")
		self.assertEqual(d["bics_sector_level_1"], "Financial")
		self.assertEqual(d["bics_industry_group_level_2"], "Banks")
		self.assertEqual(d["bics_industry_name_level_3"], "")
		self.assertEqual(d["bics_sub_industry_name_level_4"], "")
		self.assertEqual(d["parent_symbol"], "CEHIOZ CH")
		self.assertEqual(d["parent_symbol_chinese_name"], "中央匯金投資有限責任公司")
		self.assertEqual(d["parent_symbol_industry_group"], "Investment Companies")
		self.assertEqual(d["cast_parent_company_name"], "China Construction Bank Corp")
		self.assertEqual(d["country_of_risk"], "CN")
		self.assertEqual(d["country_of_issuance"], "CN")
		self.assertEqual(d["sfc_region"], "China Mainland")
		self.assertEqual(d["s_p_issuer_rating"], "A")
		self.assertEqual(d["moody_s_issuer_rating"], "")
		self.assertEqual(d["fitch_s_issuer_rating"], "A")
		self.assertEqual(d["bond_or_equity_ticker"], "CCB")
		self.assertEqual(d["s_p_rating"], "BBB+")
		self.assertEqual(d["moody_s_rating"], "")
		self.assertEqual(d["fitch_rating"], "BBB+")
		self.assertEqual(d["payment_rank"], "Subordinated")
		self.assertEqual(d["payment_rank_mbs"], "")
		self.assertEqual(d["bond_classification"], "")
		self.assertEqual(d["local_government_lgfv"], "Beijing")
		self.assertEqual(d["first_year_default_probability"], 0.000172683)
		self.assertEqual(d["contingent_capital"], "")
		self.assertEqual(d["co_co_bond_trigger"], "")
		self.assertEqual(d["capit_type_conti_conv_tri_lvl"], "")
		self.assertEqual(d["tier_1_common_equity_ratio"], 0)
		self.assertEqual(d["bail_in_capital_indicator"], "")
		self.assertEqual(d["tlac_mrel_designation"], "")
		self.assertEqual(d["classif_on_chi_state_owned_enterp"], "Sovereign")
		self.assertEqual(d["private_placement_indicator"], "N")
		self.assertEqual(d["trading_volume_90_days"], 24634300)
		#-- 2. no result return
		self.assertEqual(get_security_attribute("ISIN", "wrong value"), {})
		#-- 3. missing input
		with self.assertRaises(ValueError):
			get_security_attribute("","")

	def test_update_security_attribute(self):
		#-- preparation by adding 2 securities
		security_info = self._get_test_security_attribute()
		add_security_attribute(security_info)
		security_info = self._get_test_security_attribute2()
		add_security_attribute(security_info)
		#-- 1. normal update succeeded
		security_info = {
			"security_id_type" : "Ticker",
			"security_id" : "Ticker Test 1",
			"gics_sector" : "Financials updated",
			"gics_industry_group" : "Banks updated",
			"industry_sector" : "Financial updated",
			"industry_group" : "Banks updated",
			"bics_sector_level_1" : "Financial updated",
			"bics_industry_group_level_2" : "Banks updated",
			"bics_industry_name_level_3" : " updated",
			"bics_sub_industry_name_level_4" : " updated",
			"parent_symbol" : "CEHIOZ CH updated",
			"parent_symbol_chinese_name" : "中央匯金投資有限責任公司 updated",
			"parent_symbol_industry_group" : "Investment Companies updated",
			"cast_parent_company_name" : "China Construction Bank Corp updated",
			"country_of_risk" : "CN updated",
			"country_of_issuance" : "CN updated",
			"sfc_region" : "China Mainland updated",
			"s_p_issuer_rating" : "A updated",
			"moody_s_issuer_rating" : " updated",
			"fitch_s_issuer_rating" : "A updated",
			"bond_or_equity_ticker" : "CCB updated",
			"s_p_rating" : "BBB+ updated",
			"moody_s_rating" : "updated",
			"fitch_rating" : "BBB+ updated",
			"payment_rank" : "Subordinated updated",
			"payment_rank_mbs" : "updated",
			"bond_classification" : "updated",
			"local_government_lgfv" : "Beijing updated",
			"first_year_default_probability" : 0.000000001,
			"contingent_capital" : "updated",
			"co_co_bond_trigger" : "updated",
			"capit_type_conti_conv_tri_lvl" : "updated",
			"tier_1_common_equity_ratio" : 0.30,
			"bail_in_capital_indicator" : "updated",
			"tlac_mrel_designation" : "updated",
			"classif_on_chi_state_owned_enterp" : "Sovereign updated",
			"private_placement_indicator" : "Y",
			"trading_volume_90_days" : 100000000
		}
		self.assertEqual(update_security_attribute(security_info), 0)
		d = get_security_attribute("Ticker", "Ticker Test 1")
		#-- verify only the updated fields get updated
		self.assertEqual(d["security_id_type"], "Ticker")
		self.assertEqual(d["security_id"], "Ticker Test 1")
		self.assertEqual(d["gics_sector"], "Financials updated")
		self.assertEqual(d["gics_industry_group"], "Banks updated")
		self.assertEqual(d["industry_sector"], "Financial updated")
		self.assertEqual(d["industry_group"], "Banks updated")
		self.assertEqual(d["bics_sector_level_1"], "Financial updated")
		self.assertEqual(d["bics_industry_group_level_2"], "Banks updated")
		self.assertEqual(d["bics_industry_name_level_3"], " updated")
		self.assertEqual(d["bics_sub_industry_name_level_4"], " updated")
		self.assertEqual(d["parent_symbol"], "CEHIOZ CH updated")
		self.assertEqual(d["parent_symbol_chinese_name"], "中央匯金投資有限責任公司 updated")
		self.assertEqual(d["parent_symbol_industry_group"], "Investment Companies updated")
		self.assertEqual(d["cast_parent_company_name"], "China Construction Bank Corp updated")
		self.assertEqual(d["country_of_risk"], "CN updated")
		self.assertEqual(d["country_of_issuance"], "CN updated")
		self.assertEqual(d["sfc_region"], "China Mainland updated")
		self.assertEqual(d["s_p_issuer_rating"], "A updated")
		self.assertEqual(d["moody_s_issuer_rating"], " updated")
		self.assertEqual(d["fitch_s_issuer_rating"], "A updated")
		self.assertEqual(d["bond_or_equity_ticker"], "CCB updated")
		self.assertEqual(d["s_p_rating"], "BBB+ updated")
		self.assertEqual(d["moody_s_rating"], "updated")
		self.assertEqual(d["fitch_rating"], "BBB+ updated")
		self.assertEqual(d["payment_rank"], "Subordinated updated")
		self.assertEqual(d["payment_rank_mbs"], "updated")
		self.assertEqual(d["bond_classification"], "updated")
		self.assertEqual(d["local_government_lgfv"], "Beijing updated")
		self.assertEqual(d["first_year_default_probability"], 0.000000001)
		self.assertEqual(d["contingent_capital"], "updated")
		self.assertEqual(d["co_co_bond_trigger"], "updated")
		self.assertEqual(d["capit_type_conti_conv_tri_lvl"], "updated")
		self.assertEqual(d["tier_1_common_equity_ratio"], 0.30)
		self.assertEqual(d["bail_in_capital_indicator"], "updated")
		self.assertEqual(d["tlac_mrel_designation"], "updated")
		self.assertEqual(d["classif_on_chi_state_owned_enterp"], "Sovereign updated")
		self.assertEqual(d["private_placement_indicator"], "Y")
		self.assertEqual(d["trading_volume_90_days"], 100000000)
		#-- 2. test invalid input 
		#-- 2.1 string vlaue for trading_volume_90_days
		security_info = {
			"security_id_type" : "Ticker",
			"security_id" : "Ticker Test 1",
			"trading_volume_90_days" : "wrong input"
		}
		with self.assertRaises(ValueError):
			update_security_attribute(security_info)
		#-- 2.2 security_id_type unknown type
		security_info = {
			"security_id_type" : "unknown ticker",
			"security_id" : "Ticker Test 1",
			"trading_volume_90_days" : 1.0
		}
		with self.assertRaises(ValueError):
			update_security_attribute(security_info)
		#-- 2.3 security_id does not exist
		security_info = {
			"security_id_type" : "Ticker",
			"security_id" : "Ticker Test XXX",
			"trading_volume_90_days" : 1.0
		}
		with self.assertRaises(SecurityAttributeNotExistError):
			update_security_attribute(security_info)

	def _get_test_security_attribute(self):
		security_info = {
			"security_id_type" : "ISIN",
			"security_id" : "XS1936784161",
			"gics_sector" : "Financials",
			"gics_industry_group" : "Banks",
			"industry_sector" : "Financial",
			"industry_group" : "Banks",
			"bics_sector_level_1" : "Financial",
			"bics_industry_group_level_2" : "Banks",
			"bics_industry_name_level_3" : "",
			"bics_sub_industry_name_level_4" : "",
			"parent_symbol" : "CEHIOZ CH",
			"parent_symbol_chinese_name" : "中央匯金投資有限責任公司",
			"parent_symbol_industry_group" : "Investment Companies",
			"cast_parent_company_name" : "China Construction Bank Corp",
			"country_of_risk" : "CN",
			"country_of_issuance" : "CN",
			"sfc_region" : "China Mainland",
			"s_p_issuer_rating" : "A",
			"moody_s_issuer_rating" : "",
			"fitch_s_issuer_rating" : "A",
			"bond_or_equity_ticker" : "CCB",
			"s_p_rating" : "BBB+",
			"moody_s_rating" : "",
			"fitch_rating" : "BBB+",
			"payment_rank" : "Subordinated",
			"payment_rank_mbs" : "",
			"bond_classification" : "",
			"local_government_lgfv" : "Beijing",
			"first_year_default_probability" : 0.000172683,
			"contingent_capital" : "",
			"co_co_bond_trigger" : "",
			"capit_type_conti_conv_tri_lvl" : "",
			"tier_1_common_equity_ratio" : 0,
			"bail_in_capital_indicator" : "",
			"tlac_mrel_designation" : "",
			"classif_on_chi_state_owned_enterp" : "Sovereign",
			"private_placement_indicator" : "N",
			"trading_volume_90_days" : 24634300
		}
		return security_info
		
	def _get_test_security_attribute2(self):
		security_info = {
			"security_id_type" : "Ticker",
			"security_id" : "Ticker Test 1",
			"gics_sector" : "",
			"gics_industry_group" : "Banks Test 1",
			"industry_sector" : "Financial",
			"industry_group" : "Banks",
			"bics_sector_level_1" : "Financial",
			"bics_industry_group_level_2" : "Banks",
			"bics_industry_name_level_3" : "",
			"bics_sub_industry_name_level_4" : "",
			"parent_symbol" : "CEHIOZ CH",
			"parent_symbol_chinese_name" : "中央匯金投資有限責任公司",
			"parent_symbol_industry_group" : "Investment Companies",
			"cast_parent_company_name" : "China Construction Bank Corp",
			"country_of_risk" : "CN",
			"country_of_issuance" : "CN",
			"sfc_region" : "China Mainland",
			"s_p_issuer_rating" : "A",
			"moody_s_issuer_rating" : "",
			"fitch_s_issuer_rating" : "A",
			"bond_or_equity_ticker" : "CCB",
			"s_p_rating" : "BBB+",
			"moody_s_rating" : "",
			"fitch_rating" : "BBB+",
			"payment_rank" : "Subordinated",
			"payment_rank_mbs" : "",
			"bond_classification" : "",
			"local_government_lgfv" : "Beijing",
			"first_year_default_probability" : 0.000000003,
			"contingent_capital" : "",
			"co_co_bond_trigger" : "",
			"capit_type_conti_conv_tri_lvl" : "",
			"tier_1_common_equity_ratio" : 0,
			"bail_in_capital_indicator" : "",
			"tlac_mrel_designation" : "",
			"classif_on_chi_state_owned_enterp" : "Sovereign",
			"private_placement_indicator" : "N",
			"trading_volume_90_days" : 24634300
		}
		return security_info