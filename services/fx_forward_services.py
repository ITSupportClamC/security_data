# coding=utf-8
# 
import logging
from sqlalchemy.orm import sessionmaker
from security_data.constants import Constants
from security_data.utils.error_handling import (FxForwardAlreadyExistError,
											FxForwardNotExistError,
											OtcCounterPartyAlreadyExistError)
from security_data.models.fx_forward import FxForward

class FxForwardServices:

	def __init__(self, db, otc_counter_party_services):
		self.logger = logging.getLogger(__name__)
		self.db = db
		self.otc_counter_party_services = otc_counter_party_services

	def delete_all(self):
		try:
			session = sessionmaker(bind=self.db)()
			session.query(FxForward).delete()
			session.commit()
		except Exception as e:
			self.logger.error("Failed to delete all records in FxForward")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def create(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			has_record = bool(session.query(FxForward).filter_by(factset_id=security_info['factset_id']).first())
			if has_record:
				message = "Record " + security_info['factset_id'] + " already exists"
				self.logger.warn(message)
				raise FxForwardAlreadyExistError(message)
			else:
				fx_forward = FxForward(**security_info)
				session.add(fx_forward)
				#-- add the otc counter party
				try:
					otc_counter_party_info = {
						"geneva_counter_party" : security_info['geneva_counter_party'],
						"geneva_party_type" : Constants.COUNTER_PARTY_SECURITY_TYPE_FX_FORWARD
					}
					otc_counter_party = self.otc_counter_party_services.create(otc_counter_party_info, session)
				except OtcCounterPartyAlreadyExistError:
					#-- Skip the error in case the OTC Counter Party already exist
					#-- Other error trigger throwing exception and no commit
					self.logger.warn("Record (" + security_info['geneva_counter_party'] + "," + \
						Constants.COUNTER_PARTY_SECURITY_TYPE_FX_FORWARD + ") already exists. Skip adding.")
				session.commit()
				self.logger.info("Record " + security_info['factset_id'] + " added successfully")
		except FxForwardAlreadyExistError:
			#-- avoid FxForwardAlreadyExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to add FxForward")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def update(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			fx_forward_to_update = session.query(FxForward) \
								.filter_by(factset_id=security_info['factset_id']) \
								.first()
			#-- throw error if security_base not exists
			if not bool(fx_forward_to_update):
				message = "Record with factset_id: " + \
							security_info['factset_id'] + \
							" not found"
				self.logger.warn(message)
				raise FxForwardNotExistError(message)
			#-- update FxForward
			for key, value in security_info.items():
				setattr(fx_forward_to_update, key, value)
			session.commit()
			self.logger.info("Record " +  fx_forward_to_update.factset_id + " updated successfully")
		except FxForwardNotExistError:
			#-- avoid FxForwardNotExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to update FxForward")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def query(self, params):
		try:
			session = sessionmaker(bind=self.db)()
			fx_forward = session.query(
					FxForward.factset_id.label("factset_id"), \
					FxForward.geneva_fx_forward_name.label("geneva_fx_forward_name"), \
					FxForward.geneva_counter_party.label("geneva_counter_party"), \
					FxForward.starting_date.label("starting_date"), \
					FxForward.maturity_date.label("maturity_date"), \
					FxForward.base_currency.label("base_currency"), \
					FxForward.base_currency_quantity.label("base_currency_quantity"), \
					FxForward.term_currency.label("term_currency"), \
					FxForward.term_currency_quantity.label("term_currency_quantity"), \
					FxForward.forward_rate.label("forward_rate")) \
				.filter(FxForward.factset_id == params['factset_id']) \
				.order_by(FxForward.created_at)
			#self.logger.debug("Print the generated SQL:")
			#self.logger.debug(transaction_histories)
			#-- return as list of dictionary
			def model2dict(row):
				d = {}
				for column in row.keys():
					if column == "starting_date" or \
							column == "maturity_date":
						d[column] = str(getattr(row, column))[0:10]
					elif column == "base_currency_quantity" or \
							column == "term_currency_quantity" or \
							column == "forward_rate":
						d[column] = float(getattr(row, column))
					else:
						d[column] = str(getattr(row, column))
				return d
			fx_forward_d = [model2dict(t) for t in fx_forward]
			#self.logger.error("Print the list of dictionary output:")
			#self.logger.debug(transaction_histories_d)
			return fx_forward_d
		except Exception as e:
			self.logger.error("Error message:")
			self.logger.error(e)
			raise
		finally:
			session.close()