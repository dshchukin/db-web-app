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
    date = datetime.datetime.now()
    today = date.strftime("%d-%m-%Y")
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
        today = today,
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
    if map_table(table) == None:
        flash('No such table: ' + table, 'error')
        return redirect("/index")
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
    if map_table(table) == None:
        flash('No such table: ' + table, 'error')
        return redirect("/index")
    user = 'Denis' # user's nickname example
    columns = Base.metadata.tables[table].columns
    tbl = map_table(table)
    lines = db.session.query(tbl).filter(tbl.id == id)
    if not lines.first():
        flash('No object with such id in ' + table + ": " + str(id), 'error')
        return redirect("/index")
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
    available_examiners_exam = []
    examiners_exam = []
    competitions = []
    gyms = []
    available_participants = []
    coach_data = []
    sportsman_comp_history = []
    sportsman_c_history = []
    coach_c_history = []
    seminar_history = []
    exam_p_history = []
    exam_j_history = []
    sportsman_data = []
    judge_data = []
    participants = []
    available_participants_sem = []
    participants_sem = []
    participants_comp = []
    available_participants_comp = []
    structures = []
    available_participants_exam = []
    participants_exam = []
    org_h = None
    org_str = None
    result_j = None
    if table == "Human":
        page = "human"
        coach_data = db.session.query(Coach).filter(Coach.id == id).first()
        sportsman_comp_history = db.session.query(Result_sportsman, Competition).filter(Result_sportsman.sportsman == id).filter(Competition.id == Result_sportsman.competition)
        sportsman_c_history = db.session.query(Coaching, Coach, Human).filter(Coaching.sportsman == id).filter(Coach.id == Coaching.coach).filter(Human.id == Coach.id)
        exam_p_history = db.session.query(Examined, Exam).filter(Examined.human_id == id).filter(Examined.exam_id == Exam.id)
        exam_j_history = db.session.query(Exam).filter(Exam.id.in_(db.session.query(Examiners.exam_id).filter(Examiners.human_id == id)))
        seminar_history = db.session.query(Seminar).filter(Seminar.id.in_(db.session.query(Seminar_participating.seminar_id).filter(Seminar_participating.human_id == id)))
        sportsman_data = db.session.query(Sportsman).filter(Sportsman.id == id).first()
        judge_data = db.session.query(Judge).filter(Judge.id == id).first()
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
        participants_comp = db.session.query(Result_sportsman, Human).filter(Result_sportsman.competition == id).filter(Result_sportsman.sportsman == Human.id)
        available_participants_comp = db.session.query(Sportsman, Human).filter(Sportsman.id == Human.id)
        result_j = db.session.query(Result_judge).filter(Result_judge.competition == id).first()
    if table == "Exam":
        page = "exam"
        examiners_exam = db.session.query(Examiners, Human).filter(Examiners.exam_id == id).filter(Examiners.human_id == Human.id)
        available_examiners_exam = db.session.query(Human).filter(Human.id.notin_(db.session.query(Human.id).filter(Human.id.in_(db.session.query(Examiners.human_id).filter(Examiners.exam_id == id))))).filter(
            Human.id.notin_(db.session.query(Human.id).filter(
                Human.id.in_(db.session.query(Examined.human_id).filter(Examined.exam_id == id))))
        )
        participants_exam = db.session.query(Examined, Human).filter(Examined.exam_id == id).filter(Examined.human_id == Human.id)
        available_participants_exam = db.session.query(Human).filter(Human.id.notin_(db.session.query(Human.id).filter(Human.id.in_(db.session.query(Examined.human_id).filter(Examined.exam_id == id))))).filter(
            Human.id.notin_(db.session.query(Human.id).filter(Human.id.in_(db.session.query(Examiners.human_id).filter(Examiners.exam_id == id)))))
    if table == "Sportsman":
        page = "sportsman"
        coaches = db.session.query(Coaching, Human).filter(id == Coaching.sportsman).filter(Coaching.coach == Human.id)
        competitions = db.session.query(Result_sportsman, Competition).filter(id == Result_sportsman.sportsman).filter(Result_sportsman.competition == Competition.id)
        structures = db.session.query(Transfer, Structure).filter(id == Transfer.human).filter(Transfer.structure == Structure.id)
    if table == "Coach":
        page = "coach"
    if table == "Seminar":
        page = "seminar"
        org_h = db.session.query(Seminar, Human).filter(Seminar.id == id).filter(Human.id == Seminar.org_human).first()
        org_str = db.session.query(Seminar, Structure).filter(Seminar.id == id).filter(Structure.id == Seminar.org_structure).first()
        not_available_participants = db.session.query(Seminar_participating, Human).filter(Seminar_participating.seminar_id == id).filter(Seminar_participating.human_id == Human.id)
        nap = []
        for x in not_available_participants:
            nap.append(x[1].id)
        ap = db.session.query(Human).filter(Human.id.notin_(nap))
        available_participants_sem = ap
        participants_sem = db.session.query(Seminar_participating, Human).filter(id == Seminar_participating.seminar_id).filter(Seminar_participating.human_id == Human.id)
    date = datetime.datetime.now()
    today = date.strftime("%d-%m-%Y")
    print "returning"
    return render_template('queries/single/single_' + page +'.html',
                              id = id,
                              seminar_history = seminar_history,
                              exam_p_history = exam_p_history,
                              exam_j_history = exam_j_history,
                              available_examiners_exam = available_examiners_exam,
                              examiners_exam = examiners_exam,
                              participants_exam = participants_exam,
                              available_participants_exam = available_participants_exam,
                              result_j = result_j,
                              participants_comp = participants_comp,
                              available_participants_comp = available_participants_comp,
                              org_h = org_h,
                              org_str = org_str,
                              today = today,
                              sportsman_data = sportsman_data,
                              judge_data = judge_data,
                              sportsman_comp_history = sportsman_comp_history,
                              coach_data = coach_data,
                              title='Single object',
                              user=user,
                              participants = participants,
                              available_participants = available_participants,
                              participants_sem = participants_sem,
                              available_participants_sem = available_participants_sem,
                              gyms = gyms,
                              table=table,
                              coaches = coaches,
                              competitions = competitions,
                              structures = structures,
                              data=zip(columns, lines.first().data(), fks))

@app.route('/single/<table>/<int:id>', methods = ['POST'])
def show_single_post(table, id):
    if map_table(table) == None:
        flash('No such table: ' + table, 'error')
        return redirect("/index")
    if not db.session.query(map_table(table)).filter(map_table(table).id == id).first():
        flash('No object with such id in ' + table + ": " + str(id), 'error')
        return redirect("/index")
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
        try:
            update_coach_request = request.form['update_coach']
            try:
                new_category = request.form['new_category']
            except KeyError:
                flash('Category was not defined, but \'Update\' button was pressed', 'error')
                flash('Category was not defined, but \'Update\' button was pressed', 'error')
                return show_single(table, id)
            try:
                new_datestart = request.form['new_datestart']
                if new_datestart == '':
                    flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                    return show_single(table, id)
            except KeyError:
                flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            print(db.session.query(Coach).filter(Coach.id == id).first())
            if db.session.query(Coach).filter(Coach.id == id).first() is not None:
                try:
                    record = db.session.query(Coach).filter(Coach.id == id).update({'category': new_category, 'datestart': new_datestart})
                except sqlalchemy.exc.SQLAlchemyError, exc:
                    reason = exc.message
                    flash('Internal error. Maybe wrong values were setted in updating coach?', 'error')
                    return show_single(table, id)
            else:
                vals = [id]
                vals.append(new_category)
                vals.append(new_datestart)
                record = create_new_record('Coach', vals)
                db.session.add(record)
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
            return show_single(table, id)
        except KeyError:
            pass
        try:
            update_sportsman_request = request.form['update_sportsman']
            try:
                new_category_sportsman = request.form['new_category_sportsman']
            except KeyError:
                flash('Category was not defined, but \'Update\' button was pressed', 'error')
                return show_single(table, id)
            try:
                new_datestart_sportsman = request.form['new_datestart_sportsman']
                if new_datestart_sportsman == '':
                    flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                    return show_single(table, id)
            except KeyError:
                flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            print(db.session.query(Sportsman).filter(Sportsman.id == id).first())
            if db.session.query(Sportsman).filter(Sportsman.id == id).first() is not None:
                try:
                    record = db.session.query(Sportsman).filter(Sportsman.id == id).update(
                        {'category': new_category_sportsman, 'datestart': new_datestart_sportsman})
                except sqlalchemy.exc.SQLAlchemyError, exc:
                    reason = exc.message
                    flash('Internal error. Maybe wrong values were setted in updating coach?', 'error')
                    return show_single(table, id)
            else:
                vals = [id]
                vals.append(new_category_sportsman)
                vals.append(new_datestart_sportsman)
                record = create_new_record('Sportsman', vals)
                db.session.add(record)
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
            return show_single(table, id)
        except KeyError:
            pass
        try:
            update_judge_request = request.form['update_judge']
            try:
                new_category_judge = request.form['new_category_judge']
            except KeyError:
                flash('Category was not defined, but \'Update\' button was pressed', 'error')
                return show_single(table, id)
            try:
                new_datestart_judge = request.form['new_datestart_judge']
                if new_datestart_judge == '':
                    flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                    return show_single(table, id)
            except KeyError:
                flash('Datestart was not defined, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            print(db.session.query(Judge).filter(Judge.id == id).first())
            if db.session.query(Judge).filter(Judge.id == id).first() is not None:
                try:
                    record = db.session.query(Judge).filter(Judge.id == id).update(
                        {'category': new_category_judge, 'datestart': new_datestart_judge})
                except sqlalchemy.exc.SQLAlchemyError, exc:
                    reason = exc.message
                    flash('Internal error. Maybe wrong values were setted in updating coach?', 'error')
                    return show_single(table, id)
            else:
                vals = [id]
                vals.append(new_category_judge)
                vals.append(new_datestart_judge)
                record = create_new_record('Judge', vals)
                db.session.add(record)
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
            return show_single(table, id)
        except KeyError:
            pass
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
        try:
            print 'kicking...'
            kick_id_str = request.form['kick']
            kick_id = int(kick_id_str[7:])
            result = db.session.query(Result_sportsman).filter(Result_sportsman.id == kick_id).first()
            db.session.delete(result)
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
                result = request.form['result']
                if result == '':
                    flash('Result was not defined, but \'Add\' button was pressed', 'error')
                    return show_single(table, id)
            except KeyError:
                flash('Result was not defined, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            vals = [None]
            vals.append(result)
            vals.append(id)
            vals.append(add_human)
            record = create_new_record('Result_sportsman', vals)
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
        try:
            print 'updating result...'
            new_res_req = request.form['update_result']
            new_res = request.form['new_result']
            new_post = request.form['new_post']
            vals = []
            if (db.session.query(Result_judge).filter(Result_judge.competition == id).count() == 0):
                vals.append(None)
            else:
                vals.append(db.session.query(Result_judge).filter(Result_judge.competition == id).first().id)
            vals.append(new_res)
            vals.append(id)
            vals.append(new_post)
            record = create_new_record('Result_judge', vals)
            print vals
            if(db.session.query(Result_judge).filter(Result_judge.competition == id).count() == 0) :
                db.session.add(record)
            else:
                try:
                    record = db.session.query(Result_judge).filter(Result_judge.competition == id).update(
                        {'result': new_res, 'post': new_post})
                except sqlalchemy.exc.SQLAlchemyError, exc:
                    reason = exc.message
                    flash('Internal error. Maybe wrong values were setted in updating result?', 'error')
                    return show_single(table, id)
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
        except KeyError:
            pass
    if table == "Exam":
        page = "exam"
        try:
            print 'kicking...'
            kick_id_str = request.form['kick']
            kick_id = int(kick_id_str[5:])
            result = db.session.query(Examined).filter(Examined.human_id == kick_id).first()
            db.session.delete(result)
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
                result = request.form['result']
                if result == '':
                    flash('Result was not defined, but \'Add\' button was pressed', 'error')
                    return show_single(table, id)
            except KeyError:
                flash('Result was not defined, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            vals = [None]
            vals.append(result)
            vals.append(id)
            vals.append(int(add_human))
            record = create_new_record('Examined', vals)
            print record
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

        try:
            print 'kicking...'
            kick_id_str = request.form['kick_2']
            kick_id = int(kick_id_str[5:])
            result = db.session.query(Examiners).filter(Examiners.human_id == kick_id).first()
            db.session.delete(result)
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
            add_request = request.form['add_2']
            print 'adding...'
            try:
                add_human = request.form['add_human_2']
                print 'human to add: '
                print add_human
            except KeyError:
                flash('Human for adding was not chosen, but \'Add\' button was pressed', 'error')
                return show_single(table, id)
            vals = [None]
            vals.append(int(add_human))
            vals.append(id)
            record = create_new_record('Examiners', vals)
            print record
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
    if table == "Sportsman":
        page = "sportsman"
        coaches = db.session.query(Coaching, Human).filter(id == Coaching.sportsman).filter(Coaching.coach == Human.id)
        competitions = db.session.query(Result_sportsman, Competition).filter(id == Result_sportsman.sportsman).filter(Result_sportsman.competition == Competition.id)
        structures = db.session.query(Transfer, Structure).filter(id == Transfer.human).filter(Transfer.structure == Structure.id)
    if table == "Coach":
        page = "coach"
    if table == "Seminar":
        page = "seminar"
        try:
            print 'kicking...'
            kick_id_str = request.form['kick']
            kick_id = int(kick_id_str[5:])
            part = db.session.query(Seminar_participating).filter(Seminar_participating.human_id == kick_id, Seminar_participating.seminar_id == id)
            part = part.first()
            db.session.delete(part)
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
            vals = [None]
            vals.append(add_human)
            vals.append(id)
            record = create_new_record('Seminar_participating', vals)
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


    return show_single(table, id)


@app.route('/add/<table>')
def add(table):
    if map_table(table) == None:
        flash('No such table: ' + table, 'error')
        return redirect("/index")
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
    if map_table(table) == None:
        flash('No such table: ' + table, 'error')
        return redirect("/index")
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
    return redirect("/query/raw_sql/use/" + str(record.id))

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
    if not db.session.query(SQL_QUERY).filter(SQL_QUERY.id == query).first():
        flash('No object with such id in SQL_QUERY: ' + str(query), 'error')
        return redirect("/index")
    result = db.session.query(SQL_QUERY).filter(SQL_QUERY.id == query).first()
    sql = result.query
    params = re.findall('\[[a-zA-Z0-9_]+\]', sql)
    return render_template('queries/raw_sql_use_need_data.html',
                           params=params,
                           name=result.name,
                           description=result.description,
                           query = query,
                           title='Raw SQL query')

@app.route('/query/raw_sql/use/<query>', methods = ['POST'])
def raw_sql_use_need_data_post(query):
    if not db.session.query(SQL_QUERY).filter(SQL_QUERY.id == query).first():
        flash('No object with such id in SQL_QUERY: ' + str(query), 'error')
        return redirect("/index")
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
                           name = result.name,
                           description = result.description,
                           records = records.fetchall(),
                           title='Raw SQL query')

