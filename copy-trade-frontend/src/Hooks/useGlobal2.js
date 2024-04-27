import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { io } from "socket.io-client";
import { manageCloseOrder, manageOrderStatus, updateOrder } from "../reducers/orderReducer";
import useUtils from "../Utils/useUtils";
import { manageStatus } from "../reducers/historyReducer";

const socket = io(process.env.REACT_APP_SOCKET_URL, { autoConnect: true, reconnection: true });

const useGlobal2 = () => {
    const dispatch = useDispatch();
    const { hitToast } = useUtils();

    useEffect(() => {

        socket.on('connection', (data) => {
            console.log(data);
        });

        socket.on('partialExit', (data) => {
            dispatch(updateOrder(data));
        });

        socket.on('account', (data) => {
            console.log(data);
        });

        socket.on('order', (data) => {
            const { order, message } = data;
            hitToast(message, 'success');
            if (order.status === 'Closed') dispatch(manageCloseOrder(order));
            else dispatch(manageOrderStatus(order));
            dispatch(manageStatus(order));
        });

        return () => {
            socket.off('connection');
            socket.off('account');
            socket.off('partialExit');
        };

    }, []);

    return {
        socket,
    };
};

export default useGlobal2;