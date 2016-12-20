# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AIntegralStrategy(api_resource.ApiResource):
	"""
	积分规则
	"""
	app = 'mall'
	resource = 'integral_strategy'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		integral_strategy = corp.mall_config_repository.get_integral_strategy()

		data = {
			'id': integral_strategy.id,
			'integral_each_yuan': integral_strategy.integral_each_yuan,
			'be_member_increase_count': integral_strategy.be_member_increase_count,
			'click_shared_url_increase_count': integral_strategy.click_shared_url_increase_count,
			'buy_award_count_for_buyer': integral_strategy.buy_award_count_for_buyer,
			'order_money_percentage_for_each_buy': integral_strategy.order_money_percentage_for_each_buy,
			'buy_via_shared_url_increase_count_for_author': integral_strategy.buy_via_shared_url_increase_count_for_author,
			'buy_via_offline_increase_count_for_author': integral_strategy.buy_via_offline_increase_count_for_author,
			'buy_via_offline_increase_count_percentage_for_author': integral_strategy.buy_via_offline_increase_count_percentage_for_author,
			'use_ceiling': integral_strategy.use_ceiling,
			'review_increase': integral_strategy.review_increase,
			'can_enable_integral_ceiling': integral_strategy.can_enable_integral_ceiling
		}

		return data

	@param_required([
		'corp_id',
		'integral_each_yuan',  # 一元是多少积分
		'be_member_increase_count',  # 成为会员增加额度
		'click_shared_url_increase_count', # 分享链接给好友点击
		'buy_award_count_for_buyer',   # 购物返积分额度
		'order_money_percentage_for_each_buy',   #每次购物后，额外积分（以订单金额的百分比计算）
		'buy_via_shared_url_increase_count_for_author',  # 通过分享链接购买为分享者增加的额度
		'buy_via_offline_increase_count_for_author',  # 线下会员购买为推荐者增加的额度
		'buy_via_offline_increase_count_percentage_for_author',  # 线下会员购买为推荐者额外增加的额度
		'use_ceiling',  # 订单积分抵扣上限
		'review_increase'   # 商品好评送积分
	])
	def post(args):
		corp = args['corp']
		integral_strategy = corp.mall_config_repository.get_integral_strategy()
		integral_strategy.update(args)

		return {}