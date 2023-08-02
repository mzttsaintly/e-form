from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from loguru import logger
import os
from json import dumps

from util.connect import db, Material, Equipments, add_material, add_equipments, queryMaterial, queryEquipments

basedir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)
cors = CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True

# db方法绑定app
db.init_app(app)

with app.app_context():
    db.create_all()
    logger.debug("正在创建表")


def materials_to_json(item):
    res_list = []
    for i in item:
        res_list.append({
            'material_name': i.material_name,
            'material_lot': i.material_lot,
            'material_EOV': i.material_EOV
        })
    return dumps(res_list, ensure_ascii=False)


@app.route("/queryMaterial", methods=['POST'])
def queryMaterial():
    res = queryMaterial()
    return materials_to_json(res)


def equipments_to_json(item):
    res_list = []
    for i in item:
        res_list.append({
            'equipName': i.equipName,
            'equipNum': i.equipNum,
            'place': i.place
        })
    return dumps(res_list, ensure_ascii=False)


@app.route("/queryEquipments", methods=["POST"])
def queryEquipments():
    res = queryEquipments()
    return equipments_to_json(res)


@app.route("/add_Material", methods=["POST"])
def add_Material():
    material_name = request.json.get('material_name')
    material_lot = request.json.get('material_lot')
    material_EOV = request.json.get('material_EOV')
    res = add_material(material_name, material_lot, material_EOV)
    return res


@app.route("/add_Equipments", methods=["POST"])
def add_Equipments():
    equipName = request.json.get('equipName')
    equipNum = request.json.get('equipNum')
    place = request.json.get('place')
    res = add_material(equipName, equipNum, place)
    return res
