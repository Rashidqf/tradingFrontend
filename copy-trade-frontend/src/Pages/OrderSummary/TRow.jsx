import React, { useEffect, useState } from "react";
import Actions from "./Actions";
import UpdateOrder from "../../Components/Modal/UpdateOrder/UpdateOrder";
import formatDate from "../../Utils/formatDate";
import ActionOrder from "./ActionOrder";
import { shallowEqual, useSelector } from "react-redux";

export default function TRow({ order, idx, ordertype }) {
  const [updatedOrder, setupdatedOrder] = useState(order);
  const { parentTrade, tradeLoading } = useSelector(
    (state) => ({
      parentTrade: state.tradeStore.trades,
      tradeLoading: state.tradeStore.loading,
    }),
    shallowEqual
  );
  useEffect(() => {
    const updator = () => {
      setupdatedOrder(order);
      console.log(order);
    };
    updator();
  }, [order, parentTrade, tradeLoading]);
  
  const displayPercentage =
    updatedOrder?.percentage === 100 ? "200" : `${updatedOrder?.percentage}`;

  return (
    <div
      className={`flex flex-nowrap w-full items-center border-b-2 border-b-grey h-max py-2 px-2 cursor-pointer `}
    >
      <div className="flex-[11.11%] shrink grow text-xs font-semibold uppercase text-[#0c0d0e] flex justify-start">
        {updatedOrder?.marketData?.marketName || "---"}
      </div>
      <div className="flex-[11.11%] text-xs text-center font-semibold text-[#0c0d0e] flex justify-center">
        {formatDate(updatedOrder?.createdAt) || "---"}
      </div>
      <div className="flex-[11.11%] text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {updatedOrder?.openPrice || "---"}
      </div>
      <div className="flex-[11.11%] text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {updatedOrder?.pointsAway ||
          updatedOrder?.atPrice ||
          updatedOrder?.limitPointsAway ||
          "---"}
      </div>

      <div className="flex-[11.11%] text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {`${updatedOrder?.percentage}%` || "---"}
      </div>
      {/* <div className="flex-[11.11%] text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {ordertype === "trade" ? order?.ammount : order?.amount}
      </div> */}
      {/* <div className="flex-[11.11%] text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {order.type || '---'}
      </div> */}
      <div className="flex-[11.11%] text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {updatedOrder?.side || "---"}
      </div>
      <div className="flex-[11.11%] text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {updatedOrder?.status || "---"}
      </div>

      <div className="flex-[11.11%]  pr-2 text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        {ordertype === "order" ? (
          <ActionOrder orderData={updatedOrder} ordertype="order" />
        ) : (
          <Actions orderData={updatedOrder} ordertype={ordertype} />
        )}
      </div>
      <div className="flex-[11.11%]  text-xs font-semibold uppercase text-[#0c0d0e] flex justify-center">
        <UpdateOrder orderData={updatedOrder} ordertype={ordertype} />
      </div>
    </div>
  );
}
