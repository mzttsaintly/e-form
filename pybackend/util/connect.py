from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError
from loguru import logger
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import JWTManager
# 创建对象，所有数据库方法从db取
db = SQLAlchemy()

jwt = JWTManager()


class Material(db.Model):
    # 创建物料信息数据表模板
    __tablename__ = 'Material'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String())  # 物料名称
    material_lot = db.Column(db.String())  # 物料批号
    material_EOV = db.Column(db.String())  # 有效期

    __table_args__ = (db.UniqueConstraint('material_name', 'material_lot'),)


class Equipments(db.Model):
    # 创建设备信息数据表模板
    __tablename__ = 'Equipments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    equipName = db.Column(db.String())  # 设备名称
    equipNum = db.Column(db.String())  # 设备编号
    place = db.Column(db.String())  # 设备存放地点

    __table_args__ = (db.UniqueConstraint('equipName', 'equipNum'),)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    # 1为上传报告的权限，2为修改物料设备信息的权限，4为增加新用户的权限，可累加
    authority = db.Column(db.Integer)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, new_password):
        self.password_hash = generate_password_hash(new_password)


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


def new_user(user_name, password, authority):
    """
    创建新用户
    :param user_name:
    :param password:
    :param authority:
    :return: str,是否创建完成
    """
    try:
        db.session.add(User(
            user_name=user_name,
            password=password,
            authority=authority
        ))
        db.session.commit()
    except IntegrityError:
        return "用户名不可重复"
    except SQLAlchemyError:
        return "发生错误，请检查数据格式是否正确"
    return "创建完成"


def check_login(user_name, password):
    user = User.query.filter(User.user_name == user_name).one_or_none()
    if user and user.check_password(password):
        return user
    else:
        return None


def update_material(material_id, **kwargs):
    """
    修改物料信息
    :param material_id: 需修改的物料条目id
    :param kwargs: 需修改的内容
    :return:
    """
    Material.query.filter(Material.id == material_id).update(kwargs)
    db.session.commit()


def del_material(material_id):
    """
    删除选定物料
    :param material_id: 需删除的物料条目id
    :return:
    """
    Material.query.filter(Material.id == material_id).delete()
    db.session.commit()


def update_equipments(equipments_id, **kwargs):
    """
    修改设备信息
    :param equipments_id: 需修改的设备条目id
    :param kwargs: 修改的内容
    :return:
    """
    Equipments.query.filter(Equipments.id == equipments_id).update(kwargs)
    db.session.commit()


def del_equipment(equipments_id):
    """
    删除设备信息
    :param equipments_id: 需删除的设备条目id
    :return:
    """
    Equipments.query.filter(Equipments.id == equipments_id).delete()
    db.session.commit()


# 注册一个回调函数，该函数在使用 create_access_token 创建 JWT 时将传入的任何对象作为身份，并将其转换为 JSON 可序列化格式。
@jwt.user_identity_loader
def user_identity_lookup(user):
    logger.debug('user_identity_lookup', user)
    return user.id


# 注册一个回调函数，在访问受保护的路由时从数据库自动加载用户（current_user）。
# 这应该在成功查找时返回任何 python 对象，或者如果查找因任何原因失败（例如，如果用户已从数据库中删除）则返回 None。
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    logger.debug('user_lookup_callback', _jwt_header, jwt_data)
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

