<script setup>
import { defineProps, ref } from 'vue';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

const message_store = messageStore();
const auth_store = authStore();
const section = defineProps(['id']);

const section_data = ref({
  id: 0,
  section_name: '',
  description: '',
  date_created: '',
  section_books: []
});

let section_name = ref('');
let description = ref('');
const router = useRouter();

onMounted(() => {
  getSection(section.id);
});

function getSection(id) {
  try {
    fetch(`${auth_store.backend_url}/api/v1/section/${id}`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token

      }
    }).then(
      (response) => {
        return response.json();
      }
    ).then((data) => {
      console.log(data);
      section_name.value = data.section_name;
      description.value = data.description;
      message_store.setmessage(data.message);
    })
  } catch (error) {
    console.log(error);
  }
}

function deleteSection(id) {
  if (window.confirm('Are you sure you want to delete this Section?')) {
  try {
    fetch(`${auth_store.backend_url}/api/v1/delete_section/${id}`, {
      method: "DELETE",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token

      }
    }).then(
      (response) => {
        if (response.ok) {
          message_store.setmessage('Section deleted successfully');
          router.push('/Sections'); // Redirect to another page after deletion
        } else {
          response.json().then(data => {
            console.log(data);
            message_store.setmessage(data.message);
          });
        }
      }
    )
  } catch (error) {
    console.log(error);
  }
}
}
</script>

<template>
  <div class="container mt-4">
    <!-- Card for Librarians -->
    <div v-if="auth_store.role === 'librarian'" class="row">
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">{{ section_name }}</h5>
          <div class="btn-group">
            <button type="button" class="btn dropdown-toggle" style="background-color: #33a550; color: white;" data-bs-toggle="dropdown" aria-expanded="false">
              Actions
            </button>
            <ul class="dropdown-menu">
              <li>
                <RouterLink class="dropdown-item" :to="{ path: '/view_books', query: { sectionId: section.id, sectionName: section_name } }">View Books</RouterLink>
              </li>
              <li><a class="dropdown-item" href="#">Edit Section</a></li>
              <li><a class="dropdown-item" href="#" @click.prevent="deleteSection(section.id)">Delete Section</a></li>
              <li>
                <RouterLink class="dropdown-item" :to="{ path: '/add_book', query: { sectionId: section.id, sectionName: section_name } }">Add Books</RouterLink>
              </li>
            </ul>
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">{{ description }}</p>
        </div>
      </div>
    </div>

    <!-- Card for Other Roles -->
    <div v-else class="row">
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="mb-0">{{ section_name }}</h5>
          <div class="btn-group">
            <ul class="nav nav-pills card-header-pills">
      <li class="nav-item">
        <RouterLink class="nav-link active" style="background-color: #33a550; color: white;"  :to="{ path: '/view_books', query: { sectionId: section.id, sectionName: section_name } }">View Books</RouterLink>
      </li>
    </ul>
      
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">{{ description }}</p>
        </div>
      </div>
    </div>
  </div>


</template>
