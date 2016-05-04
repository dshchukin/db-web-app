from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db
from models import Base
from models import *
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm.interfaces
import sqlalchemy.exc

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
        competitions = competitions)

@app.route('/query', methods = ['GET', 'POST'])
def new_query():
    user = 'Denis' # user's nickname example
    return render_template('query.html', 
        title = 'New query',
        user = user)

@app.route('/query/insert')
def insert_query():
    user = 'Denis' # user's nickname example
    return render_template('queries/insert.html', 
        title = 'Insert query',
        user = user,
        tables = Base.metadata.tables.keys())

@app.route('/query/insert', methods = ['POST'])
def insert_query_post():
    user = 'Denis' # user's nickname example
    table = request.form['table']
    num_of_cols = len(Base.metadata.tables[table].columns)
    print(len(request.form))
    if len(request.form) > 2:
        vals = []
        for column in Base.metadata.tables[table].columns:
            x = request.form[str(column)]
            if x == '':
                x = None
            print('get ' + str(column) + ':' + str(x) + ';')
            vals.append(x)
        record = create_new_record(table, vals)
        db.session.add(record)
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError, exc:
            reason = exc.message
            print(reason)
            return render_template('error.html',
                title = 'Error',
                user = user,
                error_message = str(reason))
    else:
        fks = []
        for col in Base.metadata.tables[table].columns:
            fk_data = []
            print col
            if col.foreign_keys:
                for fk in col.foreign_keys:
                    print fk
                    print str(fk.column.table.name)
                    print map_fk(str(fk.column.table.name))
                    for line in db.session.query(map_fk(str(fk.column.table.name))):
                        print line.short_data()
                        fk_data.append(line.short_data())
            fks.append(fk_data)
            print(fks)
        return render_template('queries/insert.html', 
            title = 'Insert query',
            user = user,
            tables = [table],
            columns = zip(Base.metadata.tables[table].columns, fks))
    return render_template('queries/insert.html', 
        title = 'Insert query',
        user = user)

@app.route('/query/delete', methods = ['GET', 'POST'])
def delete_query():
    user = 'Denis' # user's nickname example
    return render_template('queries/delete.html', 
        title = 'Delete query',
        user = user)

@app.route('/query/update', methods = ['GET', 'POST'])
def update_query():
    user = 'Denis' # user's nickname example
    return render_template('queries/update.html', 
        title = 'Update query',
        user = user)

@app.route('/query/select')
def select_query():
    user = 'Denis' # user's nickname example
    return render_template('queries/select.html', 
        title = 'Select query',
        user = user,
        tables = Base.metadata.tables.keys())

@app.route('/query/select', methods = ['POST'])
def select_query_post():
    user = 'Denis' # user's nickname example
    table = request.form['table']
    flash('Select from ' + table)
    lines = []
    for line in db.session.query(map_table(table)):
        lines.append(line.data())
    return render_template('queries/select_result.html', 
        title = 'Select query result',
        user = user,
        result = lines,
        columns = Base.metadata.tables[table].columns,
        tables = [table])

