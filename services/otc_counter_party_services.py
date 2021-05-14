# coding=utf-8
# 
import logging
from sqlalchemy.orm import sessionmaker
from security_data.utils.error_handling import (OtcCounterPartyAlreadyExistError,
											OtcCounterPartyNotExistError)
from security_data.models.otc_counter_party import OtcCounterParty

class OtcCounterPartyServices:

	def __init__(self, db):
		self.logger = logging.getLogger(__name__)
		self.db = db

	def delete_all(self):
		try:
			session = sessionmaker(bind=self.db)()
			session.query(OtcCounterParty).delete()
			session.commit()
		except Exception as e:
			self.logger.error("Failed to delete all records in OtcCounterParty")
			self.logger.error(e)
			raise
		finally:
			session.close()

	#-- the session argument is used if the service is called by
	#-- other service and want to work under same DB session for commit and rollback
	def create(self, counter_party_info, session=None):
		try:
			close_session = False
			if session is None:
				session = sessionmaker(bind=self.db)()
				close_session = True
			has_record = bool(session.query(OtcCounterParty).filter_by( \
					geneva_counter_party=counter_party_info['geneva_counter_party'], \
					geneva_party_type=counter_party_info['geneva_party_type']).first()
				)
			if has_record:
				message = "Record (" + counter_party_info['geneva_counter_party'] + "," + \
						counter_party_info['geneva_party_type'] + ") already exists"
				self.logger.warn(message)
				raise OtcCounterPartyAlreadyExistError(message)
			else:
				otc_counter_party = OtcCounterParty(**counter_party_info)
				session.add(otc_counter_party)
				session.commit()
				self.logger.info("Record (" + counter_party_info['geneva_counter_party'] + "," + \
						counter_party_info['geneva_party_type'] + ") added successfully")
		except OtcCounterPartyAlreadyExistError:
			#-- avoid OtcCounterPartyAlreadyExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to add OtcCounterParty")
			self.logger.error(e)
			raise
		finally:
			#-- only close session if the session_in 
			if close_session:
				session.close()

	def update(self, counter_party_info):
		try:
			session = sessionmaker(bind=self.db)()
			otc_counter_party_to_update = session.query(OtcCounterParty).filter_by( \
					geneva_counter_party=counter_party_info['geneva_counter_party'], \
					geneva_party_type=counter_party_info['geneva_party_type']).first()
			#-- throw error if security_base not exists
			if not bool(otc_counter_party_to_update):
				message = "Record (" + counter_party_info['geneva_counter_party'] + "," + \
						counter_party_info['geneva_party_type'] + ") not found"
				self.logger.warn(message)
				raise OtcCounterPartyNotExistError(message)
			#-- update OtcCounterParty
			for key, value in counter_party_info.items():
				setattr(otc_counter_party_to_update, key, value)
			session.commit()
			self.logger.info("Record (" + counter_party_info['geneva_counter_party'] + "," + \
						counter_party_info['geneva_party_type'] + ") updated successfully")
		except OtcCounterPartyNotExistError:
			#-- avoid OtcCounterPartyNotExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to update OtcCounterParty")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def query(self):
		try:
			session = sessionmaker(bind=self.db)()
			otc_counter_party = session.query(
					OtcCounterParty.geneva_counter_party.label("geneva_counter_party"), \
					OtcCounterParty.geneva_party_type.label("geneva_party_type"), \
					OtcCounterParty.geneva_party_name.label("geneva_party_name"), \
					OtcCounterParty.bloomberg_ticker.label("bloomberg_ticker")) \
				.order_by(OtcCounterParty.created_at)
			#self.logger.debug("Print the generated SQL:")
			#self.logger.debug(transaction_histories)
			#-- return as list of dictionary
			def model2dict(row):
				d = {}
				for column in row.keys():
					#if column == "timestamp":
					#	d[column] = str(getattr(row, column))[0:10]
					d[column] = str(getattr(row, column))
				return d
			otc_counter_party_d = [model2dict(t) for t in otc_counter_party]
			#self.logger.error("Print the list of dictionary output:")
			#self.logger.debug(transaction_histories_d)
			return otc_counter_party_d
		except Exception as e:
			self.logger.error("Error message:")
			self.logger.error(e)
			raise
		finally:
			session.close()