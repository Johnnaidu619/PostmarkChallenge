import { useEffect, useState } from "react";
import TransactionCard from "./TransactionCard";

export default function TransactionList({ endpoint }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`https://postmarkchallenge.onrender.com${endpoint}`)
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, [endpoint]);

  if (loading) return <p>Loading...</p>;
  if (!data.length) return <p>No transactions found.</p>;

  return (
    <>
    <div className="card-grid">
      {data.map((tx) => (
        <TransactionCard key={tx._id} tx={tx} />
      ))}
      </div>
    </>
  );
}
