from operator import itemgetter
from clickhouse_orm import Model, StringField, Q, Database, F
import dataclasses
import pydantic

db = Database(
    "111", db_url="http://1.1.1.1:8123", username="111", password="123"
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

    @classmethod
    def table_name(cls):
        return "seller_info"


class Toplist(Model):
    asin = StringField()
    country_code = StringField()
    top_node = StringField()


class ProductData(pydantic.BaseModel):
    asin: str


def test():
    sql = (
        Product.objects_in(db)
        .only(Product.seller_id.column_as("seller_id"))
        .filter(Q(Product.asin == "B09Q9V6G5K") & Q(Product.country_code == "US"))
        .inner_join(
            SellerInfo,
            on=(
                Q(Product.seller_id == SellerInfo.seller_id)
                & Q(Product.country_code == SellerInfo.country_code)
            ),
        )
        .inner_join(
            Toplist,
            on=(Q(Product.asin == Toplist.asin) & Q(Product.country_code == Toplist.country_code)),
        )
        .group_by(Product.asin, Product.country_code)
        .as_sql()
    )
    print(sql)
