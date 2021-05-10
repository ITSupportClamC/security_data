# coding=utf-8
# 
import logging
from security_data.models.fixed_deposit import FixedDeposit
from sqlalchemy.orm import sessionmaker
from security_data.utils.error_handling import (FixedDepositAlreadyExistError,
											FixedDepositNotExistError)

class FixedDepositServices:

	def __init__(self, db):
		self.logger = logging.getLogger(__name__)
		self.db = db
		
	def delete_all(self):
		try:
			session = sessionmaker(bind=self.db)()
			session.query(FixedDeposit).delete()
			session.commit()
		except Exception as e:
			self.logger.error("Failed to delete all records in FixedDeposit")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def create(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			has_record = bool(session.query(FixedDeposit).filter_by(geneva_id=security_info['geneva_id']).first())
			if has_record:
				message = "Record " + security_info['geneva_id'] + " already exists"
				self.logger.warn(message)
				raise FixedDepositAlreadyExistError(message)
			else:
				fixed_deposit = FixedDeposit(**security_info)
				session.add(fixed_deposit)
				session.commit()
				self.logger.info("Record " + security_info['geneva_id'] + " added successfully")
		except FixedDepositAlreadyExistError:
			#-- avoid FixedDepositAlreadyExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to add FixedDeposit")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def update(self, security_info):
		try:
			session = sessionmaker(bind=self.db)()
			fixed_deposit_to_update = session.query(FixedDeposit) \
								.filter_by(geneva_id=security_info['geneva_id']) \
								.first()
			#-- throw error if security_base not exists
			if not bool(fixed_deposit_to_update):
				message = "Record with geneva_id: " + \
							security_info['geneva_id'] + \
							" not found"
				self.logger.warn(message)
				raise FixedDepositNotExistError(message)
			#-- update FixedDeposit
			for key, value in security_info.items():
				setattr(fixed_deposit_to_update, key, value)
			session.commit()
			self.logger.info("Record " +  fixed_deposit_to_update.geneva_id + " updated successfully")
		except FixedDepositNotExistError:
			#-- avoid FixedDepositNotExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to update FixedDeposit")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def query(self, params):
		try:
			session = sessionmaker(bind=self.db)()
			fixed_deposits = session.query(
					FixedDeposit.geneva_id.label("geneva_id"), \
					FixedDeposit.factset_id.label("factset_id"), \
					FixedDeposit.geneva_counter_party.label("geneva_counter_party"), \
					FixedDeposit.starting_date.label("starting_date"), \
					FixedDeposit.maturity_date.label("maturity_date"), \
					FixedDeposit.interest_rate.label("interest_rate")) \
				.filter(FixedDeposit.geneva_id == params['geneva_id']) \
				.order_by(FixedDeposit.created_at)
			#self.logger.debug("Print the generated SQL:")
			#self.logger.debug(transaction_histories)
			#-- return as list of dictionary
			def model2dict(row):
				d = {}
				for column in row.keys():
					if column == "starting_date" or \
							column == "maturity_date":
						d[column] = str(getattr(row, column))[0:10]
					elif column == "interest_rate":
						d[column] = float(getattr(row, column))
					else:
						d[column] = str(getattr(row, column))
				return d
			fixed_deposits_d = [model2dict(t) for t in fixed_deposits]
			#self.logger.error("Print the list of dictionary output:")
			#self.logger.debug(transaction_histories_d)
			return fixed_deposits_d
		except Exception as e:
			self.logger.error("Error message:")
			self.logger.error(e)
			raise
		finally:
			session.close()