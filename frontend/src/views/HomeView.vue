<script setup>
// import TheWelcome from '../components/TheWelcome.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
  <main>
    <!-- <TheWelcome /> -->
     <h1>Welcome to MAD2Camp!</h1>
     <p>Please <RouterLink to="/login">Login</RouterLink> or <RouterLink to="/register">Register</RouterLink> to continue.</p>
      <p>To know more, please visit <RouterLink to="/about">About</RouterLink>.</p>
  </main>
</template>
