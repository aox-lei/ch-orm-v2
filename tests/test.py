from clickhouse_orm import Model, StringField, Q, Database, F, Field, Column, ArrayField, Int64Field
import pydantic

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
    table_model = (
        SellerInfo.objects_in(db)
        .filter(Q(SellerInfo.seller_id == "seller_id"))
        .only(SellerInfo.seller_name)
        .alias("seller_info")
    )

    sql = Toplist.objects_in(db).left_join(
        table_model.as_sql(), on=(Q(SellerInfo.seller_id == Toplist.seller_id))
    ).count
    print(sql)
