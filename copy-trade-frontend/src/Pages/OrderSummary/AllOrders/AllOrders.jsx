import React from "react";
import { shallowEqual, useSelector } from "react-redux";
import Loader from "../../../Components/Shared/Loader/Loader";
import Paginations from "../../../Components/Shared/Pagination/Paginations";
import { useGlobalCtx } from "../../../Contexts/GlobalProvider";
import THead from "./THead";
import TRow from "./TRow";

export default function AllOrders() {
  const { handlePagination, WipeTrade } = useGlobalCtx();
  const { orders, loading, total, currentPage } = useSelector(
    (state) => ({
      orders: state.historyStore.allOrders,
      loading: state.historyStore.loading,
      total: state.historyStore.pagination.total,
      currentPage: state.historyStore.pagination.page,
    }),
    shallowEqual
  );

  // const wipeData = () =>{
  //   WipeTrade;
  // }

  return (
    <>
      {loading ? (
        <Loader />
      ) : (
        <section className="p-5 w-full flex flex-col h-full">
          <div className="flex-1 flex flex-col">
            <div className="flex-1">
              <div className="flex justify-between">
                <h1 className="font-semibold text-xl py-3">All Orders</h1>
              <button c onClick={WipeTrade} className="cursor-pointer font-medium outline-none border-none select-none inline-block px-4 py-[5px] bg-primary rounded-3xl text-regular mb-1">
                Wipe data
              </button>
              </div>
              
              <div className="flex flex-col w-full">
                <THead />
                {orders?.length > 0 ? (
                  orders.map((order, idx) => (
                    <TRow key={order.id} order={order} idx={idx} />
                  ))
                ) : (
                  <p className="min-h-[70vh] w-full flex justify-center items-center text-primary">
                    No Orders found !
                  </p>
                )}
              </div>
            </div>
            <div>
              <Paginations
                onChange={handlePagination}
                currentPage={currentPage}
                total={total}
              />
            </div>
          </div>
        </section>
      )}
    </>
  );
}
