import { useEffect, useState } from "react";
import PieChart from '../components/PieChart'

export default function MonthlySpend() {
  const [spend, setSpend] = useState(null);
  const [loading, setLoading] = useState(true);
  const url=import.meta.env.VITE_SITE_URL;
  useEffect(() => {
    fetch(`${url}/monthly-spend`)
      .then((res) => res.json())
      .then((json) => {
        setSpend(json);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading spend info...</p>;

  return (
    <div>
    <PieChart spent={spend.total_spent} limit={spend.monthly_limit} />
  </div>
  );
}
