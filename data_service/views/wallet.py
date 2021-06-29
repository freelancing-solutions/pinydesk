import typing
from flask import jsonify, current_app
from data_service.config.exceptions import DataServiceError
from data_service.store.mixins import AmountMixin
from data_service.store.wallet import WalletModel, WalletValidator
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context


class Validator(WalletValidator):

    def __init__(self):
        super(Validator, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @staticmethod
    def is_uid_none(uid: typing.Union[None, str]) -> bool:
        if (uid is None) or (uid == ''):
            return True
        return False

    def can_add_wallet(self, uid: typing.Union[None, str] = None) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = self.wallet_exist(uid=uid)
            if isinstance(wallet_exist, bool):
                return not wallet_exist
            raise DataServiceError('Unable to verify wallet data')
        return False

    def can_update_wallet(self, uid: typing.Union[None, str] = None) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = self.wallet_exist(uid=uid)
            if isinstance(wallet_exist, bool):
                return wallet_exist
            raise DataServiceError('Unable to verify wallet data')
        return False

    def can_reset_wallet(self, uid: typing.Union[None, str]) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = self.wallet_exist(uid=uid)
            if isinstance(wallet_exist, bool):
                return wallet_exist
            raise DataServiceError('Unable to verify wallet data')
        return False


class WalletView(Validator):
    """
        view functions for the wallet
        # TODO -  Refactor Wallet View and improve functionality
    """

    def __init__(self):
        super(WalletView, self).__init__()

    @use_context
    @handle_view_errors
    def create_wallet(self, uid: str, currency: str, paypal_address: str) -> tuple:
        if self.can_add_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel()
            amount_instance: AmountMixin = AmountMixin()
            amount_instance.amount = 0
            amount_instance.currency = currency
            wallet_instance.uid = uid
            wallet_instance.available_funds = amount_instance
            wallet_instance.paypal_address = paypal_address
            key = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                raise DataServiceError("An Error occurred creating Wallet")
            return jsonify({'status': True, 'message': 'successfully created wallet',
                            'payload': wallet_instance.to_dict()}), 200
        return jsonify({'status': False, 'message': 'Unable to create wallet'}), 500

    @use_context
    @handle_view_errors
    def get_wallet(self, uid: typing.Union[str, None]) -> tuple:
        if not(self.is_uid_none(uid=uid)):
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(), 'message': 'wallet found'}), 200
        return jsonify({'status': False, 'message': 'uid cannot be None'}), 500

    @use_context
    @handle_view_errors
    def update_wallet(self, wallet_data: dict) -> tuple:
        uid: typing.Union[str, None] = wallet_data.get("uid")
        available_funds: typing.Union[int, None] = wallet_data.get("available_funds")
        currency: typing.Union[str, None] = wallet_data.get('currency')
        paypal_address: typing.Union[str, None] = wallet_data.get("paypal_address")
        if self.can_update_wallet(uid=uid) is True:
            wall_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            wall_instance.uid = uid
            amount_instance: AmountMixin = AmountMixin(amount=available_funds, currency=currency)
            wall_instance.available_funds = amount_instance
            wall_instance.paypal_address = paypal_address
            key = wall_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                raise DataServiceError("An Error occurred updating Wallet")

            return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                            'message': 'successfully updated wallet'}), 200
        return jsonify({'status': False, 'message': 'Unable to update wallet'}), 500

    @use_context
    @handle_view_errors
    def reset_wallet(self, wallet_data: dict) -> tuple:
        uid: typing.Union[str, None] = wallet_data.get('uid')
        currency: typing.Union[str, None] = wallet_data.get('currency')
        if self.can_reset_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)
            wallet_instance.available_funds = amount_instance
            key = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                raise DataServiceError("An Error occurred resetting Wallet")

            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': 'wallet is rest'}), 200
        return jsonify({'status': False, 'message': 'Unable to reset wallet'}), 500

    @use_context
    @handle_view_errors
    def return_all_wallets(self) -> tuple:
        wallet_list: typing.List[WalletModel] = WalletModel.query().fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload,
                        'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    def return_wallets_by_balance(self, lower_bound: int, higher_bound: int) -> tuple:
        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.available_funds > lower_bound,
                                                                  WalletModel.available_funds < higher_bound).fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    def wallet_transact(self, uid: str, add: int = None, sub: int = None) -> tuple:
        if self.can_update_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            if isinstance(wallet_instance, WalletModel):
                if add is not None:
                    wallet_instance.available_funds.amount += add
                if sub is not None:
                    wallet_instance.available_funds.amount -= sub
                key = wallet_instance.put()
                if key is None:
                    message: str = "General error updating database"
                    return jsonify({'status': False, 'message': message}), 500
                message: str = "Successfully created transaction"
                return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                                'message': message}), 200
        message: str = "Unable to find wallet"
        return jsonify({'status': False, 'message': message}), 500

