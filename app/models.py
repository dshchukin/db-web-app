from app import db

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import *

from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import text

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
	cursor = dbapi_connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON")
	cursor.close()

engine = create_engine('sqlite:///app_data.db', echo = True)
#meta = MetaData(bind=engine)
Base = declarative_base()

Base.metadata.reflect(engine)


class Coach(Base):
	__table__ = Base.metadata.tables['Coach']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.category = args.pop()
		self.datestart = args.pop()
	def data(self):
		return[int(self.id), self.category, self.datestart]
class Coaching(Base):
	__table__ = Base.metadata.tables['Coaching']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.sportsman = args.pop()
		self.coach = args.pop()
		self.datestart = args.pop()
		self.dateend = args.pop()
	def data(self):
		return[int(self.id), self.sportsman, self.coach, self.datestart, self.dateend]
class Competition(Base):
	__table__ = Base.metadata.tables['Competition']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.name = args.pop()
		self.place = args.pop()
		self.status = args.pop()
		self.datestart = args.pop()
		self.dateend = args.pop()
	def short_data(self):
		return[int(self.id), self.name, self.datestart]
	def data(self):
		return[int(self.id), self.name, self.place, self.status, self.datestart, self.dateend]
class Exam(Base):
	__table__ = Base.metadata.tables['Exam']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.date = args.pop()
		self.place = args.pop()
	def short_data(self):
		return[int(self.id), self.place, self.date]
	def data(self):
		return[int(self.id), self.date, self.place]
class Examined(Base):
	__table__ = Base.metadata.tables['Examined']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.result = args.pop()
		self.exam_id = args.pop()
		self.human_id = args.pop()
	def short_data(self):
		return[int(self.id), self.result, db.session.query(Exam).filter(Exam.id == self.exam_id).first().place, db.session.query(Exam).filter(Exam.id == self.exam_id).first().date]
	def data(self):
		return[int(self.id), self.result, self.exam_id, self.human_id]
class Examiners(Base):
	__table__ = Base.metadata.tables['Examiners']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.human_id = args.pop()
		self.exam_id = args.pop()
	def data(self):
		return [self.id, self.human_id, self.exam_id]
class Gym(Base):
	__table__ = Base.metadata.tables['Gym']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.structure = args.pop()
		self.address = args.pop()
	def data(self):
		return[int(self.id), self.structure, self.address]
class Human(Base):
	__table__ = Base.metadata.tables['Human']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.firstname = args.pop()
		self.middlename = args.pop()
		self.surname = args.pop()
		self.birthdate = args.pop()
		self.TIN = args.pop()
		self.phone = args.pop()
		self.address = args.pop()
		self.country = args.pop()
		self.city = args.pop()
		self.last_medical_exam = args.pop()
		self.insurance_num = args.pop()
		self.insurance_expires = args.pop()
	def short_data(self):
		#return[int(self.id), self.firstname, self.middlename, self.surname]
		return [int(self.id), "" + str(self.firstname) + " " + str(self.surname)]
	def data(self):
		return[int(self.id), self.firstname, self.middlename, self.surname, self.birthdate, self.TIN, self.phone, self.address, self.country, self.city, self.last_medical_exam, self.insurance_num, self.insurance_expires]
class Judge(Base):
	__table__ = Base.metadata.tables['Judge']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.category = args.pop()
		self.datestart = args.pop()
	def data(self):
		return[int(self.id), self.category, self.datestart]
class Result_judge(Base):
	__table__ = Base.metadata.tables['Result_judge']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.result = args.pop()
		self.competition = args.pop()
		self.post = args.pop()
	def data(self):
		return[int(self.id), self.result, self.competition, self.post]
class Result_sportsman(Base):
	__table__ = Base.metadata.tables['Result_sportsman']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.result = args.pop()
		self.competition = args.pop()
		self.sportsman = args.pop()
	def data(self):
		return[int(self.id), self.result, self.competition, self.sportsman]
class Seminar(Base):
	__table__ = Base.metadata.tables['Seminar']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.type = args.pop()
		self.name = args.pop()
		self.place = args.pop()
		self.datestart = args.pop()
		self.dateend = args.pop()
		self.org_structure = args.pop()
		self.org_human = args.pop()
	def short_data(self):
		return[int(self.id), self.name, self.datestart]
	def data(self):
		return[int(self.id), self.type, self.name, self.place, self.datestart, self.dateend, self.org_structure, self.org_human]
class Seminar_participating(Base):
	__table__ = Base.metadata.tables['Seminar_participating']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.human_id = args.pop()
		self.seminar_id = args.pop()
	def data(self):
		return[self.id, self.human_id, self.seminar_id]
class Seminar_type(Base):
	__table__ = Base.metadata.tables['Seminar_type']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.type_name = args.pop()
	def short_data(self):
		return[int(self.id), self.type_name]
	def data(self):
		return[self.id, self.type_name]
class Sportsman(Base):
	__table__ = Base.metadata.tables['Sportsman']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.category = args.pop()
		self.datestart = args.pop()
	def data(self):
		return[int(self.id), self.category, self.datestart]
class Structure(Base):
	__table__ = Base.metadata.tables['Structure']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.type = args.pop()
		self.name = args.pop()
		self.status = args.pop()
		self.upper_structure = args.pop()
	def short_data(self):
		return[int(self.id), self.name]
	def data(self):
		return[int(self.id), self.type, self.name, self.status, self.upper_structure]
class Structure_type(Base):
	__table__ = Base.metadata.tables['Structure_type']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.type_name = args.pop()
	def short_data(self):
		return [self.id, self.type_name]
	def data(self):
		return[self.id, self.type_name]
class Transfer(Base):
	__table__ = Base.metadata.tables['Transfer']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.human = args.pop()
		self.structure = args.pop()
		self.datestart = args.pop()
		self.dateend = args.pop()
	def data(self):
		return[int(self.id), self.human, self.structure, self.datestart, self.dateend]
class SQL_QUERY(Base):
	__table__ = Base.metadata.tables['SQL_QUERY']
	def __init__(self, args):
		args = list(reversed(args))
		self.id = args.pop()
		self.name = args.pop()
		self.description = args.pop()
		self.query = args.pop()
	def short_data(self):
		return [int(self.id), self.name]
	def data(self):
		return[int(self.id), self.name, self.description, self.query]


def create_new_record(table, args):
	if table == 'Coach':
		return Coach(args)

	if table == 'Coaching':
		return Coaching(args)

	if table == 'Competition':
		return Competition(args)

	if table == 'Exam':
		return Exam(args)

	if table == 'Examined':
		return Examined(args)

	if table == 'Examiners':
		return Examiners(args)

	if table == 'Gym':
		return Gym(args)

	if table == 'Human':
		return Human(args)

	if table == 'Judge':
		return Judge(args)

	if table == 'Result_judge':
		return Result_judge(args)

	if table == 'Result_sportsman':
		return Result_sportsman(args)

	if table == 'Seminar':
		return Seminar(args)

	if table == 'Seminar_participating':
		return Seminar_participating(args)

	if table == 'Seminar_type':
		return Seminar_type(args)

	if table == 'Sportsman':
		return Sportsman(args)

	if table == 'Structure':
		return Structure(args)

	if table == 'Structure_type':
		return Structure_type(args)

	if table == 'Transfer':
		return Transfer(args)

	if table == 'SQL_QUERY':
		return SQL_QUERY(args)

def map_table(table):
	if table == 'Coach':
		return Coach

	if table == 'Coaching':
		return Coaching

	if table == 'Competition':
		return Competition

	if table == 'Exam':
		return Exam

	if table == 'Examined':
		return Examined

	if table == 'Examiners':
		return Examiners

	if table == 'Human':
		return Human

	if table == 'Judge':
		return Judge

	if table == 'Result_judge':
		return Result_judge

	if table == 'Result_sportsman':
		return Result_sportsman

	if table == 'Seminar':
		return Seminar

	if table == 'Seminar_participating':
		return Seminar_participating

	if table == 'Seminar_type':
		return Seminar_type

	if table == 'Sportsman':
		return Sportsman

	if table == 'Structure':
		return Structure

	if table == 'Structure_type':
		return Structure_type

	if table == 'Transfer':
		return Transfer

	if table == 'Gym':
		return Gym

	if table == 'SQL_QUERY':
		return SQL_QUERY

	return None

def map_fk(table):
	print('table name = ' + str(table))
	data = []
	if table == 'Human':
		for line in db.session.query(Human):
			data.append(line.short_data())

	if table == 'Sportsman':
		x = db.session.query(Sportsman, Human).join(Human)
		for line in x:
			data.append(line.Human.short_data())

	if table == 'Coach':
		x = db.session.query(Coach, Human).join(Human)
		for line in x:
			data.append(line.Human.short_data())

	if table == 'Judge':
		x = db.session.query(Judge, Human).join(Human)
		for line in x:
			data.append(line.Human.short_data())

	if table == 'Seminar':
		for line in db.session.query(Seminar):
			data.append(line.short_data())

	if table == 'Exam':
		for line in db.session.query(Exam):
			data.append(line.short_data())

	if table == 'Seminar_type':
		for line in db.session.query(Seminar_type):
			data.append(line.short_data())

	if table == 'Structure':
		for line in db.session.query(Structure):
			data.append(line.short_data())

	if table == 'Structure_type':
		for line in db.session.query(Structure_type):
			data.append(line.short_data())

	if table == 'Competition':
		for line in db.session.query(Competition):
			data.append(line.short_data())

	if table == 'Examined':
		for line in db.session.query(Examined):
			data.append(line.short_data())
	if table == 'SQL_QUERY':
		for line in db.session.query(SQL_QUERY):
			data.append(line.short_data())
	return data
