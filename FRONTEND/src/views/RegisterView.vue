<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authStore } from '../stores/authStore';
import { messageStore } from '@/stores/messageStore';

const router = useRouter();

const username = ref('');
const email = ref('');
const address = ref('');
const password = ref('');
const confirm_password = ref('');
const error_message = ref('');

const auth_store = authStore();
const message_store = messageStore();

async function onSubmit() {
    error_message.value = '';

    if (!username.value || !email.value || !address.value || !password.value || !confirm_password.value) {
        error_message.value = 'All fields are required.';
        return;
    }

    if (password.value !== confirm_password.value) {
        error_message.value = 'Passwords do not match.';
        return;
    }

    const data = {
        username: username.value,
        confirm_password: confirm_password.value,
        address: address.value,
        email: email.value,
        password: password.value,
        role: "user"
    };

    try {
        const resp = await auth_store.register(data);
        console.log(resp);
        message_store.setmessage(resp.message);
        if (resp.status) {
            router.push({ path: '/' });
        }
    } catch (error) {
        console.error('An error occurred during registration:', error);
    }
}
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header text-center">
                        <h2>Register</h2>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="onSubmit">
                            <div class="form-group mb-3">
                                <label for="username">Username</label>
                                <input type="text" id="username" class="form-control" required v-model="username">
                            </div>
                            <div class="form-group mb-3">
                                <label for="address">Address</label>
                                <input type="text" id="address" class="form-control" required v-model="address">
                            </div>
                            <div class="form-group mb-3">
                                <label for="email">Email</label>
                                <input type="email" id="email" class="form-control" required v-model="email">
                            </div>
                            <div class="form-group mb-3">
                                <label for="password">Password</label>
                                <input type="password" id="password" class="form-control" required v-model="password">
                            </div>
                            <div class="form-group mb-3">
                                <label for="confirm_password">Confirm Password</label>
                                <input type="password" id="confirm_password" class="form-control" required v-model="confirm_password">
                            </div>
                            <div v-if="error_message" class="alert alert-danger" role="alert">
                                {{ error_message }}
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Register</button>
                        </form>
                    </div>
                    <div class="card-footer text-center">
                        <p>
                            <router-link to="/login">Login if you are an existing user</router-link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
