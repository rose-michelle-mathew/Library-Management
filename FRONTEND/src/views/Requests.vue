<script setup>
import { ref, onMounted } from 'vue';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';
import { useRouter } from 'vue-router';

const auth_store = authStore();
const message_store = messageStore();
const router = useRouter();
const requests = ref([]);

onMounted(() => {
  fetchRequests();
});

function fetchRequests() {
  try {
    fetch(`${auth_store.backend_url}/api/v1/requests`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      }
    }).then(response => response.json())
      .then(data => {
        requests.value = data;
      })
      .catch(error => {
        console.log(error);
        message_store.setmessage('Failed to fetch requests');
      });
  } catch (error) {
    console.log(error);
    message_store.setmessage('Failed to fetch requests');
  }
}

function revokeRequest(requestId) {
  if (window.confirm('Are you sure you want to revoke this request?')) {
    try {
      fetch(`${auth_store.backend_url}/api/v1/revoke_book/${requestId}`, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': auth_store.token
        }
      }).then(response => {
        if (response.ok) {
          message_store.setmessage('Request revoked successfully');
          fetchRequests(); // Refresh the list of requests
        } else {
          response.json().then(data => {
            console.log(data);
            message_store.setmessage(data.message);
          });
        }
      }).catch(error => {
        console.log(error);
        message_store.setmessage('Failed to revoke request');
      });
    } catch (error) {
      console.log(error);
      message_store.setmessage('Failed to revoke request');
    }
  }
}

function approveRejectRequest(requestId, action) {
  if (window.confirm(`Are you sure you want to ${action} this request?`)) {
    try {
      fetch(`${auth_store.backend_url}/api/v1/approvals`, {
        method: "PUT",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': auth_store.token
        },
        body: JSON.stringify({ request_id: requestId, action })
      }).then(response => {
        if (response.ok) {
          message_store.setmessage(`Request ${action}ed successfully`);
          fetchRequests(); // Refresh the list of requests
        } else {
          response.json().then(data => {
            console.log(data);
            message_store.setmessage(data.message);
          });
        }
      }).catch(error => {
        console.log(error);
        message_store.setmessage(`Failed to ${action} request`);
      });
    } catch (error) {
      console.log(error);
      message_store.setmessage(`Failed to ${action} request`);
    }
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2>Book Requests</h2>
    <div v-if="auth_store.role === 'librarian'">
      <h3>All Requests</h3>
      <div v-if="requests.length > 0">
        <div v-for="request in requests" :key="request.request_id" class="card mb-3">
          <div class="card-header">
            <h5 class="mb-0">{{ request.book.name }}</h5>
            <span class="badge bg-info">{{ request.status }}</span>
            <button class="btn btn-success" @click="approveRejectRequest(request.request_id, 'approve')">Approve</button>
            <button class="btn btn-warning" @click="approveRejectRequest(request.request_id, 'reject')">Reject</button>
          </div>
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">Requested By: {{ request.user_name }}</h6>
            <h6 class="card-subtitle mb-2 text-muted">Authors: {{ request.book.authors }}</h6>
            <p class="card-text">Section: {{ request.book.section.name }}</p>
            <p class="card-text"><small class="text-muted">Requested on: {{ request.date_of_request }}</small></p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No requests found.</p>
      </div>
    </div>
    <div v-else>
      <h3>My Requests</h3>
      <div v-if="requests.length > 0">
        <div v-for="request in requests" :key="request.request_id" class="card mb-3">
          <div class="card-header">
            <h5 class="mb-0">{{ request.book.name }}</h5>
            <span class="badge bg-info">{{ request.status }}</span>
            <button class="btn btn-danger" @click="revokeRequest(request.request_id)">Revoke Request</button>
          </div>
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">Authors: {{ request.book.authors }}</h6>
            <p class="card-text">Section: {{ request.book.section.name }}</p>
            <p class="card-text"><small class="text-muted">Requested on: {{ request.date_of_request }}</small></p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No requests found.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-header h5 {
  flex: 1;
}
.card-header .badge {
  margin-left: auto;
  margin-right: 10px;
}
.card-header .btn {
  margin-left: 10px;
}
</style>
