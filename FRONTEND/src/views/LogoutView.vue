<script setup>
import { RouterLink, useRoute} from 'vue-router'
import {ref } from 'vue';
import {authStore} from '../stores/authStore';
import {messageStore} from '@/stores/messageStore';
import { useRouter } from 'vue-router';


const router = useRouter();

const auth_store = authStore();
const message_store = messageStore();

auth_store.logout().then(
    (resp)=>{
        message_store.setmessage(resp.message)
        console.log(resp)
        if (resp.status){
            router.push({path: '/'})
        }
    }
)
</script>
