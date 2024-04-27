import threading
from src.bot.main import TradeDirect
from src.helper.helper import get_fields,get_the_instance
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
status_url  = os.getenv("ORDER_STATUS_URL")
trade_url  = os.getenv("TRADE_STATUS_URL")


def place_order(instances:list , data:dict) -> None:

    if type(data.get("order")) is list :
        for order in data.get("order"):
            
            result=get_fields(order)
            # print("Order:>><<<",order)
            print("Result:", result)
            tradeId = order.get("tradeId")
            print("tradeid", tradeId)
            # print("resuklt",get_fields(order))
            op = order.get("openPrice")
            exit_type = order.get("exit")
            # print(result[-3])
            bot = get_the_instance(instances,"email",result[-3])
            # print(result[0])
            if result[0]:
                print("Placing New Order")
                p = threading.Thread(target = bot.order, args=(
                                                            result[1],result[2],result[3],
                                                            result[4],result[5],result[6],
                                                            result[7],result[8],result[9],
                                                            result[10],result[11],result[12],
                                                            result[13],result[14],status_url,
                                                            result[18]
                                                        ))
                
                p.start()
            
            if exit_type == "Partial Exit":
                print("Partial Exit")
                TradeId = order.get("tradeId")
                print(TradeId)
                p = threading.Thread(target = bot.cancel, args=(
                                                                result[2],result[1],
                                                                exit_type,result[4],
                                                                status_url,result[18],
                                                                result[19],op,TradeId
                                                                    ))
                p.start()

            elif result[16]:
                print("Ammending order")
                TradeId = order.get("tradeId")
                print(TradeId)
                p = threading.Thread(target = bot.ammend, args=(
                                                        result[1],result[9],
                                                        result[10],result[2],
                                                        status_url,
                                                        result[18],result[19],op,TradeId
                                                        ))
                p.start()

            elif exit_type == "Exit":
                print(order)
                print("Exiting")
                print(result[19])
                TradeId = order.get("tradeId")
                print(TradeId)
                p = threading.Thread(target = bot.cancel, args=(
                                                        result[2],result[1],
                                                        exit_type,result[4],
                                                        status_url,result[18],
                                                        result[19],op,TradeId
                                                        ))
            
                p.start()
                

def place_Trade(instances:list , data:dict) -> None:

    if type(data.get("order")) is list :
        for order in data.get("order"):
            if 'amount' not in order:
                print("Error: 'amount' key is missing in the order data.")
                continue
            # print("Trade:>><<<",order)
            result=get_fields(order)
            op = order.get("openPrice")
            tradeId = order.get("tradeId")
            print("open Price", op)
            print("tradeId", tradeId)
            exit_type = order.get("exit")
            myammount = order.get("amount")
            print("amount",result)
            bot = get_the_instance(instances,"email",result[-3])
            if result[0]:
                print("Placing New Order")
                p = threading.Thread(target = bot.trade, args=(
                                                            result[1],myammount,result[2],result[3],
                                                            result[4],result[5],result[6],
                                                            result[7],result[8],result[9],
                                                            result[10],result[11],result[12],
                                                            result[13],result[14],trade_url,
                                                            result[18]
                                                        ))
                
                p.start()
            
            if exit_type == "Partial Exit":
                print("Partial Exit")
                p = threading.Thread(target = bot.cancel, args=(
                                                                result[2],result[1],
                                                                exit_type,result[4],
                                                                trade_url,result[18],
                                                                result[19],op
                                                                    ))
                p.start()

            elif result[16]:
                print("Ammending trade")
                # print("Trade:>><<<",order)
                created_at = order.get("createdAt")
                TradeId = order.get("tradeId")
                print(TradeId)
                created_at_datetime = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_created_at = created_at_datetime.strftime("%d/%m/%y %H:%M:%S")
                print("Created At:", formatted_created_at)
                p = threading.Thread(target = bot.tradeammend, args=(
                                                        result[1],result[9],
                                                        result[10],result[2],
                                                        trade_url,
                                                        result[18],formatted_created_at,result[19],op,TradeId
                                                        ))
                p.start()

            elif exit_type == "Exit":
                print("Trade:>><<<",order)
                print("Exiting")
                TradeId = order.get("tradeId")
                print(TradeId)
                p = threading.Thread(target = bot.ordercancel, args=(
                                                        result[2],result[1],
                                                        exit_type,result[4],
                                                        trade_url,result[18],
                                                        result[19],op,TradeId  
                                                        ))
            
                p.start()
       

def set_accounts(instances:list,data:dict) -> None:
    # print(data)
    if type(data) is not list:
        objs =  data.get("accounts")
        acc_type =  data.get("type")
    if acc_type == "New Account":
        for instance in instances:
            bot = instance.get("inst")
            print("Closing old threads.")
            bot.close()

    instances.clear()
    data = objs

    for acc_obj in data:
        email = acc_obj.get("email")
        password = acc_obj.get("password")
        account_id = acc_obj.get("accountId")
        id = acc_obj.get("id")
        print(id,email)
        print("Thread starting . . . ")
        bot = TradeDirect()
        process = threading.Thread(target=bot.launch_account, args=(account_id,email,password,))
        process.start()

        inst_obj = {
                    "id":id,
                    "inst":bot,
                    "email":email
                    }
        
        instances.append(inst_obj)
