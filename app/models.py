from app import db

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///app_data.db', echo = True)
#meta = MetaData(bind=engine)
Base = declarative_base()
Base.metadata.reflect(engine)

from sqlalchemy.orm import relationship, backref

class Coach(Base):
    __table__ = Base.metadata.tables['Coach']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.category = args.pop()
       	self.datestart = args.pop()
    def __str__(self):
    	return ("<Coach:" + 
    		"\n\tid=" + str(self.id) + 
    		"\n\tcategory=" + str(self.category) + 
    		"\n\tdatestart=" + str(self.datestart) + 
    		"\n>")
class Coaching(Base):
    __table__ = Base.metadata.tables['Coaching']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.sportsman = args.pop()
       	self.coach = args.pop()
       	self.datestart = args.pop()
       	self.dateend = args.pop()
    def __str__(self):
    	return ("<Coaching:" +
    		"\nid=" + str(self.id) + 
    		"\n\tsportsman=" + str(self.sportsman) + 
    		"\n\tcoach=" + str(self.coach) + 
    		"\n\tdatestart=" + str(self.datestart) + 
    		"\n\tdateend=" + str(self.dateend) + 
    		"\n>")
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
class Exam(Base):
    __table__ = Base.metadata.tables['Exam']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.date = args.pop()
       	self.place = args.pop()
class Examined(Base):
    __table__ = Base.metadata.tables['Examined']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.result = args.pop()
       	self.exam_id = args.pop()
class Examiners(Base):
    __table__ = Base.metadata.tables['Examiners']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.human_id = args.pop()
       	self.exam_id = args.pop()
class Gym(Base):
    __table__ = Base.metadata.tables['Gym']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.structure = args.pop()
       	self.address = args.pop()
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
       	self.diploma = args.pop()
       	self.last_medical_exam = args.pop()
       	self.insurance_num = args.pop()
       	self.insurance_expires = args.pop()
    def __str__(self):
    	return ("<Human:" +
    		"\nid=" + str(self.id) + 
    		"\n\tfirstname=" + str(self.firstname) + 
    		"\n\tmiddlename=" + str(self.middlename) + 
    		"\n\tsurname=" + str(self.surname) + 
    		"\n\tTIN=" + str(self.TIN) + 
    		"\n\tphone=" + str(self.phone) + 
    		"\n\taddress=" + str(self.address) + 
    		"\n\tcountry=" + str(self.country) + 
    		"\n\tcity=" + str(self.city) + 
    		"\n\tdiploma=" + str(self.diploma) + 
    		"\n\tlast_medical_exam=" + str(self.last_medical_exam) + 
    		"\n\tinsurance_num=" + str(self.insurance_num) + 
    		"\n\tinsurance_expires=" + str(self.insurance_expires) + 
    		"\n>")
class Judge(Base):
    __table__ = Base.metadata.tables['Judge']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.category = args.pop()
       	self.datestart = args.pop()
class Result_judge(Base):
    __table__ = Base.metadata.tables['Result_judge']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.result = args.pop()
       	self.competition = args.pop()
       	self.post = args.pop()
class Result_sportsman(Base):
    __table__ = Base.metadata.tables['Result_sportsman']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.result = args.pop()
       	self.competition = args.pop()
       	self.sportsman = args.pop()
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
class Seminar_participating(Base):
    __table__ = Base.metadata.tables['Seminar_participating']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.human_id = args.pop()
       	self.seminar_id = args.pop()
class Seminar_type(Base):
    __table__ = Base.metadata.tables['Seminar_type']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.type_id = args.pop()
       	self.type_name = args.pop()
class Sportsman(Base):
    __table__ = Base.metadata.tables['Sportsman']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.category = args.pop()
       	self.datestart = args.pop()
class Structure(Base):
    __table__ = Base.metadata.tables['Structure']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.type = args.pop()
       	self.name = args.pop()
       	self.status = args.pop()
       	self.upper_structure = args.pop()
class Structure_type(Base):
    __table__ = Base.metadata.tables['Structure_type']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.type_id = args.pop()
       	self.type_name = args.pop()
class Transfer(Base):
    __table__ = Base.metadata.tables['Transfer']
    def __init__(self, args):
    	args = list(reversed(args))
    	self.id = args.pop()
       	self.human = args.pop()
       	self.structure = args.pop()
       	self.datestart = args.pop()
       	self.dateend = args.pop()

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
    
    return 0
    
#print(Base.metadata.tables.keys())
#print(Base.metadata.tables['Human'].columns)
#print(len(Base.metadata.tables['Human'].columns))
