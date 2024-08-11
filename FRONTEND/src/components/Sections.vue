<script setup>
import { defineProps, ref, onMounted } from 'vue';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';
import { useRouter } from 'vue-router';

const message_store = messageStore();
const auth_store = authStore();
const props = defineProps(['id']);

const sectionData = ref({
  id: 0,
  section_name: '',
  description: '',
  date_created: '',
  section_books: []
});

const router = useRouter();

onMounted(() => {
  getSection(props.id);
});

async function getSection(id) {
  try {
    const response = await fetch(`${auth_store.backend_url}/api/v1/section/${id}`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authentication-Token': auth_store.token
      }
    });
    const data = await response.json();
    if (response.ok) {
      sectionData.value = {
        id: data.id,
        section_name: data.section_name,
        description: data.description,
        date_created: data.date_created,
        section_books: data.section_books
      };
      message_store.setmessage(data.message);
    } else {
      console.error('Failed to fetch section data', data.message);
    }
  } catch (error) {
    console.error(error);
  }
}

async function deleteSection(id) {
  if (window.confirm('Are you sure you want to delete this Section?')) {
    try {
      const response = await fetch(`${auth_store.backend_url}/api/v1/delete_section/${id}`, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': auth_store.token
        }
      });

      if (response.ok) {
        message_store.setmessage('Section deleted successfully');
        sectionData.value = null; // Remove section data
        router.push('/'); // Redirect to another page after deletion
      } else {
        const data = await response.json();
        console.error('Failed to delete section', data.message);
        message_store.setmessage(data.message);
      }
    } catch (error) {
      console.error(error);
    }
  }
}
</script>

<template>
  <div class="container mt-4">
    <div v-if="sectionData" class="row" >
      <!-- Card for Librarians -->
      <div v-if="auth_store.role === 'librarian'" class="row">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">{{ sectionData.section_name }}</h5>
            <div class="btn-group">
              <button type="button" class="btn dropdown-toggle" style="background-color: #33a550; color: white;" data-bs-toggle="dropdown" aria-expanded="false">
                Actions
              </button>
              <ul class="dropdown-menu">
                <li>
                  <RouterLink class="dropdown-item" :to="{ path: '/view_books', query: { sectionId: sectionData.id, sectionName: sectionData.section_name } }">View Books</RouterLink>
                </li>
                <li>
                  <RouterLink class="dropdown-item" :to="{ path: '/edit_section', query: { sectionId: sectionData.id } }">Edit Section</RouterLink>
                </li>
                <li><a class="dropdown-item" href="#" @click.prevent="deleteSection(sectionData.id)">Delete Section</a></li>
                <li>
                  <RouterLink class="dropdown-item" :to="{ path: '/add_book', query: { sectionId: sectionData.id, sectionName: sectionData.section_name } }">Add Books</RouterLink>
                </li>
              </ul>
            </div>
          </div>
          <div class="card-body">
            <p class="card-text">{{ sectionData.description }}</p>
          </div>
        </div>
      </div>

      <!-- Card for Other Roles -->
      <div v-else class="row">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">{{ sectionData.section_name }}</h5>
            <div class="btn-group">
              <ul class="nav nav-pills card-header-pills">
                <li class="nav-item">
                  <RouterLink class="nav-link active" style="background-color: #33a550; color: white;" :to="{ path: '/view_books', query: { sectionId: sectionData.id, sectionName: sectionData.section_name } }">View Books</RouterLink>
                </li>
              </ul>
            </div>
          </div>
          <div class="card-body">
            <p class="card-text">{{ sectionData.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
