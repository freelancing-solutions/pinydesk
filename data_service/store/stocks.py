from flask import current_app
from google.cloud import ndb
import datetime
from data_service.config import Config
from data_service.utils.utils import create_id
from data_service.config.stocks import currency_symbols

class Stock(ndb.Model):
    """
        A Model for keeping stock code, stored separately on datastore
        but also a sub model of StockModel
    """

    def set_string(self, value: str) -> str:
        """
            takes in string input verifies and returns the same string
            input: value: str
            output str
        """
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(str(self)))
        return value.strip()

    def set_stock_name(self, value: str) -> str:
        """
            verify stock_name
        """

        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(str(self)))
        return value.strip().lower()

    stock_id: str = ndb.StringProperty(required=True, indexed=True, validator=set_string)
    stock_code: str = ndb.StringProperty(required=True, indexed=True, validator=set_string)
    stock_name: str = ndb.StringProperty(required=True, validator=set_stock_name)
    symbol: str = ndb.StringProperty(required=True, indexed=True, validator=set_string)

    def __eq__(self, other) -> bool:
        if self.stock_id != other.stock_id:
            return False
        if self.stock_code != other.stock_code:
            return False
        if self.symbol != other.symbol:
            return False
        return True

    def __str__(self) -> str:
        return "<Stock stock_code: {}, symbol: {}".format(self.stock_code, self.symbol)

    def __repr__(self) -> str:
        return "<Stock: {}{}{}{}".format(self.stock_id, self.stock_code, self.symbol, self.stock_name)


class Broker(ndb.Model):
    """
        a model for storing broker data
    """

    def set_id(self, broker_id: str) -> str:

        if broker_id is None or broker_id == "":
            raise ValueError("{} can only accept a string".format(str(self)))
        if not isinstance(broker_id, str):
            raise TypeError("{} can only be a string".format(str(self)))
        return broker_id.strip()

    def set_broker_code(self, broker_code: str) -> str:

        if broker_code is None or broker_code == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(broker_code, str):
            raise TypeError("{} can only be a string".format(str(self)))
        return broker_code.strip()

    def set_broker_name(self, broker_name: str) -> str:
        broker_name = broker_name.strip()
        if broker_name is None or broker_name == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(broker_name, str):
            raise TypeError("{} can only be a string".format(str(self)))
        return broker_name.strip().lower()

    broker_id: str = ndb.StringProperty(required=True, indexed=True, validator=set_id)
    broker_code: str = ndb.StringProperty(required=True, indexed=True, validator=set_broker_code)
    broker_name: str = ndb.StringProperty(required=True, validator=set_broker_name)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False

        if self.broker_id != other.broker_id:
            return False
        if self.broker_code != other.broker_code:
            return False
        return True

    def __str__(self) -> str:
        return "<Broker broker_code: {} {}".format(self.broker_code, self.broker_name)

    def __repr__(self) -> str:
        return "<Broker: {} {} {}".format(self.broker_id, self.broker_code, self.broker_name)


class StockModel(ndb.Model):
    """
        remember to set timezone info when saving date
        id,
        stock_id,
        broker_id,
        stock_code,
        stock_name,
        broker_code,
        date,
        buy_volume,
        buy_value,
        buy_ave_price,
        buy_market_val_percent,
        buy_trade_count,
        sell_volume,
        sell_value,
        sell_ave_price,
        sell_market_val_percent,
        sell_trade_count,
        net_volume,
        net_value,
        total_volume,
        total_value
    """

    def set_id(self, value: str) -> str:

        if value is None or value == "":
            raise ValueError('{} cannot be Null'.format(str(self)))
        if not isinstance(value, str):
            raise TypeError('{} may only be a string'.format(str(self)))
        return value.strip()

    def set_stock(self, stock: Stock) -> Stock:
        if not isinstance(stock, Stock):
            raise TypeError('{}, needs to be an instance of Stock'.format(str(self)))
        return stock

    def set_broker(self, broker: Broker) -> Broker:
        if not isinstance(broker, Broker):
            raise TypeError("{}, Needs to be an instance of Broker".format(str(self)))
        return broker

    exchange_id: str = ndb.StringProperty(required=True, indexed=True, validator=set_id)
    transaction_id: str = ndb.StringProperty(validator=set_id)
    stock = ndb.StructuredProperty(Stock, validator=set_stock)
    broker = ndb.StructuredProperty(Broker, validator=set_broker)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        return True

    def __str__(self) -> str:
        return "<Stock_Model: Stock : {} , Broker {}".format(str(self.stock), str(self.broker))

    def __repr__(self) -> str:
        return "<Stock_Model: {}{}{}".format(self.transaction_id, self.stock.stock_id, self.broker.broker_id)


class BuyVolumeModel(ndb.Model):
    """
        daily buy volumes
    """
    # TODO find out why it seems i can set values of None even if i am checking against
    def set_stock_id(self, value: str) -> str:
        if (value is None) or (value == ""):
            raise ValueError('{} cannot be Null'.format(str(self)))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(str(self)))

        return value.strip()

    def set_date(self, value: datetime.date) -> datetime.date:
        if isinstance(value, datetime.date):
            return value
        raise TypeError('{} can only be an object of datetime'.format(str(self)))

    def set_int_property(self, value: int) -> int:
        if value is None or value == "":
            raise ValueError("{} can not be Null".format(str(self)))

        if not isinstance(value, int):
            raise TypeError("{} can only be an Integer".format(str(self)))
        if value < 0:
            raise ValueError("{} can only be a positive integer".format(str(self)))
        return value

    def set_currency(self, value: str) -> str:
        if value not in currency_symbols():
            raise TypeError("{} not a valid currency".format(str(self)))
        return value
    transaction_id: str = ndb.StringProperty(indexed=True, required=True, default=create_id())
    stock_id: str = ndb.StringProperty(validator=set_stock_id)
    date_created: datetime.date = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET),
                                                   validator=set_date)
    currency: str = ndb.StringProperty(default=Config.CURRENCY, validator=set_currency)
    buy_volume: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_value: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_ave_price: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_market_val_percent: int = ndb.IntegerProperty(default=0, validator=set_int_property)
    buy_trade_count: int = ndb.IntegerProperty(default=0, validator=set_int_property)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        return True

    def __str__(self) -> str:
        return "<Buy_Volume: date_created: {} buy volume: {} , buy value: {}, buy ave price: {}, " \
               "buy market value percent: {}, buy trade account: {}".format(self.date_created, self.buy_volume,
                                                                            self.buy_value, self.buy_ave_price,
                                                                            self.buy_market_val_percent,
                                                                            self.buy_trade_count)

    def __repr__(self) -> str:
        return "<Buy_Volume: {}{}{}".format(self.transaction_id, self.stock_id, self.date_created)


class SellVolumeModel(ndb.Model):
    """
        daily sell volumes
    """

    def set_id(self, value: str) -> str:

        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(str(self)))
        return value.strip()

    def set_int(self, value: int) -> int:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, int):
            raise TypeError("{} can only be an integer".format(str(self)))
        if value < 0:
            raise ValueError("{} can only be a positive integer".format(str(self)))
        return value

    def set_percent(self, value: int) -> int:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, int):
            raise TypeError("{} can only be an integer".format(str(self)))
        if (value < 0) or (value > 100):
            raise ValueError("{} should be a percentage".format(str(self)))
        return value

    def set_transaction_id(self, transaction_id: str) -> str:
        if transaction_id is None or transaction_id == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(transaction_id, str):
            raise TypeError("{} can only be a str".format(str(self)))
        return transaction_id.strip()

    def set_currency(self, value: str) -> str:
        if value not in currency_symbols():
            raise TypeError("{} not a valid currency".format(str(self)))
        return value

    transaction_id: str = ndb.StringProperty(indexed=True, validator=set_transaction_id)

    stock_id: str = ndb.StringProperty(validator=set_id)
    # Auto now add can be over written
    date_created: datetime.date = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    currency: str = ndb.StringProperty(default=Config.CURRENCY, validator=set_currency)
    sell_volume: int = ndb.IntegerProperty(default=0, validator=set_int)
    sell_value: int = ndb.IntegerProperty(default=0, validator=set_int)
    sell_ave_price: int = ndb.IntegerProperty(default=0, validator=set_int)
    sell_market_val_percent: int = ndb.IntegerProperty(default=0, validator=set_percent)
    sell_trade_count: int = ndb.IntegerProperty(default=0, validator=set_int)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        return True

    def __str__(self) -> str:
        return "<Sell_Volume: Date_Created : {} , sell_volume: {}, sell_value: {}, sell_ave_price: {}, " \
               "sell_market_val_percent: {}, sell_trade_account: {}".format(self.date_created, self.sell_volume,
                                                                            self.sell_value, self.sell_ave_price,
                                                                            self.sell_market_val_percent,
                                                                            self.sell_trade_count)

    def __repr__(self) -> str:
        return "Sell_Volume: {} {} {}".format(self.transaction_id, self.stock_id, self.date_created)


class NetVolumeModel(ndb.Model):
    """
        daily net volume
    """

    def set_id(self, value: str) -> str:

        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(str(self)))
        return value.strip()

    def set_int(self, value: int) -> int:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, int):
            raise TypeError("{} can only be a string".format(str(self)))
        if value < 0:
            raise ValueError("{} cannot be Negative".format(str(self)))
        return value

    def set_date(self, value: datetime.date) -> datetime.date:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, datetime.date):
            raise TypeError("{} can only be a date instance".format(str(self)))
        return value

    def set_currency(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(str(self)))
        if not isinstance(value, str):
            raise TypeError("{} can only be string".format(str(self)))

        if not (value in currency_symbols()):
            raise TypeError("{} not a currency symbol".format(str(self)))
        return value

    stock_id: str = ndb.StringProperty(validator=set_id)
    transaction_id: str = ndb.StringProperty(validator=set_id)
    date_created: datetime.date = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET), validator=set_date)
    currency: str = ndb.StringProperty(default=Config.CURRENCY, validator=set_currency)
    net_volume: int = ndb.IntegerProperty(default=0, validator=set_int)
    net_value: int = ndb.IntegerProperty(default=0, validator=set_int)
    total_volume: int = ndb.IntegerProperty(default=0, validator=set_int)
    total_value: int = ndb.IntegerProperty(default=0, validator=set_int)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        return True

    def __str__(self) -> str:
        return "<Net_Volume: date_created: {}, net_volume: {}, net_value: {}, total_volume: {}, total_value: {}".format(
            self.date_created, self.net_volume, self.net_value, self.total_volume, self.total_value)

    def __repr__(self) -> str:
        return "<Net_Volume: {}{}{}".format(self.date_created, self.transaction_id, self.stock_id)
