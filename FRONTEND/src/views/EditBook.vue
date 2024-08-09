
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { authStore } from '../stores/authStore';
  import { messageStore } from '@/stores/messageStore';
  
  const route = useRoute();
  const router = useRouter();
  const message_store = messageStore();
  const auth_store = authStore();
  
  const editBookData = ref({
    book_name: '',
    content: '',
    authors: '',
    section_name: '',
    section_id: ''
  });
  
  onMounted(() => {
    const bookId = route.query.bookId;
    const bookName = route.query.bookName;
    const content = route.query.content;
    const authors = route.query.authors;
    const sectionName = route.query.sectionName;
    
    editBookData.value = {
      book_name: bookName,
      content: content,
      authors: authors,
      section_name: sectionName,
    };
  });
  
  function editBook() {
    const bookId = route.query.bookId;
    try {
      fetch(`${auth_store.backend_url}/api/v1/edit_book/${bookId}`, {
        method: "PUT",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authentication-Token': auth_store.token
        },
        body: JSON.stringify(editBookData.value)
      }).then(response => {
        if (response.ok) {
          response.json().then(data => {
            message_store.setmessage('Book updated successfully');
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
  function cancelEditing() {
  router.go(-1); // Go back to the previous page
}
  </script>

<template>
  <div class="container mt-4">
    <div class="row">
      <div class="col-12">
        <h2>Edit Book</h2>
        <form @submit.prevent="editBook">
          <div class="mb-3">
            <label for="book_name" class="form-label">Book Name</label>
            <input type="text" class="form-control" v-model="editBookData.book_name">
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Content</label>
            <input type="text" class="form-control" v-model="editBookData.content">
          </div>
          <div class="mb-3">
            <label for="authors" class="form-label">Authors</label>
            <input type="text" class="form-control" v-model="editBookData.authors">
          </div>
          <div class="mb-3">
            <label for="section_name" class="form-label">Section Name</label>
            <input type="text" class="form-control" v-model="editBookData.section_name">
          </div>

          <button type="submit" class="btn btn-primary">Save Changes</button>
          <button type="button" class="btn btn-secondary" @click="cancelEditing">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</template>
  