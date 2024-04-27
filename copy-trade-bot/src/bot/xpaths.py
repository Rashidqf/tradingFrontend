
login = {
		"login_username": "//input[@id='login_userid']",
		"login_password": "//input[@id='login_password']",
		"login_button": "//button[normalize-space()='Log in']",
		"launch_button": "//div[contains(text(),'{}')]/ancestor::div[@class='MuiDataGrid-row']//button[contains(@type,'button')][normalize-space()='Launch']",
		"launch_button2": "//div[contains(text(),'{}')]/ancestor::div[contains(@class,'MuiDataGrid-row MuiDataGrid-row--lastVisible')]//button[contains(@type,'button')][normalize-space()='Launch']"
          
	}
          


place_order = {
		"market_element": "//div[contains(text(),'{}')]//ancestor::tr[1]//span[contains(text(),'{}')]",
		"action_button": "//div[@class='{}-button']",
		"amount_input": "//input[@class='txtStake']",
		"hedging_checkbox": "//label[@class='check-box lblcbHedging']",
		"order_level_input": "//input[@class='txtLevel']",
		"stop_limit_dropdown": "//label[contains(text(),'Stop / Limit ')]",
		"stop_checkbox": ".check-box.lblcbStop",
		"trailing": "//a[normalize-space()='Trailing']",
		"points_away_input": "//input[@class='txtStopPoint selected isClicked']",
		"at_price_input": "//input[@class='txtStopPrice']",
		"guarantee_checkbox": "//input[@class='cbGuarantee']",
        "limit_checkbox": "//label[@class='check-box lblcbLimit']",
		"limit_points_away_input": "//input[@class='txtLimitPoint selected isClicked']",
		"limit_at_price_input": "//input[@class='txtLimitPrice']",
        "order_time": "(//td[@headers='yui-dt2-th-Period ']/div)[last()]",
		"opening_price1": "//div[contains(text(),'{}')]/preceding-sibling::div/parent::div/parent::div/parent::td/following-sibling::td[@headers='yui-dt2-th-OpeningPrice ']",
        "opening_price2": "//div[contains(text(),'{}')]/preceding-sibling::div/parent::div/parent::td/parent::tr/following-sibling::tr[1]//td[@headers='yui-dt2-th-OpeningPrice ']/div"
	}

place_trade = {
		"market_element": "//div[contains(text(),'{}')]//ancestor::tr[1]//span[contains(text(),'{}')]",
		"action_button": "/html/body/form/div[3]/div/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/div/div/div/div/div[3]/table/tbody[2]/tr[2]/td[10]/div/div/span/span[2]",
		"actionButtonNew" : '//div[@class="{}-button"]',
		"amount_input": "//input[@class='txtStake']",
		"hedging_checkbox": "//label[@class='check-box lblcbHedging']",
		"order_level_input": "//input[@class='txtLevel']",
		"stop_limit_dropdown": "//label[contains(text(),'Stop / Limit ')]",
		"stop_checkbox": ".check-box.lblcbStop",
		"trailing": "//a[normalize-space()='Trailing']",
		"points_away_input": "//input[@class='txtStopPoint selected isClicked']",
		"at_price_input": "//input[@class='txtStopPrice']",
		"guarantee_checkbox": "//input[@class='cbGuarantee']",
        "limit_checkbox": "//label[@class='check-box lblcbLimit']",
		"limit_points_away_input": "//input[@class='txtLimitPoint selected isClicked']",
		"limit_at_price_input": "//input[@class='txtLimitPrice']",
        "order_time": "(//td[@headers='yui-dt2-th-Period ']/div)[last()]",
		"opening_price1": "//div[contains(text(),'{}')]/preceding-sibling::div/parent::div/parent::div/parent::td/following-sibling::td[@headers='yui-dt2-th-OpeningPrice ']",
        "opening_price2": "//div[contains(text(),'{}')]/preceding-sibling::div/parent::div/parent::td/parent::tr/following-sibling::tr[1]//td[@headers='yui-dt2-th-OpeningPrice ']/div",
  "submit_button": "/html/body/div[2]/div/div[2]/div[2]/div/div[9]/button",
  "buy-sale": ""
	}



ammend = {
		"click_market_name": "//div[@id='divCurrentPositions']//div[contains(text(),'{}')]//ancestor::tr[1]/td[9]",
		"edit_trade": "//div[contains(text(),'{}')]/parent::td/preceding-sibling::td[@headers='yui-dt2-th-EditOrder ']",
		"edit_button" : "//div[@id='cp-edit-{}-undefined']/div[@class='editIcon']",
		"ammend_order": "//div[contains(text(),'{}')]/parent::td/following-sibling::td//span[contains(text(),'Amend')]",
		"stop_price_input_selected": "//input[@class='txtStopPrice selected']",
		"stop_price_input_not_selected": "//input[@class='txtStopPrice']",
		"stop_checkbox": ".check-box.lblcbStop",
		"stopchecbox" : "//label[@class='check-box lblcbStop']",
  		"stop_limit": ".showStopLimitMore",
		'order_checkBox': '//*[@id="yui-rec105"]/td[11]/div/div',
		"stop_point_input_selected": "//input[@class='txtStopPoint selected isClicked']",
		"points_away_input": "//input[@class='txtStopPoint isClicked selected']",
		"points_away_input_selected": "//input[@class='txtStopPoint']",
		"ammend_at_price_input": "//input[@class='txtStopPrice selected']",
	}



cancel_order = {
		"exit_path": '(//div[@id="divCurrentPositions"]//div[contains(text(),"{}")]//ancestor::tr[1]//div[@class="closeIcon"])[1]',
		"cancel_button": '//div[contains(text(),"{}")]/parent::td/following-sibling::td//div[@class="closeIcon"]',
		"cancel_button2": '(//div[contains(text(),"{}")])[2]//ancestor::td[@headers="yui-dt1-th-MarketName "]/following-sibling::td[@headers="yui-dt1-th-CloseOrder "]//div[@class="closeIcon"]',
		"amount_input": '//input[@class="txtStake"]',
		"print_button": '//button[@class="btnPrint"]',
		"last_remove": '//div[contains(text(),"{}")]/parent::td/following-sibling::td//span[contains(text(),"REMOVE")]',
		"confirm": '//button/span[text()="CONFIRM"]',
		"remove_Button" : "//div[@id='oo-currentPrice-{}']/ancestor::tr[1]//span[contains(@class, 'button') and contains(., 'REMOVE')]",
		"ammend_Butoon" : "//div[@id='oo-currentPrice-{}']/ancestor::tr[1]//span[contains(@class, 'button') and contains(., 'Amend')]",
		"trade_close" : "//div[@id='cp-close-{}-undefined']"
	}



common = {
		"submit_button": "//button[@class='btnSubmit']//span",
        "print_button": '//button[@class="btnPrint"]/span',
		"back_button": "//button[@class='btnBack']//span",
        "expand_market": '//div[contains(text(),"{}")]/preceding-sibling::div',
		"creation_time":"//div[contains(text(),'{}')]/preceding-sibling::div/parent::div/parent::td/parent::tr/following-sibling::tr[1]//td[@headers='yui-dt2-th-CreationTime ']/div",
		"creation_time2":"//div[contains(text(),'{}')]/preceding-sibling::div/parent::div/parent::div/parent::td/following-sibling::td[@headers='yui-dt2-th-CreationTime ']",
		"close_button": "(//span[@class='close'])[1]",
		"opened_order": '//div[contains(text(),"Opening Orders")]',
		"open_Trade" : '//div[contains(text(),"Open Position")]',
  		"open_Trade" : "/html/body/form/div[3]/div/table[2]/tbody/tr[2]/td[2]/div[1]/div/div/ul/li[2]/a/div",
		"trade_id" : "//span[@class='spnReferenceNo']"
	}