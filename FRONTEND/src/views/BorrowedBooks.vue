<script setup>
import { ref, onMounted } from 'vue';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';
import { useRouter } from 'vue-router';

const auth_store = authStore();
const message_store = messageStore();
const router = useRouter();
const borrowedBooks = ref([]);

onMounted(() => {
  fetchBorrowedBooks();
});

function fetchBorrowedBooks() {
  try {
    fetch(`${auth_store.backend_url}/api/v1/borrowedBooks`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      }
    }).then(response => response.json())
      .then(data => {
        borrowedBooks.value = data;
      })
      .catch(error => {
        console.log(error);
        message_store.setmessage('Failed to fetch borrowed books');
      });
  } catch (error) {
    console.log(error);
    message_store.setmessage('Failed to fetch borrowed books');
  }
}

function returnBook(borrowedId) {
  if (window.confirm('Are you sure you want to return this book?')) {
    try {
      fetch(`${auth_store.backend_url}/api/v1/return`, {
        method: "PUT",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': auth_store.token
        },
        body: JSON.stringify({ borrowed_id: borrowedId })
      }).then(response => {
        if (response.ok) {
          message_store.setmessage('Book returned successfully');
          fetchBorrowedBooks(); // Refresh the list of borrowed books
        } else {
          response.json().then(data => {
            console.log(data);
            message_store.setmessage(data.message);
          });
        }
      }).catch(error => {
        console.log(error);
        message_store.setmessage('Failed to return book');
      });
    } catch (error) {
      console.log(error);
      message_store.setmessage('Failed to return book');
    }
  }
}
</script>
<template>
  <div class="container mt-4">
    <h2>Borrowed Books</h2>
    <div v-if="borrowedBooks.length > 0">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Book Name</th>
            <th>Authors</th>
            <th>Section</th>
            <th v-if="auth_store.role === 'librarian'">Borrowed By</th>
            <th>Issue Date</th>
            <th>Due Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in borrowedBooks" :key="book.borrowed_id">
            <td>{{ book.book.name }}</td>
            <td>{{ book.book.authors }}</td>
            <td>{{ book.book.section.name }}</td>
            <td v-if="auth_store.role === 'librarian'">{{ book.user_name }}</td>
            <td>{{ book.issue_date }}</td>
            <td>{{ book.due_date }}</td>
            <td><span class="badge bg-info">{{ book.status }}</span></td>
            <td>
              <button v-if="auth_store.role === 'librarian'" class="btn btn-warning" @click="revokeAccess(book.borrowed_id)">Revoke Access</button>
              <button v-else class="btn btn-primary" @click="returnBook(book.borrowed_id)">Return Book</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No borrowed books found.</p>
    </div>
  </div>
</template>

<style scoped>
.table {
  margin-top: 20px;
}
.table th, .table td {
  vertical-align: middle;
}
</style>

