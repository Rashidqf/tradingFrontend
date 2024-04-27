import React from 'react';
import TradeForm from './TradeForm';

// const data = [
//   {
//     marketName: 'Germany 40 - Rolling Cash',
//     marketId: '17068',
//     quoteId: '6374'
//   },
//   {
//     marketName: 'UK 100 - Rolling Cash',
//     marketId: '16645',
//     quoteId: '5945'
//   },
//   {
//     marketName: 'Wall Street 30 - Rolling Cash',
//     marketId: '17322',
//     quoteId: '6647'
//   },
//   {
//     marketName: 'US Tech 100 - Rolling Cash',
//     marketId: '20190',
//     quoteId: '16917'
//   },
// ];


const data = [
  {
    marketName: 'Germany 40',
    marketId: '17068',
    quoteId: '6374'
  },
  {
    marketName: 'UK 100',
    marketId: '16645',
    quoteId: '5945'
  },
  {
    marketName: 'Wall Street 30',
    marketId: '17322',
    quoteId: '6647'
  },
  {
    marketName: 'US Tech 100',
    marketId: '20190',
    quoteId: '16917'
  },
];

export default function MarketOrder() {
  return (
    <section className="w-full">
      <div className="grid grid-cols-2 gap-y-3">
        { 
          data.map((d) => <TradeForm key={d.marketId} marketData={d} />)
        }
      </div>
    </section>
  );
}
