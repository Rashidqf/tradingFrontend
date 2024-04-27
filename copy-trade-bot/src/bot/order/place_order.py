from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import requests
from src.bot import xpaths
import threading

direction_value = None

def switch_multiple_window(driver,*args):
    
    process = threading.Thread(target=trade_order,args=(driver,*args))
    process.start()
    process.join()

    
    

def trade_order(
            driver,
            market_name:str,action_type:str,
            action_method:str,amount:int,
            hedging:bool,order_level:int,
            stop_limit:bool,stop_or_trailing:str,
            points_away:int, at_price:int,
            guarantee:bool,limit:bool,
            lAt_price:int,lPoints_away:int,
            status_url:str,id:str
            ) -> bool:
       
        global direction_value 
        """ This function create the order on trade365.

        Args:
            market_name(str): name of the marketplace.
            action_type(str): order type(Trade/Order)
            action_method(str): order method(Buy/Sell)
            amount(int):  amount of the order.
            hedging(bool):  if hedging for the order
            order_level(str):  order level for Order
            stop_limit(str): stop limit for the order
            stop_or_trailing (str):  stop or trailing for the order.
            points_away(str): stop points away for the order
            at_price(str):  stop at price for the order
            guarantee(bool):  if guarantee for the order
            limit(bool):  if limit for the order
            lPoints_away(str): limit points away for the order
            lAt_price (str): limit at price for the order
            id(str): order id

        Returns:
            The return value. True and send the status for Active, False otherwise.

        """
        
        # tradeId = 121212
        # print("Stop/Limit", stop_limit)
        # print("Ammount", amount)
        print("Received parameters:")
        print("driver:", driver)
        print("market_name:", market_name)
        print("action_type:", action_type)
        print("action_method:", action_method)
        print("amount:", amount)
        print("hedging:", hedging)
        print("order_level:", order_level)
        print("stop_limit:", stop_limit)
        print("stop_or_trailing:", stop_or_trailing)
        print("points_away:", points_away)
        print("at_price:", at_price)
        print("guarantee:", guarantee)
        print("limit:", limit)
        print("lAt_price:", lAt_price)
        print("lPoints_away:", lPoints_away)
        print("status_url:", status_url)
        print("id:", id)
        order_xpaths = xpaths.place_order
        print("trade is working")
        print(amount)
        # driver.refresh()
        driver.find_element(By.TAG_NAME,"body").send_keys(Keys.CONTROL + Keys.HOME)
        sleep(.2)
        # print(order_xpaths['market_element'].format(market_name,action_type.capitalize()))
        #placing order
        try:
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, order_xpaths['market_element'].format(market_name,action_type)))).click()
        except Exception as e:
            #print(e)
            print("2")
            requests.post(status_url, verify=False,data={"id":id,"tradeId" : direction_value,"status":"Desyncronised","message":"Ordrer Desyncronised"})
            return False

        #token amount
        try:
            # print(action_method)
            # print(amount)
            # print(order_xpaths["action_button"].format(action_method))
            elem = WebDriverWait(driver,5).until(
                         EC.element_to_be_clickable((By.XPATH,order_xpaths["amount_input"])))
            elem.clear()
            elem.send_keys(amount)
            WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, order_xpaths["action_button"].format(action_method)))).click()

        except Exception as e:
            print("Element not found")

            requests.post(status_url,verify=False,data={"id":id,"tradeId" : direction_value,"status":"Desyncronised","message":"Ordrer Desyncronised"})
            return False



        if stop_limit:
            try:
                driver.find_element(By.XPATH,order_xpaths["stop_limit_dropdown"]).click()
            except:
                #print("Unable to click stoplimit dropdown!")
                pass

            if stop_or_trailing == "stop":
                driver.find_element(By.CSS_SELECTOR,order_xpaths["stop_checkbox"]).click() 
            try:
                if points_away is not None:
                    print("points away value recieve")
                    element = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH,order_xpaths["points_away_input"])))
                    action = ActionChains(driver)
                    action.click(on_element = element)
                    action.send_keys(points_away)
                    action.perform()
                    
                if at_price is not None:
                    print("at price value recieve")
                    element2 = WebDriverWait(driver, 2).until(
                                        EC.element_to_be_clickable((By.XPATH,order_xpaths["at_price_input"])))
                    element2.send_keys(Keys.ENTER)
                    element2.clear()
                    element2.send_keys(at_price)
            except Exception as e:
                pass
                #print(e)
                #print("Error! element not found .")

        #submission for token
        try:
            # print("Submit here")
            driver.find_element(By.XPATH,xpaths.common["submit_button"]).click()
            sleep(.25)
        except Exception as e:
            pass
            #print("Error!")
        try:
            direction_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='spnReferenceNo']")))
            direction_value = direction_element.text
            sleep(0.25)
            print("Trade ID:", direction_value)
        except Exception as e:
            print("Error waiting for page to load after submission:")
            return False
        
        try:
            if action_type =="order":
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpaths.common["back_button"])))
            else:
                # print("here")
                sleep(.5)
                WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, xpaths.common["print_button"])))
            print("close")
            driver.find_element(By.XPATH, xpaths.common["close_button"]).click()
        
        except Exception as e:
            sleep(.2)
            print("close2")
            driver.find_element(By.XPATH, xpaths.common["close_button"]).click()
            requests.post(status_url,verify=False,data = {"id":id,"tradeId" : direction_value, "status":"Desyncronised","message":"Ordrer Desyncronised"})
            return False
        
        creation_time = get_creation_time(driver,market_name,action_type)

        # print(creation_time)
        # print({"market_name":market_name,"id":id,tradeId : tradeId,"creation time": creation_time})
        
        try:
            try:
                sleep(.25)
                open_price = WebDriverWait(driver, 2.5).until(EC.element_to_be_clickable((By.XPATH,order_xpaths["opening_price2"].format(market_name)))).text
            except:
                open_price = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,order_xpaths["opening_price1"].format(market_name)))).text
            print(open_price)
            print("Completed.")
        except Exception as e:
            print("Something went wrong with OpenPrice")
            open_price = None
        # print(tradeId)
        requests.post(status_url,verify=False,data={"id":id,"tradeId" : direction_value,"status":"Active","orderCreated":creation_time,"openPrice":open_price,"message":"Order Placed"})




def get_creation_time(driver,market_name:str,action:str) -> str:

    driver.find_element(By.TAG_NAME,"body").send_keys(
        Keys.CONTROL + Keys.END)


    if action == "order":
        try:
            driver.find_element(By.XPATH, xpaths.common["opened_order"].format(market_name)).click()
            sleep(.25)
            creation_time = driver.find_element(By.XPATH, xpaths.place_order["order_time"]).text
            return creation_time
        except Exception as err:
            pass
    
    try:
        try:
            driver.find_element(By.XPATH, xpaths.common["creation_time2"].format(market_name))
        except:
            sleep(.2)
            # print(xpaths.common["expand_market"].format(market_name))
            driver.find_element(By.XPATH, xpaths.common["expand_market"].format(market_name)).click()
        # print(xpaths.common["creation_time"].format(market_name))
        creation_time = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,xpaths.common["creation_time"].format(market_name)))).text
    except:
        sleep(.2)
        try:
            # print(xpaths.common["creation_time2"].format(market_name))
            creation_time = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,xpaths.common["creation_time2"].format(market_name)))).text
        except:
            creation_time = None

    return creation_time