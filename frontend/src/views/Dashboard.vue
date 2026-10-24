<template>
    <h1>Dashboard</h1>

    <button @click="LoadItems">Load Items</button>

    <ul>
        <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
</template>

<script setup>
import { ref } from 'vue'

const items = ref([])

async function LoadItems() {
    // alert(`Logging in with username: ${username.value} and password: ${password.value}`)
    fetch('http://127.0.0.1:5000/items', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // 'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    }).then(
        async resp => {
            const data = await resp.json();
            if (resp.ok) {
                items.value = data
            } else {
                console.error('Failed to load items:', data.message)
                if (resp.status === 401) {
                    alert('Unauthorized access. Please log in.')
                    // Redirect to login page
                    window.location.href = '/login'
                }
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