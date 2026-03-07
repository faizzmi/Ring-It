<template>
  <!-- ── Desktop: top navbar (≥ 860px) ── -->
  <header class="top-nav" role="banner">
    <div class="top-nav-inner">

      <!-- Logo -->
      <RouterLink to="/dashboard" class="top-logo">
        <div class="top-logo-mark">R</div>
        <span class="top-logo-name">Ring-It</span>
      </RouterLink>

      <!-- Nav links -->
      <nav class="top-links" role="navigation" aria-label="Main navigation">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="top-link"
          :class="{ 'top-link--active': isActive(item.path) }"
        >
          <span class="top-link-icon" v-html="item.icon" />
          <span class="top-link-label">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <!-- Right: user + logout -->
      <div class="top-right">
        <div class="top-user">
          <div class="top-avatar">{{ userInitial }}</div>
          <span class="top-user-name">{{ user?.full_name?.split(' ')[0] || 'Account' }}</span>
        </div>
        <button class="top-logout" @click="handleLogout" title="Sign out">
          <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
            <path d="M5.5 2.5H3a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h2.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            <path d="M10 10l3.5-2.5L10 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13.5 7.5H6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
          <span class="top-logout-label">Sign Out</span>
        </button>
      </div>

    </div>
  </header>

  <!-- ── Mobile: floating pill bottom nav (< 860px) ── -->
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
          <span class="mobile-label">{{ item.label }}</span>
        </template>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const route  = useRoute()
const router = useRouter()
const { user, logout } = useAuth()

const centerIndex = 2

const userInitial = computed(() => {
  const name = user.value?.full_name || ''
  return name.split(' ').map((w: string) => w[0]).slice(0, 2).join('').toUpperCase() || 'A'
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
    icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none">
      <rect x="2" y="2" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.5"/>
      <rect x="11" y="2" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.5"/>
      <rect x="2" y="11" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.5"/>
      <rect x="11" y="11" width="7" height="7" rx="2" stroke="currentColor" stroke-width="1.5"/>
    </svg>`,
  },
  {
    path: '/dashboard/budget',
    label: 'Budget',
    icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none">
      <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/>
      <path d="M10 5.5v9M7.5 7.5c0-1.1 1.12-2 2.5-2s2.5.9 2.5 2-1.12 1.9-2.5 2.2-2.5 1-2.5 2.1 1.12 2 2.5 2 2.5-.9 2.5-2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`,
  },
  {
    path: '/dashboard/transactions?new=1',
    label: 'Add',
    icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none">
      <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
  },
  {
    path: '/dashboard/goals',
    label: 'Goals',
    icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none">
      <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/>
      <circle cx="10" cy="10" r="3.5" stroke="currentColor" stroke-width="1.5"/>
      <path d="M10 2v2M10 16v2M2 10h2M16 10h2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`,
  },
  {
    path: '/dashboard/settings',
    label: 'Profile',
    icon: `<svg width="16" height="16" viewBox="0 0 20 20" fill="none">
      <circle cx="10" cy="7" r="3" stroke="currentColor" stroke-width="1.5"/>
      <path d="M3 18c0-3.87 3.13-7 7-7s7 3.13 7 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    </svg>`,
  },
]
</script>

<style scoped>
/* ── Desktop Top Nav ─────────────────────────────────────── */
.top-nav {
  display: none;
}

@media (min-width: 860px) {
  .top-nav {
    display: block;
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 200;
    padding: 14px 14px 0;
    pointer-events: none;
  }

  .top-nav-inner {
    display: flex;
    align-items: center;
    gap: 8px;
    max-width: 900px;
    margin: 0 auto;
    padding: 0 10px 0 10px;
    height: 52px;
    pointer-events: all;
    /* Same pill treatment as mobile */
    background: rgba(12, 12, 14, 0.82);
    backdrop-filter: blur(32px) saturate(2);
    -webkit-backdrop-filter: blur(32px) saturate(2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    box-shadow:
      0 10px 50px rgba(0,0,0,0.65),
      0 2px 12px rgba(0,0,0,0.4),
      0 0 0 0.5px rgba(255,255,255,0.05) inset,
      0 1px 0 rgba(255,255,255,0.1) inset;
  }
}

/* Logo */
.top-logo {
  display: flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  flex-shrink: 0;
  margin-right: 8px;
}
.top-logo-mark {
  width: 28px; height: 28px;
  border-radius: 8px;
  background: #800020;
  display: flex; align-items: center; justify-content: center;
  font-family: -apple-system, 'SF Pro Display', BlinkMacSystemFont, sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
  letter-spacing: -0.5px;
  flex-shrink: 0;
}
.top-logo-name {
  font-family: -apple-system, 'SF Pro Display', BlinkMacSystemFont, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.88);
  letter-spacing: -0.3px;
  white-space: nowrap;
}

/* Nav links */
.top-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
  justify-content: center;
}

.top-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.4);
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
}
.top-link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.75);
}
.top-link--active {
  background: rgba(128, 0, 32, 0.14);
  color: rgba(255, 255, 255, 0.9);
}
.top-link--active .top-link-icon :deep(path),
.top-link--active .top-link-icon :deep(rect),
.top-link--active .top-link-icon :deep(circle) {
  stroke: #800020;
}

.top-link-icon {
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.top-link-label {
  font-family: -apple-system, 'SF Pro Text', BlinkMacSystemFont, sans-serif;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.1px;
}

/* Right side */
.top-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  margin-left: 8px;
}

.top-user {
  display: flex;
  align-items: center;
  gap: 8px;
}
.top-avatar {
  width: 28px; height: 28px;
  border-radius: 50%;
  background: rgba(128, 0, 32, 0.15);
  border: 0.5px solid rgba(128, 0, 32, 0.4);
  display: flex; align-items: center; justify-content: center;
  font-family: -apple-system, 'SF Pro Text', BlinkMacSystemFont, sans-serif;
  font-size: 10px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
  letter-spacing: 0.3px;
}
.top-user-name {
  font-family: -apple-system, 'SF Pro Text', BlinkMacSystemFont, sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.55);
  letter-spacing: -0.1px;
}

.top-logout {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 8px;
  background: transparent;
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.top-logout:hover {
  background: rgba(255, 59, 48, 0.1);
  border-color: rgba(255, 59, 48, 0.3);
  color: #FF3B30;
}
.top-logout-label {
  font-family: -apple-system, 'SF Pro Text', BlinkMacSystemFont, sans-serif;
  font-size: 12px;
  font-weight: 500;
}

/* ── Mobile: floating pill bottom nav ───────────────────── */
.mobile-nav {
  display: block;
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
.mobile-item--active .mobile-icon :deep(circle) { stroke: #800020; }

.mobile-dot {
  position: absolute; bottom: -5px; left: 50%;
  transform: translateX(-50%);
  width: 4px; height: 4px; border-radius: 50%;
  background: #800020;
  box-shadow: 0 0 7px rgba(128,0,32,0.95);
}
.mobile-label {
  font-family: -apple-system, 'SF Pro Text', BlinkMacSystemFont, sans-serif;
  font-size: 9px; letter-spacing: 0.3px;
  font-weight: 500;
}

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
    0 3px 10px rgba(0,0,0,0.5);
  transition: transform 0.22s cubic-bezier(0.22,1,0.36,1);
}
.mobile-item--center:active .mobile-fab { transform: scale(0.94); }

/* Transitions */
.dot-enter-active, .dot-leave-active { transition: opacity 0.2s, transform 0.2s; }
.dot-enter-from, .dot-leave-to { opacity: 0; transform: translateX(-50%) scale(0); }
</style>