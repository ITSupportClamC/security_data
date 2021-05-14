from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base(name='BaseModel')

class FxForward(BaseModel):
	__tablename__ = "fx_forwards"
	id = Column(Integer, primary_key=True)
	factset_id = Column(String(100))
	geneva_fx_forward_name = Column(String(100))
	geneva_counter_party = Column(String(100))
	starting_date = Column(DateTime)
	maturity_date = Column(DateTime)
	base_currency = Column(String(5))
	base_currency_quantity = Column(Numeric(asdecimal=False))
	term_currency = Column(String(5))
	term_currency_quantity = Column(Numeric(asdecimal=False))
	forward_rate = Column(Numeric(asdecimal=False))
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	created_by = Column(Integer)
	updated_by = Column(Integer)

	def __init__(self, \
				factset_id, \
				geneva_fx_forward_name, \
				geneva_counter_party, \
				starting_date, \
				maturity_date, \
				base_currency, \
				base_currency_quantity, \
				term_currency, \
				term_currency_quantity, \
				forward_rate):
		self.factset_id = factset_id
		self.geneva_fx_forward_name = geneva_fx_forward_name
		self.geneva_counter_party = geneva_counter_party
		self.starting_date = starting_date
		self.maturity_date = maturity_date
		self.base_currency = base_currency
		self.base_currency_quantity = base_currency_quantity
		self.term_currency = term_currency
		self.term_currency_quantity = term_currency_quantity
		self.forward_rate = forward_rate

	def __repr__(self):
		res = {}
		columns = [m.key for m in model.__table__.columns]
		for column in columns:
			res[column] = getattr(model, column)
		return res
