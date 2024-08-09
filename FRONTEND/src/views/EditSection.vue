<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';

const route = useRoute();
const router = useRouter();
const message_store = messageStore();
const auth_store = authStore();

const sectionData = ref({
  section_name: '',
  description: ''
});

onMounted(() => {
  const sectionId = route.query.sectionId;
  fetchSectionData(sectionId);
});

function fetchSectionData(sectionId) {
  fetch(`${auth_store.backend_url}/api/v1/section/${sectionId}`, {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Authentication-Token': auth_store.token
    }
  })
    .then(response => response.json())
    .then(data => {
      sectionData.value = {
        section_name: data.section_name,
        description: data.description
      };
    })
    .catch(error => {
      console.log(error);
    });
}

function editSection() {
  const sectionId = route.query.sectionId;
  fetch(`${auth_store.backend_url}/api/v1/edit_section/${sectionId}`, {
    method: "PUT",
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Authentication-Token': auth_store.token
    },
    body: JSON.stringify(sectionData.value)
  })
    .then(response => {
      if (response.ok) {
        response.json().then(data => {
          message_store.setmessage('Section updated successfully');
          router.push('/'); // Redirect to another page after editing
        });
      } else {
        response.json().then(data => {
          console.log(data);
          message_store.setmessage(data.message);
        });
      }
    })
    .catch(error => {
      console.log(error);
    });
}

function cancelEditing() {
  router.push('/'); // Redirect to another page without saving changes
}
</script>

<template>
  <div class="container mt-4">
    <div class="row">
      <div class="col-12">
        <h2>Edit Section</h2>
        <form @submit.prevent="editSection">
          <div class="mb-3">
            <label for="section_name" class="form-label">Section Name</label>
            <input type="text" class="form-control" v-model="sectionData.section_name" id="section_name">
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea class="form-control" v-model="sectionData.description" id="description"></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Save Changes</button>
            <button type="button" class="btn btn-secondary ms-2" @click="cancelEditing">Cancel</button>

        </form>
      </div>
    </div>
  </div>
</template>
