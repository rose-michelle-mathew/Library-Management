<script setup>
import { authStore } from '@/stores/authStore';
import { RouterLink } from 'vue-router'
import { useRouter } from 'vue-router';
import { ref } from 'vue';


const auth_store = authStore();
const searchQuery = ref('');
const router = useRouter();

function handleSearch(event) {
  event.preventDefault(); // Prevent the default form submission
  if (searchQuery.value) {
    // Redirect to HomeView with the search query as a query parameter
    router.push({ path: '/', query: { search: searchQuery.value } });
  }
}

function navigateTo(path) {
  router.push(path);
}

</script>
<template>
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand h1 m-0" href="#">Library Management</a>
        
      

            <ul class="nav justify-content-end ">
                <li>

                </li>
                <li class="nav-item" v-if = "!auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/login">Login</RouterLink>
                </li>
                <li class="nav-item" v-if = "!auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/register">Register</RouterLink>
                </li>


                <li class="nav-item" v-if = "auth_store.isAuthenticated">
                    <a class="nav-link">{{auth_store.username}}</a>
                </li>

                <li class="nav-item disabled" v-if = "auth_store.isAuthenticated ">
                    <RouterLink class="nav-link" to="/">Home</RouterLink>
                </li>
                <li class="nav-item" v-if = "auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/search">Search Books</RouterLink>
                </li>
                <li class="nav-item disabled" v-if = "auth_store.isAuthenticated ">
                    <RouterLink class="nav-link" to="/dashboard">Dashboard</RouterLink>
                </li>
                <li class="nav-item disabled" v-if = "auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
                </li>

            </ul>

    </div>
    </nav>
</template>