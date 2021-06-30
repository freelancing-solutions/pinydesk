import os
from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, MethodNotAllowed, Unauthorized, HTTPException
from data_service.config.exceptions import DataServiceError, InputError
from jobs import cron_create_membership_invoices, cron_down_grade_unpaid_memberships, cron_finalize_affiliate_payments
cron_bp = Blueprint('cron', __name__)

#
# @cron_bp.route('/cron/get-tickers-eod', methods=['GET'])
# def get_exchange_tickers():
#     """
#         https://eodhistoricaldata.com/api/exchange-symbol-list/PSE?api_token=6082f94d7285f7.55471245
#         use the above url to get exchange tickers data
#         #TODO see open issue about cron jobs on github
#     """
#     pass
#
#
# @cron_bp.route('/cron/get-sell-volume', methods=["GET"])
# def get_sell_volume():
#     pass
#
#
# @cron_bp.route('/cron/get-buy-volume', methods=["GET"])
# def get_buy_volume():
#     pass
#
#
# @cron_bp.route('/cron/get-net-volume', methods=["GET"])
# def get_net_volume():
#     pass


# Memberships cron jobs
@cron_bp.route('/cron/create-memberships-invoices', methods=["GET"])
def create_memberships_invoices() -> tuple:
    """
        used to go through each membership plans and executes payments
    """
    cron_create_membership_invoices()
    return 'OK', 200


@cron_bp.route('/cron/downgrade-memberships', methods=["GET"])
def downgrade_unpaid() -> tuple:
    """
        goes through memberships plans and downgrade unpaid plans
    """
    cron_down_grade_unpaid_memberships()
    return 'OK', 200


# finalize affiliate payments schedule this job
@cron_bp.route('/cron/finalize-affiliate-payment', methods=['GET'])
def finalize_affiliate_payment() -> tuple:
    """
        send affiliate payment to wallet
    """
    cron_finalize_affiliate_payments()
    return 'OK', 200
