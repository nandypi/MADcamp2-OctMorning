<template>
    <h1>Login</h1>

    <form @submit.prevent="handleLogin">
        <input type="text" required v-model="username" placeholder="Username" />
        <input type="password" required v-model="password" placeholder="Password" />
        <button type="submit">Login</button>
    </form>
    <p>{{ msg }}</p>

    <RouterLink to="/register">Don't have an account? Register</RouterLink>
    <br>
    <RouterLink to="/">Return to Home</RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref } from 'vue'

const username = ref('user')
const password = ref('password')
const msg = ref('')

async function handleLogin() {
    // alert(`Logging in with username: ${username.value} and password: ${password.value}`)
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                username: username.value,
                password: password.value
            }
        )
    }).then(
        async resp => {
            const data = await resp.json();

            console.log('Response from server:', resp)
            console.log(data)

            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token)
                msg.value = 'Login successful!'
            } else {
                msg.value = `Login failed: ${data.message}`
            }
        }
    ).catch(
        async error => {
            console.error('Error during login:', error)
            msg.value = 'An error occurred during login. Please try again.'
        }
    )
}

</script>