<template>
    <div v-if="message" class="sov-nudge sov-nudge--warn">
      <span>⚠</span>
      <span class="t-mono">{{ message }}</span>
    </div>
  </template>
  
  <script setup lang="ts">
  withDefaults(defineProps<{ message: string | null }>(), { message: null })
  </script>