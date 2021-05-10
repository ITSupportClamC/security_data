# coding=utf-8
# 
import logging
from security_data.models.security_base import SecurityBase
from sqlalchemy.orm import sessionmaker
from security_data.utils.error_handling import (SecurityBaseAlreadyExistError,
											SecurityBaseNotExistError)

class SecurityBaseServices:

	def __init__(self, db):
		self.logger = logging.getLogger(__name__)
		self.db = db

	def delete_all(self):
		try:
			session = sessionmaker(bind=self.db)()
			session.query(SecurityBase).delete()
			session.commit()
		except Exception as e:
			self.logger.error("Failed to delete all records in SecurityBase")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def create(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			has_record = bool(session.query(SecurityBase).filter_by(geneva_id=security_info['geneva_id']).first())
			if has_record:
				message = "Record " + security_info['geneva_id'] + " already exists"
				self.logger.warn(message)
				raise SecurityBaseAlreadyExistError(message)
			else:
				security_base = SecurityBase(**security_info)
				session.add(security_base)
				session.commit()
				self.logger.info("Record " + security_info['geneva_id'] + " added successfully")
		except SecurityBaseAlreadyExistError:
			#-- avoid SecurityBaseAlreadyExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to add SecurityBase")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def update(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			security_base_to_update = session.query(SecurityBase) \
								.filter_by(geneva_id=security_info['geneva_id']) \
								.first()
			#-- throw error if security_base not exists
			if not bool(security_base_to_update):
				message = "Record with geneva_id: " + \
							security_info['geneva_id'] + \
							" not found"
				self.logger.warn(message)
				raise SecurityBaseNotExistError(message)
			#-- update transaction by updating the status to cancel
			for key, value in security_info.items():
				setattr(security_base_to_update, key, value)
			session.commit()
			self.logger.info("Record " +  security_base_to_update.geneva_id + " updated successfully")
		except SecurityBaseNotExistError:
			#-- avoid SecurityBaseNotExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to update transaction")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def query(self, params):
		try:
			session = sessionmaker(bind=self.db)()
			security_bases = session.query(
					SecurityBase.geneva_id.label("geneva_id"), \
					SecurityBase.geneva_asset_type.label("geneva_asset_type"), \
					SecurityBase.geneva_investment_type.label("geneva_investment_type"), \
					SecurityBase.ticker.label("ticker"), \
					SecurityBase.isin.label("isin"), \
					SecurityBase.bloomberg_id.label("bloomberg_id"), \
					SecurityBase.sedol.label("sedol"), \
					SecurityBase.currency.label("currency"), \
					SecurityBase.is_private.label("is_private"), \
					SecurityBase.description.label("description"), \
					SecurityBase.exchange_name.label("exchange_name"), \
					SecurityBase.timestamp.label("timestamp")) \
				.filter(SecurityBase.geneva_id == params['geneva_id']) \
				.order_by(SecurityBase.created_at)
			#self.logger.debug("Print the generated SQL:")
			#self.logger.debug(transaction_histories)
			#-- return as list of dictionary
			def model2dict(row):
				d = {}
				for column in row.keys():
					#if column == "timestamp":
					#	d[column] = str(getattr(row, column))[0:10]
					#else:
					d[column] = str(getattr(row, column))
				return d
			security_bases_d = [model2dict(t) for t in security_bases]
			#self.logger.error("Print the list of dictionary output:")
			#self.logger.debug(transaction_histories_d)
			return security_bases_d
		except Exception as e:
			self.logger.error("Error message:")
			self.logger.error(e)
			raise
		finally:
			session.close()