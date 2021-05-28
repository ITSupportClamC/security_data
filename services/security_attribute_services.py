# coding=utf-8
# 
import logging
from security_data.models.security_attribute import SecurityAttribute
from sqlalchemy.orm import sessionmaker
from security_data.utils.error_handling import (SecurityAttributeAlreadyExistError,
											SecurityAttributeNotExistError)

class SecurityAttributeServices:

	def __init__(self, db):
		self.logger = logging.getLogger(__name__)
		self.db = db

	def delete_all(self):
		try:
			session = sessionmaker(bind=self.db)()
			session.query(SecurityAttribute).delete()
			session.commit()
		except Exception as e:
			self.logger.error("Failed to delete all records in SecurityAttribute")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def create(self, security_attribute_info):
		try:
			session = sessionmaker(bind=self.db)()
			has_record = bool(session.query(SecurityAttribute).filter_by(\
					security_id_type=security_attribute_info['security_id_type'], \
					security_id=security_attribute_info['security_id']).first()
			)
			if has_record:
				message = "Record (" + security_attribute_info['security_id_type'] + "," + \
						security_attribute_info['security_id'] + ") already exists"
				self.logger.warn(message)
				raise SecurityAttributeAlreadyExistError(message)
			else:
				security_attribute = SecurityAttribute(**security_attribute_info)
				session.add(security_attribute)
				session.commit()
				self.logger.info("Record (" + security_attribute_info['security_id_type'] + "," + \
						security_attribute_info['security_id'] + ") added successfully")
		except SecurityAttributeAlreadyExistError:
			#-- avoid SecurityAttributeAlreadyExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to add SecurityAttribute")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def update(self, security_attribute_info):
		try:
			session = sessionmaker(bind=self.db)()
			security_attribute_to_update = session.query(SecurityAttribute).filter_by( \
					security_id_type=security_attribute_info['security_id_type'], \
					security_id=security_attribute_info['security_id']).first()
			#-- throw error if security_base not exists
			if not bool(security_attribute_to_update):
				message = "Record (" + security_attribute_info['security_id_type'] + "," + \
						security_attribute_info['security_id'] + ") not found"
				self.logger.warn(message)
				raise SecurityAttributeNotExistError(message)
			#-- update transaction by updating the status to cancel
			for key, value in security_attribute_info.items():
				setattr(security_attribute_to_update, key, value)
			session.commit()
			self.logger.info("Record (" + security_attribute_info['security_id_type'] + "," + \
						security_attribute_info['security_id'] + ") updated successfully")
		except SecurityAttributeNotExistError:
			#-- avoid SecurityAttributeNotExistError being captured by Exception
			raise
		except Exception as e:
			self.logger.error("Failed to update SecurityAttribute")
			self.logger.error(e)
			raise
		finally:
			session.close()

	def query(self, params):
		try:
			session = sessionmaker(bind=self.db)()
			security_attributes = session.query(
					SecurityAttribute.security_id_type.label("security_id_type"), \
					SecurityAttribute.security_id.label("security_id"), \
					SecurityAttribute.gics_sector.label("gics_sector"), \
					SecurityAttribute.gics_industry_group.label("gics_industry_group"), \
					SecurityAttribute.industry_sector.label("industry_sector"), \
					SecurityAttribute.industry_group.label("industry_group"), \
					SecurityAttribute.bics_sector_level_1.label("bics_sector_level_1"), \
					SecurityAttribute.bics_industry_group_level_2.label("bics_industry_group_level_2"), \
					SecurityAttribute.bics_industry_name_level_3.label("bics_industry_name_level_3"), \
					SecurityAttribute.bics_sub_industry_name_level_4.label("bics_sub_industry_name_level_4"), \
					SecurityAttribute.parent_symbol.label("parent_symbol"), \
					SecurityAttribute.parent_symbol_chinese_name.label("parent_symbol_chinese_name"), \
					SecurityAttribute.parent_symbol_industry_group.label("parent_symbol_industry_group"), \
					SecurityAttribute.cast_parent_company_name.label("cast_parent_company_name"), \
					SecurityAttribute.country_of_risk.label("country_of_risk"), \
					SecurityAttribute.country_of_issuance.label("country_of_issuance"), \
					SecurityAttribute.sfc_region.label("sfc_region"), \
					SecurityAttribute.s_p_issuer_rating.label("s_p_issuer_rating"), \
					SecurityAttribute.moody_s_issuer_rating.label("moody_s_issuer_rating"), \
					SecurityAttribute.fitch_s_issuer_rating.label("fitch_s_issuer_rating"), \
					SecurityAttribute.bond_or_equity_ticker.label("bond_or_equity_ticker"), \
					SecurityAttribute.s_p_rating.label("s_p_rating"), \
					SecurityAttribute.moody_s_rating.label("moody_s_rating"), \
					SecurityAttribute.fitch_rating.label("fitch_rating"), \
					SecurityAttribute.payment_rank.label("payment_rank"), \
					SecurityAttribute.payment_rank_mbs.label("payment_rank_mbs"), \
					SecurityAttribute.bond_classification.label("bond_classification"), \
					SecurityAttribute.local_government_lgfv.label("local_government_lgfv"), \
					SecurityAttribute.first_year_default_probability.label("first_year_default_probability"), \
					SecurityAttribute.contingent_capital.label("contingent_capital"), \
					SecurityAttribute.co_co_bond_trigger.label("co_co_bond_trigger"), \
					SecurityAttribute.capit_type_conti_conv_tri_lvl.label("capit_type_conti_conv_tri_lvl"), \
					SecurityAttribute.tier_1_common_equity_ratio.label("tier_1_common_equity_ratio"), \
					SecurityAttribute.bail_in_capital_indicator.label("bail_in_capital_indicator"), \
					SecurityAttribute.tlac_mrel_designation.label("tlac_mrel_designation"), \
					SecurityAttribute.classif_on_chi_state_owned_enterp.label("classif_on_chi_state_owned_enterp"), \
					SecurityAttribute.private_placement_indicator.label("private_placement_indicator"), \
					SecurityAttribute.trading_volume_90_days.label("trading_volume_90_days")) \
				.filter(SecurityAttribute.security_id_type == params['security_id_type'],
					SecurityAttribute.security_id == params['security_id']) \
				.order_by(SecurityAttribute.created_at)
			#-- return as list of dictionary
			def model2dict(row):
				d = {}
				for column in row.keys():
					if column == "first_year_default_probability" or \
							column == "tier_1_common_equity_ratio" or \
							column == "trading_volume_90_days":
						d[column] = float(getattr(row, column))
					else:
						d[column] = str(getattr(row, column))
				return d
			security_attribute_d = [model2dict(t) for t in security_attributes]
			#self.logger.error("Print the list of dictionary output:")
			#self.logger.debug(security_attribute_d)
			return security_attribute_d
		except Exception as e:
			self.logger.error("Error message:")
			self.logger.error(e)
			raise
		finally:
			session.close()