<template>
    <div class="field-group">
      <label class="check-wrap" @click="$emit('update:modelValue', !modelValue)">
        <span class="custom-check" :class="{ active: modelValue }">
          <svg v-if="modelValue" width="9" height="9" viewBox="0 0 9 9" fill="none">
            <path d="M1.5 4.5L3.5 6.5L7.5 2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
        <span class="t-mono check-text">
          <slot />
        </span>
      </label>
      <span v-if="error" class="field-error t-mono">{{ error }}</span>
    </div>
  </template>
  
  <script setup lang="ts">
  withDefaults(defineProps<{
    modelValue: boolean
    error?: string
  }>(), { error: '' })
  
  defineEmits<{ 'update:modelValue': [value: boolean] }>()
  </script>
  
  <style scoped>
  .field-group { display: flex; flex-direction: column; gap: 6px; }
  
  .check-wrap {
    display: flex; align-items: flex-start; gap: 8px;
    cursor: pointer; user-select: none;
  }
  .check-text { font-size: 10px; letter-spacing: .3px; color: var(--gun); line-height: 1.65; }
  
  .custom-check {
    width: 15px; height: 15px; flex-shrink: 0; margin-top: 1px;
    border: 1px solid rgba(224,224,224,.14); border-radius: 4px;
    background: rgba(8,8,8,.5);
    display: flex; align-items: center; justify-content: center;
    transition: all .18s;
  }
  .custom-check.active { background: var(--ox); border-color: var(--ox); color: white; }
  
  .field-error { font-size: 9px; letter-spacing: .5px; color: #ef5350; padding-left: 2px; }
  </style>