from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base(name='BaseModel')

class FixedDeposit(BaseModel):
	__tablename__ = "fixed_deposits"
	id = Column(Integer, primary_key=True)
	geneva_id = Column(String(50))
	factset_id = Column(String(100))
	geneva_counter_party = Column(String(100))
	starting_date = Column(DateTime)
	maturity_date = Column(DateTime)
	interest_rate = Column(Numeric(asdecimal=False))
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	created_by = Column(Integer)
	updated_by = Column(Integer)

	def __init__(self, \
				geneva_id, \
				factset_id, \
				geneva_counter_party, \
				starting_date, \
				maturity_date, \
				interest_rate):
		self.geneva_id = geneva_id
		self.factset_id = factset_id
		self.geneva_counter_party = geneva_counter_party
		self.starting_date = starting_date
		self.maturity_date = maturity_date
		self.interest_rate = interest_rate

	def __repr__(self):
		res = {}
		columns = [m.key for m in model.__table__.columns]
		for column in columns:
			res[column] = getattr(model, column)
		return res
