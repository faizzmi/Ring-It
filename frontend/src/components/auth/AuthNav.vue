<template>
    <nav class="glass-nav">
      <div class="nav-inner sov-container">
        <a class="nav-brand" href="/">
          <img src="@/assets/ring-it.png" alt="Ring-It Logo" class="brand-logo-img">
          <div>
            <p class="brand-name t-mono">RING-IT</p>
            <p class="brand-sub t-mono">// vault · v1.0</p>
          </div>
        </a>
        <div class="nav-end">
          <a :href="linkHref" class="sov-nav-link">{{ linkLabel }}</a>
          <a href="/" class="sov-btn sov-btn--ghost sov-btn--sm">← Back to Home</a>
        </div>
      </div>
    </nav>
  </template>
  
  <script setup lang="ts">
  defineProps<{
    linkHref: string
    linkLabel: string
  }>()
  </script>
  
  <style scoped>
  .glass-nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: rgba(8,8,8,.65);
    backdrop-filter: blur(26px) saturate(1.8);
    -webkit-backdrop-filter: blur(26px) saturate(1.8);
    border-bottom: 1px solid var(--glass-bo);
  }
  .nav-inner { height: 60px; display: flex; align-items: center; }
  .nav-brand { display: flex; align-items: center; gap: 9px; flex-shrink: 0; }
  .brand-logo-img {
    width: 32px; height: 32px; object-fit: contain;
    filter: drop-shadow(0 0 8px rgba(255,255,255,0.2));
    margin-right: 10px;
  }
  .brand-name { font-size: 12px; font-weight: 500; letter-spacing: 4px; color: var(--plat); line-height: 1; }
  .brand-sub  { font-size: 9px; letter-spacing: 2px; color: var(--gun); margin-top: 2px; }
  .nav-end { display: none; margin-left: auto; gap: 8px; align-items: center; }
  @media (min-width: 640px) { .nav-end { display: flex; } }
  </style>