<template>
    <div class="chart-container">
      <div v-if="auth_store.isAuthenticated && auth_store.role === 'librarian'" class="chart-card">
        <h3 class="chart-title">Most Borrowed Books</h3>
        <div class="chart-wrapper">
          <canvas ref="chart1"></canvas>
        </div>
      </div>
      <div v-if="auth_store.isAuthenticated && auth_store.role === 'librarian'" class="chart-card">
        <h3 class="chart-title">Popular Authors</h3>
        <div class="chart-wrapper">
          <canvas ref="chart2"></canvas>
        </div>
      </div>
      <div v-if="auth_store.isAuthenticated && auth_store.role === 'librarian'" class="chart-card">
        <h3 class="chart-title">Active Users</h3>
        <div class="chart-wrapper">
          <canvas ref="chart3"></canvas>
        </div>
      </div>
      <div v-if="auth_store.isAuthenticated && auth_store.role === 'librarian'" class="chart-card">
        <h3 class="chart-title">Popular Sections</h3>
        <div class="chart-wrapper">
          <canvas ref="chart4"></canvas>
        </div>
      </div>
      <div v-if="auth_store.isAuthenticated && auth_store.role != 'librarian'" class="chart-card">
        <h3 class="chart-title">Your Activity</h3>
        <div class="chart-wrapper">
          <canvas ref="chart5"></canvas>
        </div>
      </div>
      <div v-if="auth_store.isAuthenticated && auth_store.role != 'librarian'" class="chart-card">
        <h3 class="chart-title">Books Borrowed By Section</h3>
        <div class="chart-wrapper">
          <canvas ref="chart6"></canvas>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { Colors } from 'chart.js';
  import { ref, onMounted } from 'vue';
  import { Chart } from 'chart.js/auto';
  import { authStore } from '../stores/authStore';
  
  const auth_store = authStore();
  Chart.register(Colors);
  
  const chart1 = ref(null); // Most Borrowed Books
  const chart2 = ref(null); // Popular Authors
  const chart3 = ref(null); // Active Users
  const chart4 = ref(null); // Popular Sections
  const chart5 = ref(null); // Active Users
  const chart6 = ref(null); // Popular Sections
  
  function renderChart(canvasRef, data, type) {
  const ctx = canvasRef.value.getContext('2d');

  new Chart(ctx, {
    type: type, // Pass 'pie' for pie chart
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.label || '';
              if (context.parsed !== null) {
                label += `: ${context.parsed}`;
              }
              return label;
            }
          }
        }
      },
      // Conditionally include scales based on chart type
      scales: type === 'pie' || type === 'doughnut' ? undefined : {
        x: { beginAtZero: true },
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) { return Math.ceil(value) }, // Ensure whole numbers only
          },
          suggestedMax: Math.max(...data.datasets[0].data) + 3
        },
      },
    },
  });
}

  async function fetchChartData(apiEndpoint, chartRef, type) {
    try {
      const response = await fetch(apiEndpoint, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': auth_store.token,
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        renderChart(chartRef, data, type);
      } else {
        console.error('Failed to fetch chart data');
      }
    } catch (error) {
      console.log('Error:', error);
    }
  }
  
  onMounted(() => {
    fetchChartData(`${auth_store.backend_url}/api/v1/most-borrowed-books`, chart1, 'bar');
    fetchChartData(`${auth_store.backend_url}/api/v1/popular-authors`, chart2, 'line');
    fetchChartData(`${auth_store.backend_url}/api/v1/active-users`, chart3, 'pie');
    fetchChartData(`${auth_store.backend_url}/api/v1/popular-sections`, chart4, 'line');
    fetchChartData(`${auth_store.backend_url}/api/v1/recent-user-activity`, chart5, 'bar');
    fetchChartData(`${auth_store.backend_url}/api/v1/borrowed-books-by-section`, chart6, 'bar');


    
  });
  </script>
  
  <style scoped>
  .chart-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* Two columns */
    gap: 30px; /* Increased space between cards */
    padding: 50px 100px; /* Added padding around the container */
  }
  
  .chart-card {
    background-color: #ffffff;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.267);
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .chart-card:hover {
    transform: translateY(-14px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  }
  
  .chart-title {
    margin-bottom: 20px;
    font-size: 1.6em;
    color: #333;
    text-align: center;
    font-family: 'Roboto', sans-serif; /* Improved font */
  }
  
  .chart-wrapper {
    width: 100%;
    height: 250px; /* Increased chart height for better visibility */
    position: relative;
  }
  
  canvas {
    width: 100% !important;
    height: 100% !important;
  }
  </style>
  