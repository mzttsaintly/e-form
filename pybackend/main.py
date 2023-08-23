import json

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from loguru import logger
import os
from json import dumps
import datetime

from util.connect import db, Material, Equipments, User, add_material, add_equipments, queryMaterial, queryEquipments, \
    new_user, check_login, jwt
from util.get_report import mkdir, mk_json, get_report_list, read_report

from flask_jwt_extended import create_access_token, current_user
from flask_jwt_extended import jwt_required

basedir = os.path.abspath(os.path.dirname(__name__))
path = os.path.join(basedir, "report")
app = Flask(__name__)
cors = CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True

app.config["JWT_SECRET_KEY"] = "test-secret-key"  # 设置JWT密钥

# db方法绑定app
db.init_app(app)

jwt.init_app(app)

with app.app_context():
    db.create_all()
    logger.debug("正在创建表")


# 登录器
@app.route("/login", methods=["POST"])
def login():
    user_name = request.json.get('user_name', None)
    password = request.json.get('password', None)
    user = check_login(user_name, password)
    if not user:
        return jsonify("用户名或密码错误"), 401
    # 创建access_token
    access_token = create_access_token(identity=user)
    return jsonify(access_token='Bearer ' + access_token)


def materials_to_json(item):
    """
    将物料信息转换为json
    :param item: 物料对象列表
    :return: 物料信息json
    """
    res_list = []
    for i in item:
        res_list.append({
            'material_name': i.material_name,
            'material_lot': i.material_lot,
            'material_EOV': i.material_EOV
        })
    return dumps(res_list, ensure_ascii=False)


@app.route("/queryMaterial", methods=['POST'])
def query_material():
    """
    获取物料信息
    :return: 所有的物料信息json
    """
    res = queryMaterial()
    return materials_to_json(res)


def equipments_to_json(item):
    """
    将设备信息转换为json
    :param item: 设备信息列表
    :return: 设备信息json
    """
    res_list = []
    for i in item:
        res_list.append({
            'equipName': i.equipName,
            'equipNum': i.equipNum,
            'place': i.place
        })
    return dumps(res_list, ensure_ascii=False)


@app.route("/queryEquipments", methods=["POST"])
def query_equipments():
    """
    获取设备信息
    :return: 所有的设备信息json
    """
    res = queryEquipments()
    return equipments_to_json(res)


@app.route("/add_Material", methods=["POST"])
@jwt_required()
def add_Material():
    """
    添加物料信息
    :return: 添加的结果列表
    """
    res_list = []
    json_list = request.json
    for js in json_list:
        material_name = js['material_name']
        material_lot = js['material_lot']
        material_EOV = js['material_EOV']
        res_list.append(add_material(material_name, material_lot, material_EOV))
    return dumps(res_list, ensure_ascii=False)


@app.route("/add_Equipments", methods=["POST"])
@jwt_required()
def add_Equipments():
    """
    添加设备信息
    :return: 添加的结果列表
    """
    logger.debug('登录用户是：' + current_user.user_name)
    logger.debug('用户权限等级为：' + str(current_user.authority))
    res_list = []
    json_list = request.json
    for js in json_list:
        equipName = js['equipName']
        equipNum = js['equipNum']
        place = js['place']
        res_list.append(add_equipments(equipName, equipNum, place))
    return dumps(res_list, ensure_ascii=False)


@app.route("/get_data", methods=["POST"])
@jwt_required()
def get_data():
    """
    接收前端回传的报告内容并写入json文件中
    :return: 写入是否成功的提示
    """
    data = json.dumps(request.json, ensure_ascii=False)
    logger.debug(data)

    now_today = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    mkdir(path)
    filename = path + os.path.sep + now_today + '.json'
    res = mk_json(data, filename)
    return res


@app.route("/return_report_list", methods=["POST"])
@jwt_required()
def return_report_list():
    """
    返回文件夹中报告文件的列表
    :return:
    """
    logger.debug('登录用户是：' + current_user.user_name)
    logger.debug('用户权限等级为：' + str(current_user.authority))
    mkdir(path)
    res = get_report_list(path)
    return dumps(res, ensure_ascii=False)


@app.route("/return_report_json", methods=["POST"])
@jwt_required()
def return_report_json():
    """
    返回所选文件中的json内容
    :return:
    """
    logger.debug('登录用户是：' + current_user.user_name)
    logger.debug('用户权限等级为：' + str(current_user.authority))
    filename = request.json.get('filename')
    res = read_report(path + os.path.sep + filename)
    return dumps(res, ensure_ascii=False)


@app.route("/create_user", methods=["POST"])
@jwt_required()
def create_user():
    """
    新建用户
    :return:
    """
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    authority = request.json.get('authority')
    res = new_user(user_name, password, authority)
    return res
