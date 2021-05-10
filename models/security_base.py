from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base(name='BaseModel')

class SecurityBase(BaseModel):
	__tablename__ = "security_base"
	id = Column(Integer, primary_key=True)
	geneva_id = Column(String(100))
	geneva_asset_type = Column(String(100))
	geneva_investment_type = Column(String(100))
	ticker = Column(String(50))
	isin = Column(String(50))
	bloomberg_id = Column(String(50))
	sedol = Column(String(50))
	currency = Column(String(5))
	is_private = Column(String(5))
	description = Column(String(200))
	exchange_name = Column(String(100))
	timestamp = Column(DateTime)
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	created_by = Column(Integer)
	updated_by = Column(Integer)

	def __init__(self, \
				geneva_id, \
				geneva_asset_type, \
				geneva_investment_type, \
				ticker, \
				isin, \
				bloomberg_id, \
				sedol, \
				currency, \
				is_private, \
				description, \
				exchange_name, \
				timestamp):
		self.geneva_id = geneva_id
		self.geneva_asset_type = geneva_asset_type
		self.geneva_investment_type = geneva_investment_type
		self.ticker = ticker
		self.isin = isin
		self.bloomberg_id = bloomberg_id
		self.sedol = sedol
		self.currency = currency
		self.is_private = is_private
		self.description = description
		self.exchange_name = exchange_name
		self.timestamp = timestamp

	def __repr__(self):
		res = {}
		columns = [m.key for m in model.__table__.columns]
		for column in columns:
			res[column] = getattr(model, column)
		return res
