<template>
    <div class="field-group">
      <label class="field-label t-label" :for="id">{{ label }}</label>
      <div class="field-wrap" :class="{ 'field-wrap--error': error, 'field-wrap--focus': isFocused }">
  
        <!-- Leading icon slot -->
        <span class="field-icon">
          <slot name="icon" />
        </span>
  
        <!-- Input or Select -->
        <select
          v-if="type === 'select'"
          :id="id"
          :value="modelValue"
          class="field-input field-select t-mono"
          @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
          @focus="isFocused = true"
          @blur="isFocused = false; $emit('blur')"
        >
          <slot name="options" />
        </select>
  
        <input
          v-else
          :id="id"
          :type="inputType"
          :value="modelValue"
          :placeholder="placeholder"
          :autocomplete="autocomplete"
          class="field-input t-mono"
          @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
          @focus="isFocused = true"
          @blur="isFocused = false; $emit('blur')"
        />
  
        <!-- Trailing toggle slot (e.g. password visibility) -->
        <slot name="toggle" />
      </div>
      <span v-if="error" class="field-error t-mono">{{ error }}</span>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from 'vue'
  
  const props = withDefaults(defineProps<{
    id: string
    label: string
    modelValue: string
    type?: string
    placeholder?: string
    autocomplete?: string
    error?: string
    showValue?: boolean   // for password toggle — parent passes true/false
  }>(), {
    type: 'text',
    placeholder: '',
    autocomplete: 'off',
    error: '',
    showValue: false,
  })
  
  defineEmits<{
    'update:modelValue': [value: string]
    'blur': []
  }>()
  
  const isFocused = ref(false)
  
  // If type is 'password', parent controls visibility via showValue prop
  const inputType = computed(() => {
    if (props.type === 'password') return props.showValue ? 'text' : 'password'
    return props.type
  })
  </script>
  
  <style scoped>
  .field-group { display: flex; flex-direction: column; gap: 6px; }
  .field-label { display: block; }
  
  .field-wrap {
    position: relative; display: flex; align-items: center;
    background: rgba(8,8,8,.5);
    border: 1px solid rgba(224,224,224,.08);
    border-radius: var(--r-sm);
    transition: border-color .2s, box-shadow .2s;
  }
  .field-wrap--focus {
    border-color: rgba(128,0,32,.5);
    box-shadow: 0 0 0 3px rgba(128,0,32,.08);
  }
  .field-wrap--error { border-color: rgba(176,0,32,.4); }
  
  .field-icon {
    display: flex; align-items: center; justify-content: center;
    padding: 0 12px; color: var(--gun); flex-shrink: 0;
  }
  
  .field-input {
    flex: 1; background: transparent; border: none; outline: none;
    color: var(--plat); font-size: 12px; letter-spacing: .5px;
    padding: 11px 0; min-width: 0;
  }
  .field-input::placeholder { color: rgba(117,117,117,.35); }
  
  .field-select { cursor: pointer; appearance: none; padding-right: 12px; }
  .field-select option { background: #121214; color: var(--plat); }
  
  .field-error { font-size: 9px; letter-spacing: .5px; color: #ef5350; padding-left: 2px; }
  </style>