<template>
    <div class="container mt-4">
      <h2>Search Books</h2>
      <form @submit.prevent="searchBooks">
        <div class="form-group">
          <label for="section_name">Section Name</label>
          <input type="text" v-model="searchParams.section_name" class="form-control" id="section_name">
        </div>
        <div class="form-group">
          <label for="author_name">Author Name</label>
          <input type="text" v-model="searchParams.author_name" class="form-control" id="author_name">
        </div>
        <div class="form-group">
          <label for="book_name">Book Name</label>
          <input type="text" v-model="searchParams.book_name" class="form-control" id="book_name">
        </div>
        <div class="form-group">
          <label for="content">Content</label>
          <input type="text" v-model="searchParams.content" class="form-control" id="content">
        </div>
        <button type="submit" class="btn btn-primary mt-3">Search</button>
      </form>
  
      <div v-if="searchResults.length > 0" class="mt-4">
        <h3>Search Results</h3>
        <ul class="list-group">
          <li v-for="book in searchResults" :key="book.id" class="list-group-item shadow-sm">
            <div class="book-info">
              <div class="section-label" :style="{ backgroundColor:  'rgba(75, 192, 192, 0.7)' }">
                {{ book.section_name }}
              </div>
              <h4>{{ book.name }}</h4>
              <p class="text-muted">by {{ book.authors }}</p>
              <p>{{ book.content }}</p>
            </div>
          </li>
        </ul>
      </div>
  
      <div v-else-if="searchPerformed" class="mt-4">
        <p>No results found.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { authStore } from '@/stores/authStore';
  
  const auth_store = authStore();
  
  const searchParams = ref({
    section_name: '',
    author_name: '',
    book_name: '',
    content: ''
  });
  
  const searchResults = ref([]);
  const searchPerformed = ref(false);
  
  async function searchBooks() {
    try {
      const response = await fetch(`${auth_store.backend_url}/api/v1/search`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': auth_store.token
        },
        body: JSON.stringify(searchParams.value)
      });
  
      if (response.ok) {
        const data = await response.json();
        searchResults.value = data.books;
      } else {
        searchResults.value = [];
        console.error('Failed to fetch search results');
      }
    } catch (error) {
      searchResults.value = [];
      console.error(error);
    }
  
    searchPerformed.value = true;
  }
  

  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  
  .list-group-item {
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    background-color: #fdfdfd;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .list-group-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  .book-info {
    position: relative;
    padding: 20px 10px 10px;
  }
  
  .section-label {
    position: absolute;
    top: -10px;
    right: -10px;
    padding: 5px 10px;
    font-size: 14px;
    font-weight: bold;
    color: white;
    border-radius: 5px;
  }
  
  </style>
  