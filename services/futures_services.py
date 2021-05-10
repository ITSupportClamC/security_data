# coding=utf-8
# 
import logging
from datetime import datetime
from security_data.models.futures import Futures
from sqlalchemy.orm import sessionmaker
from security_data.utils.error_handling import (FuturesAlreadyExistError,
											FuturesNotExistError)

class FuturesServices:

	def __init__(self, db):
		self.logger = logging.getLogger(__name__)
		self.db = db

	def delete_all(self):
		try:
			session = sessionmaker(bind=self.db)()
			session.query(Futures).delete()
			session.commit()
		except Exception as e:
			self.logger.error("Failed to delete all records in Futures")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def create(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			has_record = bool(session.query(Futures).filter_by(ticker=security_info['ticker']).first())
			if has_record:
				message = "Record " + security_info['ticker'] + " already exists"
				self.logger.warn(message)
				raise FuturesAlreadyExistError(message)
			else:
				futures = Futures(**security_info)
				session.add(futures)
				session.commit()
				self.logger.info("Record " + security_info['ticker'] + " added successfully")
		except FuturesAlreadyExistError:
			#-- avoid FuturesAlreadyExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to add Futures")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def update(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			futures_to_update = session.query(Futures) \
								.filter_by(ticker=security_info['ticker']) \
								.first()
			#-- throw error if security_base not exists
			if not bool(futures_to_update):
				message = "Record with ticker: " + \
							security_info['ticker'] + \
							" not found"
				self.logger.warn(message)
				raise FuturesNotExistError(message)
			#-- update Futures
			for key, value in security_info.items():
				setattr(futures_to_update, key, value)
			session.commit()
			self.logger.info("Record " +  futures_to_update.ticker + " updated successfully")
		except FuturesNotExistError:
			#-- avoid FuturesNotExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to update Futures")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def query(self, params):
		try:
			session = sessionmaker(bind=self.db)()
			futures = session.query(
					Futures.ticker.label("ticker"), \
					Futures.underlying_id.label("underlying_id"), \
					Futures.contract_size.label("contract_size"), \
					Futures.value_of_1pt.label("value_of_1pt"), \
					Futures.timestamp.label("timestamp")) \
				.filter(Futures.ticker == params['ticker']) \
				.order_by(Futures.created_at)
			#self.logger.debug("Print the generated SQL:")
			#self.logger.debug(transaction_histories)
			#-- return as list of dictionary
			def model2dict(row):
				d = {}
				for column in row.keys():
					#if column == "timestamp":
					#	d[column] = str(getattr(row, column))[0:10]
					if column == "contract_size" or \
							column == "value_of_1pt":
						d[column] = float(getattr(row, column))
					else:
						d[column] = str(getattr(row, column))
				return d
			futures_d = [model2dict(t) for t in futures]
			#self.logger.error("Print the list of dictionary output:")
			#self.logger.debug(transaction_histories_d)
			return futures_d
		except Exception as e:
			self.logger.error("Error message:")
			self.logger.error(e)
			raise
		finally:
			session.close()