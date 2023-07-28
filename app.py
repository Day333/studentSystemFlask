import re  # 正则表达式
import flask
from flask import Flask, url_for
from flask_migrate import Migrate

import configs
from exts import db
import models

# 初始化实例
app = Flask(__name__)
# 加载配置文件
app.config.from_object(configs)
# 增加session会话保护(任意字符串,用来对session进行加密)
app.secret_key = "day3"
# db绑定app
db.init_app(app)
migrate = Migrate(app, db)

# 存储登录用户的名字用户其他网页的显示
users = []


@app.route("/", methods=["GET", "POST"])
def login():
    # 增加会话保护机制(未登陆前login的session值为空)
    flask.session['login'] = ''
    if flask.request.method == 'POST':
        user = flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")
        # 防止sql注入,如:select * from admins where admin_name = '' or 1=1 -- and password='';
        # 利用正则表达式进行输入判断
        result_user = re.search(r"^[a-zA-Z]+$", user)  # 限制用户名为全字母
        result_pwd = re.search(r"^[a-zA-Z\d]+$", pwd)  # 限制密码为 字母和数字的组合
        if result_user is not None and result_pwd is not None:  # 验证通过
            msg = '用户名或密码错误'
            # 正则验证通过后与数据库中数据进行比较
            admins1 = models.admins.query.filter(models.admins.admin_name == user).first()
            # 匹配得到结果即管理员数据库中存在此管理员
            if admins1.admin_password == pwd:
                # 登陆成功
                flask.session['login'] = 'OK'
                users.append(user)  # 存储登陆成功的用户名用于显示
                return flask.redirect(flask.url_for('student'))
        else:  # 输入验证不通过
            msg = '非法输入'
    else:
        msg = ''
        user = ''
    users.append(user)
    return flask.render_template('login.html', msg=msg, user=user)


@app.route('/student', methods=['GET', "POST"])
def student():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登录有存储信息时显示用户名，否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''

    # 获取学生数据信息
    if flask.request.method == 'GET':
        student1 = models.students_infos.query.all()
        results = student1
    if flask.request.method == 'POST':
        # 获取输入的学生信息
        student_id = flask.request.values.get("student_id", "")
        student_class = flask.request.values.get("student_class", "")
        student_name = flask.request.values.get("student_name", "")
        print(student_id, student_class, student_name)
        try:
            # 信息存入数据库
            student2 = models.students_infos(student_id=student_id, student_name=student_name,
                                             student_class=student_class)
            db.session.add(student2)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            # result = cursor.fetchone()
            insert_result = "成功存入一条学生信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "学生信息插入失败"
            print(insert_result)
            pass
        try:
            db.session.commit()
        except:
            db.session.rollback()
        # POST方法时显示数据
    student1 = models.students_infos.query.all()
    results = student1
    return flask.render_template('student.html', insert_result=insert_result, user_info=user_info, results=results)


@app.route('/teacher', methods=['GET', "POST"])
def teacher():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # ,当用户登陆有存储信息时显示用户名否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        student1 = models.students_decision_infos.query.all()
        results = student1
    if flask.request.method == 'POST':
        # 获取输入的学生选课信息
        student_id = flask.request.values.get("student_id", "")
        student_class_id = flask.request.values.get("student_class_id", "")
        teacher_id = flask.request.values.get("teacher_id", "")
        print(student_id, student_class_id, teacher_id)
        try:
            # 信息存入数据库
            student2 = models.students_decision_infos(student_id=student_id, teacher_id=teacher_id,
                                                      student_class_id=student_class_id)
            db.session.add(student2)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            insert_result = "成功存入一条选课信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "选课信息插入失败"
            print(insert_result)
            pass
        try:
            db.session.commit()
        except:
            db.session.rollback()
        # POST显示数据
    student1 = models.students_decision_infos.query.all()
    results = student1
    return flask.render_template('teacher.html', insert_result=insert_result, user_info=user_info, results=results)


@app.route('/grade1', methods=['GET', "POST"])
def grade():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        # grade11 = grade_infos.query.all()
        grade11 = models.grade_infos.query.all()
        results = grade11
    if flask.request.method == 'POST':
        # 获取输入的学生成绩信息
        student_id = flask.request.values.get("student_id", "")
        student_class_id = flask.request.values.get("student_class_id", "")
        grade3 = flask.request.values.get("grade", "")
        print(student_id, student_class_id, grade3)
        # 信息存入数据库
        try:
            grade2 = models.grade_infos(student_id=student_id, student_class_id=student_class_id,
                                        grade=grade3)
            db.session.add(grade2)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            insert_result = "成功存入一条学生成绩信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "学生成绩信息插入失败"
            print(insert_result)
            pass
        try:
            db.session.commit()
        except:
            db.session.rollback()
    # POST获取数据
    grade11 = models.grade_infos.query.all()
    results = grade11
    return flask.render_template('grade.html', insert_result=insert_result, user_info=user_info, results=results)


@app.route('/grade_infos', methods=['GET', 'POST'])
def grade_infos():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    query_result = ''
    results = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取下拉框的数据
    if flask.request.method == 'POST':
        select = flask.request.form.get('selected_one')
        query1 = flask.request.values.get('query')
        print(select, query1)
        # 判断不同输入对数据表进行不同的处理
        if select == '学号':
            try:
                grade_infos1 = models.grade_infos.query.filter(models.grade_infos.student_id == query1).all()
                results = grade_infos1
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
        if select == '姓名':
            try:
                students_id3 = models.students_infos.query.filter(models.students_infos.student_name == query1).first()
                grade_infos1 = models.grade_infos.query.filter(models.grade_infos1.student_id == students_id3).all()
                results = grade_infos1
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass

        if select == '课程号':
            try:
                grade_infos1 = models.grade_infos.query.filter(models.grade_infos.student_class_id == query1).all()
                results = grade_infos1
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass

        if select == "所在班级":
            try:
                students_class3 = models.students_infos.query.filter(
                    models.students_infos.student_class == query1).first()
                grade_infos1 = models.grade_infos.query.filter(models.grade_infos1.student_id == students_class3).all()
                results = grade_infos1
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
    return flask.render_template('grade_infos.html', query_result=query_result, user_info=user_info, results=results)


@app.route('/adminstator', methods=['GET', "POST"])
def adminstator():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        grade14 = models.admins.query.all()
        results = grade14
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    if flask.request.method == 'POST':
        # 获取输入的管理员信息
        admin_name = flask.request.values.get("admin_name", "")
        admin_password = flask.request.values.get("admin_password", "")
        #print(admin_name, admin_password)
        admin_name_result = re.search(r"^[a-zA-Z]+$", admin_name)  # 限制用户名为全字母
        admin_password_result = re.search(
            r"^[a-zA-Z\d]+$", admin_password)  # 限制密码为 字母和数字的组合
        # 验证通过
        if admin_name_result != None and admin_password_result != None:  # 验证通过
            # 获取下拉框的数据
            select = flask.request.form.get('selected_one')
            if select == '增加管理员':
                try:
                    admin12 = models.admins(admin_name=admin_name, admin_password=admin_password)
                    db.session.add(admin12)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                    insert_result = "成功增加了一名管理员"
                    print(insert_result)
                except Exception as err:
                    print(err)
                    insert_result = "增加管理员操作失败"
                    print(insert_result)
                    pass
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
            if select == '修改管理员密码':
                try:
                    admin3 = models.admins.query.filter(
                        models.admins.admin_name == admin_name).first()
                    db.session.delete(admin3)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                    admin4 = models.admins(admin_name=admin_name, admin_password=admin_password)
                    db.session.add(admin4)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                    insert_result = "管理员" + admin_name + "的密码修改成功!"
                except Exception as err:
                    print(err)
                    insert_result = "修改管理员密码失败!"
                    pass
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
            if select == '删除管理员':
                try:
                    admin3 = models.admins.query.filter(
                        models.admins.admin_name == admin_name).first()
                    db.session.delete(admin3)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                    insert_result = "成功删除管理员" + admin_name
                except Exception as err:
                    print(err)
                    insert_result = "删除管理员失败"
                    pass
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

        else:  # 输入验证不通过
            insert_result = "输入的格式不符合要求!"
        # POST方法时显示数据
        sql_list = models.admins.query.all()
        results = sql_list
    return flask.render_template('adminstator.html', user_info=user_info, insert_result=insert_result, results=results)

if __name__ == '__main__':
    try:
        app.run()
    except Exception as err:
        db.close()  # 关闭数据库连接