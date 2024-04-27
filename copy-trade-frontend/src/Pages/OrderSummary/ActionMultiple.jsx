import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { useGlobalCtx } from "../../Contexts/GlobalProvider";
import "./Actions.css";

const ammounts = [
  {
    name: "100%",
    value: 100,
  },
  {
    name: "75%",
    value: 75,
  },
  {
    name: "50%",
    value: 50,
  },
  {
    name: "25%",
    value: 25,
  },
];

export default function ActionMultiple({ orderDataList, ordertype }) {
  const side = orderDataList[0]?.childrens[0]?.side === "buy" ? "sell" : "buy";
  // const side = "buy";
  const { handleSubmit, register, reset, setValue } = useForm();
  const { updateTrade, createOrder, updateOrderNew } = useGlobalCtx();
  const modalRef = useRef();
  const [tradeType, setTradeType] = useState("trade");
  const [orderTypes, setOrderTypes] = useState(side);
  const [stopLimit, setStopLimit] = useState("");
  const [isVisible, setIsVisible] = useState(false);
  useLayoutEffect(() => {
    setOrderTypes(side);
  }, []);
  useEffect(() => {
    orderDataList.forEach((orderData) => {
      Object.keys(orderData).forEach(
        (key) => key !== "percentage" && setValue(key, orderData[key])
      );
    });
  }, [orderDataList]);

  const handleModal = () => {
    modalRef.current.classList.toggle("hidden");
  };

  const onSubmit = (data) => {
    orderDataList.forEach((parentOrder) => {
      if (parentOrder.childrens.length > 0) {
        const childOrder = parentOrder.childrens[0];
        const updatedChildOrder = {
          ...childOrder,
          percentage: Number(data.percentage),
          exit: "Partial Exit",
          placeOrder: false,
        };
        delete updatedChildOrder.__v;
        updateTrade(childOrder.id, updatedChildOrder);
      }
    });
    handleModal();
    reset();
  };

  const exitAllOrders = () => {
    orderDataList.forEach((orderData) => {
      const childId =
        orderData.childrens.length > 0 ? orderData.childrens[0].id : null;
      if (childId) {
        if (ordertype === "order") {
          updateOrderNew(childId, {
            status: "Closed",
            exit: "Exit",
            placeOrder: false,
          });
        } else {
          updateTrade(childId, {
            status: "Closed",
            exit: "Exit",
            placeOrder: false,
          });
        }
      }
    });
    window.location.reload(); // Reload the page after exit
  };
  

  return (
    <>
      <div className="flex gap-5">
        <button
          disabled={orderDataList.some(
            (orderData) => orderData.status === "Closed"
          )}
          onClick={exitAllOrders}
          className="font-semibold text-regular py-2 px-7 inline-block rounded-md bg-warning disabled:bg-grey-400"
        >
          Exit
        </button>
        {ordertype === "order" ? (
          <></>
        ) : (
          <button
            disabled={orderDataList.some(
              (orderData) => orderData.status === "Closed"
            )}
            onClick={handleModal}
            className="font-semibold text-regular py-2 px-7 inline-block rounded-md bg-black disabled:bg-grey-400"
          >
            Partial Exit
          </button>
        )}
      </div>
      <section ref={modalRef} className="trade hidden h-max">
        <p
          onClick={() => {
            handleModal();
          }}
          className="text-4xl absolute top-4 right-8 cursor-pointer"
        >
          &#215;
        </p>
        <div>
          <h2 className="text-black font-bold text-xl text-center pb-2">
            Partial Exit
          </h2>
          <section className="w-[18rem] border border-grey-700 rounded bg-grey">
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="p-3">
                <div className="flex justify-center">
                  <button
                    disabled
                    onClick={(e) => {
                      e.preventDefault();
                      setTradeType("trade");
                      reset();
                    }}
                    className={`uppercase font-bold tracking-wide px-8 py-[2px] rounded ${
                      tradeType === "trade" ? "bg-primary" : "bg-black"
                    } text-regular text-lg`}
                  >
                    Trade
                  </button>
                </div>
                <p className="text-sm tracking-normal font-medium pt-1 px-1 pb-3 border-b border-b-grey-400"></p>
                <div className="pt-1 flex items-end border-b border-b-grey-400 pb-3">
                  <button
                    disabled
                    onClick={(e) => {
                      e.preventDefault();
                      setOrderTypes("sell");
                    }}
                    className={`rounded-r-none rounded capitalize font-bold text-lg text-regular w-20 text-left pl-2 h-12 ${
                      orderTypes === "buy" ? "bg-grey-400" : "bg-warning"
                    }`}
                  >
                    Sell
                  </button>
                  <div>
                    <p className="text-xs font-extralight text-center">
                      Amount
                    </p>
                    <select
                      {...register("percentage")}
                      className="w-28 outline-none text-xs tracking-wider appearance-none text-center px-1 h-10 border border-grey-400 placeholder:text-xs placeholder:font-mono placeholder:-tracking-wider"
                    >
                      <option value="" selected disabled>
                        Select Amount
                      </option>
                      {ammounts.map((amount) => (
                        <option key={amount.value} value={amount.value}>
                          {amount.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <button
                    disabled
                    onClick={(e) => {
                      e.preventDefault();
                      setOrderTypes("buy");
                    }}
                    className={`rounded-l-none rounded capitalize font-bold text-lg text-regular  w-20 text-right pr-2 h-12 ${
                      orderTypes === "sell" ? "bg-grey-400" : "bg-primary"
                    }`}
                  >
                    Buy
                  </button>
                </div>
                <div
                  className={`flex items-end ${
                    tradeType !== "order" && "justify-between"
                  } gap-1 px-1 mt-1`}
                >
                  {tradeType === "order" ? (
                    <div>
                      <p className="text-xs text-center font-thin tracking-wide">
                        Order Level
                      </p>
                      <input
                        disabled
                        type="number"
                        {...register("orderLevel")}
                        className="w-28 outline-none border border-grey-400 px-1"
                      />
                    </div>
                  ) : (
                    <></>
                  )}
                  <div></div>
                </div>  
                <div className="flex justify-center pt-4">
                  <button
                    type="submit"
                    className="uppercase font-bold tracking-wide px-8 py-[2px] rounded bg-warning text-regular text-lg"
                  >
                    Submit
                  </button>
                </div>
              </div>
            </form>
          </section>
        </div>
      </section>
    </>
  );
}
