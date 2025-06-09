import TransactionList from "../components/TransactionList";
import MonthlySpend from "../components/MonthlySpend";
import LineChart from "../components/LineChart";
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [history, setHistory] = useState([]);
  const url=import.meta.env.VITE_SITE_URL;

  useEffect(() => {
    fetch(`${url}/monthly-spend-history`)
      .then(res => res.json())
      .then(data => setHistory(data));
  }, []);
  return (
    <div>
      {/* <div className="section">
        <h2>🔍 All Transactions</h2>
        <TransactionList endpoint="/transactions" />
      </div> */}

<div className="graph-wrapper">
  <div className="section">
    <h2>💸 Monthly Spend</h2>
    <MonthlySpend />
  </div>

  <div className="section">
    <h2>History</h2>
    <LineChart data={history} />
  </div>
</div>


      <div className="section">
        <h2>🏦 Bank Transactions</h2>
        <TransactionList endpoint="/transactions/banks" />
      </div>

      {/* <div className="section">
        <h2>🔐 High Confidence</h2>
        <TransactionList endpoint="/transactions/high-confidence" />
      </div> */}
    </div>
  );
}
