import typing
from google.cloud import ndb
import datetime
from flask import current_app, jsonify
from pinoydesk.store.stocks import Stock, Broker, StockModel, BuyVolumeModel, SellVolumeModel, NetVolumeModel


class StockView:
    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.PROJECT)
        with current_app.app_context():
            self.timezone = datetime.timezone(current_app.config.UTC_OFFSET)

    def create_stock_data(self, stock_data: dict) -> tuple:
        with self.client.context():

            if 'stock_id' in stock_data and stock_data['stock_id'] != "":
                stock_id = stock_data['stock_id']
            else:
                return jsonify({'status': False, 'message': 'Stock Id is required'}), 500
            if 'stock_code' in stock_data and stock_data['stock_code'] != "":
                stock_code = stock_data['stock_code']
            else:
                return jsonify({'status': False, 'message': 'Stock Code is required'}), 500

            if 'stock_name' in stock_data and stock_data['stock_name'] != "":
                stock_name = stock_data['stock_name']
            else:
                return jsonify({'status': False, 'message': 'Stock Name is required'}), 500
            if 'symbol' in stock_data and stock_data['symbol'] != "":
                symbol = stock_data['symbol']
            else:
                return jsonify({'status': False, 'message': 'Stock Symbol is required'}), 500
            try:
                stock_instance = Stock(stock_id=stock_id, stock_code=stock_code, stock_name=stock_name, symbol=symbol)
                key = stock_instance.put()

            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500

            return jsonify({'status': True,
                            'message': 'successfully saved stock data',
                            "payload": {"stock_instance": stock_instance.to_dict()}}), 200

    def create_broker_data(self, broker_data: dict) -> tuple:
        with self.client.context():

            if "broker_id" in broker_data and broker_data['broker_id'] != "":
                broker_id = broker_data['broker_id']
            else:
                return jsonify({'status': False, 'message': 'Broker ID is required'}), 500

            if "broker_code" in broker_data and broker_data['broker_code'] != "":
                broker_code = broker_data['broker_code']
            else:
                return jsonify({'status': False, 'message': 'Broker ID is required'}), 500

            try:
                broker_instance = Broker(broker_id=broker_id, broker_code=broker_code)
                key = broker_instance.put()
            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500

            return jsonify({'status': True, 'message': 'successfully saved broker data',
                            'payload': broker_instance.to_dict()}), 200

    def create_stock_model(self, exchange_id: str, sid: str, stock_id: str, broker_id: str) -> tuple:
        with self.client.context():
            try:
                stock_list: typing.List[Stock] = Stock.query(Stock.stock_id == stock_id).fetch()
                stock = [0]
                broker_list: typing.List[Broker] = Broker.query(Broker.broker_id == broker_id).fetch()
                broker = broker_list[0]
                stock_model_instance = StockModel(exchange_id=exchange_id, sid=sid, stock=stock, broker=broker)
                key = stock_model_instance.put()
            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': e}), 500
            return jsonify({'status': True, 'message': 'Stock Model Successfully created',
                            'payload': stock_model_instance.to_dict()}), 200

    def create_buy_model(self, buy_data: dict) -> tuple:
        with self.client.context():
            if "stock_id" in buy_data and buy_data['stock_id'] != "":
                stock_id: str = buy_data['stock_id']
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500
            if "date" in buy_data and buy_data['date'] != "":
                date: datetime.date = buy_data['date']
            else:
                return jsonify({'status': False, 'message': "date is required"}), 500

            if "buy_volume" in buy_data and buy_data['buy_volume'] != "":
                buy_volume: int = int(buy_data['buy_volume'])
            else:
                return jsonify({'status': False, 'message': "buy volume is required"}), 500

            if "buy_value" in buy_data and buy_data["buy_value"] != "":
                buy_value: int = int(buy_data["buy_value"])
            else:
                return jsonify({'status': False, 'message': "buy value is required"}), 500

            if "buy_ave_price" in buy_data and buy_data["buy_ave_price"] != "":
                buy_ave_price: int = int(buy_data["buy_ave_price"])
            else:
                return jsonify({'status': False, 'message': "buy average price is required"}), 500

            if "buy_market_val_percent" in buy_data and buy_data["buy_market_val_percent"] != "":
                buy_market_val_percent: int = int(buy_data["buy_market_val_percent"])
            else:
                return jsonify({'status': False, 'message': "buy market value percent is required"}), 500

            if "buy_trade_count" in buy_data and buy_data["buy_trade_count"] != "":
                buy_trade_count: int = int(buy_data["buy_trade_count"])
            else:
                return jsonify({'status': False, 'message': "buy trade account"}), 500
            try:
                buy_volume_instance: BuyVolumeModel = BuyVolumeModel(stock_id=stock_id, date=date, buy_volume=buy_volume, buy_value=buy_value,
                                                                     buy_ave_price=buy_ave_price, buy_market_val_percent=buy_market_val_percent,
                                                                     buy_trade_count=buy_trade_count)
                key = buy_volume_instance.put()
            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            return jsonify({'status': True, 'message': 'Stock Model Successfully created',
                            'payload': buy_volume_instance.to_dict()}), 200

    def create_sell_volume(self, sell_data: dict) -> tuple:
        with self.client.context():
            if "stock_id" in sell_data and sell_data['stock_id'] != "":
                stock_id: str = sell_data['stock_id']
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500

            if "date" in sell_data and sell_data["date"] != "":
                date: datetime.date = sell_data['date']
            else:
                return jsonify({'status': False, 'message': "date is required"}), 500

            if "sell_volume" in sell_data and sell_data["sell_volume"] != "":
                sell_volume: int = int(sell_data["sell_volume"])
            else:
                return jsonify({"status": False , "message": "sell volume is required"}), 500

            if "sell_value" in sell_data and sell_data["sell_value"] != "":
                sell_value: int = int(sell_data["sell_value"])
            else:
                return jsonify({"status": False, "message": "sell value is required"}), 500

            if "sell_ave_price" in sell_data and sell_data["sell_ave_price"] != "":
                sell_ave_price: int = int(sell_data["sell_ave_price"])
            else:
                return jsonify({"status": False, "message": "sell ave price is required"}), 500

            if "sell_market_val_percent" in sell_data and sell_data["sell_market_val_percent"] != "":
                sell_market_val_percent: int = int(sell_data["sell_market_val_percent"])
            else:
                return jsonify({"status": False, "message": "sell market value percent price is required"}), 500

            if "sell_trade_count" in sell_data and sell_data["sell_trade_count"] != "":
                sell_trade_count: int = int(sell_data["sell_trade_count"])
            else:
                return jsonify({"status": False, "message": "sell trade account percent price is required"}), 500

            try:
                sell_volume_instance: SellVolumeModel = SellVolumeModel(stock_id=stock_id, date=date, sell_volume=sell_volume,
                                                                        sell_value=sell_value, sell_ave_price=sell_ave_price,
                                                                        sell_market_val_percent=sell_market_val_percent,
                                                                        sell_trade_count=sell_trade_count)
                key = sell_volume_instance.put()
            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500

            return jsonify({'status': True, 'message': 'Sell Volume Successfully created',
                            'payload': sell_volume_instance.to_dict()}), 200

    def create_net_volume(self, net_volume_data: dict) -> tuple:
        with self.client.context():
            if "stock_id" in net_volume_data and net_volume_data["stock_id"] != "":
                stock_id: str = net_volume_data["stock_id"]
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500
            if "date" in net_volume_data and net_volume_data['date'] != "":
                date: datetime.date = net_volume_data['date']
            else:
                return jsonify({'status': False, 'message': "date is required"}), 500

            if "transaction_id" in net_volume_data and net_volume_data["transaction_id"] != "":
                transaction_id: str = net_volume_data["transaction_id"]
            else:
                return jsonify({'status': False, 'message': "transaction id is required"}), 500

            if "net_volume" in net_volume_data and net_volume_data["net_volume"] != "":
                net_volume: int = int(net_volume_data["net_volume"])
            else:
                return jsonify({'status': False, 'message': "net volume is required"}), 500

            if "net_value" in net_volume_data and net_volume_data["net_value"] != "":
                net_value: int = int(net_volume_data["net_value"])
            else:
                return jsonify({'status': False, 'message': "net value is required"}), 500

            if "total_value" in net_volume_data and net_volume_data["total_value"] != "":
                total_value: int = int(net_volume_data["total_value"])
            else:
                return jsonify({'status': False, 'message': "total value is required"}), 500

            if "total_volume" in net_volume_data and net_volume_data["total_volume"] != "":
                total_volume: int = int(net_volume_data['total_volume'])
            else:
                return jsonify({'status': False, 'message': "total volume is required"}), 500

            try:
                net_volume_instance: NetVolumeModel = NetVolumeModel(stock_id=stock_id, transaction_id=transaction_id, date=date,
                                                                     net_volume=net_volume, net_value=net_value, total_value=total_value,
                                                                     total_volume=total_volume)
                key = net_volume_instance.put()

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            return jsonify({'status': True, 'message': 'Net Volume Successfully created',
                            'payload': net_volume_instance.to_dict()}), 200






