# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.integral_strategy import IntegralStrategy

class AIntegralStrategy(api_resource.ApiResource):
	"""
	积分规则
	"""
	app = 'mall'
	resource = 'integral_strategy'

	@param_required(['owner_id'])
	def get(args):
		integral_strategy, has_a_integral_strategy, show_guide = IntegralStrategy.from_owner_id({'owner_id': args['owner_id']})
		if integral_strategy:
			return {
				'integral_strategy': integral_strategy.to_dict(),
				'has_a_integral_strategy': has_a_integral_strategy,
				'show_guide': show_guide
			}
		else:
			msg = u'owner_id {} not exist'.format(args['owner_id'])
			return 500, {'msg': msg}

	@param_required([
		'owner_id',
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
		integral_strategy = IntegralStrategy.from_owner_id({'owner_id': args['owner_id']})
		if integral_strategy:
			integral_strategy.update({
				'integral_each_yuan': args['integral_each_yuan'],
				'be_member_increase_count': args['be_member_increase_count'],
				'click_shared_url_increase_count': args['click_shared_url_increase_count'],
				'buy_award_count_for_buyer': args['buy_award_count_for_buyer'],
				'order_money_percentage_for_each_buy': args['order_money_percentage_for_each_buy'],
				'buy_via_shared_url_increase_count_for_author': args['buy_via_shared_url_increase_count_for_author'],
				'buy_via_offline_increase_count_for_author': args['buy_via_offline_increase_count_for_author'],
				'buy_via_offline_increase_count_percentage_for_author': args['buy_via_offline_increase_count_percentage_for_author'],
				'use_ceiling': args['use_ceiling'],
				'review_increase': args['review_increase'],
			})
			return {}
		else:
			msg = u'owner_id {} not exist'.format(args['owner_id'])
			return 500, {'msg': msg}