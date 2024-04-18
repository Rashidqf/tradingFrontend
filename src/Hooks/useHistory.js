import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { setValue } from "../reducers/historyReducer";
import { useEffect } from "react";
import req from "./req";

const useHistory = () => {
  const dispatch = useDispatch();
  const page = useSelector(
    (state) => state.historyStore.pagination.page,
    shallowEqual
  );

  useEffect(() => {
    dispatch(setValue({ target: "loading", value: true }));
    req({
      method: "GET",
      uri: `order/getAll?${new URLSearchParams({
        page,
        paginate: false,
        orderType: "child",
      })}`,
    })
      .then(({ data: { docs, totalDocs } }) => {
        dispatch((update, getState) => {
          const { pagination } = getState().historyStore;
          update(setValue({ target: "allOrders", value: docs }));
          update(
            setValue({
              target: "pagination",
              value: { ...pagination, total: totalDocs },
            })
          );
        });
      })
      .catch((err) => console.log(err))
      .finally(() => dispatch(setValue({ target: "loading", value: false })));
  }, [page]);

  const handlePagination = (event, value) => {
    dispatch((update, getState) => {
      const { pagination } = getState().historyStore;
      update(
        setValue({
          target: "pagination",
          value: { ...pagination, page: value },
        })
      );
    });
  };

  return {
    handlePagination,
  };
};

export default useHistory;
