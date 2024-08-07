<script setup>
import { ref } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';
import { format } from 'date-fns';

const router = useRouter();
const route = useRoute(); // Initialize route with useRoute


const book_name = ref('');
const section_name = ref(route.query.sectionName || ''); // Default to empty if not provided
const section_id = ref('');
const content = ref('');
const authors = ref('');
const error_message = ref('');

const auth_store = authStore();
const message_store = messageStore();


async function addBook()
{
  const date_created = format(new Date(), 'yyyy-MM-dd HH:mm:ss');

const book_details =
    {
    book_name: book_name.value,
    section_name:section_name.value,
    content:content.value,
    authors:authors.value,
    date_created: date_created

    }
    try {
    const response = await fetch(`${auth_store.backend_url}/api/v1/add_book`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      },
      body: JSON.stringify(book_details)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Error Adding Book');
    }

    console.log(data.message);
    message_store.setmessage(data.message);
    // router.push('/');
  } catch (error) {
    console.log(error.message);
    message_store.setmessage(error.message);
  }

    }


</script>

<template>
    <div class="container mt-5">
  <div class="card">
    <div class= "card-header">
      Add a New Book
    </div>
    <div class="card-body">
      <form @submit.prevent="addBook">
        <div class="mb-3">
          <label for="bookName" class="form-label">Book Name</label>
          <input type="text" class="form-control" id="bookName" v-model="book_name" required>
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">Content</label>
          <textarea class="form-control" id="content" v-model="content" rows="3" required></textarea>
        </div>
        <div class="mb-3">
          <label for="authors" class="form-label">Authors</label>
          <input type="text" class="form-control" id="authors" v-model="authors" required>
        </div>
        <div class="mb-3">
          <label for="section" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="section" v-model="section_name" required>
        </div>
        <button type="submit" class="btn btn-primary">Add Book</button>
      </form>
    </div>
  </div>
</div>

</template>