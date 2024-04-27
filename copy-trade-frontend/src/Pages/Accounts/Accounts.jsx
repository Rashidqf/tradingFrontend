import React from 'react';
import THead from './THead';
import { useGlobalCtx } from '../../Contexts/GlobalProvider';
import TRow from './TRow';
import sortByPercentage from '../../Utils/sortByPercentage';
import Paginations from '../../Components/Shared/Pagination/Paginations';
import { shallowEqual, useSelector } from 'react-redux';

export default function Accounts() {
    const { accounts, total } = useSelector((state) => ({
        accounts: state.acountStore.accounts,
        total: state.acountStore.pagination.page
    }), shallowEqual);
    const { sendAllAccounts, handlePagination } = useGlobalCtx();

    console.log(accounts)
    return (
        <section className="p-5 w-full flex flex-col h-full">
            <div className='flex-1 flex flex-col'>
                <div className="flex-1">
                    <div className="flex justify-between">
                        <h1 className="font-semibold text-xl py-3">Accounts Summary</h1>
                        <button onClick={sendAllAccounts} disabled={accounts?.length > 0 ? false : true} className="cursor-pointer font-medium select-none disabled:bg-grey-400 disabled:cursor-default h-7 px-2 bg-primary rounded-sm text-regular">UPDATE</button>
                    </div>
                    <div className="flex-col w-full">
                        <THead />
                        {
                            accounts?.length > 0 ? sortByPercentage(accounts).map((account, idx) => <TRow idx={idx} key={account.id} data={account} />) : <p className="min-h-[70vh] w-full flex justify-center items-center">No Accounts found !</p>
                        }
                    </div>
                </div>
                <div>
                    <Paginations onChange={handlePagination} total={total} />
                </div>
            </div>
        </section>
    );
}