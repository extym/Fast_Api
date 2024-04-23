from flask_login import UserMixin
# from flask_user import UserMixin
from project import db
from sqlalchemy import ForeignKey


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    login = db.Column(db.String(250))
    name = db.Column(db.String(250))
    company_id = db.Column(db.String(250))
    roles = db.Column(db.String(250))
    photo = db.Column(db.String(250))
    date_added = db.Column(db.String(250))
    date_modifed = db.Column(db.String(250))


class ConsultUsers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    current_user_id = db.Column(db.String(250))
    name = db.Column(db.String(250))
    phone = db.Column(db.String(250))
    company_id = db.Column(db.String(250))
    role = db.Column(db.String(250))
    date_added = db.Column(db.String(250))
    date_modifed = db.Column(db.String(250))



class Product(db.Model):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    articul_product = db.Column(db.String(250), unique=True)
    shop_name = db.Column(db.String(250))
    store_id = db.Column(db.String(250))
    quantity = db.Column(db.Integer())
    reserved = db.Column(db.Integer())
    price_product_base = db.Column(db.Integer())
    final_price = db.Column(db.String(250))
    old_price = db.Column(db.String(250))
    discount = db.Column(db.Double())
    description_product = db.Column(db.String(250))
    photo = db.Column(db.String(250))
    id_1c = db.Column(db.String(250))
    date_added = db.Column(db.String(250))
    date_modifed = db.Column(db.String(250))
    selected_mp = db.Column(db.String(250))
    name_product = db.Column(db.String(250))
    status_mp = db.Column(db.String(250))
    images_product = db.Column(db.String(250))
    price_add_k = db.Column(db.Double())
    discount_mp_product = db.Column(db.Double())
    set_shop_name = db.Column(db.String(250))
    external_sku = db.Column(db.String(250))
    alias_prod_name = db.Column(db.String(250))
    status_in_shop = db.Column(db.String(250))
    shop_k_product = db.Column(db.String(250))
    discount_shop_product = db.Column(db.String(250))
    quantity_for_shop = db.Column(db.Integer())
    description_product_add = db.Column(db.String(500))
    uid_edit_user = db.Column(db.Integer())
    description_category_id = db.Column(db.Integer())
    type_id = db.Column(db.Integer())
    volume_weight = db.Column(db.Double())
    barcode = db.Column(db.String(50))
    cart_id = db.Column(db.String(250))
    brand = db.Column(db.String(250))
    brand_id = db.Column(db.String(250))

    # attributes_product = db.Column(db.Integer())   #'attributes_product.id')


class AttributesProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer)
    articul_product = db.Column(db.String(250))
    depth = db.Column(db.String(250))
    width = db.Column(db.String(250))
    height = db.Column(db.String(250))
    dimension_unit = db.Column(db.String(250))
    weight = db.Column(db.String(250))
    weight_unit = db.Column(db.String(250))
    barcode = db.Column(db.String(250))
    category_id_oson = db.Column(db.String(250))
    created_at = db.Column(db.String(250))
    images = db.Column(db.String(250))
    marketing_price = db.Column(db.String(250))
    min_ozon_price= db.Column(db.String(250))
    old_price = db.Column(db.String(250))
    premium_price = db.Column(db.String(250))
    price = db.Column(db.String(250))
    recommended_price = db.Column(db.String(250))
    min_price = db.Column(db.String(250))
    stocks = db.Column(db.Boolean())
    vat = db.Column(db.String(250))
    visible = db.Column(db.Boolean())
    commissions = db.Column(db.String(250))
    is_prepayment = db.Column(db.Boolean())
    is_prepayment_allowed = db.Column(db.Boolean())
    images360 = db.Column(db.String(250))
    color_image = db.Column(db.String(250))
    primary_image = db.Column(db.String(250))
    is_kgt = db.Column(db.Boolean())
    discounted_stocks = db.Column(db.String(250))
    sku = db.Column(db.Integer())
    description_category_id = db.Column(db.Integer())
    type_id = db.Column(db.Integer())
    volume_weight = db.Column(db.Double())


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_order_id = db.Column(db.String(250))
    mp_order_id = db.Column(db.String(250))
    article = db.Column(db.String(250))
    article_mp = db.Column(db.String(250))
    id_1c = db.Column(db.String(250))
    name = db.Column(db.String(250))
    shop_name = db.Column(db.String(250))
    mp = db.Column(db.String(250))
    company_id = db.Column(db.String(250))
    quantity = db.Column(db.Integer())
    price = db.Column(db.String(250))
    add_price = db.Column(db.String(250))
    discount = db.Column(db.Double())
    description = db.Column(db.String(250))
    photo = db.Column(db.String(250))
    category = db.Column(db.String(250))
    shipment_date = db.Column(db.String(250))
    order_status = db.Column(db.String(250))
    shop_status = db.Column(db.String(250))
    delivery_type = db.Column(db.String(250))
    delivery_point = db.Column(db.String(250))
    returned = db.Column(db.Boolean())
    date_added = db.Column(db.String(250))
    date_modifed = db.Column(db.String(250))


class SalesToday(db.Model):
    __tablename__='order_items'
    id = db.Column(db.Integer, primary_key=True)
    shop_order_id = db.Column(db.String(250))
    mp_order_id = db.Column(db.String(250), primary_key=True)
    article = db.Column(db.String(250))
    article_mp = db.Column(db.String(250))
    id_1c = db.Column(db.String(250))
    name = db.Column(db.String(250))
    shop_name = db.Column(db.String(250))
    mp = db.Column(db.String(250))
    company_id = db.Column(db.String(250))
    quantity = db.Column(db.Integer())
    price = db.Column(db.String(250))
    add_price = db.Column(db.String(250))
    # discount = db.Column(db.Double())
    photo = db.Column(db.String(250))
    category = db.Column(db.String(250))
    shipment_date = db.Column(db.String(250))
    order_status = db.Column(db.String(250))
    shop_status = db.Column(db.String(250))
    delivery_type = db.Column(db.String(250))
    delivery_point = db.Column(db.String(250))
    is_cancelled = db.Column(db.Boolean())
    date_added = db.Column(db.String(250))
    date_modifed = db.Column(db.String(250))


class Marketplaces(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(50))
    seller_id = db.Column(db.String(50))
    name_mp = db.Column(db.String(50))
    key_mp = db.Column(db.String(1000))
    shop_name = db.Column(db.String(50))
    shop_id = db.Column(db.Integer())
    company_id = db.Column(db.String(50))
    warehouses = db.Column(db.Integer())
    mp_discount = db.Column(db.Double())
    mp_markup = db.Column(db.Double())
    store_discount = db.Column(db.Double())
    store_markup = db.Column(db.Double())
    date_added = db.Column(db.String(50))
    date_modifed = db.Column(db.String(50))


class InternalImport(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    internal_import_mp_1 = db.Column(db.String(50))
    internal_import_store_1 = db.Column(db.String(50))
    internal_import_role_1 = db.Column(db.String(50))
    internal_import_discount_1 = db.Column(db.Integer())
    internal_import_markup_1 = db.Column(db.Integer())
    internal_import_mp_2 = db.Column(db.String(50))
    internal_import_store_2 = db.Column(db.String(50))
    internal_import_role_2 = db.Column(db.String(50))
    internal_import_discount_2 = db.Column(db.Integer())
    internal_import_markup_2 = db.Column(db.Integer())
    company_id = db.Column(db.String(50))
    user_id = db.Column(db.String(50))



#
# Define Role model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define UserRoles model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
