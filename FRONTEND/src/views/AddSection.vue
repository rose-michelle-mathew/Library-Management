<script setup>

import { ref } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';

const router = useRouter();
const section_name = ref('');
const description = ref('');


const auth_store = authStore();
const message_store = messageStore();

async function addSection() {
  const date_created = new Date().toISOString();

  const section_details = {
    section_name: section_name.value,
    description: description.value,
    date_created: "2024-06-22 10:00:00"
  };

    try {
    const response = await fetch(`${auth_store.backend_url}/api/v1/add_section`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      },
      body: JSON.stringify(section_details)
    });

    const data = await response.json();

    if (!response.ok) {
        console.log(date_created)
      throw new Error(data.message || 'Error Adding Section');
    }

    console.log(data.message);
    console.log(date_created);
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
      Add a New Section
    </div>
    <div class="card-body">
      <form @submit.prevent="addSection">
        <div class="mb-3">
          <label for="bookName" class="form-label">Section Name</label>
          <input type="text" class="form-control" id="sectionName" v-model="section_name" required>
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">Description</label>
          <textarea class="form-control" id="description" v-model="description" rows="3" required></textarea>
        </div>
        
        <button type="submit" class="btn btn-primary">Add Section</button>
      </form>
    </div>
  </div>
</div>

</template>