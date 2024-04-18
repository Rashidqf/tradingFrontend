import React from "react";
import Actions from "./Actions";
import UpdateOrder from "../../Components/Modal/UpdateOrder/UpdateOrder";
import formatDate from "../../Utils/formatDate";
import ActionOrder from "./ActionOrder";

export default function TRow({ order, idx, ordertype }) {
  const displayPercentage =
    order?.percentage === 100 ? "200" : `${order?.percentage}`;

  return (
    <div
      className={`flex flex-nowrap w-full items-center border-b-2 border-b-grey h-max py-2 px-2 cursor-pointer `}
    >
      <div className="w-[100%] shrink grow text-xs font-semibold uppercase text-[#64748B] flex justify-start">
        {order?.marketData?.marketName || "---"}
      </div>
      <div className="w-[100%] text-xs text-center font-semibold text-[#64748B] flex justify-center">
        {formatDate(order?.createdAt) || "---"}
      </div>
      <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {order?.openPrice || "---"}
      </div>
      <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {order?.pointsAway || order?.atPrice || order?.limitPointsAway || "---"}
      </div>

      <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {`${order?.percentage}%` || "---"}
      </div>
      <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {ordertype === "trade" ? order?.ammount : order?.amount}
      </div>
      {/* <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {order.type || '---'}
      </div> */}
      <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {order?.side || "---"}
      </div>
      <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {order?.status || "---"}
      </div>

      <div className="w-[100%] pr-2 text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        {ordertype === "order" ? (
          <ActionOrder  orderData={order} ordertype="order" />
        ) : (
          <Actions orderData={order} ordertype={ordertype} />
        )}
      </div>
      <div className="w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center">
        <UpdateOrder orderData={order} ordertype={ordertype} />
      </div>
    </div>
  );
}
