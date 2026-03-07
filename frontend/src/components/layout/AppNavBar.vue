<template>
    <!-- ── Mobile: floating pill (< 860px) ── -->
    <nav class="mobile-nav" role="navigation" aria-label="Main navigation">
      <div class="mobile-pill">
        <RouterLink
          v-for="(item, index) in navItems"
          :key="item.path"
          :to="item.path"
          class="mobile-item"
          :class="{
            'mobile-item--active': isActive(item.path),
            'mobile-item--center': index === centerIndex,
          }"
          :aria-label="item.label"
        >
          <template v-if="index === centerIndex">
            <div class="mobile-fab">
              <span v-html="item.icon" />
            </div>
          </template>
          <template v-else>
            <div class="mobile-icon-wrap">
              <span class="mobile-icon" v-html="item.icon" />
              <Transition name="dot">
                <span v-if="isActive(item.path)" class="mobile-dot" />
              </Transition>
            </div>
            <span class="mobile-label t-mono">{{ item.label }}</span>
          </template>
        </RouterLink>
      </div>
    </nav>
  
    <!-- ── Desktop: left sidebar rail (≥ 860px) ── -->
    <aside class="desktop-rail" :class="{ 'desktop-rail--expanded': expanded }">
  
      <!-- Logo -->
      <div class="rail-logo" @click="expanded = !expanded">
        <div class="rail-logo-mark">
          <span class="rail-logo-r">R</span>
        </div>
        <Transition name="label-slide">
          <span v-if="expanded" class="rail-logo-name t-display">Ring-It</span>
        </Transition>
      </div>
  
      <!-- Nav links -->
      <nav class="rail-nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="rail-item"
          :class="{ 'rail-item--active': isActive(item.path) }"
          :title="!expanded ? item.label : undefined"
        >
          <span class="rail-icon" v-html="item.icon" />
          <Transition name="label-slide">
            <span v-if="expanded" class="rail-label t-mono">{{ item.label }}</span>
          </Transition>
          <Transition name="dot">
            <span v-if="isActive(item.path) && !expanded" class="rail-active-pip" />
          </Transition>
        </RouterLink>
      </nav>
  
      <!-- Bottom: user + logout -->
      <div class="rail-footer">
        <div class="rail-user" :title="!expanded ? (user?.full_name || 'Account') : undefined">
          <div class="rail-avatar t-mono">{{ userInitial }}</div>
          <Transition name="label-slide">
            <div v-if="expanded" class="rail-user-info">
              <span class="rail-user-name t-mono">{{ user?.full_name?.split(' ')[0] || 'Vault' }}</span>
              <span class="rail-user-status t-mono" :class="user?.is_verified ? 'status--green' : 'status--amber'">
                {{ user?.is_verified ? '✓ verified' : '⚡ unverified' }}
              </span>
            </div>
          </Transition>
        </div>
        <button class="rail-logout" @click="handleLogout" title="Logout">
          <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
            <path d="M5.5 2.5H3a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h2.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
            <path d="M10 10l3.5-2.5L10 5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13.5 7.5H6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </aside>
  </template>
  
  <script setup lang="ts">
  import { ref, computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useAuth } from '@/composables/useAuth'
  
  const route  = useRoute()
  const router = useRouter()
  const { user, logout } = useAuth()
  
  const expanded    = ref(false)
  const centerIndex = 2
  
  const userInitial = computed(() => {
    const name = user.value?.full_name || ''
    return name.split(' ').map((w: string) => w[0]).slice(0, 2).join('').toUpperCase() || 'V'
  })
  
  function isActive(path: string) {
    if (path === '/dashboard') return route.path === '/dashboard'
    return route.path.startsWith(path.split('?')[0] ?? path)
  }
  
  async function handleLogout() {
    await logout()
    router.push('/login')
  }
  
  const navItems = [
    {
      path: '/dashboard',
      label: 'Vault',
      icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect x="2" y="2" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.4"/>
        <rect x="11" y="2" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.4"/>
        <rect x="2" y="11" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.4"/>
        <rect x="11" y="11" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.4"/>
      </svg>`,
    },
    {
      path: '/dashboard/budget',
      label: 'Budget',
      icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.4"/>
        <path d="M10 5.5v9M7.5 7.5c0-1.1 1.12-2 2.5-2s2.5.9 2.5 2-1.12 1.9-2.5 2.2-2.5 1-2.5 2.1 1.12 2 2.5 2 2.5-.9 2.5-2" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
      </svg>`,
    },
    {
      path: '/dashboard/transactions?new=1',
      label: 'Add',
      icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>`,
    },
    {
      path: '/dashboard/goals',
      label: 'Goals',
      icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.4"/>
        <circle cx="10" cy="10" r="3.5" stroke="currentColor" stroke-width="1.4"/>
        <path d="M10 2v2M10 16v2M2 10h2M16 10h2" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/>
      </svg>`,
    },
    {
      path: '/dashboard/settings',
      label: 'Profile',
      icon: `<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.4"/>
        <path d="M3 18c0-3.87 3.13-7 7-7s7 3.13 7 7" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
      </svg>`,
    },
  ]
  </script>
  
  <style scoped>
  /* ════════════════════════════════
     MOBILE: floating pill bottom nav
     visible only below 860px
  ════════════════════════════════ */
  .mobile-nav {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 200;
    padding: 0 14px;
    padding-bottom: max(18px, env(safe-area-inset-bottom));
    pointer-events: none;
  }
  @media (min-width: 860px) { .mobile-nav { display: none; } }
  
  .mobile-pill {
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: rgba(12, 12, 14, 0.82);
    backdrop-filter: blur(32px) saturate(2);
    -webkit-backdrop-filter: blur(32px) saturate(2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    padding: 10px 6px;
    pointer-events: all;
    box-shadow:
      0 10px 50px rgba(0,0,0,0.65),
      0 2px 12px rgba(0,0,0,0.4),
      0 0 0 0.5px rgba(255,255,255,0.05) inset,
      0 1px 0 rgba(255,255,255,0.1) inset;
  }
  
  .mobile-item {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 3px; flex: 1; padding: 4px 0;
    color: rgba(117,117,117,0.75);
    text-decoration: none;
    transition: color 0.2s cubic-bezier(0.22,1,0.36,1);
    -webkit-tap-highlight-color: transparent;
  }
  .mobile-item--active { color: rgba(224,224,224,0.95); }
  
  .mobile-icon-wrap {
    position: relative; width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
  }
  .mobile-icon {
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.22s cubic-bezier(0.22,1,0.36,1);
  }
  .mobile-item--active .mobile-icon { transform: scale(1.1); }
  .mobile-item--active .mobile-icon :deep(path),
  .mobile-item--active .mobile-icon :deep(rect),
  .mobile-item--active .mobile-icon :deep(circle) { stroke: var(--ox, #800020); }
  
  .mobile-dot {
    position: absolute; bottom: -5px; left: 50%;
    transform: translateX(-50%);
    width: 4px; height: 4px; border-radius: 50%;
    background: var(--ox, #800020);
    box-shadow: 0 0 7px rgba(128,0,32,0.95);
  }
  .mobile-label { font-size: 8.5px; letter-spacing: 0.8px; text-transform: uppercase; }
  
  .mobile-item--center { flex: 0 0 auto; width: 60px; }
  .mobile-fab {
    width: 50px; height: 50px; border-radius: 17px;
    background: linear-gradient(150deg, rgba(170,10,45,0.96), rgba(90,0,18,0.94));
    border: 1px solid rgba(180,20,50,0.45);
    display: flex; align-items: center; justify-content: center;
    color: rgba(224,224,224,0.95);
    margin-top: -10px;
    box-shadow:
      0 8px 28px rgba(128,0,32,0.55),
      0 3px 10px rgba(0,0,0,0.5),
      0 0 0 1px rgba(255,255,255,0.08) inset,
      0 1px 0 rgba(255,255,255,0.18) inset;
    transition: all 0.22s cubic-bezier(0.22,1,0.36,1);
  }
  .mobile-item--center:active .mobile-fab { transform: scale(0.94); }
  
  /* ════════════════════════════════
     DESKTOP: left sidebar rail
     visible only at 860px+
  ════════════════════════════════ */
  .desktop-rail {
    display: none;
  }
  @media (min-width: 860px) {
    .desktop-rail {
      display: flex;
      flex-direction: column;
      position: fixed;
      left: 0; top: 0; bottom: 0;
      width: 68px;
      background: rgba(10, 10, 12, 0.96);
      border-right: 1px solid rgba(255,255,255,0.06);
      z-index: 200;
      transition: width 0.3s cubic-bezier(0.22,1,0.36,1);
      overflow: hidden;
    }
    .desktop-rail--expanded { width: 210px; }
  }
  
  /* Logo */
  .rail-logo {
    display: flex; align-items: center; gap: 12px;
    padding: 18px 18px 14px;
    cursor: pointer;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    min-height: 64px; flex-shrink: 0;
    overflow: hidden;
  }
  .rail-logo-mark {
    width: 30px; height: 30px; border-radius: 9px;
    background: rgba(128,0,32,0.9);
    border: 1px solid rgba(180,20,50,0.5);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 0 14px rgba(128,0,32,0.4);
  }
  .rail-logo-r {
    font-family: var(--display, 'Syne', sans-serif);
    font-size: 14px; font-weight: 800;
    color: rgba(224,224,224,0.95); line-height: 1;
  }
  .rail-logo-name {
    font-size: 1rem; color: var(--plat, #E0E0E0);
    letter-spacing: -0.02em; white-space: nowrap;
  }
  
  /* Nav */
  .rail-nav {
    flex: 1; display: flex; flex-direction: column;
    gap: 2px; padding: 10px 8px;
    overflow-y: auto; overflow-x: hidden;
  }
  .rail-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px; border-radius: 12px;
    color: var(--gun, #757575);
    text-decoration: none;
    transition: all 0.18s;
    position: relative;
    border: 1px solid transparent;
    min-height: 44px; white-space: nowrap;
    overflow: hidden;
  }
  .rail-item:hover {
    background: rgba(224,224,224,0.05);
    color: rgba(224,224,224,0.75);
  }
  .rail-item--active {
    background: rgba(128,0,32,0.12);
    color: rgba(224,224,224,0.92);
    border-color: rgba(128,0,32,0.22);
  }
  .rail-item--active .rail-icon :deep(path),
  .rail-item--active .rail-icon :deep(rect),
  .rail-item--active .rail-icon :deep(circle) { stroke: var(--ox, #800020); }
  
  .rail-icon {
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }
  .rail-label { font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase; }
  
  /* Active pip when collapsed */
  .rail-active-pip {
    position: absolute; right: 8px; top: 50%;
    transform: translateY(-50%);
    width: 4px; height: 4px; border-radius: 50%;
    background: var(--ox, #800020);
    box-shadow: 0 0 6px rgba(128,0,32,0.9);
  }
  
  /* Footer */
  .rail-footer {
    padding: 10px 10px 16px;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex; align-items: center; justify-content: space-between;
    gap: 8px; min-height: 64px;
  }
  .rail-user { display: flex; align-items: center; gap: 10px; overflow: hidden; min-width: 0; }
  .rail-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    background: rgba(128,0,32,0.15);
    border: 1px solid rgba(128,0,32,0.35);
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; color: rgba(224,224,224,0.7);
    flex-shrink: 0;
  }
  .rail-user-info { display: flex; flex-direction: column; gap: 1px; overflow: hidden; }
  .rail-user-name {
    font-size: 10px; letter-spacing: 0.5px; color: rgba(224,224,224,0.7);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .rail-user-status { font-size: 8px; letter-spacing: 0.5px; }
  .status--green { color: var(--grn, #4CAF50); }
  .status--amber { color: var(--amb, #FB8C00); }
  
  .rail-logout {
    width: 32px; height: 32px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px; color: var(--gun, #757575);
    background: rgba(224,224,224,0.04);
    border: 1px solid rgba(224,224,224,0.07);
    cursor: pointer; transition: all 0.18s;
  }
  .rail-logout:hover { color: #ef5350; background: rgba(239,83,80,0.08); border-color: rgba(239,83,80,0.2); }
  
  /* Transitions */
  .label-slide-enter-active, .label-slide-leave-active { transition: opacity 0.18s, transform 0.2s; }
  .label-slide-enter-from, .label-slide-leave-to { opacity: 0; transform: translateX(-8px); }
  .dot-enter-active, .dot-leave-active { transition: opacity 0.2s, transform 0.2s; }
  .dot-enter-from, .dot-leave-to { opacity: 0; transform: translateX(-50%) scale(0); }
  </style>