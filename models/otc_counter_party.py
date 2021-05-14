from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base(name='BaseModel')

class OtcCounterParty(BaseModel):
	__tablename__ = "otc_counter_parties"
	id = Column(Integer, primary_key=True)
	geneva_counter_party = Column(String(100))
	geneva_party_type = Column(String(100))
	geneva_party_name = Column(String(100))
	bloomberg_ticker = Column(String(50))
	created_at = Column(DateTime)
	updated_at = Column(DateTime)
	created_by = Column(Integer)
	updated_by = Column(Integer)

	def __init__(self, \
				geneva_counter_party, \
				geneva_party_type, \
				geneva_party_name=None, \
				bloomberg_ticker=None):
		self.geneva_counter_party = geneva_counter_party
		self.geneva_party_type = geneva_party_type
		self.geneva_party_name = geneva_party_name
		self.bloomberg_ticker = bloomberg_ticker

	def __repr__(self):
		res = {}
		columns = [m.key for m in model.__table__.columns]
		for column in columns:
			res[column] = getattr(model, column)
		return res
