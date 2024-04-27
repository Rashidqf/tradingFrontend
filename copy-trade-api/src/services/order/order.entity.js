import axios from "axios";
import { ObjectId } from "mongodb";
import Account from "../account/acount.schema";
import { genLog, getAmmount } from "./order.helper";
import Order from "./order.schema"; // this is TradeSchema Named as Order

const createAllowed = new Set([
  "childrens",
  "percentage",
  "ammount",
  "side",
  "marketData",
  "pointsAway",
  "atPrice",
  "stopLimit",
  "account",
  "status",
  "partialExit",
  "exitFrom",
  "ammend",
  "openPrice",
  "orderCreated",
  "logs",
  "orderType",
  "exit",
  "placeOrder",
  "tradeId",
]);

const populate = { path: "account", select: "email password  accountId" };

const allowedQuery = new Set([
  "page",
  "orderType",
  "childrens",
  "paginate",
  "history",
]);

export const createOrder =
  ({ db, ws }) =>
  async (req, res) => {
    try {
      console.log("Request Body:", req.body);

      const isValid = Object.keys(req.body).every((key) =>
        createAllowed.has(key)
      );
      console.log("Validation Result:", isValid);
      if (!isValid) {
        return res.status(400).send({ message: "Bad Request" });
      }
      

      const accounts = await db.find({
        table: Account,
        key: { paginate: req.query.paginate === "false" },
      });
      console.log("Accounts:", accounts);
      if (!accounts)
        return res.status(400).send({ message: "No accounts found for trade" });

      const { marketData, percentage, exitFrom } = req.body;

      let orders = [];
      await Promise.all(
        accounts.map(async (account) => {
          // const ammount = exitFrom ? await calcAmmount(number, percentage) : await getAmmount({ marketData, account, percentage });
          const ammount = await getAmmount({ marketData, account, percentage });

          if (exitFrom) {
            delete req.body.logs;
            req.body.ammend = undefined;
            const parent = await Order.findOne({
              childrens: { $in: [ObjectId(exitFrom)] },
            }).populate({ path: "childrens" });
            const exited = await Promise.all(
              parent.childrens.map(async (children) => {
                const newPer =
                  Number(children.percentage) - Number(req.body.percentage);
                const single = await db.update({
                  table: Order,
                  key: {
                    _id: children._id,
                    body: { partialExit: true, percentage: newPer, ammount },
                  },
                });
                req.body.orderCreated = single.orderCreated;
                return single;
              })
            );
            parent.childrens = exited;
            await ws.emit("partialExit", parent);
          }

          if (ammount !== 0) {
            const log = await genLog("Pending", "Order Created");
            const order = await db.create({
              table: Order,
              key: {
                ...req.body,
                ammount,
                logs: [log],
                account: account._id,
                populate,
              },
            });
            orders.push(order);
          }
        })
      );

      if (!orders.length > 0)
        return res.status(400).send({ message: "Bad Request" });

      const ids = orders.map((order) => order._id);
      const data = { orderType: "parent", childrens: ids };
      const parentOrder = await db.create({
        table: Order,
        key: { ...data, populate: { path: "childrens" } },
      });

      res.status(201).send(parentOrder);

      try {
        const payLoad = { accounts: accounts, order: orders };
        console.log("payload", payLoad);
        const response = await axios(`${process.env.BOT_SERVER_URL}/order`, {
          method: "POST",
          data: payLoad,
        });
        await ws.emit("account", response.data);
      } catch (err) {
        console.log(err);
      }
    } catch (err) {
      console.log(err);
      return res
        .status(500)
        .send({ message: err.message || "Internal Server Error" });
    }
  };

export const getAll =
  ({ db }) =>
  async (req, res) => {
    try {
      let orders = await db.find({
        table: Order,
        key: {
          query: { ...req.query },
          allowedQuery,
          paginate: req.query.paginate === "false",
          populate: { path: "account childrens" },
        },
      });
      if (!orders) return res.status(404).send({ message: "Orders not found" });
      if (req.query.orderType === "parent")
        orders = orders.filter(
          (order) =>
            !order.childrens.some((c) => c.status === "Closed" || c.exitFrom)
        );
      return res.status(200).send(orders);
    } catch (err) {
      console.log(err);
      return res
        .status(500)
        .send({ message: err.message || "Internal Server Error" });
    }
  };

export const getAllHistory =
  ({ db }) =>
  async (req, res) => {
    try {
      let orders = await db.find({
        table: Order,
        key: {
          query: { history: true, ...req.query },
          allowedQuery,
          history: req.query.history,
          paginate: req.query.paginate === "false",
          populate: { path: "account childrens" },
        },
      });
      if (!orders) return res.status(404).send({ message: "Orders not found" });
      if (req.query.orderType === "parent")
        orders = orders.filter(
          (order) =>
            !order.childrens.some((c) => c.status === "Closed" || c.exitFrom)
        );
      return res.status(200).send(orders);
    } catch (err) {
      console.log(err);
      return res
        .status(500)
        .send({ message: err.message || "Internal Server Error" });
    }
  };

export const wipeHistory =
  ({ db }) =>
  async (req, res) => {
    try {
      console.log(req.query.history);
      if (req.query.history === "false") {
        await db.updateMany({
          table: Order,
          key: { query: {}, update: { history: false } },
        });
      }
      let orders = await db.find({
        table: Order,
        key: {
          query: { history: true, ...req.query },
          allowedQuery,
          paginate: req.query.paginate === "false",
          populate: { path: "account childrens" },
        },
      });
      if (!orders.length)
        return res.status(404).send({ message: "Orders not found" });
      if (req.query.orderType === "parent") {
        orders = orders.filter(
          (order) =>
            !order.childrens.some((c) => c.status === "Closed" || c.exitFrom)
        );
      }
      return res.status(200).send(orders);
    } catch (err) {
      console.log(err);
      return res
        .status(500)
        .send({ message: err.message || "Internal Server Error" });
    }
  };

export const updateOrder =
  ({ db, ws }) =>
  async (req, res) => {
    try {
      const { id } = req.params;
      const isExist = await db.findOne({ table: Order, key: { _id: id } });
      if (!isExist) return res.status(404).send({ message: "No Order found" });

      const orders = await Order.findOne({
        childrens: { $in: [ObjectId(id)] },
      }).populate({ path: "childrens" });
      if (!orders) {
        return res
          .status(404)
          .send({ message: "No order found with the specified ID" });
      }
      const accounts = await db.find({
        table: Account,
        key: { paginate: req.query.paginate === "true" },
      });

      const order = await Promise.all(
        orders.childrens.map(async (order) => {
          if (
            (req.body.exit === "Partial Exit" || req.body.exit === "Exit") &&
            order.ammend === true
          )
            req.body.ammend = undefined;
          if (req.body.ammend === true && order.exit === "Partial Exit")
            req.body.exit = undefined;
          req.body.placeOrder = false;
          req.body.logs = [
            ...order.logs,
            await genLog("Updated", "Order Updated"),
          ];
          const updated = await db.update({
            table: Order,
            key: { _id: order._id, body: req.body, populate },
          });
          return updated;
        })
      );

      orders.childrens = order;
      res.status(200).send(orders);
      console.log(order, accounts);

      try {
        const payLoad = { accounts, order };
        const response = await axios(`${process.env.BOT_SERVER_URL}/order`, {
          method: "POST",
          data: payLoad,
        });
        ws.emit("account", response.data);
      } catch (err) {
        console.log(err);
      }
    } catch (err) {
      console.log(err);
      return res
        .status(500)
        .send({ message: err.message || "Internal Server Error" });
    }
  };

export const closeOrder =
  ({ db }) =>
  async (req, res) => {
    try {
      const { id } = req.params;
      if (!id) return res.status(400).send({ message: "Invalid Request" });
      const trade = await Order.findOne({
        childrens: { $in: [ObjectId(id)] },
      }).populate({ path: "childrens" });
      if (!trade) return res.status(404).send({ message: "No order found" });
      const childs = await Promise.all(
        trade.childrens.map(async (children) => {
          const logs = [
            ...children.logs,
            await genLog("Closed", "Order Closed"),
          ];
          const updated = await db.update({
            table: Order,
            key: { _id: children._id, body: { status: "Closed", logs } },
          });
          return updated;
        })
      );
      trade.childrens = childs;
      return res.status(200).send(trade);
    } catch (err) {
      console.log(err);
      return res.status(500).send({ message: "Something went wrong" });
    }
  };

export const manageOrder =
  ({ db, ws }) =>
  async (req, res) => {
    try {
      const { status, orderCreated, openPrice, id, message, tradeId } =
        req.body;
      console.log(req.body);
      const order = await db.findOne({
        table: Order,
        key: { _id: id, populate },
      });
      if (!order) return res.send(404).send({ message: "Order not found" });
      order.status = status;
      order.orderCreated = orderCreated;
      order.openPrice = openPrice;
      order.tradeId = tradeId;
      console.log(tradeId, order.tradeId);
      order.logs = [...order.logs, await genLog(status, message)];
      await db.save(order);
      ws.emit("order", {
        order,
        message: `Order has been ${status} from account ${order.account.email}`,
      });
      return res.status(200).send(order);
    } catch (err) {
      console.log(err);
      return res.status(500).send({ message: "Something went wrong" });
    }
  };
