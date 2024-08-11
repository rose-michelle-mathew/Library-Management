<script setup>
import { RouterLink } from 'vue-router';
import { authStore } from '../stores/authStore';
import { defineProps, ref, onMounted } from 'vue'; 

import { messageStore } from '@/stores/messageStore';
const auth_store = authStore();

const message_store = messageStore();

import  Sections  from '../components/Sections.vue';

const all_sections = ref([]);
onMounted(()=>{
  fetch_sections();
})

function fetch_sections(){
  try{
    fetch(`${auth_store.backend_url}/api/v1/get_all_sections`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    }).then(
      (response) => {
        if (!response.ok){
          const data =  response.json()
          const rsp = {
              'status': false,
              'message': data.message
          }
          return rsp
        }
        else {
          return response.json()
        }
      }
    ).then(
      (data) => {
        if (data.status === false){
          messageStore.addMessage(data.message, 'danger')
          return
        }
        all_sections.value = data;
        console.log('From Home component');
        console.log(all_sections.value);
      }
    )
  }
  catch(error){
    console.log(error);
  }
}


</script>


<template>
  <div >
    <div v-if="auth_store.isAuthenticated">
      <Sections v-for="section in all_sections" :key="section.id" :id="section.id" />
      
      <div v-if="auth_store.role === 'librarian'" class="row mt-4">
        <div class="col-12 text-center">
          <RouterLink to="/add_section">
            <button type="button" class="btn btn-primary">Add Section</button>
          </RouterLink>
        </div>
      </div>
    </div>
    
    <div class="landing-page" v-else>
      <div class="row justify-content-center">
        <div class="col-md-8 text-center">
          <h1 class="display-4" style="color: white;  margin-left: 44px; margin-right: 50px; margin-top: 300px;">Welcome to our Library!</h1>
<p class="lead" style="color: white; ">Browse through our Best Collections!</p>
<RouterLink class="btn btn-outline-dark btn-lg mt-3" style=" margin-left: 40px; color: white; border-color: white;" to="/login">Start Reading</RouterLink>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.landing-page {
  background-image: url('/home/michelle/IITM/MAD2_proj/FRONTEND/src/assets/photo-1481627834876-b7833e8f5570.avif'); /* Adjust the path to your image */
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  color: white;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

</style>
