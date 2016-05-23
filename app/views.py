from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db
from models import Base
from models import *
import sqlalchemy
import re
import sqlalchemy.ext.declarative
import sqlalchemy.orm.interfaces
from sqlalchemy.sql import text
import sqlalchemy.exc
import random
import datetime
from jinja2 import *

@app.route('/')
@app.route('/index')
def index():
    user = 'User'
    competitions = [
        { 
            'name': '21-01-2016', 
            'date': 'Competition 1' 
        },
        { 
            'name': '08-04-2016', 
            'date': 'Competition 2'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        rand=random.randint(1, 5),
        competitions = competitions)

@app.route('/query', methods = ['GET', 'POST'])
def new_query():
    user = 'Denis' # user's nickname example
    return render_template('query.html', 
        title = 'New query',
        rand=random.randint(1, 5),
        user = user)

@app.route('/query/insert')
def insert_query():
    user = 'Denis' # user's nickname example
    return render_template('queries/insert.html', 
        title = 'Insert query',
        rand = random.randint(1,5),
        user = user,
        tables = Base.metadata.tables.keys())

@app.route('/query/insert', methods = ['POST'])
def insert_query_post():
    user = 'Denis' # user's nickname example
    table = request.form['table']
    num_of_cols = len(Base.metadata.tables[table].columns)
    print "here"
    if len(request.form) > 2:
        vals = []
        for column in Base.metadata.tables[table].columns:
            print column.name
            try:
                x = request.form[column.name]
            except KeyError:
                return render_template('error.html',
                    title = 'Error',
                    user = user,
                    error_message = "Wrong " + column.name)
            if x == '':
                x = None
            print('get ' + column.name + ':' + str(x) + ';')
            vals.append(x)
        db.session.commit()
        print vals
        record = create_new_record(table, vals)
        print vals
        db.session.add(record)
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            print(reason)
            return render_template('error.html',
                title = 'Error',
                rand = random.randint(1,5),
                user = user,
                error_message = str(reason))
        return show_single(table, vals[0])
    else:
        fks = []
        for col in Base.metadata.tables[table].columns:
            fk_data = None
            if col.foreign_keys:
                fk_data = []
                for fk in col.foreign_keys:
                    fk_data = map_fk(str(fk.column.table.name))
            fks.append(fk_data)
        return render_template('queries/insert.html', 
            title = 'Insert query',
            user = user,
            rand = random.randint(1,5),
            table = table,
            columns = zip(Base.metadata.tables[table].columns, fks))


@app.route('/query/select')
def select_query():
    return render_template('queries/select.html', 
        title = 'Select query',
        tables = Base.metadata.tables.keys())

@app.route('/query/select/<table>')
def select(table):
    user = 'Denis' # user's nickname example
    flash('Select from ' + table, 'note')
    lines = []
    for line in db.session.query(map_table(table)):
        lines.append(line.data())
    return render_template('queries/select_result.html',
        title = 'Select query result',
        user = user,
        result = lines,
        columns = Base.metadata.tables[table].columns,
        table = table)

@app.route('/query/select', methods = ['POST'])
def select_query_post():
    user = 'Denis' # user's nickname example
    table = request.form['table']
    flash('Select from ' + table, 'note')
    lines = []
    for line in db.session.query(map_table(table)):
        lines.append(line.data())
    return render_template('queries/select_result.html',
        title = 'Select query result',
        user = user,
        result = lines,
        columns = Base.metadata.tables[table].columns,
        table = table)

@app.route('/single/<table>/<int:id>')
def show_single(table, id):
    user = 'Denis' # user's nickname example
    columns = Base.metadata.tables[table].columns
    tbl = map_table(table)
    lines = db.session.query(tbl).filter(tbl.id == id)
    if not lines.first():
        return render_template('error.html',
            title = 'Error',
            user = user,
            error_message = "No object with such id")
    fks = []
    for col in Base.metadata.tables[table].columns:
        fk_data = None
        # print col
        if col.foreign_keys:
            fk_data = []
            for fk in col.foreign_keys:
                fk_data = map_fk(str(fk.column.table.name))
        fks.append(fk_data)
    print(fks)
    print(lines.first().data())
    page = "base"
    coaches = []
    competitions = []
    gyms = []
    available_participants = []
    coach_data = []
    participants = []
    structures = []
    if table == "Human":
        page = "human"
        coach_data = db.session.query(Coach).filter(Coach.id == id).first()
    if table == "Structure":
        page = "structure"
        gyms = db.session.query(Gym).filter(Gym.structure == id)
        not_available_participants = db.session.query(Transfer, Human).filter(Transfer.dateend == None).filter(Transfer.human == Human.id)
        nap = []
        for x in not_available_participants:
            nap.append(x[1].id)
        print nap
        ap = db.session.query(Human).filter(Human.id.notin_(nap))
        available_participants = ap
        participants = db.session.query(Transfer, Human).filter(id == Transfer.structure, Transfer.dateend == None).filter(Transfer.human == Human.id)
    if table == "Competition":
        page = "competition"
    if table == "Exam":
        page = "exam"
    if table == "Sportsman":
        page = "sportsman"
        coaches = db.session.query(Coaching, Human).filter(id == Coaching.sportsman).filter(Coaching.coach == Human.id)
        competitions = db.session.query(Result_sportsman, Competition).filter(id == Result_sportsman.sportsman).filter(Result_sportsman.competition == Competition.id)
        structures = db.session.query(Transfer, Structure).filter(id == Transfer.human).filter(Transfer.structure == Structure.id)
    if table == "Coach":
        page = "coach"
    if table == "Seminar":
        page = "seminar"
    date = datetime.datetime.now()
    today = date.strftime("%d-%m-%Y")
    #print coach_data.category
    #print coach_data.datestart
    return render_template('queries/single/single_' + page +'.html',
                              id = id,
                              today = today,
                              coach_data = coach_data,
                              title='Single object',
                              user=user,
                              participants = participants,
                              available_participants = available_participants,
                              gyms = gyms,
                              table=table,
                              coaches = coaches,
                              competitions = competitions,
                              structures = structures,
                              data=zip(columns, lines.first().data(), fks))

@app.route('/single/<table>/<int:id>', methods = ['POST'])
def show_single_post(table, id):
    print 'post'
    date = datetime.datetime.now()
    today = date.strftime("%d-%m-%Y")
    user = 'Denis' # user's nickname example
    columns = Base.metadata.tables[table].columns
    tbl = map_table(table)
    lines = db.session.query(tbl).filter(tbl.id == id)
    deleted = False
    updated = False
    try:
        print 'check update button'
        updated = request.form['update']
        updated = True
        vals = []
        print 'update button was pressed'
        try:
            #print 'update id=' + str(id)  + ' from ' + table
            for column in columns:
                try:
                    x = request.form[column.name]
                except KeyError:
                    return render_template('error.html',
                                           title='Error',
                                           user=user,
                                           error_message="Wrong " + column.name)
                if x == '':
                    x = None
                if column.name == 'id':
                    vals.append(id)
                else:
                    vals.append(x)
                record = db.session.query(map_table(table)).filter(map_table(table).id == id).update({column.name: x})
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            print(reason)
            return render_template('error.html',
                                   title='Error',
                                   rand=random.randint(1, 5),
                                   user=user,
                                   error_message=str(reason))
    except KeyError:
        print('no one updated')
    if updated:
        print 'updated'
        return redirect("single/" + table + '/' + str(id))
    if deleted:
        print 'deleted'
        return redirect("query/select/" + table)
    try:
        print 'check delete button'
        deleted = request.form['delete']
        deleted = True
        print 'delete button was pressed'
        try:
            query = db.session.query(map_table(table)).filter(map_table(table).id == id).delete()
            print 'delete id=' + str(id) + ' from ' + table
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            print(reason)
            return render_template('error.html',
                                   title='Error',
                                   rand=random.randint(1, 5),
                                   user=user,
                                   error_message=str(reason))
    except KeyError:
        print('no one deleted')
    if deleted:
        print 'deleted'
        return redirect("query/select/" + table)
    if table == "Human":
        page = "human"
    if table == "Structure":
        page = "structure"
        try:
            print 'kicking...'
            kick_id_str = request.form['kick']
            kick_id = int(kick_id_str[5:])
            x = db.session.query(Transfer).filter(Transfer.dateend == None)
            print x.count()
            transfer = db.session.query(Transfer).filter(Transfer.human == kick_id).filter(Transfer.dateend == None)
            print transfer.count()
            transfer = transfer.first()
            transfer.dateend = today
            db.session.add(transfer)
            try:
                db.session.commit()
            except sqlalchemy.exc.SQLAlchemyError, exc:
                reason = exc.message
                print(reason)
                return render_template('error.html',
                                       title='Error',
                                       rand=random.randint(1, 5),
                                       user=user,
                                       error_message=str(reason))
            print 'kick ' + str(kick_id)
        except KeyError:
            print 'no one was kicked'

        try:
            add_request = request.form['add']
            print 'adding...'
            try:
                add_human = request.form['add_human']
                print 'human to add: '
                print add_human
            except KeyError:
                flash('Human for adding was not chosen, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            try:
                datestart = request.form['datestart']
                if datestart == '':
                    flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                    return show_single(table, id)
            except KeyError:
                flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            vals = [None]
            vals.append(add_human)
            vals.append(id)
            vals.append(datestart)
            vals.append(None)
            record = create_new_record('Transfer', vals)
            db.session.add(record)
            print vals
            try:
                db.session.commit()
                print 'add ' + str(vals[0])
            except sqlalchemy.exc.SQLAlchemyError, exc:
                reason = exc.message
                print(reason)
                return render_template('error.html',
                                       title='Error',
                                       rand=random.randint(1, 5),
                                       user=user,
                                       error_message=str(reason))
            return show_single(table, id)
        except KeyError:
            print 'no one was added'

        gyms = db.session.query(Gym).filter(id == Gym.structure)
        participants = db.session.query(Transfer, Human).filter(id == Transfer.human and not Transfer.dateend).filter(Transfer.human == Human.id)
    if table == "Competition":
        page = "competition"
    if table == "Exam":
        page = "exam"
    if table == "Sportsman":
        page = "sportsman"
        coaches = db.session.query(Coaching, Human).filter(id == Coaching.sportsman).filter(Coaching.coach == Human.id)
        competitions = db.session.query(Result_sportsman, Competition).filter(id == Result_sportsman.sportsman).filter(Result_sportsman.competition == Competition.id)
        structures = db.session.query(Transfer, Structure).filter(id == Transfer.human).filter(Transfer.structure == Structure.id)
    if table == "Coach":
        page = "coach"
    if table == "Seminar":
        page = "seminar"
    return show_single(table, id)


@app.route('/add/<table>')
def add(table):
    fks = []
    for col in Base.metadata.tables[table].columns:
        fk_data = None
        # print col
        if col.foreign_keys:
            fk_data = []
            for fk in col.foreign_keys:
                fk_data = map_fk(str(fk.column.table.name))
            if col.name == 'org_structure' or col.name == 'org_human':
                fk_data.append(None)
        fks.append(fk_data)
    return render_template('queries/add.html',
                           title='Insert query',
                           table=table,
                           columns=zip(Base.metadata.tables[table].columns, fks))



@app.route('/add/<table>', methods = ['POST'])
def add_post(table):
    user = 'Denis' # user's nickname example
    num_of_cols = len(Base.metadata.tables[table].columns)
    vals = []
    for column in Base.metadata.tables[table].columns:
        print column.name
        try:
            x = request.form[column.name]
        except KeyError:
            return render_template('error.html',
                title = 'Error',
                user = user,
                error_message = "Wrong " + column.name)
        if x == '':
            x = None
        print('get ' + column.name + ':' + str(x) + ';')
        vals.append(x)
    print vals
    record = create_new_record(table, vals)
    db.session.add(record)
    if table == 'Seminar':
        if record.org_human != None and record.org_structure != None:
            flash('Only one of field \'org_structure\' and \'org_human\' should be defined', 'error')
            return add(table)
        if record.org_human == None and record.org_structure == None:
            flash('One of field \'org_structure\' and \'org_human\' should be defined', 'error')
            return add(table)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError, exc:
        reason = exc.message
        print(reason)
        return render_template('error.html',
            title = 'Error',
            rand = random.randint(1,5),
            user = user,
            error_message = str(reason))
    return redirect("single/" + table + '/' + str(record.id))

@app.route('/query/raw_sql')
def raw_sql():
    return render_template('queries/raw_sql.html',
                           title='Raw SQL query')

@app.route('/query/raw_sql/add')
def raw_sql_add():
    return render_template('queries/raw_sql_add.html',
                           title='Raw SQL query')

@app.route('/query/raw_sql/add', methods = ['POST'])
def raw_sql_add_post():
    sql = request.form['code']
    if re.search('(?<!\[)(insert|delete|update|drop|alter|create)(?!\])', sql) is not None:
        flash('Restricted keyword was used in SQL query', 'error')
        return raw_sql_add()
    name = request.form['name']
    description = ''
    try:
        description = request.form['description']
    except KeyError:
        description = ''
    vals = []
    vals.append(None)
    vals.append(name)
    vals.append(description)
    vals.append(sql)
    record = create_new_record('SQL_QUERY', vals)
    db.session.add(record)
    try:
        db.session.commit()
        print 'add ' + str(record.id)
    except sqlalchemy.exc.SQLAlchemyError, exc:
        reason = exc.message
        print(reason)
        return render_template('error.html',
                               title='Error',
                               error_message=str(reason))
    print(vals)
    #return redirect("/query/raw_sql/use/" + str(record.id))
    return redirect("/query/raw_sql")

@app.route('/query/raw_sql/use')
def raw_sql_use():
    for line in db.session.query(SQL_QUERY):
        print line.id
    return render_template('queries/raw_sql_use.html',
                           queries = db.session.query(SQL_QUERY),
                           title='Raw SQL query')

@app.route('/query/raw_sql/use', methods = ['POST'])
def raw_sql_use_post():
    try:
        print 'deleting query...'
        kick_id_str = request.form['delete']
        kick_id = int(kick_id_str[7:])
        x = db.session.query(SQL_QUERY).filter(SQL_QUERY.id == kick_id).delete()
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            print(reason)
            return render_template('error.html',
                                   title='Error',
                                   error_message=str(reason))
    except KeyError:
        print 'no one was deleted'
    return render_template('queries/raw_sql_use.html',
                           queries = db.session.query(SQL_QUERY),
                           title='Raw SQL query')

@app.route('/query/raw_sql/use/<query>')
def raw_sql_use_need_data(query):

    result = db.session.query(SQL_QUERY).filter(SQL_QUERY.id == query).first()
    sql = result.query
    params = re.findall('\[[a-zA-Z0-9_]+\]', sql)
    return render_template('queries/raw_sql_use_need_data.html',
                           params=params,
                           query = query,
                           title='Raw SQL query')

@app.route('/query/raw_sql/use/<query>', methods = ['POST'])
def raw_sql_use_need_data_post(query):
    result = db.session.query(SQL_QUERY).filter(SQL_QUERY.id == query).first()
    sql = result.query
    params = re.findall('\[[a-zA-Z0-9_]+\]', sql)
    vals = {}
    for param in params:
        try:
            x = request.form[param]
        except KeyError:
            return render_template('error.html',
                                  title='Error',
                                  error_message="Wrong " + param)
        new_param = re.sub('\[([a-zA-Z0-9_]+)\]', r'\1', param)
        vals[new_param] = x
    new_sql = re.sub('\[([a-zA-Z0-9_]+)\]', r':\1', sql)
    records = []
    try:
        records = db.session.execute(text(new_sql), vals)
    except sqlalchemy.exc.SQLAlchemyError, exc:
        reason = exc.message
        print(reason)
        return render_template('error.html',
                               title='Error',
                               error_message=str(reason))
    return render_template('queries/raw_sql_use_result.html',
                           params=params,
                           records = records.fetchall(),
                           title='Raw SQL query')

