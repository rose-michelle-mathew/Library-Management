import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const messageStore = defineStore('messageStore',()=>{
    const flash_message = ref('')

    function setmessage(message){
        flash_message.value = message
        setTimeout(()=>{flash_message.value=''},10000)
    }

    const message = computed(()=> flash_message.value)

    return { setmessage, flash_message}
})