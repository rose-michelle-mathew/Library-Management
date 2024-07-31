<script setup>
import { ref, onMounted } from 'vue';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';

const auth_store = authStore();
const message_store = messageStore();
const history = ref(null);

onMounted(() => {
  fetchHistory();
});

async function fetchHistory() {
  try {
    const response = await fetch(`${auth_store.backend_url}/api/v1/history`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      }
    });
    if (response.ok) {
      history.value = await response.json();
    } else {
      const data = await response.json();
      console.log(data);
      message_store.setmessage(data.message || 'Failed to fetch history');
    }
  } catch (error) {
    console.log(error);
    message_store.setmessage('Failed to fetch history');
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2>User History</h2>
    <div v-if="history">
      <div>
        <h3>Activity Logs</h3>
        <table class="table table-striped" v-if="history.activity_logs.length > 0">
          <thead>
            <tr>
              <th>Book Name</th>
              <th>Section</th>
              <th>Requested Date</th>
              <th>Approved Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="activity in history.activity_logs" :key="activity.activity_id">
              <td>{{ activity.book.name }}</td>
              <td>{{ activity.book.section.name }}</td>
              <td>{{ activity.requested_date }}</td>
              <td>{{ activity.approved_date }}</td>
              <td>
                <span :class="statusClass(activity.status)">{{ activity.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>No activity logs found.</p>
      </div>
    </div>
    <div v-else>
      <p>Loading history...</p>
    </div>
  </div>
</template>

<script>
function statusClass(status) {
  if (status === 'rejected') {
    return 'badge bg-danger';
  } else if (status === 'returned') {
    return 'badge bg-success';
  } else {
    return 'badge bg-info';
  }
}
</script>

<style scoped>
.table {
  margin-top: 20px;
}
.table th, .table td {
  vertical-align: middle;
}
</style>
