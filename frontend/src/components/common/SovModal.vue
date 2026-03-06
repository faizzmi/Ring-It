<template>
    <Teleport to="body">
      <Transition name="sov-modal">
        <div
          v-if="modelValue"
          class="sov-modal-backdrop"
          @click.self="onBackdropClick"
          role="dialog"
          :aria-modal="true"
          :aria-labelledby="titleId"
        >
          <div
            class="sov-modal-shell"
            :class="[`sov-modal-shell--${variant}`, `sov-modal-shell--${size}`]"
            ref="shellRef"
          >
            <!-- Top accent bar -->
            <div class="sov-modal-bar" :class="`sov-modal-bar--${variant}`" />
  
            <!-- Header -->
            <div class="sov-modal-header">
              <div class="sov-modal-header-left">
                <span class="sov-modal-dot" :class="`sov-modal-dot--${variant}`" />
                <span class="t-mono sov-modal-tag">{{ tag }}</span>
              </div>
              <button
                v-if="closable"
                class="sov-modal-close"
                @click="$emit('update:modelValue', false)"
                aria-label="Close"
              >
                <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                  <path d="M1 1l9 9M10 1L1 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
  
            <!-- Icon area -->
            <div v-if="$slots.icon" class="sov-modal-icon-wrap" :class="`sov-modal-icon-wrap--${variant}`">
              <slot name="icon" />
            </div>
  
            <!-- Content -->
            <div class="sov-modal-body">
              <h3 :id="titleId" class="sov-modal-title t-display">{{ title }}</h3>
              <p class="sov-modal-desc t-mono">{{ description }}</p>
              <slot />
            </div>
  
            <!-- Actions -->
            <div v-if="$slots.actions" class="sov-modal-actions">
              <slot name="actions" />
            </div>
  
            <!-- Footer note -->
            <div v-if="$slots.footer" class="sov-modal-footer">
              <slot name="footer" />
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, watch, nextTick } from 'vue'
  
  const props = withDefaults(defineProps<{
    modelValue: boolean
    title: string
    description?: string
    tag?: string
    variant?: 'success' | 'error' | 'warning' | 'info' | 'default'
    size?: 'sm' | 'md' | 'lg'
    closable?: boolean
    persistent?: boolean   // if true, backdrop click doesn't close
  }>(), {
    description: '',
    tag: '// VAULT',
    variant: 'default',
    size: 'md',
    closable: true,
    persistent: false,
  })
  
  const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'close'): void
  }>()
  
  const shellRef = ref<HTMLElement | null>(null)
  const titleId = computed(() => `sov-modal-title-${Math.random().toString(36).slice(2)}`)
  
  function onBackdropClick() {
    if (!props.persistent) {
      emit('update:modelValue', false)
      emit('close')
    }
  }
  
  // Trap focus + lock body scroll when open
  watch(() => props.modelValue, async (open) => {
    if (open) {
      document.body.style.overflow = 'hidden'
      await nextTick()
      shellRef.value?.focus()
    } else {
      document.body.style.overflow = ''
    }
  })
  </script>
  
  <style scoped>
  /* ── Backdrop ── */
  .sov-modal-backdrop {
    position: fixed;
    inset: 0;
    z-index: 9000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(8, 8, 8, 0.82);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
  }
  
  /* ── Shell ── */
  .sov-modal-shell {
    position: relative;
    background: var(--color-iron, #121214);
    border: 1px solid rgba(224, 224, 224, 0.09);
    border-radius: 14px;
    overflow: hidden;
    outline: none;
    box-shadow:
      0 0 0 1px rgba(255, 255, 255, 0.04) inset,
      0 32px 80px rgba(0, 0, 0, 0.7),
      0 0 60px rgba(0, 0, 0, 0.4);
  }
  
  /* Size variants */
  .sov-modal-shell--sm { width: 100%; max-width: 380px; }
  .sov-modal-shell--md { width: 100%; max-width: 460px; }
  .sov-modal-shell--lg { width: 100%; max-width: 580px; }
  
  /* Color variants — border accent */
  .sov-modal-shell--success { border-color: rgba(76, 175, 80, 0.2); }
  .sov-modal-shell--error   { border-color: rgba(176, 0, 32, 0.25); }
  .sov-modal-shell--warning { border-color: rgba(251, 140, 0, 0.2); }
  .sov-modal-shell--info    { border-color: rgba(33, 150, 243, 0.2); }
  
  /* ── Top accent bar ── */
  .sov-modal-bar { height: 2px; width: 100%; }
  .sov-modal-bar--default { background: linear-gradient(90deg, rgba(128,0,32,0.6), rgba(128,0,32,0.1)); }
  .sov-modal-bar--success { background: linear-gradient(90deg, rgba(76,175,80,0.8), rgba(76,175,80,0.1)); }
  .sov-modal-bar--error   { background: linear-gradient(90deg, rgba(176,0,32,0.8), rgba(176,0,32,0.1)); }
  .sov-modal-bar--warning { background: linear-gradient(90deg, rgba(251,140,0,0.8), rgba(251,140,0,0.1)); }
  .sov-modal-bar--info    { background: linear-gradient(90deg, rgba(33,150,243,0.8), rgba(33,150,243,0.1)); }
  
  /* ── Header ── */
  .sov-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px 0;
  }
  .sov-modal-header-left {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .sov-modal-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .sov-modal-dot--default { background: var(--color-ox, #800020); box-shadow: 0 0 6px rgba(128,0,32,0.9); }
  .sov-modal-dot--success { background: var(--color-grn, #4CAF50); box-shadow: 0 0 6px rgba(76,175,80,0.9); }
  .sov-modal-dot--error   { background: #ef5350; box-shadow: 0 0 6px rgba(239,83,80,0.8); }
  .sov-modal-dot--warning { background: var(--color-amb, #FB8C00); box-shadow: 0 0 6px rgba(251,140,0,0.8); }
  .sov-modal-dot--info    { background: #2196F3; box-shadow: 0 0 6px rgba(33,150,243,0.8); }
  .sov-modal-tag {
    font-size: 8.5px;
    letter-spacing: 2.5px;
    color: var(--color-gun, #757575);
    text-transform: uppercase;
  }
  .sov-modal-close {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-gun, #757575);
    background: rgba(224, 224, 224, 0.04);
    border: 1px solid rgba(224, 224, 224, 0.08);
    transition: all 0.18s;
    cursor: pointer;
  }
  .sov-modal-close:hover {
    color: var(--color-plat, #E0E0E0);
    background: rgba(224, 224, 224, 0.09);
  }
  
  /* ── Icon area ── */
  .sov-modal-icon-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 24px auto 0;
    width: 64px;
    height: 64px;
    border-radius: 50%;
  }
  .sov-modal-icon-wrap--success { background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.2); }
  .sov-modal-icon-wrap--error   { background: rgba(176,0,32,0.1);  border: 1px solid rgba(176,0,32,0.22); }
  .sov-modal-icon-wrap--warning { background: rgba(251,140,0,0.08); border: 1px solid rgba(251,140,0,0.2); }
  .sov-modal-icon-wrap--info    { background: rgba(33,150,243,0.08); border: 1px solid rgba(33,150,243,0.2); }
  .sov-modal-icon-wrap--default { background: rgba(128,0,32,0.1); border: 1px solid rgba(128,0,32,0.22); }
  
  /* ── Body ── */
  .sov-modal-body {
    padding: 20px 28px 24px;
    text-align: center;
  }
  .sov-modal-title {
    font-size: 1.35rem;
    margin-bottom: 8px;
    color: var(--color-plat, #E0E0E0);
  }
  .sov-modal-desc {
    font-size: 9px;
    letter-spacing: 1.5px;
    color: var(--color-gun, #757575);
    margin-bottom: 0;
    text-transform: uppercase;
  }
  
  /* ── Actions ── */
  .sov-modal-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0 28px 24px;
  }
  
  /* ── Footer ── */
  .sov-modal-footer {
    padding: 14px 28px 20px;
    border-top: 1px solid rgba(224, 224, 224, 0.06);
    text-align: center;
  }
  
  /* ── Transition ── */
  .sov-modal-enter-active,
  .sov-modal-leave-active {
    transition: opacity 0.22s ease;
  }
  .sov-modal-enter-active .sov-modal-shell,
  .sov-modal-leave-active .sov-modal-shell {
    transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.22s ease;
  }
  .sov-modal-enter-from,
  .sov-modal-leave-to {
    opacity: 0;
  }
  .sov-modal-enter-from .sov-modal-shell {
    transform: translateY(18px) scale(0.97);
    opacity: 0;
  }
  .sov-modal-leave-to .sov-modal-shell {
    transform: translateY(8px) scale(0.98);
    opacity: 0;
  }
  </style>