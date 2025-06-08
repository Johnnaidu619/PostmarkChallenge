import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChart = ({ spent, limit }) => {
  const data = {
    labels: ['Spent', 'Remaining'],
    datasets: [
      {
        label: 'Monthly Spend',
        data: [spent, Math.max(limit - spent, 0)],
        backgroundColor: ['#f87171', '#34d399'], // red, green
        borderWidth: 1,
      },
    ],
  };

  return (
    <div style={{ width: '300px', margin: 'auto' }}>
      <h3 style={{ textAlign: 'center' }}>Monthly Spending</h3>
      <Pie data={data} />
    </div>
  );
};

export default PieChart;
