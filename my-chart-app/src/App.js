import React from 'react';
import { Line, Bar, Pie, Radar } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, BarElement, PointElement, ArcElement, Filler, RadarController } from 'chart.js';

// Register necessary components for Chart.js
ChartJS.register(
    Title, Tooltip, Legend,
    LineElement, BarElement, PointElement,
    ArcElement, Filler,
    RadarController
);

const App = () => {
    // Sample data for the charts
    const lineData = {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [
            {
                label: 'Sales',
                data: [65, 59, 80, 81, 56],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }
        ]
    };

    const barData = {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [
            {
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }
        ]
    };

    const pieData = {
        labels: ['Red', 'Blue', 'Yellow'],
        datasets: [
            {
                label: '# of Votes',
                data: [300, 50, 100],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }
        ]
    };

    const radarData = {
        labels: ['Running', 'Swimming', 'Eating', 'Cycling'],
        datasets: [
            {
                label: 'User A',
                data: [120, 140, 180, 150],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'User B',
                data: [100, 110, 160, 170],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }
        ]
    };

    return (
        <>
         <div style={{ padding: '20px' }}>
            <h1>Line Chart</h1>
            <Line data={barData} />
        </div>
        </>
    );
};

export default App;
