<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';

const route = useRoute();
const router = useRouter();
const message_store = messageStore();
const auth_store = authStore();

const books = ref([]);
const section_name = ref(route.query.sectionName);

onMounted(() => {
  getBooks(route.query.sectionId);
});

function getBooks(sectionId) {
  try {
    fetch(`${auth_store.backend_url}/api/v1/section/${sectionId}/get_all_books`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    })
    .then(response => response.json())
    .then(data => {
      books.value = data;
      message_store.setmessage(data.message);
    });
  } catch (error) {
    console.log(error);
  }
}

function borrowBook(sectionName, bookName) {
  try {
    fetch(`${auth_store.backend_url}/api/v1/request_book`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      },
      body: JSON.stringify({ book_name: bookName, section_name: sectionName })
    }).then(response => {
      if (response.ok) {
        response.json().then(data => {
          message_store.setmessage('Book request added successfully');
        });
      } else {
        response.json().then(data => {
          console.log(data);
          message_store.setmessage(data.message);
        });
      }
    });
  } catch (error) {
    console.log(error);
  }
}

function deleteBook(bookId) {
  if (window.confirm('Are you sure you want to delete this book?')) {
    try {
      fetch(`${auth_store.backend_url}/api/v1/delete_book/${bookId}`, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': auth_store.token
        }
      }).then(response => {
        if (response.ok) {
          books.value = books.value.filter(book => book.book_id !== bookId);

          message_store.setmessage('Book deleted successfully');
        } else {
          response.json().then(data => {
            console.log(data);
            message_store.setmessage(data.message);
          });
        }
      });
    } catch (error) {
      console.log(error);
    }
  }
}

function editBook(book) {
  router.push({
    path: '/edit_book',
    query: {
      bookId: book.book_id,
      bookName: book.name,
      content: book.description,
      authors: book.authors,
      sectionName: section_name.value,
      sectionId: route.query.sectionId
    }
  });
}
</script>

<template>
  <div class="container mt-4">
    <div class="row">
      <div class="col-12">
        <h2>{{ section_name }}</h2>

        <div v-if="books.length === 0" class="alert alert-info">
          No books found in this section.
        </div>

        <div v-for="book in books" :key="book.book_id" class="card mb-3">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">{{ book.name }}</h5>
            <div class="btn-group" v-if="auth_store.role === 'librarian'">
              <button type="button" class="btn dropdown-toggle" style="background-color: #33a550; color: white;" data-bs-toggle="dropdown" aria-expanded="false">Actions</button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#" @click.prevent="deleteBook(book.book_id)">Delete Book</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="editBook(book)">Edit Book</a></li>
              </ul>
            </div>
            <div class="btn-group" v-else>
              <ul class="nav nav-pills card-header-pills">
                <li class="nav-item">
                  <a class="nav-link active" style="background-color: #33a550; color: white;" @click.prevent="borrowBook(section_name, book.name)">Borrow Book</a>
                </li>
              </ul>
            </div>
          </div>
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">Authors: {{ book.authors }}</h6>
            <p class="card-text">Content: {{ book.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
