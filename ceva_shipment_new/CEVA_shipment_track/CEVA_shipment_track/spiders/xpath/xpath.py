import os
import sys

viewstate_xpath='//input[contains(@id,"__VIEWSTATE")]/@value'
viewstategenerator_xpath='//input[contains(@id,"__VIEWSTATEGENERATOR")]/@value'


waybill_number_xpath='//td[contains(text(),"Waybill Number:")]/following-sibling::td/text()'
ship_date_xpath='//td[contains(text(),"Ship Date:")]/following-sibling::td/text()'
due_date_xpath='//td[contains(text(),"Due Date:")]/following-sibling::td/text()'
estimated_delivery_date_xpath='//td[contains(text(),"Estimated Delivery Date:")]/following-sibling::td/text()'
shipper_location_xpath='//td[contains(text(),"Shipper Location")]/following-sibling::td/text()'
consignee_location_xpath='//td[contains(text(),"Consignee Location")]/following-sibling::td/text()'
totalpcs_xpath='//td[contains(text(),"Total Pieces:")]/following-sibling::td/text()'
actual_weight_xpath='//td[contains(text(),"Actual Weight:")]/following-sibling::td/text()'
charge_weight_xpath='//td[contains(text(),"Charge Weight:")]/following-sibling::td/text()'
freight_terms_xpath='//td[contains(text(),"Freight Terms:")]/following-sibling::td/text()'
service_level_xpath='//td[contains(text(),"Service Level:")]/following-sibling::td/text()'
delivery_type_xpath='//td[contains(text(),"Delivery Type:")]/following-sibling::td/text()'
movement_type_xpath='//td[contains(text(),"Movement Type:")]/following-sibling::td/text()'

history_data_column_xpath='//table[tr[td[contains(text(),"Key Event History")]]]/following-sibling::table[2][@border="0"]/tr/td[1]/text()'
#history_data_column_xpath='//table[tr[td[contains(text(),"Key Event History")]]]/following-sibling::table[2]//tr//td'
signature_remarks="//td[text()='%s']/following-sibling::td/a/text()"

history_data="//td[text()='%s']/following-sibling::td/text()"