from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# 创建对象，所有数据库方法从db取
db = SQLAlchemy()


class Material(db.Model):
    # 创建物料信息数据表模板
    __tablename__ = 'Material'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String())  # 物料名称
    material_lot = db.Column(db.String())  # 物料批号
    material_EOV = db.Column(db.String())  # 有效期

    __table_args__ = (db.UniqueConstraint('material_name', 'material_lot'), )


class Equipments(db.Model):
    # 创建设备信息数据表模板
    __tablename__ = 'Equipments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipName = db.Column(db.String())  # 设备名称
    equipNum = db.Column(db.String())  # 设备编号
    place = db.Column(db.String())  # 设备存放地点

    __table_args__ = (db.UniqueConstraint('equipName', 'equipNum'), )


def add_material(material_name, material_lot, material_EOV):
    try:
        db.session.add(Material(
            material_name=material_name,
            material_lot=material_lot,
            material_EOV=material_EOV
        ))
        db.session.commit()
    except SQLAlchemyError:
        return "发生错误，请检查数据格式是否正确"
    return "写入完成"


def add_equipments(equipName, equipNum, place):
    try:
        db.session.add(Equipments(
            equipName=equipName,
            equipNum=equipNum,
            place=place
        ))
        db.session.commit()
    except SQLAlchemyError:
        return "发生错误，请检查数据格式是否正确"
    return "写入完成"


def queryMaterial():
    res = Material.query.all()
    return res


def queryEquipments():
    res = Equipments.query.all()
    return res
