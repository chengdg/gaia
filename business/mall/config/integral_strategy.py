# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from bdem import msgutil
from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from db.member import models as member_models
from db.account import models as account_models
from db.mall import promotion_models
from business.mall.corporation_factory import CorporationFactory
from gaia_conf import TOPIC


class IntegralStrategy(business_model.Model):
	"""
	积分规则
	"""
	__slots__ = (
		'id',
		'webapp_id',
		'click_shared_url_increase_count_after_buy',  # 点击分享链接为购买后的分享者增加的额度
		'click_shared_url_increase_count_before_buy', # 点击分享链接为未购买的分享者增加的额度
		'buy_increase_count_for_father',  # 成为会员增加额度
		'increase_integral_count_for_brring_customer_by_qrcode',  # 使用二维码带来用户增加的额度
		'integral_each_yuan', # 一元是多少积分
		'usable_integral_or_conpon',  # 积分与优惠券可同时使用
		'be_member_increase_count',   # 成为会员增加额度
		'order_money_percentage_for_each_buy',   #每次购物后，额外积分（以订单金额的百分比计算）
		'buy_via_offline_increase_count_for_author', # 线下会员购买为推荐者增加的额度
		'click_shared_url_increase_count',  # 分享链接给好友点击
		'buy_award_count_for_buyer',  # 购物返积分额度
		'buy_via_shared_url_increase_count_for_author',  # 通过分享链接购买为分享者增加的额度
		'buy_via_offline_increase_count_percentage_for_author',   # 线下会员购买为推荐者额外增加的额度
		'use_ceiling',  # 订单积分抵扣上限
		'review_increase',   # 商品好评送积分
		'is_all_conditions'   # 自动升级条件
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def update(self, update_params):
		"""
		更新积分规则
		"""
		corp = CorporationFactory.get()
		member_models.IntegralStrategySettings.update(
			integral_each_yuan = update_params['integral_each_yuan'],
			be_member_increase_count = update_params['be_member_increase_count'],
			click_shared_url_increase_count = update_params['click_shared_url_increase_count'],
			buy_award_count_for_buyer = update_params['buy_award_count_for_buyer'],
			order_money_percentage_for_each_buy = update_params['order_money_percentage_for_each_buy'],
			buy_via_shared_url_increase_count_for_author = update_params['buy_via_shared_url_increase_count_for_author'],
			buy_via_offline_increase_count_for_author = update_params['buy_via_offline_increase_count_for_author'],
			buy_via_offline_increase_count_percentage_for_author = update_params['buy_via_offline_increase_count_percentage_for_author'],
			use_ceiling = update_params['use_ceiling'],
			review_increase = update_params['review_increase']
		).dj_where(webapp_id=corp.webapp_id).execute()

		msg_name = 'webapp_owner_info_updated'
		topic_name = TOPIC['mall_config']
		data = {
			"corp_id": corp.id,

		}
		msgutil.send_message(topic_name, msg_name, data)

