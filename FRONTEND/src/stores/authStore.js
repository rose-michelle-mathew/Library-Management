import {defineStore} from 'pinia'
import {computed, ref} from 'vue';

// computed and ref are vue functions used to create reactive states

export const authStore = defineStore('authStore', () => { // creates a new pinia store with name authStore
    const backend_url ="http://127.0.0.1:5000"
    const token = ref(localStorage.getItem('token'))
    const user_details = ref(localStorage.getItem('user_details'))
    const isAuthenticated = ref(computed(() => token.value != null))
    const username = computed(() => JSON.parse(user_details.value).username)
    const role = computed(()=>JSON.parse(user_details.value).role)

    function updateToken()
    {
        token.value=localStorage.getItem('token')
    }

    function updateUserDetails()
    {
        user_details.value = localStorage.getItem('user_details')
    }
    function setToken(token){
        localStorage.setItem('token',token)
    }

    function removeToken()
    {
        localStorage.removeItem('token')
        token.value = null;
    }

    function removeuserDetails()
    {
        localStorage.removeItem('user_details')
        user_details.value=null;

    }

    function setuserDetails(user_dets)
    {
        localStorage.setItem('user_details',user_dets)
    }

    async function logout()
    {
        try{
            const response = await fetch(`${backend_url}/api/v1/logout`,{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*',
                    'Authentication-Token':token.value
                }
            })

            if (!response.ok)
            {
                const data = await response.json()
                const resp = {
                'status':false,
                'message':data.message
            }
        
            return resp
            }

            else{
                const data = await response.json()
                const resp = {
                    'status':true,
                    'message':data.message
                }
                    removeToken()
                    removeuserDetails()
            return resp
            }
        }
        
        catch(error){
            console.error(error)
            const resp = {
                'status':false,
                'message':'Oops something went worng'
            }
            return resp
        }

    }

    async function login(user_details)
    {
        console.log(user_details)
        try 
        {
            const response = await fetch(`${backend_url}/api/v1/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin':'*'
            },
            body: JSON.stringify(user_details)
        })
        if (!response.ok){
            const data = await response.json()
            const resp = {
                'status':false,
                'message':data.message
            }
        
            return resp
        }
        else{
            const data = await response.json()
            if (data.user.auth_token){
                setToken(data.user.auth_token)
                const user_dets = {
                    'username':data.user.username,
                    'role':data.user.roles[0],
                    'address':data.user.address,
                    'email':data.user.email
                }
                setuserDetails(JSON.stringify(user_dets))
                const resp = {
                    'status':true,
                    'message':data.message
                }
                return resp
            }
        }

            // console.log(await response.json())
        }

        catch(error){
            console.error(error)
            const resp = {
                'status':true,
                'message':'Oops something went worng'
            }
            return resp
        }

        return true 
    }

    async function register(user_details)
    {
            console.log(user_details)
            try 
            {
                const response = await fetch(`${backend_url}/api/v1/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin':'*'
                },
                body: JSON.stringify(user_details)
            })
            if (!response.ok){
                const data = await response.json()
                const resp = {
                    'status':false,
                    'message':data.message
                }
            
                return resp
            }
            else{
                const data = await response.json()
                    const resp = {
                        'status':true,
                        'message':data.message
                    }
                    return resp
                }
    
                // console.log(await response.json())
            }
    
            catch(error){
                console.error(error)
                const resp = {
                    'status':true,
                    'message':'Oops something went worng'
                }
                return resp
            }
        }

    return {login,logout,register,token,username,isAuthenticated, backend_url,role, updateToken,updateUserDetails};


  });
  