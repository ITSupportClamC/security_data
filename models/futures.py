from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base(name='BaseModel')

class Futures(BaseModel):
	__tablename__ = "futures"
	id = Column(Integer, primary_key=True)
	ticker = Column(String(50))
	underlying_id = Column(String(100))
	contract_size = Column(Numeric(asdecimal=False))
	value_of_1pt = Column(Numeric(asdecimal=False))
	timestamp = Column(DateTime)
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	created_by = Column(Integer)
	updated_by = Column(Integer)

	def __init__(self, \
				ticker, \
				underlying_id, \
				contract_size, \
				value_of_1pt, \
				timestamp):
		self.ticker = ticker
		self.underlying_id = underlying_id
		self.contract_size = contract_size
		self.value_of_1pt = value_of_1pt
		self.timestamp = timestamp

	def __repr__(self):
		res = {}
		columns = [m.key for m in model.__table__.columns]
		for column in columns:
			res[column] = getattr(model, column)
		return res
