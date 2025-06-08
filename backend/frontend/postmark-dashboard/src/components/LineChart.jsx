import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend,
  } from 'chart.js';
  import { Line } from 'react-chartjs-2';
  
  ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);
  
  const LineChart = ({ data }) => {
    const chartData = {
      labels: data.map(item => item.month),
      datasets: [
        {
          label: 'Total Spend',
          data: data.map(item => item.total_spent),
          fill: false,
          borderColor: '#3b82f6',
          tension: 0.3,
        },
      ],
    };
  
    return (
      <div style={{ width: '100%', maxWidth: '600px', margin: '2rem auto' }}>
        <h3 style={{ textAlign: 'center' }}>Spend (Last 6 Months)</h3>
        <Line data={chartData} />
      </div>
    );
  };
  
  export default LineChart;
  