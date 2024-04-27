import asyncio
from fastapi import FastAPI, Request
from urllib3 import PoolManager
from fastapi.middleware.cors import CORSMiddleware
from src.trigger.bot import place_order, set_accounts, place_Trade

# initiate the server
app = FastAPI()
http = PoolManager(num_pools=10)  # Adjust the pool size as needed

origins = [
    "http://localhost:3000",
    "http://localhost:9998/api"
]

# ignore cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=['Accept', 'Accept-Language', 'Content-Language', 'Content-Type'],
)

all_instance = []

# Define a queue to store incoming order requests
order_queue = asyncio.Queue()

# Define a queue to store incoming trade requests
trade_queue = asyncio.Queue()


# Function to process orders with a delay of 2 seconds
async def process_order():
    while True:
        if not order_queue.empty():
            obj = await order_queue.get()
            place_order(all_instance, obj)
            await asyncio.sleep(3)  # Delay of 2 seconds before processing the next request
        else:
            await asyncio.sleep(1)  # If the queue is empty, wait for 1 second before checking again


# Function to process trades with a delay of 2 seconds
async def process_trade():
    while True:
        if not trade_queue.empty():
            obj = await trade_queue.get()
            place_Trade(all_instance, obj)
            await asyncio.sleep(3)  # Delay of 2 seconds before processing the next request
        else:
            await asyncio.sleep(1)  # If the queue is empty, wait for 1 second before checking again


@app.post("/api/order")
async def create_order(request: Request):
    """
    Get order from user and trigger the bot.

    Args:
        request: Request body from the user.

    Return:
        send response order received.

    """
    obj = await request.json()
    print(obj)
    await order_queue.put(obj)  # Put the received order into the queue
    return {"status": "Order Received"}


@app.post("/api/trade")
async def create_trade(request: Request):
    """
    Get trade data from user and trigger the bot.

    Args:
        request: Request body from the user.

    Return:
        send response trade received.

    """
    obj = await request.json()
    print("trade data", obj)
    await trade_queue.put(obj)  # Put the received trade into the queue
    return {"status": "Trade Received"}


@app.post("/api/accounts")
async def accounts(req: Request):
    """
    Get all accounts and create bot instance.

    Args:
        request: Request body from the user.

    Return:
        send response accounts received.

    """
    acc_objs = await req.json()
    set_accounts(all_instance, acc_objs)

    return {"message": "accounts received"}


@app.post("/api/log")
async def log_data(request: Request):
    """
    Log data to the console.

    Args:
        request: Request body containing the data to log.

    Return:
        send response confirming data logged.

    """
    data = await request.json()
    logger.info("Received data: %s", data)

    return {"status": "Data Logged"}

# Start the order and trade processing loops
asyncio.create_task(process_order())
asyncio.create_task(process_trade())
