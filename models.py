from exts import db

# 学生信息表
class students_infos(db.Model):
    __tablename__ = 'students_infos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), nullable=False, unique=True)
    student_class = db.Column(db.String(50), unique=False)
    student_name = db.Column(db.String(50), unique=False)


# 学生选课表
class students_decision_infos(db.Model):
    __tablename__ = 'students_decision_infos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students_infos.student_id'))  # 定义外键
    student_class_id = db.Column(db.String(20), nullable=False, unique=False)
    teacher_id = db.Column(db.String(20), nullable=False, unique=False)


# 学生成绩信息表
class grade_infos(db.Model):
    __tablename__ = 'grade_infos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students_infos.student_id'))
    student_class_id = db.Column(db.String(20))
    grade = db.Column(db.String(20))


# 管理员信息表
class admins(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(20), nullable=False, unique=True)
    admin_password = db.Column(db.String(20), nullable=False, unique=False)