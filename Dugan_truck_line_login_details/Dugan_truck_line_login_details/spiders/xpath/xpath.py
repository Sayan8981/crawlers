
import os
import sys

viewstate_xpath='//input[contains(@name,"__VIEWSTATE")]/@value'
eventvalidation_xpath='//input[contains(@name,"__EVENTVALIDATION")]/@value'

pro_number_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblProNumber"]//text()'
status_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_Label1"]/following-sibling::table//td//text()'
trip_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_Label1"]/following-sibling::table//td//text()'
bill_of_lading_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblBillOfLading"]/font/text()'
pickedup_date_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblPickupDate"]/font/text()'
delivery_date='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblDeliveryDate"]/font/text()'
eta_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblScheduledDate"]/font/text()'

shipper_name_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblShipperName"]/font/text()'
shipper_addr_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblShipperAddress1"]/font/text()'
shipper_city_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblShipperCity"]/font/text()'
shipper_state_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblShipperState"]/font/text()'
shipper_zip_xpath='//span[@id="ctl00_ContentPlaceHolder1_FormView1_lblShipperZip"]/font/text()'

consignee_name_xpath='//span[contains(@id,"lblConsigneeName")]//text()'
consignee_addr_xpath='//span[contains(@id,"lblConsigneeAddress")]//text()'
consignee_state_xpath='//span[contains(@id,"lblConsigneeState")]//text()'
consignee_city_xpath='//span[contains(@id,"lblConsigneeCity")]//text()'
consignee_zip_xpath='//span[contains(@id,"lblConsigneeZip")]//text()'