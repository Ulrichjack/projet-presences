<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
main {
  width: 100%;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}
</style>