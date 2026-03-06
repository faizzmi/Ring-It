<template>
    <SovModal
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
      :title="title"
      :description="codeLabel"
      tag="// VAULT ERROR"
      variant="error"
      size="sm"
      :closable="true"
    >
      <template #icon>
        <svg width="26" height="26" viewBox="0 0 26 26" fill="none" class="err-icon">
          <circle cx="13" cy="13" r="11" stroke="#ef5350" stroke-width="1.4"/>
          <path d="M13 8v5.5" stroke="#ef5350" stroke-width="1.6" stroke-linecap="round"/>
          <circle cx="13" cy="18" r="1" fill="#ef5350"/>
        </svg>
      </template>
  
      <div class="err-body">
        <p class="err-message t-body">{{ message }}</p>
        <div v-if="hint" class="err-hint t-mono">
          <svg width="9" height="9" viewBox="0 0 9 9" fill="none" style="flex-shrink:0;margin-top:1px">
            <circle cx="4.5" cy="4.5" r="4" stroke="currentColor" stroke-width="1.1"/>
            <path d="M4.5 4v2.5" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>
            <circle cx="4.5" cy="2.8" r=".5" fill="currentColor"/>
          </svg>
          {{ hint }}
        </div>
      </div>
  
      <template #actions>
        <button class="sov-btn sov-btn--ghost" style="justify-content:center" @click="$emit('update:modelValue', false)">
          Try Again
        </button>
      </template>
    </SovModal>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue'
  import SovModal from '@/components/common/SovModal.vue'
  
  const props = defineProps<{
    modelValue: boolean
    message: string
    statusCode?: number
  }>()
  
  defineEmits<{
    (e: 'update:modelValue', value: boolean): void
  }>()
  
  const title = computed(() => {
    switch (props.statusCode) {
      case 409: return 'Already Registered'
      case 401: return 'Auth Failed'
      case 403: return 'Access Denied'
      case 429: return 'Too Many Attempts'
      case 500: return 'Server Error'
      default:  return 'Something Went Wrong'
    }
  })
  
  const codeLabel = computed(() =>
    props.statusCode ? `// HTTP ${props.statusCode}` : '// VAULT ERROR'
  )
  
  const hint = computed(() => {
    switch (props.statusCode) {
      case 409: return 'Try signing in instead, or use a different email address.'
      case 401: return 'Double-check your email and password. Both are case-sensitive.'
      case 429: return 'Too many requests. Wait a moment before trying again.'
      case 500: return 'Our servers encountered an issue. Please try again in a moment.'
      default:  return null
    }
  })
  </script>
  
  <style scoped>
  .err-icon {
    animation: errShake 0.35s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  }
  @keyframes errShake {
    10%, 90% { transform: translate3d(-1px, 0, 0); }
    20%, 80% { transform: translate3d(2px, 0, 0); }
    30%, 50%, 70% { transform: translate3d(-2px, 0, 0); }
    40%, 60% { transform: translate3d(2px, 0, 0); }
  }
  
  .err-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding-top: 4px;
  }
  
  .err-message {
    font-size: 13px;
    color: rgba(224, 224, 224, 0.65);
    text-align: center;
    line-height: 1.7;
    margin: 0;
  }
  
  .err-hint {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    padding: 9px 14px;
    background: rgba(239, 83, 80, 0.06);
    border: 1px solid rgba(239, 83, 80, 0.14);
    border-radius: 8px;
    font-size: 9px;
    letter-spacing: 0.3px;
    color: rgba(239, 83, 80, 0.7);
    text-transform: none;
    line-height: 1.6;
    text-align: left;
  }
  </style>