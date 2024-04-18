import React from 'react';

const heads = [
  {
    name: "MarketPlace",
    classNames:
      "100%rem] shrink grow text-xs font-semibold uppercase text-[#64748B] flex justify-start",
  },
  {
    name: "Order Date",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Open Price",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Stop Loss",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Percentage",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Total",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Side",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Status",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Actions",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-center",
  },
  {
    name: "Ammend",
    classNames:
      "w-[100%] text-xs font-semibold uppercase text-[#64748B] flex justify-start",
  },
];

export default function THead() {
  return (
    <div className="flex flex-nowrap w-full items-center bg-secondary h-max py-2 px-2">
      {heads.map((h, i) => (
        <div className={`select-none ${h.classNames}`} key={i}>
          {h.name}
        </div>
      ))}
    </div>
  );
}
