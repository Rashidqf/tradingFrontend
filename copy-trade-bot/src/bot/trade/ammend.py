from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
import requests
from src.bot import xpaths

TradeValue = None

def order_ammend(
        driver, market_name: str,
        ammend_point_away: int,
        ammend_at_price: int,
        action_type: str, status_url: str,
        id: str, order_created, formatted_created_at, open_price: str,TradeId : str) -> bool:
    
    global TradeIdValue 
    # Assign the value to the global variable
    TradeIdValue = TradeId
    
    print("TradeId", TradeIdValue)
    print("formatted_created_at", formatted_created_at)
    print("Market Name:", market_name)
    print("Amend Point Away:", ammend_point_away)
    print("Amend At Price:", ammend_at_price)
    print("Action Type:", action_type)
    print("Status URL:", status_url)
    print("ID:", id)
    print("order_created:", order_created)
    print("Order Created:", order_created)
    print("Open Price:", open_price)

    ammend_xpaths = xpaths.ammend

    # Scroll to the end of the page
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + Keys.END)

    try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, xpaths.common["opened_order"]))).click()
            print("Clicked on the opened order.")
    except NoSuchElementException:
            print("Element not found. Check if the XPath expression is correct.")
    except ElementClickInterceptedException:
            print("Element is not clickable. Check if it's overlapped by another element or disabled.")
    except TimeoutException:
            print("Timeout: Element was not clickable within the specified time.")
    print(TradeIdValue)
    try:
            # Wait for the element to be clickable
        cancel_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, xpaths.cancel_order["ammend_Butoon"].format(TradeIdValue)))
            )
            
            # Click on the button
        cancel_button.click()
        print("Clicked on the ammend Butoon.")
    except NoSuchElementException  as e:
            print("Element not found. Check if the XPath expression is correct.",e)
    except ElementClickInterceptedException  as e:
            print("Element is not clickable. Check if it's overlapped by another element or disabled.",e)
    except TimeoutException as e:
            print("Timeout: Element was not clickable within the specified time.",e)
        
        
            
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//label[@class="showStopLimitMore enabledStopLimit"]'))).click()
        print("Clicked on the stop loss order.")
    except Exception as e:
        print("not working on the stop loss order.")
        
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='checkbox']//label[@class='check-box lblcbStop']/span"))).click()
        print("Clicked on the tick")
    except Exception as e:
        print("not working on the tick")

    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'clickStopPrice')]//input[@type='number']"))
        )
        # ammend_elem = driver.find_element(By.XPATH,"//div[contains(@class, 'clickStopPrice')]//input[@type='number' and @disabled]")
        
        # ammend_elem.send_keys(Keys.ENTER)
        # ammend_elem.clear()
        # ammend_elem.send_keys(ammend_at_price)

        # Check if the input field is enabled
        if not input_field.is_enabled():
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='checkbox']//label[@class='check-box lblcbStop']/span"))).click()
                input_field.clear()
                input_field.send_keys(ammend_at_price)
                print("Amount entered on the input")
                print("Clicked on the tick")
            except Exception as e:
                print("not working on the tick")
                print("Input field is disabled. Data cannot be entered directly.")
        else:
            input_field.clear()
            input_field.send_keys(ammend_at_price)
            print("Amount entered on the input")
    except TimeoutException:
        print("Timeout: Unable to locate the input field within the specified time.")
    except NoSuchElementException:
        print("Element not found. Check if the XPath expression is correct or if the element exists on the page.")
    except Exception as e:
            print("error  on the input value",e)

    # else:
    #     WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, ammend_xpaths["edit_trade"].format(order_created)))).click()
    #     print("Clicked on the edit trade button.")
    #     sleep(.2)
    

    # try:
    #     try:
    #         WebDriverWait(driver, 10).until(
    #             EC.element_to_be_clickable((By.XPATH, ammend_xpaths["stop_price_input_selected"])))
    #         already_selected = True
    #     except TimeoutException:
    #         driver.find_element(By.CSS_SELECTOR, ammend_xpaths["stop_checkbox"]).click()
    #         already_selected = False

    #     if ammend_point_away:
    #         if already_selected:
    #             input_path = ammend_xpaths["points_away_input_selected"]
    #         else:
    #             input_path = ammend_xpaths["stop_point_input_selected"]
    #         input_elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, input_path)))
    #         input_elem.click()
    #         print("Clicked on the input element.")
    #         sleep(.1)
    #         if not already_selected:
    #             input_elem.send_keys(ammend_point_away)
    #         else:
    #             send_amount_elem = WebDriverWait(driver, 10).until(
    #                 EC.element_to_be_clickable((By.XPATH, ammend_xpaths["points_away_input"])))
    #             send_amount_elem.clear()
    #             send_amount_elem.send_keys(ammend_point_away)

    #     elif ammend_at_price:
    #         if not already_selected:
    #             at_price_path = ammend_xpaths["stop_price_input_not_selected"]
    #         else:
    #             at_price_path = ammend_xpaths["ammend_at_price_input"]

    #         ammend_elem = driver.find_element(By.XPATH, at_price_path)
    #         ammend_elem.send_keys(Keys.ENTER)
    #         print("Clicked on the amend element.")
    #         ammend_elem.clear()
    #         ammend_elem.send_keys(ammend_at_price)

    # except TimeoutException:
    #     print("Timeout: Failed to enter amend details.")
    #     print("Current URL:", driver.current_url)
    #     return False

    try:
        # Click on the submit button
        submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpaths.common["submit_button"]))
        )
        submit_button.click()
        print("Clicked on the submit button.")
        sleep(.2)

        # Wait for the appropriate button based on the action type
        if action_type == "trade":
            back_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths.common["back_button"]))
            )
            print("Clicked on the back button.")
        else:
            print("Clicked on the print button.")
            print_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths.common["print_button"])))

        # Post request
        print(TradeIdValue)
        requests.post(status_url, verify=False, data={"id": id, "status": "Active", "orderCreated": order_created,"openPrice": open_price, "message": "Order Amend","tradeId": TradeIdValue})

    except TimeoutException:
        print("Timeout: Failed to click on the submit button or wait for subsequent elements.")
    except NoSuchElementException:
        print("Element not found. Check if the XPath expression is correct or if the element exists on the page.")
    except ElementNotInteractableException:
        print("Element is not interactable. It might be overlapped by another element or disabled.")
    except Exception as e:
        print("An unexpected error occurred:", e)


    try:
        driver.find_element(By.XPATH, xpaths.common["close_button"]).click()
        print("Clicked on the close button.")
    except:
        pass

    print("Success")
    return True
