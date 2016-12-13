# -*- coding: utf-8 -*-
from business.mall.template_message.template_message_detail import TemplateMessageDetail
from business.mall.template_message.template_message import TemplateMessage
from db.mall import models as mall_models

from business import model as business_model


class TemplateMessageDetailRepository(business_model.Service):
	def get_template_message(self, corp_id, send_point):

		template_message_detail = mall_models.MarketToolsTemplateMessageDetail.select().join(
				mall_models.MarketToolsTemplateMessage).where(
				mall_models.MarketToolsTemplateMessageDetail.owner == corp_id,
				mall_models.MarketToolsTemplateMessage.send_point == send_point,
				mall_models.MarketToolsTemplateMessageDetail.status == mall_models.MESSAGE_STATUS_ON).first()
		template_message = mall_models.MarketToolsTemplateMessage.select().join(
				mall_models.MarketToolsTemplateMessageDetail).where(
				mall_models.MarketToolsTemplateMessageDetail.owner == corp_id,
				mall_models.MarketToolsTemplateMessage.send_point == send_point,
				mall_models.MarketToolsTemplateMessageDetail.status == mall_models.MESSAGE_STATUS_ON).first()

		return TemplateMessageDetail(template_message_detail),TemplateMessage(template_message)