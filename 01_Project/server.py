#! -*- coding:utf-8 -*-

import sys
import os
import shutil
# import webview
from datetime import datetime
from flask import Flask ,g ,request ,session ,redirect ,url_for ,render_template, json, jsonify, Response
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
from os.path import expanduser

import xlrd

import scan
import generate

reload(sys)
sys.setdefaultencoding('utf-8')

home_path = expanduser("~")

ident_path = os.path.join(home_path, 'ident')
if not os.path.exists(ident_path):
	os.mkdir(ident_path)

error_path = os.path.join(ident_path, 'error')
if not os.path.exists(error_path):
	os.mkdir(error_path)

DATABASE = os.path.join(ident_path, 'db.sqlite')
print('DATABASE File',DATABASE)

ERRORPATH = error_path
print('ERRORPATH File',ERRORPATH)


# print( 'sys.argv[0] is', sys.argv[0] )
# print( 'sys.executable is', sys.executable )
# print( 'os.getcwd is', os.getcwd() )

if getattr(sys, 'frozen', False):
	template_folder = os.path.join(sys._MEIPASS, 'templates')
	static_folder = os.path.join(sys._MEIPASS, 'static')
	app = Flask(__name__, template_folder=template_folder,static_folder=static_folder)
else:
	app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'kpi'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

def load():
    db.create_all()
    if Admin.query.count()==0:
        db.session.add(Admin(username='admin',password='1'))
        db.session.commit()
    if Exam.query.count()==0:
        db.session.add(Exam(name=u'领导班子年度综合考评',sort=1))
        db.session.add(Exam(name=u'中层干部年度综合考评',sort=2))
        db.session.commit()
    if ExamContent.query.count()==0:
        exam = Exam.query.filter_by(name=u'领导班子年度综合考评').first()
        db.session.add(ExamContent(exam_id=exam.id,content=u'政治素质',sort=1,show=1))
        db.session.add(ExamContent(exam_id=exam.id,content=u'经营业绩',sort=2,show=1))
        db.session.add(ExamContent(exam_id=exam.id,content=u'团结协作',sort=3,show=1))
        db.session.add(ExamContent(exam_id=exam.id,content=u'作风形象',sort=4,show=1))
        db.session.add(ExamContent(exam_id=exam.id,content=u'业绩考核',sort=0,show=0))
        exam = Exam.query.filter_by(name=u'中层干部年度综合考评').first()
        db.session.add(ExamContent(exam_id=exam.id,content=u'素质',sort=1,show=1))
        db.session.add(ExamContent(exam_id=exam.id,content=u'能力',sort=2,show=1))
        db.session.add(ExamContent(exam_id=exam.id,content=u'业绩',sort=3,show=1))
        db.session.add(ExamContent(exam_id=exam.id,content=u'考核',sort=0,show=0))
        db.session.commit()
    if ExamMeasure.query.count()==0:
        exam_content = ExamContent.query.filter_by(content=u'业绩考核').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'企业党建',weight=10,sort=0,show=0))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'绩效成果',weight=35,sort=0,show=0))
        exam_content = ExamContent.query.filter_by(content=u'考核').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'班子业绩',weight=30,sort=0,show=0))
        
        exam_content = ExamContent.query.filter_by(content=u'政治素质').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'政治方向',weight=10,sort=1,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'社会责任',weight=5,sort=2,show=1))
        exam_content = ExamContent.query.filter_by(content=u'经营业绩').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'可持续发展',weight=15,sort=3,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'创新成效',weight=15,sort=4,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'科学管理',weight=15,sort=5,show=1))
        exam_content = ExamContent.query.filter_by(content=u'团结协作').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'发扬民主',weight=10,sort=6,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'整体合力',weight=10,sort=7,show=1))
        exam_content = ExamContent.query.filter_by(content=u'作风形象').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'诚信务实',weight=6,sort=8,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'联系群众',weight=6,sort=9,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'廉洁自律',weight=8,sort=10,show=1))
        
        exam_content = ExamContent.query.filter_by(content=u'素质').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'政治素质',weight=9,sort=1,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'职业素养',weight=8,sort=2,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'廉洁自律',weight=8,sort=3,show=1))
        exam_content = ExamContent.query.filter_by(content=u'能力').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'决策能力',weight=6,sort=4,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'执行能力',weight=6,sort=5,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'领导能力',weight=6,sort=6,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'学习能力',weight=5,sort=7,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'创新能力',weight=6,sort=8,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'沟通能力',weight=6,sort=9,show=1))
        exam_content = ExamContent.query.filter_by(content=u'业绩').first()
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'内控管理',weight=10,sort=10,show=1))
        db.session.add(ExamMeasure(exam_content_id=exam_content.id,name=u'履职绩效',weight=30,sort=11,show=1))
        db.session.commit()
    if ExamEntity.query.count()==0:
        db.session.add(ExamEntity(name=u'A票',sort=1))
        db.session.add(ExamEntity(name=u'B票',sort=2))
        db.session.add(ExamEntity(name=u'C票',sort=3))
        db.session.add(ExamEntity(name=u'D票',sort=4))
        db.session.add(ExamEntity(name=u'E票',sort=5))
        db.session.commit()
    if OrgType.query.count()==0:
        db.session.add(OrgType(name=u'基层单位',sort=1))
        db.session.add(OrgType(name=u'机关部门',sort=2))
        db.session.commit()
    if ManagerType.query.count()==0:
        db.session.add(ManagerType(name=u'正处',sort=1))
        db.session.add(ManagerType(name=u'副处',sort=2))
        db.session.commit()
    # if ManagerTitle.query.count()==0:
    #     db.session.add(ManagerTitle(name=u'部长',sort=1))
    #     db.session.add(ManagerTitle(name=u'副部长',sort=2))
    #     db.session.add(ManagerTitle(name=u'总经理',sort=3))
    #     db.session.add(ManagerTitle(name=u'副总经理',sort=4))
    #     db.session.commit()
    if ExamSystem.query.count()==0:
        exam = Exam.query.filter_by(name=u'领导班子年度综合考评').first()
        org_type = OrgType.query.filter_by(name=u'基层单位').first()
        db.session.add(ExamSystem(exam_id=exam.id,org_type_id=org_type.id,manager_type_id=None,name=u'基层单位领导班子',sort=1))
        exam = Exam.query.filter_by(name=u'中层干部年度综合考评').first()
        manager_type = ManagerType.query.filter_by(name=u'正处').first()
        db.session.add(ExamSystem(exam_id=exam.id,org_type_id=org_type.id,manager_type_id=manager_type.id,name=u'基层单位正职',sort=2))
        manager_type = ManagerType.query.filter_by(name=u'副处').first()
        db.session.add(ExamSystem(exam_id=exam.id,org_type_id=org_type.id,manager_type_id=manager_type.id,name=u'基层单位副职',sort=3))
        exam = Exam.query.filter_by(name=u'领导班子年度综合考评').first()
        org_type = OrgType.query.filter_by(name=u'机关部门').first()
        db.session.add(ExamSystem(exam_id=exam.id,org_type_id=org_type.id,manager_type_id=None,name=u'机关部门领导班子',sort=4))
        exam = Exam.query.filter_by(name=u'中层干部年度综合考评').first()
        manager_type = ManagerType.query.filter_by(name=u'正处').first()
        db.session.add(ExamSystem(exam_id=exam.id,org_type_id=org_type.id,manager_type_id=manager_type.id,name=u'机关部门正职',sort=5))
        manager_type = ManagerType.query.filter_by(name=u'副处').first()
        db.session.add(ExamSystem(exam_id=exam.id,org_type_id=org_type.id,manager_type_id=manager_type.id,name=u'机关部门副职',sort=6))
        db.session.commit()
    if ExamEntityWeight.query.count()==0:
        exam_system = ExamSystem.query.filter_by(name=u'基层单位领导班子').first()
        exam_entity = ExamEntity.query.filter_by(name=u'A票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=1,exam_user=u'公司正职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'B票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=20,sort=2,exam_user=u'公司其他副职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'C票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=5,sort=3,exam_user=u'司属单位正职'))
        exam_entity = ExamEntity.query.filter_by(name=u'D票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=5,sort=4,exam_user=u'司属单位副职'))
        exam_entity = ExamEntity.query.filter_by(name=u'E票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=40,sort=5,exam_user=u'司属单位职工代表'))
        exam_system = ExamSystem.query.filter_by(name=u'基层单位正职').first()
        exam_entity = ExamEntity.query.filter_by(name=u'A票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=1,exam_user=u'公司正职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'B票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=20,sort=2,exam_user=u'公司其他副职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'C票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=0,sort=3,exam_user=u'司属单位正职'))
        exam_entity = ExamEntity.query.filter_by(name=u'D票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=4,exam_user=u'司属单位副职'))
        exam_entity = ExamEntity.query.filter_by(name=u'E票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=40,sort=5,exam_user=u'司属单位职工代表'))
        exam_system = ExamSystem.query.filter_by(name=u'基层单位副职').first()
        exam_entity = ExamEntity.query.filter_by(name=u'A票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=1,exam_user=u'公司正职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'B票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=20,sort=2,exam_user=u'公司其他副职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'C票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=3,exam_user=u'司属单位正职'))
        exam_entity = ExamEntity.query.filter_by(name=u'D票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=0,sort=4,exam_user=u'司属单位副职'))
        exam_entity = ExamEntity.query.filter_by(name=u'E票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=40,sort=5,exam_user=u'司属单位职工代表'))
        exam_system = ExamSystem.query.filter_by(name=u'机关部门领导班子').first()
        exam_entity = ExamEntity.query.filter_by(name=u'A票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=1,exam_user=u'公司正职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'B票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=2,exam_user=u'联系点（分管部门）领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'C票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=20,sort=3,exam_user=u'公司其他副职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'D票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=4,exam_user=u'公司本部正职'))
        exam_entity = ExamEntity.query.filter_by(name=u'E票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=5,exam_user=u'本部部门员工'))
        exam_system = ExamSystem.query.filter_by(name=u'机关部门正职').first()
        exam_entity = ExamEntity.query.filter_by(name=u'A票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=1,exam_user=u'公司正职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'B票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=2,exam_user=u'联系点（分管部门）领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'C票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=20,sort=3,exam_user=u'公司其他副职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'D票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=4,exam_user=u'公司本部副职'))
        exam_entity = ExamEntity.query.filter_by(name=u'E票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=5,exam_user=u'本部部门员工'))
        exam_system = ExamSystem.query.filter_by(name=u'机关部门副职').first()
        exam_entity = ExamEntity.query.filter_by(name=u'A票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=1,exam_user=u'公司正职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'B票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=2,exam_user=u'联系点（分管部门）领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'C票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=20,sort=3,exam_user=u'公司其他副职领导'))
        exam_entity = ExamEntity.query.filter_by(name=u'D票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=10,sort=4,exam_user=u'公司本部正职'))
        exam_entity = ExamEntity.query.filter_by(name=u'E票').first()
        db.session.add(ExamEntityWeight(exam_system_id=exam_system.id,exam_entity_id=exam_entity.id,weight=30,sort=5,exam_user=u'本部部门员工'))
        db.session.commit()

class Base(db.Model):
	__abstract__ = True

	def json(self):
		return { c.name:getattr(self, c.name) for c in self.__table__.columns }

class Admin(Base):
	__tablename__ = 'T_ADMIN' #管理员表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	username = db.Column(db.String(200),unique = True) #用户名
	password = db.Column(db.String(200),unique = False) #密码
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, username, password):
		self.username = username
		self.password = generate_password_hash(password)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password,password)

	def is_authenticated(self):
		return Ture

	def is_active(self):
		return Ture

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<Admin %r>' % self.username

class Exam(Base):
	__tablename__ = 'T_EXAM' #评价表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(200),unique = False) #名称
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, name, sort):
		self.name = name
		self.sort = sort

	def __repr__(self):
		return '<Exam %r>' % self.name

class ExamContent(Base):
	__tablename__ = 'T_EXAM_CONTENT' #评价内容表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	exam_id = db.Column(db.Integer, db.ForeignKey('T_EXAM.id')) #评价表ID
	exam = db.relationship('Exam', lazy='joined') #评价
	content = db.Column(db.String(200),unique = False) #内容
	sort = db.Column(db.Integer,unique = False) #显示顺序
	show = db.Column(db.Integer,unique = False) #显示
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, exam_id, content, sort, show):
		self.exam_id = exam_id
		self.content = content
		self.sort = sort
		self.show = show

	def __repr__(self):
		return '<ExamContent %r>' % self.content

	def json(self):
		return {
			'id' : self.id,
			'exam_id' : self.exam_id,
			'exam' : self.exam.json() if self.exam != None else None,
			'content' : self.content,
			'sort' : self.sort,
			'show' : self.show,
			'create_at' : self.create_at,
			'update_at' : self.update_at
		}

class ExamMeasure(Base):
	__tablename__ = 'T_EXAM_MEASURE' #评价指标表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	exam_content_id = db.Column(db.Integer, db.ForeignKey('T_EXAM_CONTENT.id')) #内容ID
	exam_content = db.relationship('ExamContent', lazy='joined') #内容
	name = db.Column(db.String(100),unique = False) #名称
	weight = db.Column(db.Float,unique = False) #权重
	sort = db.Column(db.Integer,unique = False) #显示顺序
	show = db.Column(db.Integer,unique = False) #是否显示
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, exam_content_id, name, weight, sort, show):
		self.exam_content_id = exam_content_id
		self.name = name
		self.weight = weight
		self.sort = sort
		self.show = show

	def __repr__(self):
		return '<ExamMeasure %r>' % self.name

	def json(self):
		return {
			'id' : self.id,
			'exam_content_id' : self.exam_content_id,
			'exam_content' : self.exam_content.json() if self.exam_content != None else None,
			'name' : self.name,
			'weight' : self.weight,
			'sort' : self.sort,
			'show' : self.show,
			'create_at' : self.create_at,
			'update_at' : self.update_at
		}

class ExamEntity(Base):
	__tablename__ = 'T_EXAM_ENTITY' #测评主体表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(200),unique = False) #简称
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, name, sort):
		self.name = name
		self.sort = sort

	def __repr__(self):
		return '<ExamEntity %r>' % self.name

class ExamSystem(Base):
	__tablename__ = 'T_EXAM_SYSTEM' #测评体系表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	exam_id = db.Column(db.Integer, db.ForeignKey('T_EXAM.id')) #评价表ID
	exam = db.relationship('Exam', lazy='joined') #评价
	org_type_id = db.Column(db.Integer, db.ForeignKey('T_ORG_TYPE.id')) #单位类型ID
	org_type = db.relationship('OrgType', lazy='joined') #单位类型
	manager_type_id = db.Column(db.Integer, db.ForeignKey('T_MANAGER_TYPE.id')) #人员类型ID
	manager_type = db.relationship('ManagerType', lazy='joined') #人员类型
	name = db.Column(db.String(200),unique = False) #描述
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, exam_id, org_type_id, manager_type_id, name, sort):
		self.exam_id = exam_id
		self.org_type_id = org_type_id
		self.manager_type_id = manager_type_id
		self.name = name
		self.sort = sort

	def __repr__(self):
		return '<ExamSystem %r>' % self.name

	def json(self):
		return {
			'id' : self.id,
			'exam_id' : self.exam_id,
			'exam' : self.exam.json() if self.exam != None else None,
			'org_type_id' : self.org_type_id,
			'org_type' : self.org_type.json() if self.org_type != None else None,
			'manager_type_id' : self.manager_type_id,
			'manager_type' : self.manager_type.json() if self.manager_type != None else None,
			'name' : self.name,
			'sort' : self.sort,
			'create_at' : self.create_at,
			'update_at' : self.update_at
		}

class ExamEntityWeight(Base):
	__tablename__ = 'T_EXAM_ENTITY_WEIGHT' #测评主体权重表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	exam_system_id = db.Column(db.Integer,db.ForeignKey('T_EXAM_SYSTEM.id')) #测评体系ID
	exam_system = db.relationship('ExamSystem', lazy='joined') #测评体系
	exam_entity_id = db.Column(db.Integer,db.ForeignKey('T_EXAM_ENTITY.id')) #测评主体ID
	exam_entity = db.relationship('ExamEntity', lazy='joined') #测评主体
	weight = db.Column(db.Float,unique = False) #权重
	sort = db.Column(db.Integer,unique = False) #显示顺序
	exam_user = db.Column(db.String(200),unique = False) #测评人员
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, exam_system_id,exam_entity_id,weight,sort,exam_user):
		self.exam_system_id = exam_system_id
		self.exam_entity_id = exam_entity_id
		self.weight = weight
		self.sort = sort
		self.exam_user = exam_user

	def __repr__(self):
		return '<ExamEntityWeight %r>' % self.weight

	def json(self):
		return {
			'id' : self.id,
			'exam_system_id':self.exam_system_id,
			'exam_system':self.exam_system.json() if self.exam_system != None else None,
			'exam_entity_id':self.exam_entity_id,
			'exam_entity':self.exam_entity.json() if self.exam_entity != None else None,
			'weight':self.weight,
			'sort':self.sort,
			'exam_user':self.exam_user,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class OrgType(Base):
	__tablename__ = 'T_ORG_TYPE' #单位类型表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(200),unique = False) #简称
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, name, sort):
		self.name = name
		self.sort = sort

	def __repr__(self):
		return '<OrgType %r>' % self.name

class Org(Base):
	__tablename__ = 'T_ORG' #单位表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	org_type_id = db.Column(db.Integer, db.ForeignKey('T_ORG_TYPE.id')) #单位类型ID
	org_type = db.relationship('OrgType', lazy='joined') #单位类型
	short_name = db.Column(db.String(200),unique = False) #单位简称
	full_name = db.Column(db.String(500),unique = False) #单位全称
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, org_type_id, short_name,full_name,sort):
		self.org_type_id = org_type_id
		self.short_name = short_name
		self.full_name = full_name
		self.sort = sort

	def __repr__(self):
		return '<Org %r>' % self.short_name

	def json(self):
		return {
			'id':self.id,
			'org_type_id':self.org_type_id,
			'org_type':self.org_type.json() if self.org_type != None else None,
			'short_name':self.short_name,
			'full_name':self.full_name,
			'sort':self.sort,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class TeamYearWeight(Base):
	__tablename__ = 'T_TEAM_YEAR_WEIGHT' #班子业绩权重表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	org_id = db.Column(db.Integer,db.ForeignKey('T_ORG.id')) #单位ID
	org = db.relationship('Org', lazy='joined') #单位
	year = db.Column(db.Integer,unique = False) #年度
	weight = db.Column(db.Float,unique = False) #权重
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, org_id,year,weight):
		self.org_id = org_id
		self.year = year
		self.weight = weight

	def __repr__(self):
		return '<TeamYearWeight %r>' % self.year

	def json(self):
		return {
			'id':self.id,
			'org_id':self.org_id,
			'org':self.org.json() if self.org != None else None,
			'year':self.year,
			'weight':self.weight,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class TeamScore(Base):
	__tablename__ = 'T_TEAM_SCORE' #班子业绩表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	org_id = db.Column(db.Integer,db.ForeignKey('T_ORG.id')) #单位ID
	org = db.relationship('Org', lazy='joined') #单位
	year = db.Column(db.Integer,unique = False) #年度
	exam_measure_id = db.Column(db.Integer,db.ForeignKey('T_EXAM_MEASURE.id')) #指标ID
	exam_measure = db.relationship('ExamMeasure', lazy='joined') #指标
	score = db.Column(db.Float,unique = False) #分数
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, org_id,year,exam_measure_id,score):
		self.org_id = org_id
		self.year = year
		self.exam_measure_id = exam_measure_id
		self.score = score

	def __repr__(self):
		return '<TeamScore %r>' % self.year

	def json(self):
		return {
			'id':self.id,
			'org_id':self.org_id,
			'org':self.org.json() if self.org != None else None,
			'year':self.year,
			'exam_measure_id':self.exam_measure_id,
			'exam_measure':self.exam_measure.json() if self.exam_measure != None else None,
			'score':self.score,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

# class ManagerTitle(Base):
# 	__tablename__ = 'T_MANAGER_TITLE' #职务表
# 	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
# 	name = db.Column(db.String(50),unique = False) #名称
# 	sort = db.Column(db.Integer,unique = False) #显示顺序
# 	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
# 	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
# 	def __init__(self, name, sort):
# 		self.name = name
# 		self.sort = sort

# 	def __repr__(self):
# 		return '<ManagerTitle %r>' % self.name

class ManagerType(Base):
	__tablename__ = 'T_MANAGER_TYPE' #人员类型表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(50),unique = False) #名称
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, name, sort):
		self.name = name
		self.sort = sort

	def __repr__(self):
		return '<ManagerType %r>' % self.name

class Manager(Base):
	__tablename__ = 'T_MANAGER' #中层干部表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	org_id = db.Column(db.Integer, db.ForeignKey('T_ORG.id')) #单位ID
	org = db.relationship('Org', lazy='joined') #单位
	name = db.Column(db.String(200),unique = False) #姓名
	title = db.Column(db.String(200),unique = False) #职务
	manager_type_id = db.Column(db.Integer, db.ForeignKey('T_MANAGER_TYPE.id')) #人员类型ID
	manager_type = db.relationship('ManagerType', lazy='joined') #人员类型
	# manager_title_id = db.Column(db.Integer, db.ForeignKey('T_MANAGER_TITLE.id')) #职务ID
	# manager_title = db.relationship('ManagerTitle', lazy='joined') #职务
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	# def __init__(self, org_id,name,manager_type_id,manager_title_id,sort):
	def __init__(self, org_id,name,title,manager_type_id,sort):
		self.org_id = org_id
		self.name = name
		self.title = title
		self.manager_type_id = manager_type_id
		# self.manager_title_id = manager_title_id
		self.sort = sort

	def __repr__(self):
		return '<Manager %r>' % self.name

	def json(self):
		return {
			'id':self.id,
			'org_id':self.org_id,
			'org':self.org.json() if self.org != None else None,
			'name':self.name,
			'title':self.title,
			'manager_type_id':self.manager_type_id,
			'manager_type':self.manager_type.json() if self.manager_type != None else None,
			# 'manager_title_id':self.manager_title_id,
			# 'manager_title':self.manager_title.json() if self.manager_title != None else None,
			'sort':self.sort,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class ManagerYearWeight(Base):
	__tablename__ = 'T_MANAGER_YEAR_WEIGHT' #中层干部年度权重表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	manager_id = db.Column(db.Integer,db.ForeignKey('T_MANAGER.id')) #中层干部ID
	manager = db.relationship('Manager', lazy='joined') #中层干部
	year = db.Column(db.Integer,unique = False) #年度
	weight = db.Column(db.Float,unique = False) #权重
	sort = db.Column(db.Integer,unique = False) #显示顺序
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, manager_id,year,weight,sort):
		self.manager_id = manager_id
		self.year = year
		self.weight = weight
		self.sort = sort

	def __repr__(self):
		return '<TeamYearWeight %r>' % self.year

	def json(self):
		return {
			'id':self.id,
			'manager_id':self.manager_id,
			'manager':self.manager.json() if self.manager != None else None,
			'year':self.year,
			'weight':self.weight,
			'sort':self.sort,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class ExamResultManager(Base):
	__tablename__ = 'T_EXAM_RESULT_MANAGER' #中层干部投票数据表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	exam_measure_id = db.Column(db.Integer, db.ForeignKey('T_EXAM_MEASURE.id')) #指标ID
	exam_measure = db.relationship('ExamMeasure', lazy='joined') #指标
	year = db.Column(db.Integer,unique = False) #年度
	manager_id = db.Column(db.Integer, db.ForeignKey('T_MANAGER.id')) #中层干部ID
	manager = db.relationship('Manager', lazy='joined') #中层干部
	exam_entity_id = db.Column(db.Integer, db.ForeignKey('T_EXAM_ENTITY.id')) #测评主体ID
	exam_entity = db.relationship('ExamEntity', lazy='joined') #测评主体
	score = db.Column(db.Integer,unique = False) #分数
	validity = db.Column(db.Integer,unique = False) #是否有效
	image_path = db.Column(db.String(500),unique = False) #扫描图片路径
	scan_result = db.Column(db.Text,unique = False) #扫描结果
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, image_path,scan_result,exam_measure_id,year,manager_id,exam_entity_id,score,validity):
		self.exam_measure_id = exam_measure_id
		self.year = year
		self.manager_id = manager_id
		self.exam_entity_id = exam_entity_id
		self.score = score
		self.validity = validity
		self.image_path = image_path
		self.scan_result = scan_result

	def __repr__(self):
		return '<ExamResultManager %r>' % self.year

	def json(self):
		return {
			'id':self.id,
			'exam_measure_id':self.exam_measure_id,
			'exam_measure':self.exam_measure.json() if self.exam_measure != None else None,
			'year':self.year,
			'manager_id':self.manager_id,
			'manager':self.manager.json() if self.manager != None else None,
			'exam_entity_id':self.exam_entity_id,
			'exam_entity':self.exam_entity.json() if self.exam_entity != None else None,
			'score':self.score,
			'validity':self.validity,
			'image_path':self.image_path,
			'scan_result':self.scan_result,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class ExamResultTeam(Base):
	__tablename__ = 'T_EXAM_RESULT_TEAM' #班子投票数据表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	exam_measure_id = db.Column(db.Integer, db.ForeignKey('T_EXAM_MEASURE.id')) #指标ID
	exam_measure = db.relationship('ExamMeasure', lazy='joined') #指标
	year = db.Column(db.Integer,unique = False) #年度
	org_id = db.Column(db.Integer, db.ForeignKey('T_ORG.id')) #单位ID
	org = db.relationship('Org', lazy='joined') #单位
	exam_entity_id = db.Column(db.Integer, db.ForeignKey('T_EXAM_ENTITY.id')) #主体ID
	exam_entity = db.relationship('ExamEntity', lazy='joined') #主体
	score = db.Column(db.Float,unique = False) #分数
	validity = db.Column(db.Integer,unique = False) #是否有效
	image_path = db.Column(db.String(500),unique = False) #扫描图片路径
	scan_result = db.Column(db.Text,unique = False) #扫描结果
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self, image_path,scan_result,exam_measure_id,year,org_id,exam_entity_id,score,validity):
		self.exam_measure_id = exam_measure_id
		self.year = year
		self.org_id = org_id
		self.exam_entity_id = exam_entity_id
		self.score = score
		self.validity = validity
		self.image_path = image_path
		self.scan_result = scan_result

	def __repr__(self):
		return '<ExamResultTeam %r>' % self.year

	def json(self):
		return {
			'id':self.id,
			'exam_measure_id':self.exam_measure_id,
			'exam_measure':self.exam_measure.json() if self.exam_measure != None else None,
			'year':self.year,
			'org_id':self.org_id,
			'org':self.org.json() if self.org != None else None,
			'exam_entity_id':self.exam_entity_id,
			'exam_entity':self.exam_entity.json() if self.exam_entity != None else None,
			'score':self.score,
			'validity':self.validity,
			'image_path':self.image_path,
			'scan_result':self.scan_result,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class TeamExamScore(Base):
	__tablename__ = 'T_TEAM_EXAM_SCORE' #总分表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	org_id = db.Column(db.Integer,db.ForeignKey('T_ORG.id')) #单位ID
	org = db.relationship('Org', lazy='joined') #单位
	year = db.Column(db.Integer,unique = False) #年度
	org_score = db.Column(db.Float,unique = False) #考评得分
	org_sum_score = db.Column(db.Float,unique = False) #汇总得分
	dj_score = db.Column(db.Float,unique = False) #企业党建分数
	yj_score = db.Column(db.Float,unique = False) #班子业绩分数
	content_score_1 = db.Column(db.Float,unique = False) #小计1(政治素质)
	content_score_2 = db.Column(db.Float,unique = False) #小计2(经营业绩)
	content_score_3 = db.Column(db.Float,unique = False) #小计3(团结协作)
	content_score_4 = db.Column(db.Float,unique = False) #小计4(作风形象)
	measure_score_4 = db.Column(db.Float,unique = False) #政治方向分数
	measure_score_5 = db.Column(db.Float,unique = False) #社会责任分数
	measure_score_6 = db.Column(db.Float,unique = False) #可持续发展分数
	measure_score_7 = db.Column(db.Float,unique = False) #创新成效分数
	measure_score_8 = db.Column(db.Float,unique = False) #科学管理分数
	measure_score_9 = db.Column(db.Float,unique = False) #发扬民主分数
	measure_score_10 = db.Column(db.Float,unique = False) #整体合力分数
	measure_score_11 = db.Column(db.Float,unique = False) #诚信务实分数
	measure_score_12 = db.Column(db.Float,unique = False) #联系群众分数
	measure_score_13 = db.Column(db.Float,unique = False) #廉洁自律分数
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self,org_id,year,org_score,org_sum_score,dj_score,yj_score,content_score_1,content_score_2,content_score_3,content_score_4,
	measure_score_4,measure_score_5,measure_score_6,measure_score_7,measure_score_8,measure_score_9,measure_score_10,measure_score_11,measure_score_12,measure_score_13):
		self.org_id = org_id
		self.year = year
		self.org_score = org_score
		self.org_sum_score = org_sum_score
		self.dj_score = dj_score
		self.yj_score = yj_score
		self.content_score_1 = content_score_1
		self.content_score_2 = content_score_2
		self.content_score_3 = content_score_3
		self.content_score_4 = content_score_4
		self.measure_score_4 = measure_score_4
		self.measure_score_5 = measure_score_5
		self.measure_score_6 = measure_score_6
		self.measure_score_7 = measure_score_7
		self.measure_score_8 = measure_score_8
		self.measure_score_9 = measure_score_9
		self.measure_score_10 = measure_score_10
		self.measure_score_11 = measure_score_11
		self.measure_score_12 = measure_score_12
		self.measure_score_13 = measure_score_13

	def __repr__(self):
		return '<TeamExamScore %r>' % self.year

	def json(self):
		return {
			'id':self.id,
			'org_id':self.org_id,
			'org':self.org.json() if self.org != None else None,
			'year':self.year,
			'org_score':self.org_score,
			'org_sum_score':self.org_sum_score,
			'dj_score':self.dj_score,
			'yj_score':self.yj_score,
			'content_score_1':self.content_score_1,
			'content_score_2':self.content_score_2,
			'content_score_3':self.content_score_3,
			'content_score_4':self.content_score_4,
			'measure_score_4':self.measure_score_4,
			'measure_score_5':self.measure_score_5,
			'measure_score_6':self.measure_score_6,
			'measure_score_7':self.measure_score_7,
			'measure_score_8':self.measure_score_8,
			'measure_score_9':self.measure_score_9,
			'measure_score_10':self.measure_score_10,
			'measure_score_11':self.measure_score_11,
			'measure_score_12':self.measure_score_12,
			'measure_score_13':self.measure_score_13,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

class ManagerExamScore(Base):
	__tablename__ = 'T_MANAGER_EXAM_SCORE' #总分表
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	manager_id = db.Column(db.Integer,db.ForeignKey('T_ORG.id')) #单位ID
	manager = db.relationship('Org', lazy='joined') #单位
	year = db.Column(db.Integer,unique = False) #年度
	manager_score = db.Column(db.Float,unique = False) #考评得分
	manager_sum_score = db.Column(db.Float,unique = False) #汇总得分
	org_sum_score = db.Column(db.Float,unique = False) #部门业绩得分
	content_score_6 = db.Column(db.Float,unique = False) #小计1(素质)
	content_score_7 = db.Column(db.Float,unique = False) #小计2(能力)
	content_score_8 = db.Column(db.Float,unique = False) #小计3(业绩)
	measure_score_14 = db.Column(db.Float,unique = False) #政治素质分数
	measure_score_15 = db.Column(db.Float,unique = False) #职业素养分数
	measure_score_16 = db.Column(db.Float,unique = False) #廉洁自律分数
	measure_score_17 = db.Column(db.Float,unique = False) #决策能力分数
	measure_score_18 = db.Column(db.Float,unique = False) #执行能力分数
	measure_score_19 = db.Column(db.Float,unique = False) #领导能力分数
	measure_score_20 = db.Column(db.Float,unique = False) #学习能力分数
	measure_score_21 = db.Column(db.Float,unique = False) #创新能力分数
	measure_score_22 = db.Column(db.Float,unique = False) #沟通能力分数
	measure_score_23 = db.Column(db.Float,unique = False) #内控管理分数
	measure_score_24 = db.Column(db.Float,unique = False) #履职绩效分数
	create_at = db.Column(db.DateTime(timezone=True),server_default=db.func.now()) #创建时间
	update_at = db.Column(db.DateTime(timezone=True),onupdate=db.func.now(), server_onupdate=db.func.now()) #更新时间
	def __init__(self,manager_id,year,manager_score,manager_sum_score,org_sum_score,content_score_6,content_score_7,content_score_8,
	measure_score_14,measure_score_15,measure_score_16,measure_score_17,measure_score_18,measure_score_19,measure_score_20,measure_score_21,measure_score_22,measure_score_23,measure_score_24):
		self.manager_id = manager_id
		self.year = year
		self.manager_score = manager_score
		self.manager_sum_score = manager_sum_score
		self.org_sum_score = org_sum_score
		self.content_score_6 = content_score_6
		self.content_score_7 = content_score_7
		self.content_score_8 = content_score_8
		self.measure_score_14 = measure_score_14
		self.measure_score_15 = measure_score_15
		self.measure_score_16 = measure_score_16
		self.measure_score_17 = measure_score_17
		self.measure_score_18 = measure_score_18
		self.measure_score_19 = measure_score_19
		self.measure_score_20 = measure_score_20
		self.measure_score_21 = measure_score_21
		self.measure_score_22 = measure_score_22
		self.measure_score_23 = measure_score_23
		self.measure_score_24 = measure_score_24

	def __repr__(self):
		return '<ManagerExamScore %r>' % self.year

	def json(self):
		return {
			'id':self.id,
			'manager_id':self.manager_id,
			'manager':self.manager.json() if self.manager != None else None,
			'year':self.year,
			'manager_score':self.manager_score,
			'manager_sum_score':self.manager_sum_score,
			'org_sum_score':self.org_sum_score,
			'content_score_6':self.content_score_6,
			'content_score_7':self.content_score_7,
			'content_score_8':self.content_score_8,
			'measure_score_14':self.measure_score_14,
			'measure_score_15':self.measure_score_15,
			'measure_score_16':self.measure_score_16,
			'measure_score_17':self.measure_score_17,
			'measure_score_18':self.measure_score_18,
			'measure_score_19':self.measure_score_19,
			'measure_score_20':self.measure_score_20,
			'measure_score_21':self.measure_score_21,
			'measure_score_22':self.measure_score_22,
			'measure_score_23':self.measure_score_23,
			'measure_score_24':self.measure_score_24,
			'create_at':self.create_at,
			'update_at':self.update_at
		}

login = LoginManager(app)

@app.before_first_request
def before_first_request():
	load()

@login.user_loader
def load_user(id):
	return Admin.query.filter_by(id=id).first()

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    return response

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def do_get(path):
    return render_template("index.html")

@app.route('/api/v1/verify', methods=['POST'])
def do_verify():
	if (request.form['username'] and request.form['password']):
		admin = Admin.query.filter_by(username=request.form['username']).first()
		if (admin and admin.check_password(request.form['password'])):
			login_user(admin)
			admin_json = admin.json()
			del (admin_json['password'])
			return jsonify({'success':1,'admin':admin_json})
	return jsonify(success=0)

@app.route('/api/v1/<model>', methods=['GET'])
@login_required
def do_list(model):
	# print(model)
	list = []
	success = 0
	message = None
	# page = int(request.args.get('page', '1'))
	# size = int(request.args.get('size', '10'))
	try:
		if(model=='exam'):
			list = Exam.query.order_by(Exam.sort).all()
			success = 1
		elif(model=='exam_content'):
			exam_id = int(request.args.get('exam_id', '0'))
			list = ExamContent.query.filter_by(exam_id=exam_id).order_by(ExamContent.sort).all()
			success = 1
		elif(model=='exam_measure'):
			exam_id = int(request.args.get('exam_id', '0'))
			list = ExamMeasure.query.join(ExamMeasure.exam_content).filter(ExamContent.exam_id==exam_id).filter_by(show=1).order_by(ExamMeasure.sort).all()
			success = 1
		elif(model=='exam_entity'):
			list = ExamEntity.query.order_by(ExamEntity.sort).all()
			success = 1
		elif(model=='exam_system'):
			list = ExamSystem.query.order_by(ExamSystem.sort).all()
			success = 1
		elif(model=='exam_entity_weight'):
			exam_system_id = int(request.args.get('exam_system_id', '0'))
			list = ExamEntityWeight.query.filter_by(exam_system_id=exam_system_id).order_by(ExamEntityWeight.sort).all()
			success = 1
		elif(model=='org_type'):
			list = OrgType.query.order_by(OrgType.sort).all()
			success = 1
		elif(model=='org'):
			org_type_id = int(request.args.get('org_type_id', '0'))
			if org_type_id == 0:
				list = Org.query.order_by(Org.sort).all()
			else:
				list = Org.query.filter_by(org_type_id=org_type_id).order_by(Org.sort).all()
			success = 1
		elif(model=='team_year_weight'):
			org_id = int(request.args.get('org_id', '0'))
			list = TeamYearWeight.query.filter_by(org_id=org_id).order_by(TeamYearWeight.year.desc()).all()
			success = 1
		elif(model=='team_score'):
			org_id = int(request.args.get('org_id', '0'))
			list = TeamScore.query.filter_by(org_id=org_id).order_by(TeamScore.year.desc()).all()
			success = 1
		# elif(model=='manager_title'):
		# 	list = ManagerTitle.query.order_by(ManagerTitle.sort).all()
		# 	success = 1
		elif(model=='manager_type'):
			list = ManagerType.query.order_by(ManagerType.sort).all()
			success = 1
		elif(model=='manager'):
			org_id = int(request.args.get('org_id', '0'))
			org_type_id = int(request.args.get('org_type_id', '0'))
			search_name = request.args.get('search_name', None)
			if search_name != None:
				list = Manager.query.filter(Manager.name.like('%'+search_name+'%')).order_by(Manager.sort).all()
			else:
				if org_id == 0:
					if org_type_id == 0:
						list = Manager.query.order_by(Manager.org_id.asc(),Manager.sort.asc()).all()
					else:
						list = Manager.query.join(Manager.org).filter(Org.org_type_id==org_type_id).order_by(Manager.sort).all()
				else:
					list = Manager.query.filter_by(org_id=org_id).order_by(Manager.sort).all()
			# if org_id == 0:
			# 	if org_type_id == 0:
			# 		if search_name != None:
			# 			list = Manager.query.filter_by(org_id=org_id).filter(Manager.name.like('%'+search_name+'%')).order_by(Manager.sort).all()
			# 		else:
			# 			list = Manager.query.order_by(Manager.org_id.asc(),Manager.sort.asc()).all()
			# 	else:
			# 		if search_name != None:
			# 			list = Manager.query.join(Manager.org).filter(Org.org_type_id==org_type_id).filter(Manager.name.like('%'+search_name+'%')).order_by(Manager.sort).all()
			# 		else:
			# 			list = Manager.query.join(Manager.org).filter(Org.org_type_id==org_type_id).order_by(Manager.sort).all()
			# else:
			# 	if search_name != None:
			# 		list = Manager.query.filter_by(org_id=org_id).filter(Manager.name.like('%'+search_name+'%')).order_by(Manager.sort).all()
			# 	else:
			# 		list = Manager.query.filter_by(org_id=org_id).order_by(Manager.sort).all()
			success = 1
		elif(model=='manager_year_weight'):
			manager_id = int(request.args.get('manager_id', '0'))
			list = ManagerYearWeight.query.filter_by(manager_id=manager_id).order_by(ManagerYearWeight.year.desc()).all()
			success = 1
		elif(model=='exam_result_manager'):
			year = int(request.args.get('year', 0))
			org_id = int(request.args.get('org_id', 0))
			# manager_id = int(request.args.get('manager_id', '0'))
			exam_entity_id = int(request.args.get('exam_entity_id', 0))
			list = ExamResultManager.query.join(ExamResultManager.manager).filter(Manager.org_id==org_id).filter(ExamResultManager.year==year).filter(ExamResultManager.exam_entity_id==exam_entity_id).order_by(ExamResultManager.manager_id,ExamResultManager.exam_measure_id).all()
			success = 1
		elif(model=='exam_result_manager_year'):
			manager_id = int(request.args.get('manager_id', '0'))
			years = db.session.query(ExamResultManager.year).distinct().filter_by(manager_id=manager_id).all()
			list = []
			for year in years:
				for y in year:
					list.append(y)
			success = 1
			return jsonify(success=success,list=list,message=message)
		elif(model=='exam_result_manager_all_year'):
			years = db.session.query(ExamResultManager.year).distinct().all()
			# list =  db.session.query(ExamResultManager.year,Manager.org_id).join(Manager.org).group_by(ExamResultManager.year,Manager.org_id).all()
			list = []
			for year in years:
				for y in year:
					list.append(y)
			success = 1
			return jsonify(success=success,list=list,message=message)
		elif(model=='exam_result_team_year'):
			org_id = int(request.args.get('org_id', '0'))
			years = db.session.query(ExamResultTeam.year).distinct().filter_by(org_id=org_id).all()
			list = []
			for year in years:
				for y in year:
					list.append(y)
			success = 1
			return jsonify(success=success,list=list,message=message)
		elif(model=='exam_result_team'):
			year = int(request.args.get('year', '0'))
			org_id = int(request.args.get('org_id', '0'))
			exam_entity_id = int(request.args.get('exam_entity_id', '0'))
			list = ExamResultTeam.query.filter_by(year=year,org_id=org_id,exam_entity_id=exam_entity_id).order_by(ExamResultTeam.exam_measure_id).all()
			success = 1
		elif(model=='exam_result_team_score'):
			org_id = int(request.args.get('org_id', '0'))
			list = TeamExamScore.query.filter_by(org_id=org_id).all()
			success = 1
	except:
		success = 0
	else:
		pass
		
	return jsonify(success=success,list=[i.json() for i in list],message=message)

@app.route('/api/v1/<model>/<id>', methods=['GET'])
@login_required
def do_view(model,id):
	# print(model,id)
	success = 0
	view = None
	message = None
	if(model=='exam'):
		if(id!=None):
			view = Exam.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_content'):
		if(id!=None):
			view = ExamContent.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_measure'):
		if(id!=None):
			view = ExamMeasure.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_entity'):
		if(id!=None):
			view = ExamEntity.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_system'):
		if(id!=None):
			view = ExamSystem.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_entity_weight'):
		exam_system_id = request.form.get('exam_system_id', None)
		exam_entity_id = request.form.get('exam_entity_id', None)
		if(exam_system_id!=None and exam_entity_id!=None):
			view = ExamEntityWeight.query.filter_by(exam_system_id=exam_system_id,exam_entity_id=exam_entity_id).first()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='org_type'):
		if(id!=None):
			view = OrgType.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='org'):
		if(id!=None):
			view = Org.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='team_year_weight'):
		org_id = request.form.get('org_id', None)
		year = request.form.get('year', None)
		if(org_id!=None and year!=None):
			view = TeamYearWeight.query.filter_by(org_id=org_id,year=year).first()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='team_score'):
		org_id = request.form.get('org_id', None)
		year = request.form.get('year', None)
		exam_measure_id = request.form.get('exam_measure_id', None)
		if(org_id!=None and year!=None and exam_measure_id!=None):
			view = TeamScore.query.filter_by(org_id=org_id,exam_measure_id=exam_measure_id,year=year).first()
			success = 1
		else:
			success = 0
			message = '数据为空'
	# elif(model=='manager_title'):
	# 	if(id!=None):
	# 		view = ManagerTitle.query.get(id)
	# 		success = 1
	# 	else:
	# 		success = 0
	# 		message = '数据为空'
	elif(model=='manager_type'):
		if(id!=None):
			view = ManagerType.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='manager'):
		if(id!=None):
			view = Manager.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='manager_year_weight'):
		manager_id = request.form.get('manager_id', None)
		year = request.form.get('year', None)
		if(manager_id!=None and year!=None):
			view = ManagerYearWeight.query.filter_by(manager_id=manager_id,year=year).first()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_result_manager'):
		if(id!=None):
			view = ExamResultManager.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_result_team'):
		if(id!=None):
			view = ExamResultTeam.query.get(id)
			success = 1
		else:
			success = 0
			message = '数据为空'
	return jsonify(success=success,view=view.json(),message=message)

@app.route('/api/v1/<model>', methods=['POST'])
@login_required
def do_add(model):
	# print(model)
	success = 0
	message = None
	if(model=='exam'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(name!=None):
			db.session.add(Exam(name=name,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_content'):
		exam_id = request.form.get('exam_id', None)
		content = request.form.get('content', None)
		sort = request.form.get('sort', None)
		if(content!=None):
			db.session.add(ExamContent(exam_id=exam_id,content=content,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_measure'):
		exam_content_id = request.form.get('exam_content_id', None)
		name = request.form.get('name', None)
		weight = request.form.get('weight', None)
		sort = request.form.get('sort', None)
		if(name!=None):
			db.session.add(ExamMeasure(exam_content_id=exam_content_id,name=name,weight=weight,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_entity'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(name!=None):
			db.session.add(ExamEntity(name=name,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_system'):
		exam_id = request.form.get('exam_id', None)
		org_type_id = request.form.get('org_type_id', None)
		manager_type_id = request.form.get('manager_type_id', None)
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(name!=None):
			db.session.add(ExamSystem(exam_id=exam_id,org_type_id=org_type_id,manager_type_id=manager_type_id,name=name,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_entity_weight'):
		exam_system_id = request.form.get('exam_system_id', None)
		exam_entity_id = request.form.get('exam_entity_id', None)
		weight = request.form.get('weight', None)
		sort = request.form.get('sort', None)
		if(weight!=None):
			db.session.add(ExamEntityWeight(exam_system_id=exam_system_id,exam_entity_id=exam_entity_id,weight=weight,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='org_type'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(name!=None):
			db.session.add(OrgType(name=name,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='org'):
		org_type_id = request.form.get('org_type_id', None)
		short_name = request.form.get('short_name', None)
		full_name = request.form.get('full_name', None)
		sort = request.form.get('sort', None)
		if(short_name!=None):
			db.session.add(Org(org_type_id=org_type_id,short_name=short_name,full_name=full_name,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='team_year_weight'):
		org_id = request.form.get('org_id', None)
		if(org_id!=None):
			team_year_weights = TeamYearWeight.query.filter_by(org_id=org_id).order_by(TeamYearWeight.year.desc()).all()
			if(len(team_year_weights)==1):
				previous_team_year_weight = team_year_weights[0]

				year = previous_team_year_weight.year - 1
				if previous_team_year_weight.year != datetime.now().year:
					year = datetime.now().year
				weight = 50
				db.session.add(TeamYearWeight(org_id=org_id,year=year,weight=weight))

				previous_team_year_weight.weight = 50
			elif(len(team_year_weights)==2):
				previous_previous_team_year_weight = team_year_weights[0]
				previous_team_year_weight = team_year_weights[1]

				year = previous_team_year_weight.year - 1
				if previous_previous_team_year_weight.year != datetime.now().year:
					year = datetime.now().year
				weight = 30

				db.session.add(TeamYearWeight(org_id=org_id,year=year,weight=weight))

				previous_previous_team_year_weight.weight = 40

				previous_team_year_weight.weight = 30
			else:
				year = datetime.now().year
				weight = 100
				db.session.add(TeamYearWeight(org_id=org_id,year=year,weight=weight))

			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='team_score'):
		pass
		# org_id = request.form.get('org_id', None)
		# year = request.form.get('year', None)
		# exam_measure_id = request.form.get('exam_measure_id', None)
		# score = request.form.get('score', None)
		# if(score!=None):
		# 	db.session.add(TeamScore(exam_id=exam_id,content=content,sort=sort))
		# 	db.session.commit()
		# 	success = 1
		# else:
		# 	success = 0
		# 	message = '数据为空'
	# elif(model=='manager_title'):
	# 	name = request.form.get('name', None)
	# 	sort = request.form.get('sort', None)
	# 	if(name!=None):
	# 		db.session.add(ManagerTitle(name=name,sort=sort))
	# 		db.session.commit()
	# 		success = 1
	# 	else:
	# 		success = 0
	# 		message = '数据为空'
	elif(model=='manager_type'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(name!=None):
			db.session.add(ManagerType(name=name,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='manager'):
		org_id = request.form.get('org_id', None)
		name = request.form.get('name', None)
		title = request.form.get('title', None)
		manager_type_id = request.form.get('manager_type_id', None)
		# manager_title_id = request.form.get('manager_title_id', None)
		sort = request.form.get('sort', None)
		if(name!=None):
			# db.session.add(Manager(org_id=org_id,name=name,manager_type_id=manager_type_id,manager_title_id=manager_title_id,sort=sort))
			db.session.add(Manager(org_id=org_id,name=name,manager_type_id=manager_type_id,title=title,sort=sort))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='manager_year_weight'):
		manager_id = request.form.get('manager_id', None)
		year = request.form.get('year', None)
		weight = request.form.get('weight', None)
		sort = request.form.get('sort', None)
		if(weight!=None):
			manager_year_weights = ManagerYearWeight.query.filter_by(manager_id=manager_id).order_by(ManagerYearWeight.year.desc()).all()
			if(len(manager_year_weights)==1):
				previous_manager_year_weight = manager_year_weights[0]

				year = previous_manager_year_weight.year - 1
				if previous_manager_year_weight.year != datetime.now().year:
					year = datetime.now().year
				weight = 50
				db.session.add(ManagerYearWeight(manager_id=manager_id,year=year,weight=weight,sort=sort))

				previous_manager_year_weight.weight = 50
			elif(len(manager_year_weights)==2):
				previous_previous_manager_year_weight = manager_year_weights[0]
				previous_manager_year_weight = manager_year_weights[1]

				year = previous_manager_year_weight.year - 1
				if previous_previous_manager_year_weight.year != datetime.now().year:
					year = datetime.now().year
				weight = 30

				db.session.add(ManagerYearWeight(manager_id=manager_id,year=year,weight=weight,sort=sort))

				previous_previous_manager_year_weight.weight = 40

				previous_manager_year_weight.weight = 30
			else:
				year = datetime.now().year
				weight = 100
				db.session.add(ManagerYearWeight(manager_id=manager_id,year=year,weight=weight,sort=sort))

			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_result_manager'):
		image_path = request.form.get('image_path', None)
		scan_result = request.form.get('scan_result', None)
		exam_measure_id = request.form.get('exam_measure_id', None)
		year = request.form.get('year', None)
		manager_id = request.form.get('manager_id', None)
		exam_entity_id = request.form.get('exam_entity_id', None)
		score = request.form.get('score', None)
		if(score!=None):
			db.session.add(ExamResultManager(image_path=image_path,scan_result=scan_result,exam_measure_id=exam_measure_id,year=year,manager_id=manager_id,exam_entity_id=exam_entity_id,score=score))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_result_team'):
		image_path = request.form.get('image_path', None)
		scan_result = request.form.get('scan_result', None)
		exam_measure_id = request.form.get('exam_measure_id', None)
		year = request.form.get('year', None)
		org_id = request.form.get('org_id', None)
		exam_entity_id = request.form.get('exam_entity_id', None)
		score = request.form.get('score', None)
		if(score!=None):
			db.session.add(ExamResultTeam(image_path=image_path,scan_result=scan_result,exam_measure_id=exam_measure_id,year=year,org_id=org_id,exam_entity_id=exam_entity_id,score=score))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	return jsonify(success=success,message=message)

@app.route('/api/v1/<model>/<id>', methods=['POST'])
@login_required
def do_update(model,id):
	# print(model,id)
	success = 0
	message = None
	if(model=='exam'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			exam = Exam.query.get(id)
			if(name!=None):
				exam.name = name
			if(sort!=None):
				exam.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_content'):
		exam_id = request.form.get('exam_id', None)
		content = request.form.get('content', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			exam_content = ExamContent.query.get(id)
			if(exam_id!=None):
				exam_content.exam_id = exam_id
			if(content!=None):
				exam_content.content = content
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_measure'):
		exam_content_id = request.form.get('exam_content_id', None)
		name = request.form.get('name', None)
		weight = request.form.get('weight', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			exam_measure = ExamMeasure.query.get(id)
			if(exam_content_id!=None):
				exam_measure.exam_content_id = exam_content_id
			if(name!=None):
				exam_measure.name = name
			if(weight!=None):
				exam_measure.weight = weight
			if(sort!=None):
				exam_measure.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_entity'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			exam_entity = ExamEntity.query.get(id)
			if(name!=None):
				exam_entity.name = name
			if(sort!=None):
				exam_entity.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_system'):
		exam_id = request.form.get('exam_id', None)
		org_type_id = request.form.get('org_type_id', None)
		manager_type_id = request.form.get('manager_type_id', None)
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			exam_system = ExamSystem.query.get(id)
			if(exam_id!=None):
				exam_system.exam_id = exam_id
			if(org_type_id!=None):
				exam_system.org_type_id = org_type_id
			if(manager_type_id!=None):
				exam_system.manager_type_id = manager_type_id
			if(name!=None):
				exam_system.name = name
			if(sort!=None):
				exam_system.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_entity_weight'):
		exam_system_id = request.form.get('exam_system_id', None)
		exam_entity_id = request.form.get('exam_entity_id', None)
		weight = request.form.get('weight', None)
		sort = request.form.get('sort', None)
		if(exam_system_id!=None and exam_entity_id!=None):
			exam_entity_weight = ExamEntityWeight.query.filter_by(exam_system_id=exam_system_id,exam_entity_id=exam_entity_id).first()
			if(exam_system_id!=None):
				exam_entity_weight.exam_system_id = exam_system_id
			if(exam_entity_id!=None):
				exam_entity_weight.exam_entity_id = exam_entity_id
			if(weight!=None):
				exam_entity_weight.weight = weight
			if(sort!=None):
				exam_entity_weight.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='org_type'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			org_type = OrgType.query.get(id)
			if(name!=None):
				org_type.name = name
			if(sort!=None):
				org_type.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='org'):
		org_type_id = request.form.get('org_type_id', None)
		short_name = request.form.get('short_name', None)
		full_name = request.form.get('full_name', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			org = Org.query.get(id)
			if(org_type_id!=None):
				org.org_type_id = org_type_id
			if(short_name!=None):
				org.short_name = short_name
			if(full_name!=None):
				org.full_name = full_name
			if(sort!=None):
				org.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='team_year_weight'):
		org_id = request.form.get('org_id', None)
		year = request.form.get('year', None)
		weight = request.form.get('weight', None)
		score_1 = request.form.get('score_1', None)
		score_2 = request.form.get('score_2', None)
		if(org_id!=None and year!=None):
			team_year_weight = TeamYearWeight.query.filter_by(org_id=org_id,year=year).first()
			if team_year_weight==None:
				db.session.add(TeamYearWeight(org_id=org_id,year=year,weight=weight))
				team_year_weight = TeamYearWeight.query.filter_by(org_id=org_id,year=year).first()
			if(weight!=None):
				team_year_weight.weight = weight
			if(score_1!=None):
				exam_content = ExamContent.query.filter_by(content=u'业绩考核').first()
				exam_measure = ExamMeasure.query.filter_by(exam_content_id=exam_content.id,name=u'企业党建').first()
				team_score = TeamScore.query.filter_by(org_id=org_id,year=year,exam_measure_id=exam_measure.id).first()
				if(team_score!=None):
					team_score.score = score_1
				else:
					db.session.add(TeamScore(org_id=org_id,year=year,exam_measure_id=exam_measure.id,score=score_1))
			if(score_2!=None):
				exam_content = ExamContent.query.filter_by(content=u'业绩考核').first()
				exam_measure = ExamMeasure.query.filter_by(exam_content_id=exam_content.id,name=u'绩效成果').first()
				team_score = TeamScore.query.filter_by(org_id=org_id,year=year,exam_measure_id=exam_measure.id).first()
				if(team_score!=None):
					team_score.score = score_2
				else:
					db.session.add(TeamScore(org_id=org_id,year=year,exam_measure_id=exam_measure.id,score=score_2))
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='team_score'):
		pass
		# org_id = request.form.get('org_id', None)
		# year = request.form.get('year', None)
		# exam_measure_id = request.form.get('exam_measure_id', None)
		# score = request.form.get('score', None)
		# if(org_id!=None and year!=None and exam_measure_id!=None):
		# 	team_score = TeamScore.query.filter_by(org_id=org_id,exam_measure_id=exam_measure_id,year=year).first()
		# 	if(org_id!=None):
		# 		team_score.org_id = org_id
		# 	if(year!=None):
		# 		team_score.year = year
		# 	if(exam_measure_id!=None):
		# 		team_score.exam_measure_id = exam_measure_id
		# 	if(score!=None):
		# 		team_score.score = score
		# 	db.session.commit()
		# 	success = 1
		# else:
		# 	success = 0
		# 	message = '数据为空'
	# elif(model=='manager_title'):
	# 	name = request.form.get('name', None)
	# 	sort = request.form.get('sort', None)
	# 	if(id!=None):
	# 		manager_title = ManagerTitle.query.get(id)
	# 		if(name!=None):
	# 			manager_title.name = name
	# 		if(sort!=None):
	# 			manager_title.sort = sort
	# 		db.session.commit()
	# 		success = 1
	# 	else:
	# 		success = 0
	# 		message = '数据为空'
	elif(model=='manager_type'):
		name = request.form.get('name', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			manager_type = ManagerType.query.get(id)
			if(name!=None):
				manager_type.name = name
			if(sort!=None):
				manager_type.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='manager'):
		org_id = request.form.get('org_id', None)
		name = request.form.get('name', None)
		title = request.form.get('title', None)
		manager_type_id = request.form.get('manager_type_id', None)
		# manager_title_id = request.form.get('manager_title_id', None)
		sort = request.form.get('sort', None)
		if(id!=None):
			manager = Manager.query.get(id)
			if(org_id!=None):
				manager.org_id = org_id
			if(name!=None):
				manager.name = name
			if(title!=None):
				manager.title = title
			if(manager_type_id!=None):
				manager.manager_type_id = manager_type_id
			# if(manager_title_id!=None):
			# 	manager.manager_title_id = manager_title_id
			if(sort!=None):
				manager.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='manager_year_weight'):
		manager_id = request.form.get('manager_id', None)
		year = request.form.get('year', None)
		weight = request.form.get('weight', None)
		sort = request.form.get('sort', None)
		if(manager_id!=None and year!=None):
			manager_year_weight = ManagerYearWeight.query.filter_by(manager_id=manager_id,year=year).first()
			if(manager_id!=None):
				manager_year_weight.manager_id = manager_id
			if(year!=None):
				manager_year_weight.year = year
			if(weight!=None):
				manager_year_weight.weight = weight
			if(sort!=None):
				manager_year_weight.sort = sort
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_result_manager'):
		image_path = request.form.get('image_path', None)
		scan_result = request.form.get('scan_result', None)
		exam_measure_id = request.form.get('exam_measure_id', None)
		year = request.form.get('year', None)
		manager_id = request.form.get('manager_id', None)
		exam_entity_id = request.form.get('exam_entity_id', None)
		score = request.form.get('score', None)
		if(id!=None):
			exam_result_manager = ExamResultManager.query.get(id)
			if(image_path!=None):
				exam_result_manager.image_path = image_path
			if(scan_result!=None):
				exam_result_manager.scan_result = scan_result
			if(exam_measure_id!=None):
				exam_result_manager.exam_measure_id = exam_measure_id
			if(year!=None):
				exam_result_manager.year = year
			if(manager_id!=None):
				exam_result_manager.manager_id = manager_id
			if(exam_entity_id!=None):
				exam_result_manager.exam_entity_id = exam_entity_id
			if(score!=None):
				exam_result_manager.score = score
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='exam_result_team'):
		image_path = request.form.get('image_path', None)
		scan_result = request.form.get('scan_result', None)
		exam_measure_id = request.form.get('exam_measure_id', None)
		year = request.form.get('year', None)
		org_id = request.form.get('org_id', None)
		exam_entity_id = request.form.get('exam_entity_id', None)
		score = request.form.get('score', None)
		if(id!=None):
			exam_result_team = ExamResultTeam.query.get(id)
			if(image_path!=None):
				exam_result_team.image_path = image_path
			if(scan_result!=None):
				exam_result_team.scan_result = scan_result
			if(exam_measure_id!=None):
				exam_result_team.exam_measure_id = exam_measure_id
			if(year!=None):
				exam_result_team.year = year
			if(org_id!=None):
				exam_result_team.org_id = org_id
			if(exam_entity_id!=None):
				exam_result_team.exam_entity_id = exam_entity_id
			if(score!=None):
				exam_result_team.score = score
			db.session.commit()
			success = 1
		else:
			success = 0
			message = '数据为空'
	elif(model=='admin'):
		admin_id = current_user.id
		old_password = request.form.get('old_password', None)
		new_password = request.form.get('new_password', None)
		confirm_password = request.form.get('confirm_password', None)
		if(admin_id!=None):
			admin = Admin.query.get(admin_id)
			if (admin and admin.check_password(old_password) and new_password==confirm_password):
				admin.set_password(new_password)
				db.session.commit()
				login_user(admin)
				admin_json = admin.json()
				del (admin_json['password'])
				return jsonify({'success':1,'admin':admin_json})
			else:
				success = 0
				message = '密码错误'
		else:
			success = 0
			message = '数据为空'
	return jsonify(success=success,message=message)

@app.route('/api/v1/<model>/delete', methods=['POST'])
@login_required
def do_delete(model):
	# print(model,request.form)
	ids = request.form.getlist('ids[]')
	if(model=='exam'):
		for id in ids:
			exam = Exam.query.get(id)
			if(exam!=None):
				db.session.delete(exam)
		db.session.commit()
		success = 1
	elif(model=='exam_content'):
		for id in ids:
			exam_content = ExamContent.query.get(id)
			if(exam_content!=None):
				db.session.delete(exam_content)
		db.session.commit()
		success = 1
	elif(model=='exam_measure'):
		for id in ids:
			exam_measure = ExamMeasure.query.get(id)
			if(exam_measure!=None):
				db.session.delete(exam_measure)
		db.session.commit()
		success = 1
	elif(model=='exam_entity'):
		for id in ids:
			exam_entity = ExamEntity.query.get(id)
			if(exam_entity!=None):
				db.session.delete(exam_entity)
		db.session.commit()
		success = 1
	elif(model=='exam_system'):
		for id in ids:
			exam_system = ExamSystem.query.get(id)
			if(exam_system!=None):
				db.session.delete(exam_system)
		db.session.commit()
		success = 1
	elif(model=='exam_entity_weight'):
		for id in ids:
			exam_entity_weight = ExamEntityWeight.query.get(id)
			if(exam_entity_weight!=None):
				db.session.delete(exam_entity_weight)
		db.session.commit()
		success = 1
	elif(model=='org_type'):
		for id in ids:
			org_type = OrgType.query.get(id)
			if(org_type!=None):
				db.session.delete(org_type)
		db.session.commit()
		success = 1
	elif(model=='org'):
		for id in ids:
			org = Org.query.get(id)
			if(org!=None):
				db.session.delete(org)
		db.session.commit()
		success = 1
	elif(model=='team_year_weight'):
		for id in ids:
			team_year_weight = TeamYearWeight.query.get(id)
			if(team_year_weight!=None):
				team_scores = TeamScore.query.filter_by(org_id=team_year_weight.org_id,year=team_year_weight.year).all()
				for team_score in team_scores:
					db.session.delete(team_score)
				db.session.delete(team_year_weight)
		db.session.commit()
		success = 1
	elif(model=='team_score'):
		pass
		# for id in ids:
		# 	team_score = TeamScore.query.get(id)
		# 	if(team_score!=None):
		# 		db.session.delete(team_score)
		# db.session.commit()
		# success = 1
	# elif(model=='manager_title'):
	# 	for id in ids:
	# 		manager_title = ManagerTitle.query.get(id)
	# 		if(manager_title!=None):
	# 			db.session.delete(manager_title)
	# 	db.session.commit()
	# 	success = 1
	elif(model=='manager_type'):
		for id in ids:
			manager_type = ManagerType.query.get(id)
			if(manager_type!=None):
				db.session.delete(manager_type)
		db.session.commit()
		success = 1
	elif(model=='manager'):
		for id in ids:
			manager = Manager.query.get(id)
			if(manager!=None):
				db.session.delete(manager)
		db.session.commit()
		success = 1
	elif(model=='manager_year_weight'):
		for id in ids:
			manager_year_weight = ManagerYearWeight.query.get(id)
			if(manager_year_weight!=None):
				db.session.delete(manager_year_weight)
		db.session.commit()
		success = 1
	elif(model=='exam_result_manager'):
		for id in ids:
			exam_result_manager = ExamResultManager.query.get(id)
			if(exam_result_manager!=None):
				db.session.delete(exam_result_manager)
		db.session.commit()
		success = 1
	elif(model=='exam_result_team'):
		for id in ids:
			exam_result_team = ExamResultTeam.query.get(id)
			if(exam_result_team!=None):
				db.session.delete(exam_result_team)
		db.session.commit()
		success = 1

	return jsonify(success=success)

@app.route('/api/v1/org_import', methods=['POST'])
@login_required
def do_org_import():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('import path:',request.form)

	path = request.form.get('path', None)

	def process():

		wb = xlrd.open_workbook(path)
		sheet=wb.sheets()[0]
		row_count = sheet.nrows

		org_types = OrgType.query.all()
		orgs = Org.query.all()

		for row_index in range(row_count):
			if row_index==0:
				continue

			org_exist_id = None
			org_type_id = None
			short_name = None
			full_name = None
			
			for col_index in range(3):
				tmp_str = sheet.row_values(row_index)[col_index]
				
				if col_index == 0: #单位类型
					for org_type in org_types:
						if org_type.name == tmp_str:
							org_type_id = org_type.id
							break

				if col_index == 1: #单位简称
					short_name = tmp_str
					for org in orgs:
						if org.short_name == tmp_str:
							org_exist_id = org.id
							break

				if col_index == 2: #单位全称
					full_name = tmp_str
					for org in orgs:
						if org.full_name == tmp_str:
							org_exist_id = org.id
							break

			if org_exist_id == None:
				db.session.add(Org(org_type_id=org_type_id,short_name=short_name,full_name=full_name,sort=1))
			else:
				yield "message:" + short_name + "" + u"已经存在"
				time.sleep(1)
		
			yield "data:" + str(((row_index+1)*100/row_count)) + ""
			time.sleep(1)

		db.session.commit()

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/org_export', methods=['POST'])
@login_required
def do_org_export():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('export path:',request.form)

	path = request.form.get('path', None)
	
	def process():

		orgs = Org.query.order_by(Org.sort).all();

		generate.gen_org(path,orgs)

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/manager_export', methods=['POST'])
@login_required
def do_manager_export():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('export path:',request.form)

	path = request.form.get('path', None)
	
	def process():

		managers = Manager.query.order_by(Manager.org_id.asc(),Manager.sort.asc()).all()

		generate.gen_manager(path,managers)

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/manager_import', methods=['POST'])
@login_required
def do_manager_import():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('import path:',request.form)

	path = request.form.get('path', None)

	def process():

		wb = xlrd.open_workbook(path)
		sheet=wb.sheets()[0]
		row_count = sheet.nrows

		orgs = Org.query.all()
		managers = Manager.query.all()
		manager_types = ManagerType.query.all()
		# manager_titles = ManagerTitle.query.all()

		for row_index in range(row_count):
			if row_index==0:
				continue

			manager_exist_id = None
			org_id = None
			name = None
			title = None
			manager_type_id = None
			# manager_title_id = None
			sort = 1
			
			for col_index in range(5):
				tmp_str = sheet.row_values(row_index)[col_index]
				
				if col_index == 0: #单位
					for org in orgs:
						if org.short_name == tmp_str or org.full_name == tmp_str:
							org_id = org.id
							break

				if col_index == 1: #姓名
					name = tmp_str
					for manager in managers:
						if manager.org_id == org_id and manager.name == tmp_str:
							manager_exist_id = manager.id
							break

				if col_index == 2: #人员类型
					for manager_type in manager_types:
						if manager_type.name == tmp_str:
							manager_type_id = manager_type.id
							break

				# if col_index == 3: #职务
				# 	for manager_title in manager_titles:
				# 		if manager_title.name == tmp_str:
				# 			manager_title_id = manager_title.id
				# 			break

				if col_index == 3: #职务
					title = tmp_str

				if col_index == 4: #显示顺序
					sort = int(tmp_str)

			if manager_exist_id == None:
				# db.session.add(Manager(org_id=org_id,name=name,manager_type_id=manager_type_id,manager_title_id=manager_title_id,sort=1))
				db.session.add(Manager(org_id=org_id,name=name,manager_type_id=manager_type_id,title=title,sort=sort))
			else:
				yield "message:" + name + "" + u"已经存在"
				#time.sleep(1)
		
			yield "data:" + str(((row_index+1)*100/row_count)) + ""
			#time.sleep(1)

		db.session.commit()

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/result_org_export', methods=['POST'])
@login_required
def do_result_org_export():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('export path:',request.form)

	path = request.form.get('path', None)
	year  = request.form.get('year', None)
	org_id = request.form.get('org_id', None)
	exam_entity_id = request.form.get('exam_entity_id', None)
	
	def process():

		orgs = Org.query.order_by(Org.sort).all()
		exam_entitys = ExamEntity.query.order_by(ExamEntity.sort).all()
		exam_contents = ExamContent.query.filter_by(show=1).order_by(ExamContent.exam_id,ExamContent.sort).all()
		exam_measures = ExamMeasure.query.filter_by(show=1).order_by(ExamMeasure.exam_content_id,ExamMeasure.sort).all()
		exam_result_teams = ExamResultTeam.query.filter_by(validity=1).all()

		generate.gen_result_org(path,year,org_id,exam_entity_id,orgs,exam_entitys,exam_contents,exam_measures,exam_result_teams)

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/result_manager_export', methods=['POST'])
@login_required
def do_result_manager_export():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('export path:',request.form)

	path = request.form.get('path', None)
	year  = request.form.get('year', None)
	manager_id = request.form.get('manager_id', None)
	exam_entity_id = request.form.get('exam_entity_id', None)
	
	def process():

		orgs = Org.query.order_by(Org.sort).all()
		exam_entitys = ExamEntity.query.order_by(ExamEntity.sort).all()
		exam_contents = ExamContent.query.filter_by(show=1).order_by(ExamContent.exam_id,ExamContent.sort).all()
		exam_measures = ExamMeasure.query.filter_by(show=1).order_by(ExamMeasure.exam_content_id,ExamMeasure.sort).all()
		exam_result_teams = ExamResultTeam.query.filter_by(validity=1).all()

		managers = Manager.query.order_by(Manager.org_id.asc(),Manager.sort.asc()).all()
		exam_result_managers = ExamResultManager.query.filter_by(validity=1).all()

		generate.gen_result_manager(path,year,manager_id,exam_entity_id,orgs,exam_entitys,exam_contents,exam_measures,exam_result_teams,managers,exam_result_managers)

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/generate', methods=['POST'])
@login_required
def do_generate():
	orgs = request.form.getlist('orgs[]')
	datetimestr = request.form.get('datetime')
	path = request.form.get('path', None)
	year = request.form.get('datetime') # add by yelong

	datetimestr = datetimestr + u'年'

	dir_path = os.path.join(path, u'投票表')
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)

	def process():
		count = len(orgs)
		for index,org_id in enumerate(orgs):
			org = Org.query.get(org_id)

			if(org!=None):
				
				org_path = os.path.join(dir_path, org.short_name)
				if not os.path.exists(org_path):
					os.mkdir(org_path)

				org_datetime_path = os.path.join(org_path, datetimestr)
				if not os.path.exists(org_datetime_path):
					os.mkdir(org_datetime_path)

				exams = Exam.query.order_by(Exam.sort).all()
				contents = ExamContent.query.filter_by(show=1).order_by(ExamContent.sort).all()
				measures = ExamMeasure.query.filter_by(show=1).order_by(ExamMeasure.sort).all()
				managers = Manager.query.filter_by(org_id=org.id).order_by(Manager.sort, Manager.id).all()
				entities = ExamEntity.query.order_by(ExamEntity.sort).all()

				# add by yelong
				teamWeight = TeamYearWeight.query.filter_by(year=year,org_id=org.id).first()
				managers_exist = []
				for manager in managers:
					managerWeight = ManagerYearWeight.query.filter_by(year=year,manager_id=manager.id).first()
					print('managerWeight:', managerWeight)
					if managerWeight != None:
						if managerWeight.weight > 0:
							managers_exist.append(manager)
				
				# edit by yelong
				#generate.gen_excel(org_datetime_path,datetimestr,org,exams,contents,measures,managers,entities)
				generate.gen_excel(org_datetime_path,datetimestr,org,exams,contents,measures,
					managers_exist,entities,teamWeight)

			yield "data:" + str(((index+1)*100/count)) + ""
			time.sleep(1)

		yield "path:" + org_datetime_path + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')
	# success = 1
	# return jsonify(success=success,path=org_datetime_path)

# # add by yelong
# def replace_sign(str_has_sign):
# 	str_no_sign = str_has_sign.replace(":", "")
# 	str_no_sign = str_no_sign.replace("：", "")
# 	str_no_sign = str_no_sign.replace(".", "")
# 	str_no_sign = str_no_sign.replace(" ", "")
# 	return str_no_sign

@app.route('/api/v1/scan', methods=['POST'])
@login_required
def do_scan():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('scan request:',request.form)
	year = request.form.get('datetime')
	paths = request.form.getlist('path[]')
	request_orgs = request.form.getlist('orgs[]')
	org_id = None
	for i,request_org_id in enumerate(request_orgs):
		org_id = request_org_id

	print('scan request_orgs:',request_orgs)
	print('scan org_id:',org_id)
	print('scan year:',year)
	print('scan path:',paths)

	def process():
		# all_files = scan.get_all_files(paths)
		all_files = paths

		count = len(all_files)

		print('file count:',count)

		have_errors = False

		for file_index,file_path in enumerate(all_files):
			have_errors = False  #add by yelong
			print('scan result:',file_path)

			result = None

			try:

				# file_path = file_path.encode('gbk')

				result = scan.ident(file_path)

			except:
				
				shutil.copy(file_path,ERRORPATH)

				have_errors = True

			else:

				print('result',result != None,result.has_key('data'),(result['data']).has_key('datas'))
				print(result)

				if result != None and result.has_key('data') and result['data'].has_key('datas'):

					data = result['data']

					image_path = file_path
					scan_result = json.dumps(data)

					# org_name = ''
					# date_str = ''
					entity_name = ''

					exams = Exam.query.order_by(Exam.sort).all()
					contents = ExamContent.query.filter_by(show=1).order_by(ExamContent.sort).all()
					measures = ExamMeasure.query.filter_by(show=1).order_by(ExamMeasure.sort).all()
					managers = Manager.query.order_by(Manager.org_id.asc(),Manager.sort.asc()).all()
					entities = ExamEntity.query.order_by(ExamEntity.sort).all()
					orgs = Org.query.order_by(Org.sort).all()

					if (data['type']==1):
						# ExamResultTeam.query().filter_by(image_path=image_path).delete(synchronize_session=False)
						db.session.query(ExamResultTeam).filter(ExamResultTeam.image_path==image_path).delete(synchronize_session=False)

						current_exams = filter(lambda c: c.name==u'领导班子年度综合考评',exams)
						current_exam = current_exams[0]
						current_contents = filter(lambda c: c.exam_id==current_exam.id,contents)

						# delete by yelong 部门、年份识别，不再使用汉字识别
						# date_str = ''
						# year = ''
						# year_found = False

						# if data.has_key('date'):
						# 	print data['date']

						# if data.has_key('date') and len(data['date']) > 4 and data['date'][0:4] == u'单位名称':
						# 	# edit by yelong
						# 	#org_name = data['date'][5:]
						# 	org_name = replace_sign(data['date'])[4:]
						# 	year = date_str[0:4]
						# 	year_found = True
						# elif data.has_key('date') and len(data['date']) > 4 and (data['date'][0:4] == u'考评年度' or data['date'][0:4] == u'考评时间'):
						# 	# edit by yelong
						# 	#date_str = data['date'][5:]
						# 	date_str = replace_sign(data['date'])[4:]
						# 	year = date_str[0:4]
						# 	year_found = True

						# org_name = ''

						# if data.has_key('org'):
						# 	print data['org']

						# if data.has_key('org') and len(data['org']) > 4 and data['org'][0:4] == u'单位名称':
						# 	# edit by yelong
						# 	#org_name = data['org'][5:]
						# 	org_name = replace_sign(data['org'])[4:]
						# elif data.has_key('org') and len(data['org']) > 4 and (data['org'][0:4] == u'考评年度' or data['org'][0:4] == u'考评时间'):
						# 	# edit by yelong
						# 	#date_str = data['org'][5:]
						# 	date_str = replace_sign(data['org'])[4:]

						# org_id = None
						# org_found = False
						# for org in orgs:
						# 	if (org.short_name == org_name or org.full_name == org_name):
						# 		org_id = org.id
						# 		org_found = True
						# 		break
						
						# if not org_found:
						# 	# 半角括号转全角括号
						# 	org_name = org_name.replace("(", "（");
						# 	org_name = org_name.replace(")", "）");
						# 	for org in orgs:
						# 		if (org.short_name == org_name or org.full_name == org_name):
						# 			org_id = org.id
						# 			org_found = True
						# 			break

						# if not org_found:
						# 	print org_name

						# if org_found and year_found:

						entity_name = data['entity']

						exam_entity_id = None
						for entity in entities:
							if entity.name == entity_name:
								exam_entity_id = entity.id
								break

						data_datas = data['datas']
						for data_data in data_datas:

							exam_measure_id = None

							data_index = 1
							found = False
							for current_content in current_contents:
								current_measures = filter(lambda c: c.exam_content_id==current_content.id,measures)
								for current_measure in current_measures:
									if data_data['index'] == data_index:
										exam_measure_id = current_measure.id
										found = True
										break
									data_index = data_index + 1
								if found:
									break

							score = data_data['point']

							validity = 0
							#edit by yelong(score!=0)
							#if(exam_measure_id!=None and year!=None and org_id!=None and exam_entity_id!=None and score!=0):
							if(exam_measure_id!=None and year!=None and org_id!=None and exam_entity_id!=None):
								validity = 1
							
								db.session.add(ExamResultTeam(image_path=image_path,scan_result=scan_result,exam_measure_id=exam_measure_id,year=year,org_id=org_id,exam_entity_id=exam_entity_id,score=score,validity=validity))
							else:
								db.session.query(ExamResultTeam).filter(ExamResultTeam.image_path==image_path).delete(synchronize_session=False) #add by yelong

								shutil.copy(file_path,ERRORPATH)

								have_errors = True

							if have_errors:
								break
						# else:

						# 	shutil.copy(file_path,ERRORPATH)

						# 	have_errors = True

					if (data['type']==2):

						# ExamResultManager.query().filter_by(image_path=image_path).delete(synchronize_session=False)
						db.session.query(ExamResultManager).filter(ExamResultManager.image_path==image_path).delete(synchronize_session=False)

						current_exams = filter(lambda c: c.name==u'中层干部年度综合考评',exams)
						current_exam = current_exams[0]
						current_contents = filter(lambda c: c.exam_id==current_exam.id,contents)

						# delete by yelong 部门、年份识别，不再使用汉字识别
						# org_name = ''
						# date_str = ''

						# if data.has_key('org'):
						# 	print data['org']

						# if data.has_key('org') and len(data['org'])>4 and data['org'][0:4] == u'单位名称':
						# 	# edit by yelong
						# 	#org_name = data['org'][5:]
						# 	org_name = replace_sign(data['org'])[4:]
						# elif data.has_key('org') and len(data['org'])>4 and (data['org'][0:4] == u'考评年度' or data['org'][0:4] == u'考评时间'):
						# 	# edit by yelong
						# 	#date_str = data['org'][5:]
						# 	date_str = replace_sign(data['org'])[4:]

						# if data.has_key('date'):
						# 	print data['date']

						# if data.has_key('date') and len(data['date'])>4 and data['date'][0:4] == u'单位名称':
						# 	# edit by yelong
						# 	#org_name = data['date'][5:]
						# 	org_name = replace_sign(data['date'])[4:]
						# elif data.has_key('date') and len(data['date'])>4 and (data['date'][0:4] == u'考评年度' or data['date'][0:4] == u'考评时间'):
						# 	# edit by yelong
						# 	#date_str = data['date'][5:]
						# 	date_str = replace_sign(data['date'])[4:]

						# year = None
						# if date_str != None and len(date_str) > 4:
						# 	 year = date_str[0:4]

						# org_id = None
						# org_found = False
						# for org in orgs:
						# 	if (org.short_name == org_name or org.full_name == org_name):
						# 		org_id = org.id
						# 		org_found = True
						# 		break
						
						# if not org_found:
						# 	# 半角括号转全角括号
						# 	org_name = org_name.replace("(", "（");
						# 	org_name = org_name.replace(")", "）");
						# 	for org in orgs:
						# 		if (org.short_name == org_name or org.full_name == org_name):
						# 			org_id = org.id
						# 			org_found = True
						# 			break

						# if not org_found:
						# 	print org_name

						# if org_found:

						entity_name = data['entity']

						exam_entity_id = None
						for entity in entities:
							if entity.name == entity_name:
								exam_entity_id = entity.id
								break

						data_datas = data['datas']
						for data_data in data_datas:
							# edit by yelong 增加人员考评票的页数，用于人员的识别，不再使用汉字识别
							# manager_name = data_data['name']

							# manager_id = None
							# for manager in managers:
							# 	if manager.name == manager_name and manager.org_id == org_id:
							# 		manager_id = manager.id
							# 		break
							manager_id = None
							manager_index = data_data['index']
							page_no = data['pageno']
							if page_no != None:
								org_managers = Manager.query.filter_by(org_id=org_id).order_by(Manager.sort, Manager.id).all()
								managers_exist = []
								for manager in org_managers:
									managerWeight = ManagerYearWeight.query.filter_by(year=year,manager_id=manager.id).first()
									if managerWeight != None:
										if managerWeight.weight > 0:
											managers_exist.append(manager)
							
								manager_index = page_no * 4 + manager_index - 1
								if len(managers_exist) > manager_index:
									manager_id = managers_exist[manager_index].id
							else:
								shutil.copy(file_path,ERRORPATH)

							data_data_datas = data_data['datas']
							for data_data_data in data_data_datas:

								exam_measure_id = None

								data_index = 1
								found = False
								for current_content in current_contents:
									current_measures = filter(lambda c: c.exam_content_id==current_content.id,measures)
									for current_measure in current_measures:
										if data_data_data['index'] == data_index:
											exam_measure_id = current_measure.id
											found = True
											break
										data_index = data_index + 1
									if found:
										break

								score = data_data_data['point']

								validity = 0
								#edit by yelong(score!=0)
								# if(manager_id!=None and score == 0):
								# 	db.session.query(ExamResultManager).filter(ExamResultManager.image_path==image_path).delete(synchronize_session=False) #add by yelong

								# 	shutil.copy(file_path,ERRORPATH)

								# 	have_errors = True
								# else:
								if(exam_measure_id!=None and year!=None and exam_entity_id!=None):
									validity = 1

									if(manager_id!=None):
										db.session.add(ExamResultManager(image_path=image_path,scan_result=scan_result,exam_measure_id=exam_measure_id,year=year,manager_id=manager_id,exam_entity_id=exam_entity_id,score=score,validity=validity))
								else:
									db.session.query(ExamResultManager).filter(ExamResultManager.image_path==image_path).delete(synchronize_session=False) #add by yelong

									shutil.copy(file_path,ERRORPATH)

									have_errors = True

								if have_errors:
									break

							if have_errors:
								break
						# else:

						# 	shutil.copy(file_path,ERRORPATH)

						# 	have_errors = True

					# yield "data:" + str(((file_index+1)*100/count)) + ""
					time.sleep(1)

				else:

					shutil.copy(file_path,ERRORPATH)

					have_errors = True

		db.session.commit()

		if have_errors:
			yield ERRORPATH

	return Response(process(),mimetype='text/event-stream')
	# success = 1
	# return jsonify(success=success,result=result)

@app.route('/api/v1/check', methods=['POST'])
@login_required
def do_check():
	success = 1
	message = []
	year = request.form.get('year', None)
	request_orgs = request.form.getlist('orgs[]')
	orgn_id = None
	for i,request_org_id in enumerate(request_orgs):
		orgn_id = int(request_org_id)

	if Org.query.count()==0:
		message.append('单位信息为空!')
	if Manager.query.count()==0:
		message.append('机关干部信息为空!')
	
	for row in db.engine.execute('SELECT T1.org_id, T2.short_name, T1.exam_entity_id, T3.name, COUNT(T1.id) / 10 CNT FROM T_EXAM_RESULT_TEAM T1 INNER JOIN T_ORG T2 ON T1.org_id = T2.id INNER JOIN T_EXAM_ENTITY T3 ON T1.exam_entity_id = T3.id  WHERE T1.year = ' + year + ' GROUP BY T1.org_id, T2.short_name, T1.exam_entity_id, T3.name'):
		if row[0]==orgn_id:
			message.append(str(row[1]) + '[领导班子年度综合考评](' + str(row[3]) + ')数量为：' + str(row[4]))

	for row in db.engine.execute('SELECT T2.org_id, T3.short_name, T1.exam_entity_id, T4.name, COUNT(T1.id) / 11 CNT FROM T_EXAM_RESULT_MANAGER T1 INNER JOIN T_MANAGER T2 ON T1.manager_id = T2.id INNER JOIN T_ORG T3 ON T2.org_id = T3.id INNER JOIN T_EXAM_ENTITY T4 ON T1.exam_entity_id = T4.id WHERE T1.year = ' + year + ' GROUP BY T2.org_id, T3.short_name, T1.exam_entity_id, T4.name'):
		if row[0]==orgn_id:
			message.append(str(row[1]) + '[中层干部年度综合考评](' + str(row[3]) + ')数量为：' + str(row[4]))

	for row in db.engine.execute('select ec.exam_id,sum(em.weight) from T_EXAM_MEASURE em,T_EXAM_CONTENT ec where em.exam_content_id = ec.id and ec.show=1 and em.show=1 group by ec.exam_id'):
		if row[1]!=100:
			exam = Exam.query.get(row[0])
			message.append('评价指标 ['+exam.name+'] 当前权重 ['+str(row[1])+'%] 不为100%!')

	for row in db.engine.execute('select exam_system_id,sum(weight) from T_EXAM_ENTITY_WEIGHT group by exam_system_id'):
		if row[1]!=100:
			exam_system = ExamSystem.query.get(row[0])
			message.append('测评主体 ['+exam_system.name+'] 当前权重 ['+str(row[1])+'%] 不为100%!')

	for row in db.engine.execute('select org_id,sum(weight) from T_TEAM_YEAR_WEIGHT group by org_id'):
		if row[1]!=100 and row[0]==orgn_id:
			org = Org.query.get(row[0])
			message.append('领导班子 ['+org.short_name+'] 当前权重 ['+str(row[1])+'%] 不为100%!')
	
	for row in db.engine.execute('select manager_id,sum(weight) from T_MANAGER_YEAR_WEIGHT group by manager_id'):
		if row[1]!=100:
			manager = Manager.query.get(row[0])
			if manager.org_id==orgn_id:
				message.append('中层干部 ['+manager.name+'] 当前权重 ['+str(row[1])+'%] 不为100%!')
	
	for row in db.engine.execute('select manager_id,count(0) from t_manager_year_weight group by (manager_id)'):
		if row[1]==0:
			manager = Manager.query.get(row[0])
			if manager.org_id==orgn_id:
				message.append('中层干部 ['+manager.name+'] 未配置权重!')

	for row in db.engine.execute('select org_id,count(0) from t_team_year_weight group by (org_id)'):
		if row[1]==0 and row[0]==orgn_id:
			org = Org.query.get(row[0])
			message.append('领导班子 ['+org.short_name+'] 未配置权重!')

	for row1 in db.engine.execute('select DISTINCT tee.id from T_EXAM_ENTITY tee left join T_EXAM_ENTITY_WEIGHT tenw on tee.id = tenw.exam_entity_id where tenw.weight > 0'):
		for row2 in db.engine.execute('SELECT torg.id org_id, (SELECT count(tert.score) FROM T_EXAM_RESULT_TEAM tert WHERE torg.id = tert.org_id AND tert.exam_entity_id = ' + str(row1[0]) + ' AND tert.year = ' + year + ') cnt FROM T_ORG torg'):
			if row2[1]==0 and row2[0]==orgn_id:
				entity = ExamEntity.query.get(row1[0])
				org = Org.query.get(row2[0])
				message.append('领导班子 ['+org.short_name+'] 扫描数据中缺少'+entity.name+'的数据')

	for row1 in db.engine.execute('select DISTINCT tee.id from T_EXAM_ENTITY tee left join T_EXAM_ENTITY_WEIGHT tenw on tee.id = tenw.exam_entity_id where tenw.weight > 0'):
		for row2 in db.engine.execute('SELECT tman.id manager_id, (SELECT count(term.score) FROM T_EXAM_RESULT_MANAGER term WHERE term.manager_id = tman.id AND term.exam_entity_id = ' + str(row1[0]) + ' AND term.year = ' + year + ') cnt FROM T_MANAGER tman'):
			if row2[1]==0:
				entity = ExamEntity.query.get(row1[0])
				manager = Manager.query.get(row2[0])
				if manager.org_id==orgn_id:
					message.append('中层干部 ['+manager.name+'] 扫描数据中缺少'+entity.name+'的数据')

	return jsonify(success=success,message=message)

def get_team_report(year):
	examlist = []
	team_exam_scores = TeamExamScore.query.filter_by(year=year).order_by(TeamExamScore.org_sum_score.desc()).all()
	if team_exam_scores != None: 
		if len(team_exam_scores) > 0:
			sortIndex = 0
			for team_exam_score in team_exam_scores:
				result = {}
				result["org_id"] = team_exam_score.org_id
				result["year"] = team_exam_score.year
				result["org_score"] = round(team_exam_score.org_score, 2)
				result["org_sum_score"] = round(team_exam_score.org_sum_score, 2)
				result["dj_score"] = team_exam_score.dj_score
				result["yj_score"] = team_exam_score.yj_score
				result["content_score_1"] = team_exam_score.content_score_1
				result["content_score_2"] = team_exam_score.content_score_2
				result["content_score_3"] = team_exam_score.content_score_3
				result["content_score_4"] = team_exam_score.content_score_4
				result["measure_score_4"] = team_exam_score.measure_score_4
				result["measure_score_5"] = team_exam_score.measure_score_5
				result["measure_score_6"] = team_exam_score.measure_score_6
				result["measure_score_7"] = team_exam_score.measure_score_7
				result["measure_score_8"] = team_exam_score.measure_score_8
				result["measure_score_9"] = team_exam_score.measure_score_9
				result["measure_score_10"] = team_exam_score.measure_score_10
				result["measure_score_11"] = team_exam_score.measure_score_11
				result["measure_score_12"] = team_exam_score.measure_score_12
				result["measure_score_13"] = team_exam_score.measure_score_13

				tempOrg = Org.query.filter_by(id=result["org_id"]).first()
				if tempOrg != None:
					sortIndex = sortIndex + 1
					result["org_index"] = sortIndex
					result["org_name"] = tempOrg.short_name
					result["org_sum_sort"] = sortIndex
					if sortIndex > 1:
						if result["org_sum_score"] == examlist[sortIndex-2]["org_sum_score"]:
							result["org_sum_sort"] = examlist[sortIndex-2]["org_sum_sort"]

					examlist.append(result)
	
	return examlist

def get_manager_report(year):
	examlist = []
	manager_exam_scores = ManagerExamScore.query.filter_by(year=year).order_by(ManagerExamScore.manager_sum_score.desc()).all()
	if manager_exam_scores != None: 
		if len(manager_exam_scores) > 0:
			sortIndex = 0
			for manager_exam_score in manager_exam_scores:
				result = {}
				result["manager_id"] = manager_exam_score.manager_id
				result["year"] = manager_exam_score.year
				result["manager_score"] = round(manager_exam_score.manager_score, 2)
				result["manager_sum_score"] = round(manager_exam_score.manager_sum_score, 2)
				result["org_score"] = round(manager_exam_score.org_sum_score, 2)
				result["content_score_6"] = manager_exam_score.content_score_6
				result["content_score_7"] = manager_exam_score.content_score_7
				result["content_score_8"] = manager_exam_score.content_score_8
				result["measure_score_14"] = manager_exam_score.measure_score_14
				result["measure_score_15"] = manager_exam_score.measure_score_15
				result["measure_score_16"] = manager_exam_score.measure_score_16
				result["measure_score_17"] = manager_exam_score.measure_score_17
				result["measure_score_18"] = manager_exam_score.measure_score_18
				result["measure_score_19"] = manager_exam_score.measure_score_19
				result["measure_score_20"] = manager_exam_score.measure_score_20
				result["measure_score_21"] = manager_exam_score.measure_score_21
				result["measure_score_22"] = manager_exam_score.measure_score_22
				result["measure_score_23"] = manager_exam_score.measure_score_23
				result["measure_score_24"] = manager_exam_score.measure_score_24

				tempManager = Manager.query.filter_by(id=result["manager_id"]).first()
				if tempManager != None:
					sortIndex = sortIndex + 1
					result["manager_index"] = sortIndex
					result["org_id"] = tempManager.org_id
					tempOrg = Org.query.filter_by(id=result["org_id"]).first()
					if tempOrg != None:
						result["org_name"] = tempOrg.short_name
					
					result["manager_name"] = tempManager.name
					result["title"] = tempManager.title
					result["manager_sum_sort"] = sortIndex
					if sortIndex > 1:
						if result["manager_sum_score"] == examlist[sortIndex-2]["manager_sum_score"]:
							result["manager_sum_sort"] = examlist[sortIndex-2]["manager_sum_sort"]

					examlist.append(result)

	return examlist

@app.route('/api/v1/report_teams', methods=['POST'])
@login_required
def report_teams():
	success = 1

	year = request.form.get('year', None)

	if year == None:
		year = datetime.now().year

	# edit by yelong
	# examlist = []
	# list = []
	# team_exam_scores = TeamExamScore.query.filter_by(year=year).all()
	# if team_exam_scores != None: 
	# 	if len(team_exam_scores) > 0:
	# 		list = compute_org_score(year,False)
	# 		# add by yelong
	# 		for team_exam_score in team_exam_scores:
	# 			for result in list:
	# 				if result['org_id'] == team_exam_score.org_id and team_exam_score.org_score > 0 and team_exam_score.org_sum_score > 0:
	# 					examlist.append(result)
			
	# 		examlist = sorted(examlist, key = lambda result: result["org_sum_score"], reverse=True)

	examlist = get_team_report(year)
	print(examlist)

	return jsonify(success=success,list=examlist)

@app.route('/api/v1/report_managers', methods=['POST'])
@login_required
def report_managers():
	success = 1

	year = request.form.get('year', None)

	if year == None:
		year = datetime.now().year

	# edit by yelong
	# examlist = []
	# list = []
	# manager_exam_scores = ManagerExamScore.query.filter_by(year=year).all()
	# if manager_exam_scores != None: 
	# 	if len(manager_exam_scores) > 0:
	# 		list = compute_manager_score(year,False)
	# 		# add by yelong
	# 		for manager_exam_score in manager_exam_scores:
	# 			for result in list:
	# 				if result['manager_id'] == manager_exam_score.manager_id and manager_exam_score.manager_score > 0 and manager_exam_score.manager_sum_score > 0:
	# 					examlist.append(result)

	# 		examlist = sorted(examlist, key = lambda result: result["manager_sum_score"], reverse=True)

	examlist = get_manager_report(year)
	print(examlist)

	return jsonify(success=success,list=examlist)

@app.route('/api/v1/report_peoples', methods=['POST'])
@login_required
def report_peoples():
	success = 1

	year = datetime.now().year

	list = compute_manager_score(year,False)

	print(list)

	return jsonify(success=success,list=list)

@app.route('/api/v1/compute', methods=['POST'])
@login_required
def compute():
	success = 1

	year = request.form.get('year')
	request_orgs = request.form.getlist('orgs[]')
	orgn_id = None
	for i,request_org_id in enumerate(request_orgs):
		orgn_id = int(request_org_id)

	list = compute_org_score(year,orgn_id,True)

	print(list)

	list = compute_manager_score(year,orgn_id,True)

	print(list)

	return jsonify(success=success,message=[])

def compute_org_score(year,orgn_id,save_db=False):

	print year

	list = []

	systems = ExamSystem.query.all()
	entity_weights = ExamEntityWeight.query.all()
	team_scores = TeamScore.query.filter_by(year=year).all()

	team_year_weights = TeamYearWeight.query.all()

	orgs = Org.query.order_by(Org.sort).all()
	exam_entitys = ExamEntity.query.order_by(ExamEntity.sort).all()
	exam_contents = ExamContent.query.filter_by(show=1).order_by(ExamContent.exam_id,ExamContent.sort).all()
	exam_measures = ExamMeasure.query.filter_by(show=1).order_by(ExamMeasure.exam_content_id,ExamMeasure.sort).all()
	#exam_result_teams = ExamResultTeam.query.filter_by(validity=1).all()

	# 班子业绩
	bzyj_measure = ExamMeasure.query.filter_by(show=0,name=u'绩效成果').first()

	# 企业党建
	qydj_measure = ExamMeasure.query.filter_by(show=0,name=u'企业党建').first()
	
	for org in orgs:
		if org.id != orgn_id: continue
		if org.org_type_id == 2: continue
		# add by yelong
		teamWeight = TeamYearWeight.query.filter_by(year=year,org_id=org.id).first()
		if teamWeight == None: continue
		if teamWeight.weight == 0: continue

		result = {}

		result["org_id"] = org.id
		result["org_name"] = org.short_name
		result["year"] = year

		org_score = 0
		
		if save_db:
		
			for content in exam_contents:
				if(content.exam_id != 1):
					continue

				content_score = 0
				content_sum = 0
				
				for measure in exam_measures:
					if(measure.exam_content_id!=content.id):
						continue

					measure_score = 0
					# measure_sum = 0

					for entity in exam_entitys:
		
						entity_score = 0
						entity_sum = 0
						entity_count = 0

						#优化计算速度，根据org_id查询exam_result_teams
						exam_result_teams = ExamResultTeam.query.filter_by(org_id=org.id,validity=1).all()
						for exam_result_team in exam_result_teams:

							if exam_result_team.year != int(year):
								continue
							if exam_result_team.org_id != org.id:
								continue
							if exam_result_team.exam_measure_id != measure.id:
								continue
							if exam_result_team.exam_entity_id != entity.id:
								continue
							
							#0分项入库的数据，考评计算时不算平均分
							if exam_result_team.score == 0:
								continue

							entity_sum = entity_sum + exam_result_team.score
							entity_count = entity_count + 1
						
						if entity_sum > 0 and entity_count > 0:
							entity_score = float(entity_sum) / entity_count

						found = False
						for system in systems:
							#if system.name=='基层单位领导班子':
							if system.exam_id==1 and system.org_type_id==org.org_type_id:
								for weight in entity_weights:
									if weight.exam_system_id == system.id and weight.exam_entity_id == entity.id:
										measure_score = measure_score + entity_score * weight.weight / 100
										# measure_sum = measure_sum + entity_score
										found = True
										break
								if found:
									break

						result["measure_score_"+str(measure.id)] = round(measure_score,2) if measure_score>0 else ""
					
					content_score = content_score + measure_score * measure.weight / 100
					content_sum = content_sum + measure_score
					result["content_score_"+str(content.id)] = round(content_sum,2) if content_sum>0 else ""

				org_score = org_score + content_score

		# 企业党建
		org_qydj = 0
		for team_score in team_scores:
			if team_score.org_id != org.id:
				continue
			if team_score.year != int(year):
				continue
			if team_score.exam_measure_id != qydj_measure.id:
				continue
			org_qydj = team_score.score
			break

		org_qydj = org_qydj * qydj_measure.weight / 100

		result["org_qydj"] = round(org_qydj,2) if org_qydj>0 else ""

		# 班子业绩
		org_bzyj = 0
		for team_score in team_scores:
			if team_score.org_id != org.id:
				continue
			if team_score.year != int(year):
				continue
			if team_score.exam_measure_id != bzyj_measure.id:
				continue
			org_bzyj = team_score.score
			break

		org_bzyj = org_bzyj * bzyj_measure.weight / 100

		result["org_bzyj"] = round(org_bzyj,2) if org_bzyj>0 else ""

		# 民主测评
		org_mzcp = 0
		team_exam_scores = TeamExamScore.query.all()
		found = False
		for team_exam_score in team_exam_scores:
			for team_year_weight in team_year_weights:
				if team_year_weight.year != team_exam_score.year:
					continue
				if team_year_weight.org_id != team_exam_score.org_id:
					continue
				if team_year_weight.year == int(year):
					continue
				found = True
				history_org_sum_score = team_exam_score.org_sum_score * team_year_weight.weight / 100
				org_mzcp = history_org_sum_score
				all_year_org_sum_score = all_year_org_sum_score + history_org_sum_score
				break
			if found:
				break
		
		result["org_mzcp"] = round(org_mzcp,2) if org_mzcp>0 else ""

		if save_db:
			# 考评得分
			all_org_exam_score = org_score * 10

			org_score_ratio = 100 - qydj_measure.weight - bzyj_measure.weight
			org_score = all_org_exam_score * org_score_ratio / 100

			# 企业党建
			org_qydj = 0
			for team_score in team_scores:
				if team_score.org_id != org.id:
					continue
				if team_score.year != int(year):
					continue
				if team_score.exam_measure_id != qydj_measure.id:
					continue
				org_qydj = team_score.score
				break

			dj_score = org_qydj
			org_qydj = org_qydj * qydj_measure.weight / 100

			# add by yelong 部门的企业党建分数为0时，计算时不做考虑(民主测评比例 = 企业党建比例 + 民主测评比例)
			if org_qydj == 0:
				org_score = all_org_exam_score * (100 - bzyj_measure.weight) / 100

			# 班子业绩
			org_bzyj = 0
			for team_score in team_scores:
				if team_score.org_id != org.id:
					continue
				if team_score.year != int(year):
					continue
				if team_score.exam_measure_id != bzyj_measure.id:
					continue
				org_bzyj = team_score.score
				break

			yj_score = org_bzyj
			org_bzyj = org_bzyj * bzyj_measure.weight / 100

			# 年份权重 之前的 汇总得分
			org_sum_score = org_score + org_qydj + org_bzyj

			year_org_sum_score = 0
			for team_year_weight in team_year_weights:
				if team_year_weight.year != int(year):
					continue
				if team_year_weight.org_id != org.id:
					continue
				year_org_sum_score = org_sum_score * team_year_weight.weight / 100
				break

			all_year_org_sum_score = year_org_sum_score

			# 获取历史年份数据
			team_exam_scores = TeamExamScore.query.all()
			found = False
			for team_exam_score in team_exam_scores:
				for team_year_weight in team_year_weights:
					if team_year_weight.year != team_exam_score.year:
						continue
					if team_year_weight.org_id != team_exam_score.org_id:
						continue
					if team_year_weight.year == int(year):
						continue
					found = True
					history_org_sum_score = team_exam_score.org_sum_score * team_year_weight.weight / 100
					all_year_org_sum_score = all_year_org_sum_score + history_org_sum_score
					break
				if found:
					break

			# 存历史数据表
			db.session.query(TeamExamScore).filter(TeamExamScore.org_id==org.id,TeamExamScore.year==year).delete(synchronize_session=False)
			#db.session.add(TeamExamScore(org_id=org.id,year=year,org_score=all_org_exam_score,org_sum_score=all_year_org_sum_score))
			content_score_1 = float(result["content_score_1"]) if result["content_score_1"] != None and result["content_score_1"] != '' else 0
			content_score_2 = float(result["content_score_2"]) if result["content_score_2"] != None and result["content_score_2"] != '' else 0
			content_score_3 = float(result["content_score_3"]) if result["content_score_3"] != None and result["content_score_3"] != '' else 0
			content_score_4 = float(result["content_score_4"]) if result["content_score_4"] != None and result["content_score_4"] != '' else 0
			measure_score_4 = float(result["measure_score_4"]) if result["measure_score_4"] != None and result["measure_score_4"] != '' else 0
			measure_score_5 = float(result["measure_score_5"]) if result["measure_score_5"] != None and result["measure_score_5"] != '' else 0
			measure_score_6 = float(result["measure_score_6"]) if result["measure_score_6"] != None and result["measure_score_6"] != '' else 0
			measure_score_7 = float(result["measure_score_7"]) if result["measure_score_7"] != None and result["measure_score_7"] != '' else 0
			measure_score_8 = float(result["measure_score_8"]) if result["measure_score_8"] != None and result["measure_score_8"] != '' else 0
			measure_score_9 = float(result["measure_score_9"]) if result["measure_score_9"] != None and result["measure_score_9"] != '' else 0
			measure_score_10 = float(result["measure_score_10"]) if result["measure_score_10"] != None and result["measure_score_10"] != '' else 0
			measure_score_11 = float(result["measure_score_11"]) if result["measure_score_11"] != None and result["measure_score_11"] != '' else 0
			measure_score_12 = float(result["measure_score_12"]) if result["measure_score_12"] != None and result["measure_score_12"] != '' else 0
			measure_score_13 = float(result["measure_score_13"]) if result["measure_score_13"] != None and result["measure_score_13"] != '' else 0
			db.session.add(TeamExamScore(org_id=org.id,year=year,org_score=all_org_exam_score,org_sum_score=all_year_org_sum_score,
				dj_score=dj_score,yj_score=yj_score,content_score_1=content_score_1,content_score_2=content_score_2,
				content_score_3=content_score_3,content_score_4=content_score_4,measure_score_4=measure_score_4,
				measure_score_5=measure_score_5,measure_score_6=measure_score_6,measure_score_7=measure_score_7,
				measure_score_8=measure_score_8,measure_score_9=measure_score_9,measure_score_10=measure_score_10,
				measure_score_11=measure_score_11,measure_score_12=measure_score_12,measure_score_13=measure_score_13))
			db.session.commit()

			# 考评得分
			result["org_score"] = round(all_org_exam_score,2) if all_org_exam_score>0 else ""
			# 汇总得分
			result["org_sum_score"] = round(all_year_org_sum_score,2) if all_year_org_sum_score>0 else ""

		else:

			all_org_exam_score = 0
			all_year_org_sum_score = 0

			team_exam_scores = TeamExamScore.query.all()
			for team_exam_score in team_exam_scores:
				if team_exam_score.year != int(year):
					continue
				if team_exam_score.org_id != org.id:
					continue
				all_org_exam_score = team_exam_score.org_score
				all_year_org_sum_score = team_exam_score.org_sum_score

				break

			# 考评得分
			result["org_score"] = round(all_org_exam_score,2) if all_org_exam_score>0 else ""
			# 汇总得分
			result["org_sum_score"] = round(all_year_org_sum_score,2) if all_year_org_sum_score>0 else ""

		list.append(result)

	list = sorted(list, key = lambda result: result["org_sum_score"], reverse=True)
	# for result_index,result in enumerate(list):
	# 	result["org_sum_sort"] = result_index + 1
	last_score = 0
	score_index = 0
	for result in list:
		if last_score == 0:
			last_score = result["org_sum_score"]
			result["org_sum_sort"] = score_index + 1
		elif last_score == result["org_sum_score"]:
			result["org_sum_sort"] = score_index + 1
		else:
			score_index = score_index + 1
			last_score = result["org_sum_score"]
			result["org_sum_sort"] = score_index + 1

	return list

def compute_manager_score(year,orgn_id,save_db=False):

	print year

	list = []

	systems = ExamSystem.query.all()
	entity_weights = ExamEntityWeight.query.all()

	#orgs = Org.query.order_by(Org.sort).all()
	exam_entitys = ExamEntity.query.order_by(ExamEntity.sort).all()
	exam_contents = ExamContent.query.filter_by(show=1,exam_id=2).order_by(ExamContent.exam_id,ExamContent.sort).all()
	#exam_measures = ExamMeasure.query.filter_by(show=1).order_by(ExamMeasure.exam_content_id,ExamMeasure.sort).all()
	exam_result_teams = ExamResultTeam.query.filter_by(validity=1).all()

	managers = Manager.query.order_by(Manager.org_id.asc(),Manager.sort.asc()).all()
	#exam_result_managers = ExamResultManager.query.filter_by(validity=1).all()

	manager_year_weights = ManagerYearWeight.query.all()

	# 班子业绩
	bzyj_measure = ExamMeasure.query.filter_by(show=0,name=u'班子业绩').first()
	
	for manager in managers:
		if manager.org.id != orgn_id: continue
		# add by yelong
		managerWeight = ManagerYearWeight.query.filter_by(year=year,manager_id=manager.id).first()
		if managerWeight == None: continue
		if managerWeight.weight == 0: continue
		
		# manOrg = Org.query.filter_by(id=manager.org_id).first()
		# if manOrg == None: continue

		result = {}

		result["manager_id"] = manager.id
		result["manager_name"] = manager.name
		result["org_id"] = manager.org.id
		result["org_name"] = manager.org.short_name
		# result["title_id"] = manager.manager_title.id
		# result["title_name"] = manager.manager_title.name
		result["title"] = manager.title

		manager_score = 0
		
		for content in exam_contents:
			if(content.exam_id != 2):
				continue

			content_score = 0
			content_sum = 0
			
			#优化计算速度，根据exam_content_id查询t_exam_measure
			exam_measures = ExamMeasure.query.filter_by(show=1,exam_content_id=content.id).order_by(ExamMeasure.exam_content_id,ExamMeasure.sort).all()
			for measure in exam_measures:
				if(measure.exam_content_id!=content.id):
					continue

				measure_score = 0
				# measure_sum = 0

				for entity in exam_entitys:

					entity_score = 0
					entity_sum = 0
					entity_count = 0

					#优化计算速度，根据manager_id查询exam_result_managers
					exam_result_managers = ExamResultManager.query.filter_by(year=int(year),manager_id=manager.id,exam_measure_id=measure.id,exam_entity_id=entity.id,validity=1).all()
					for exam_result_manager in exam_result_managers:
						
						# if exam_result_manager.year != int(year):
						# 	continue
						# if exam_result_manager.manager_id != manager.id:
						# 	continue
						# if exam_result_manager.exam_measure_id != measure.id:
						# 	continue
						# if exam_result_manager.exam_entity_id != entity.id:
						# 	continue
						
						#0分项入库的数据，考评计算时不算平均分
						if exam_result_manager.score > 0:
							entity_sum = entity_sum + exam_result_manager.score
							entity_count = entity_count + 1

					if entity_sum > 0 and entity_count > 0:
						entity_score = float(entity_sum) / entity_count

					found = False
					for system in systems:
						#if system.name=='基层单位领导班子':
						if system.exam_id==2 and system.manager_type_id==manager.manager_type_id and system.org_type_id==manager.org.org_type_id:
							for weight in entity_weights:
								if weight.exam_system_id == system.id and weight.exam_entity_id == entity.id:
									measure_score = measure_score + entity_score * weight.weight / 100
									# measure_sum = measure_sum + entity_score
									found = True
									break
							if found:
								break

					result["measure_score_"+str(measure.id)] = round(measure_score,2) if measure_score>0 else ""

				content_score = content_score + measure_score * measure.weight / 100
				content_sum = content_sum + measure_score
				result["content_score_"+str(content.id)] = round(content_sum,2) if content_sum>0 else ""

			manager_score = manager_score + content_score

		# 班子业绩
		manager_bzyj = 0

		#基层单位
		if manager.org.org_type_id == 1:
			team_exam_scores = TeamExamScore.query.all()

			for team_exam_score in team_exam_scores:
				if(team_exam_score.org_id==manager.org.id and team_exam_score.year==int(year)):
					manager_bzyj = team_exam_score.org_sum_score
					break

		#机关部门
		if manager.org.org_type_id == 2:
			team_score = TeamScore.query.filter_by(year=year,org_id=manager.org.id,exam_measure_id=2).first()
			if team_score != None:
				manager_bzyj = team_score.score

		org_sum_score = manager_bzyj
		manager_bzyj = manager_bzyj * bzyj_measure.weight / 100
		result["manager_bzyj"] = round(manager_bzyj,2) if manager_bzyj>0 else ""

		if save_db:
			# 考评得分
			all_manager_exam_score = manager_score * 10

			manager_score_ratio = 100 - bzyj_measure.weight
			manager_score = all_manager_exam_score * manager_score_ratio / 100

			# 年份权重 之前的 汇总得分
			manager_sum_score = manager_score + manager_bzyj

			year_manager_sum_score = 0
			for manager_year_weight in manager_year_weights:
				if manager_year_weight.year != int(year):
					continue
				if manager_year_weight.manager_id != manager.id:
					continue
				year_manager_sum_score = manager_sum_score * manager_year_weight.weight / 100
				break

			all_year_manager_sum_score = year_manager_sum_score

			# 获取历史年份数据
			manager_exam_scores = ManagerExamScore.query.all()
			found = False
			for manager_exam_score in manager_exam_scores:
				for manager_year_weight in manager_year_weights:
					if manager_year_weight.year != manager_exam_score.year:
						continue
					if manager_year_weight.manager_id != manager_exam_score.manager_id:
						continue
					if manager_year_weight.year == int(year):
						continue
					found = True
					history_manager_sum_score = manager_exam_score.manager_sum_score * manager_year_weight.weight / 100
					all_year_manager_sum_score = all_year_manager_sum_score + history_manager_sum_score
					break
				if found:
					break

			# 存历史数据表
			db.session.query(ManagerExamScore).filter(ManagerExamScore.manager_id==manager.id,ManagerExamScore.year==year).delete(synchronize_session=False)
			#db.session.add(ManagerExamScore(manager_id=manager.id,year=year,manager_score=all_manager_exam_score,manager_sum_score=all_year_manager_sum_score))
			content_score_6 = float(result["content_score_6"]) if result["content_score_6"] != None and result["content_score_6"] != '' else 0
			content_score_7 = float(result["content_score_7"]) if result["content_score_7"] != None and result["content_score_7"] != '' else 0
			content_score_8 = float(result["content_score_8"]) if result["content_score_8"] != None and result["content_score_8"] != '' else 0
			measure_score_14 = float(result["measure_score_14"]) if result["measure_score_14"] != None and result["measure_score_14"] != '' else 0
			measure_score_15 = float(result["measure_score_15"]) if result["measure_score_15"] != None and result["measure_score_15"] != '' else 0
			measure_score_16 = float(result["measure_score_16"]) if result["measure_score_16"] != None and result["measure_score_16"] != '' else 0
			measure_score_17 = float(result["measure_score_17"]) if result["measure_score_17"] != None and result["measure_score_17"] != '' else 0
			measure_score_18 = float(result["measure_score_18"]) if result["measure_score_18"] != None and result["measure_score_18"] != '' else 0
			measure_score_19 = float(result["measure_score_19"]) if result["measure_score_19"] != None and result["measure_score_19"] != '' else 0
			measure_score_20 = float(result["measure_score_20"]) if result["measure_score_20"] != None and result["measure_score_20"] != '' else 0
			measure_score_21 = float(result["measure_score_21"]) if result["measure_score_21"] != None and result["measure_score_21"] != '' else 0
			measure_score_22 = float(result["measure_score_22"]) if result["measure_score_22"] != None and result["measure_score_22"] != '' else 0
			measure_score_23 = float(result["measure_score_23"]) if result["measure_score_23"] != None and result["measure_score_23"] != '' else 0
			measure_score_24 = float(result["measure_score_24"]) if result["measure_score_24"] != None and result["measure_score_24"] != '' else 0
			db.session.add(ManagerExamScore(manager_id=manager.id,year=year,manager_score=all_manager_exam_score,manager_sum_score=all_year_manager_sum_score,
				org_sum_score=org_sum_score,content_score_6=content_score_6,content_score_7=content_score_7,content_score_8=content_score_8,
				measure_score_14=measure_score_14,measure_score_15=measure_score_15,measure_score_16=measure_score_16,measure_score_17=measure_score_17,
				measure_score_18=measure_score_18,measure_score_19=measure_score_19,measure_score_20=measure_score_20,measure_score_21=measure_score_21,
				measure_score_22=measure_score_22,measure_score_23=measure_score_23,measure_score_24=measure_score_24))
			db.session.commit()

			# 考评得分
			result["manager_score"] = round(all_manager_exam_score,2) if all_manager_exam_score>0 else ""
			# 汇总得分
			result["manager_sum_score"] = round(all_year_manager_sum_score,2) if all_year_manager_sum_score>0 else ""

		else:

			all_manager_exam_score = 0
			all_year_manager_sum_score = 0

			manager_exam_scores = ManagerExamScore.query.all()
			for manager_exam_score in manager_exam_scores:
				if manager_exam_score.year != int(year):
					continue
				if manager_exam_score.manager_id != manager.id:
					continue
				all_manager_exam_score = manager_exam_score.manager_score
				all_year_manager_sum_score = manager_exam_score.manager_sum_score
				break

			# 考评得分
			result["manager_score"] = round(all_manager_exam_score,2) if all_manager_exam_score>0 else ""
			# 汇总得分
			result["manager_sum_score"] = round(all_year_manager_sum_score,2) if all_year_manager_sum_score>0 else ""

		all_org_exam_score = 0
		all_year_org_sum_score = 0

		team_exam_scores = TeamExamScore.query.all()
		for team_exam_score in team_exam_scores:
			if team_exam_score.year != int(year):
				continue
			if team_exam_score.org_id != manager.org.id:
				continue
			all_org_exam_score = team_exam_score.org_score
			all_year_org_sum_score = team_exam_score.org_sum_score
			break

		# 部门业绩得分
		result["org_score"] = round(all_year_org_sum_score,2) if all_year_org_sum_score>0 else ""

		list.append(result)

	list = sorted(list, key = lambda result: result["org_score"], reverse=True)
	# for result_index,result in enumerate(list):
	# 	result["org_sort"] = result_index + 1
	last_score = 0
	score_index = 0
	for result in list:
		if last_score == 0:
			last_score = result["org_score"]
			result["org_sort"] = score_index + 1
		elif last_score == result["org_score"]:
			result["org_sort"] = score_index + 1
		else:
			score_index = score_index + 1
			last_score = result["org_score"]
			result["org_sort"] = score_index + 1


	list = sorted(list, key = lambda result: result["manager_score"], reverse=True)
	# for result_index,result in enumerate(list):
	# 	result["manager_sort"] = result_index + 1
	last_score = 0
	score_index = 0
	for result in list:
		if last_score == 0:
			last_score = result["manager_score"]
			result["manager_sort"] = score_index + 1
		elif last_score == result["manager_score"]:
			result["manager_sort"] = score_index + 1
		else:
			score_index = score_index + 1
			last_score = result["manager_score"]
			result["manager_sort"] = score_index + 1


	list = sorted(list, key = lambda result: result["manager_sum_score"], reverse=True)
	# for result_index,result in enumerate(list):
	# 	result["manager_sum_sort"] = result_index + 1
	last_score = 0
	score_index = 0
	for result in list:
		if last_score == 0:
			last_score = result["manager_sum_score"]
			result["manager_sum_sort"] = score_index + 1
		elif last_score == result["manager_sum_score"]:
			result["manager_sum_sort"] = score_index + 1
		else:
			score_index = score_index + 1
			last_score = result["manager_sum_score"]
			result["manager_sum_sort"] = score_index + 1	

	return list

@app.route('/api/v1/report_teams_chart', methods=['POST'])
@login_required
def report_teams_chart():
	start_year = request.form.get('start_year', None)
	end_year = request.form.get('end_year', None)

	org_id = request.form.get('org_id', None)

	success = 1

	list = None

	if start_year != None and end_year != None:
		# list = TeamExamScore.query.filter({ TeamExamScore.org_id==org_id,TeamExamScore.year>=start_year,TeamExamScore.year<=end_year }).all()
		datas = TeamExamScore.query.filter_by(org_id=org_id).all()
		list = []
		for data in datas:
			if data.year >= int(start_year) and data.year <= end_year:
				list.append(data)
	else:
		list = TeamExamScore.query.filter_by(org_id=org_id).all()

	return jsonify(success=success,list=[i.json() for i in list])

@app.route('/api/v1/report_managers_chart', methods=['POST'])
@login_required
def report_managers_chart():
	start_year = request.form.get('start_year', None)
	end_year = request.form.get('end_year', None)

	manager_id = request.form.get('manager_id', None)

	success = 1

	list = None

	if start_year != None and end_year != None:
		# list = ManagerExamScore.query.filter({ ManagerExamScore.manager_id==manager_id,ManagerExamScore.year>=start_year,ManagerExamScore.year<=end_year }).all()
		datas = ManagerExamScore.query.filter_by(manager_id=manager_id).all()
		list = []
		for data in datas:
			if data.year >= int(start_year) and data.year <= end_year:
				list.append(data)
	else:
		list = ManagerExamScore.query.filter_by(manager_id=manager_id).all()

	return jsonify(success=success,list=[i.json() for i in list])

@app.route('/api/v1/db_export', methods=['POST'])
@login_required
def db_export():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('export path:',request.form)

	path = request.form.get('path', None)
	
	def process():

		shutil.copy2(DATABASE,path)

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/db_import', methods=['POST'])
@login_required
def db_import():
	# path   = webview.create_file_dialog(webview.FOLDER_DIALOG)
	print('import path:',request.form)

	path = request.form.get('path', None)

	def process():

		shutil.copy2(path,DATABASE)
		
		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/report_manager_export', methods=['POST'])
@login_required
def report_manager_export():
	print('export path:',request.form)

	path = request.form.get('path', None)
	year  = request.form.get('year', None)
	
	if year == None:
		year = datetime.now().year

	def process():
		# exams = []
		# manager_exam_scores = ManagerExamScore.query.filter_by(year=year).all()
		# if manager_exam_scores != None: 
		# 	if len(manager_exam_scores) > 0:
		# 		list = compute_manager_score(year,False)
		# 		for manager_exam_score in manager_exam_scores:
		# 			for result in list:
		# 				if result['manager_id'] == manager_exam_score.manager_id and manager_exam_score.manager_score > 0 and manager_exam_score.manager_sum_score > 0:
		# 					exams.append(result)

		# 		exams = sorted(exams, key = lambda result: result["manager_sum_score"], reverse=True)
		
		exams = get_manager_report(year)
		print(exams)

		measures = ExamMeasure.query.join(ExamMeasure.exam_content).filter(ExamContent.exam_id==2).filter_by(show=1).order_by(ExamMeasure.sort).all()
		
		contents = ExamContent.query.filter_by(exam_id=2).order_by(ExamContent.sort).all()

		generate.gen_report_manager(path,year,exams,measures,contents)

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

@app.route('/api/v1/report_team_export', methods=['POST'])
@login_required
def report_team_export():
	print('export path:',request.form)

	path = request.form.get('path', None)
	year  = request.form.get('year', None)
	
	if year == None:
		year = datetime.now().year

	def process():
		# exams = []
		# team_exam_scores = TeamExamScore.query.filter_by(year=year).all()
		# if team_exam_scores != None: 
		# 	if len(team_exam_scores) > 0:
		# 		list = compute_org_score(year,False)
		# 		for team_exam_score in team_exam_scores:
		# 			for result in list:
		# 				if result['org_id'] == team_exam_score.org_id and team_exam_score.org_score > 0 and team_exam_score.org_sum_score > 0:
		# 					exams.append(result)
				
		# 		exams = sorted(exams, key = lambda result: result["org_sum_score"], reverse=True)

		exams = get_team_report(year)
		print(exams)

		measures = ExamMeasure.query.join(ExamMeasure.exam_content).filter(ExamContent.exam_id==1).filter_by(show=1).order_by(ExamMeasure.sort).all()
		
		contents = ExamContent.query.filter_by(exam_id=1).order_by(ExamContent.sort).all()

		generate.gen_report_team(path,year,exams,measures,contents)

		yield "data:" + str(100) + ""
		time.sleep(1)

	return Response(process(),mimetype='text/event-stream')

def start():
	app.run(host='0.0.0.0', port=5000)

def main(argv):
	start()	

if __name__ == '__main__':
    main(sys.argv[1:])