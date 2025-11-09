from clickhouse_orm import Model, StringField, Q, Database, F, Field, Column, ArrayField, Int64Field
import pydantic

from clickhouse_orm.funcs import SubQuery

db = Database(
    "kumiao", db_url="http://60.205.139.141:8123", username="kumiao", password="123Abc@@@"
)


class Product(Model):
    asin = StringField()
    country_code = StringField()
    item_name = StringField()
    seller_id = StringField()


class SellerInfo(Model):
    seller_id = StringField()
    country_code = StringField()
    seller_name = StringField()
    price = Int64Field()

    @classmethod
    def table_name(cls):
        return "seller_info"


class Toplist(Model):
    seller_id = StringField()
    asin = StringField()
    country_code = StringField()
    top_node = StringField()
    child_asins = ArrayField(StringField())


class ProductData(pydantic.BaseModel):
    asin: str


def test():
    sql = Toplist.objects_in(db).filter(Q(Column("(seller_id, asin)").isIn([(1, 2), (3, 4)]))).as_sql()
    print(sql)
    
