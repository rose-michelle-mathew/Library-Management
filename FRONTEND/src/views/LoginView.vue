<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';

const router = useRouter();

const email = ref('');
const password = ref('');
const auth_store = authStore();
const message_store = messageStore();

async function onSubmit() {
    const data = {
        email: email.value,
        password: password.value
    };

    try {
        const resp = await auth_store.login(data);
        console.log(resp);
        message_store.setmessage(resp.message);
        if (resp.status) {
            auth_store.updateToken()
            auth_store.updateUserDetails()
            router.push({ path: '/' });
        }
    } catch (error) {
        console.error('An error occurred during login:', error);
    }
}
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-4">
                <div class="card">
                    <div class="card-header text-center">
                        <h2>Login</h2>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <div class="form-group mb-3">
                                <label for="email">Email address</label>
                                <input type="email" class="form-control" id="email" placeholder="Enter email" required v-model="email">
                            </div>
                            <div class="form-group mb-3">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" placeholder="Password" required v-model="password">
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Submit</button>
                        </form>
                    </div>
                    <div class="card-footer text-center">
                        <p>
                            <router-link to="/register">Register if you are a new user</router-link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
