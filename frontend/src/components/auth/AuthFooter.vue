<template>
    <div class="auth-page-footer t-mono">
      <span>© 2026 Sontiqo &amp; Co · MIT License</span>
      <div style="display:flex;gap:18px">
        <a href="/privacy" class="auth-link">Privacy</a>
        <a href="/terms" class="auth-link">Terms</a>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  // No props — static content
  </script>
  
  <style scoped>
  .auth-page-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 32px;
    border-top: 1px solid var(--glass-bo);
    font-size: 10px;
    color: rgba(117,117,117,.4);
    letter-spacing: 1px;
  }
  .auth-link {
    font-size: inherit;
    letter-spacing: .5px;
    color: var(--ox);
    transition: color .18s;
  }
  .auth-link:hover { color: rgba(200,50,80,.9); }
  </style>