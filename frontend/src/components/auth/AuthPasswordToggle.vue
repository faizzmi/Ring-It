<template>
    <button type="button" class="field-toggle" @click="$emit('toggle')" tabindex="-1">
      <!-- Eye open -->
      <svg v-if="!show" width="13" height="13" viewBox="0 0 13 13" fill="none">
        <ellipse cx="6.5" cy="6.5" rx="5.5" ry="3.5" stroke="currentColor" stroke-width="1.2"/>
        <circle cx="6.5" cy="6.5" r="1.5" fill="currentColor"/>
      </svg>
      <!-- Eye closed -->
      <svg v-else width="13" height="13" viewBox="0 0 13 13" fill="none">
        <path d="M2 2L11 11M5.5 4.5A3.5 3.5 0 0 1 6.5 4.5c2.76 0 4.5 2 4.5 2s-.6 1.1-1.8 1.8M4 8.5A4.47 4.47 0 0 1 2 6.5S3.74 4.5 6.5 4.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
      </svg>
    </button>
  </template>
  
  <script setup lang="ts">
  defineProps<{ show: boolean }>()
  defineEmits<{ toggle: [] }>()
  </script>
  
  <style scoped>
  .field-toggle {
    display: flex; align-items: center; justify-content: center;
    padding: 0 12px; color: rgba(117,117,117,.5);
    transition: color .18s; flex-shrink: 0;
  }
  .field-toggle:hover { color: var(--gun); }
  </style>