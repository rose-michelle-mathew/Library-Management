<script setup>
import { useRouter } from 'vue-router';
import LineChart from '../components/LineChart.vue';

import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';

const auth_store = authStore();
const message_store = messageStore();
const router = useRouter();


async function downloadReport() {
  try {
    const response = await fetch(`${auth_store.backend_url}/api/v1/download-csv`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      }
    });

    if (response.ok) {
      console.log('Task started');
      message_store.setmessage('Report generation started. You will receive an email when it is ready.');
    } else {
      console.log('Failed to start task:', errorData);
      message_store.setmessage('Failed to start report generation.');
    }
  } catch (error) {
    console.error('Error:', error);
    message_store.setmessage('An error occurred while starting the report generation.');
  }
}

function navigateTo(path) {
  router.push(path);
}
</script>

<template>
  <div class="container mt-4">
    <h2>Librarian Dashboard</h2>
    <div class="dashboard-bar">
      <span class="dashboard-text">User Activity Overview</span>
      <button @click="downloadReport" class="btn btn-primary">Download Report</button>
    </div>

    <div class="dashboard-bar mt-3">
      <span class="dashboard-text">Book Requests</span>
      <button v-if="auth_store.isAuthenticated" @click="navigateTo('/requests')" class="btn btn-primary">View Book Requests</button>
    </div>

    <div class="dashboard-bar mt-3">
      <span class="dashboard-text">Borrowed Books</span>
      <button v-if="auth_store.isAuthenticated && auth_store.role === 'librarian'" @click="navigateTo('/borrowed')" class="btn btn-primary">View Borrowed Books</button>
    </div>

    <!-- Charts Section -->
    <div class="mt-4">
     
      <LineChart />
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 100%;
  padding: 0 15px;
}

.dashboard-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}

.dashboard-text {
  font-size: 1.3em;
  font-family: 'Roboto', sans-serif; /* Improved font */

}

.btn {
  padding: 10px 20px;
  font-size: 1em;
  background-color: rgb(58, 148, 65);
  border-color: rgb(58, 148, 65);
}

.mt-4 {
  margin-top: 1.5rem;
}
</style>
