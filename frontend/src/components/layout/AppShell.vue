<template>
  <div class="shell">
    <AuthAmbient />

    <!-- ── Side Rail (desktop ≥ 860px) ─────────────────────────────────── -->
    <aside class="rail" :class="{ 'rail--expanded': railExpanded }">

      <div class="rail-logo" @click="railExpanded = !railExpanded">
        <div class="rail-logo-mark">
          <span class="rail-logo-r">R</span>
        </div>
        <Transition name="rail-label">
          <span v-if="railExpanded" class="rail-logo-name t-display">Ring-It</span>
        </Transition>
      </div>

      <nav class="rail-nav" role="navigation" aria-label="Main navigation">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="rail-item"
          :class="{ 'rail-item--active': isActive(item.path) }"
          :title="item.label"
        >
          <span class="rail-item-icon" v-html="item.icon" />
          <Transition name="rail-label">
            <span v-if="railExpanded" class="rail-item-label t-mono">{{ item.label }}</span>
          </Transition>
        </RouterLink>
      </nav>

      <div class="rail-bottom">
        <div class="rail-user" :title="user?.full_name || 'Account'">
          <div class="rail-avatar">
            <span class="t-mono">{{ userInitial }}</span>
          </div>
          <Transition name="rail-label">
            <div v-if="railExpanded" class="rail-user-info">
              <span class="rail-user-name t-mono">{{ user?.full_name?.split(' ')[0] || 'Vault' }}</span>
              <span class="rail-user-status t-mono" :class="user?.is_verified ? 'status--green' : 'status--amber'">
                {{ user?.is_verified ? '✓ verified' : '⚡ unverified' }}
              </span>
            </div>
          </Transition>
        </div>
        <button class="rail-logout" @click="handleLogout" title="Logout">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M5 2H2a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
            <path d="M9.5 9.5L13 7l-3.5-2.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13 7H5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </aside>

    <!-- ── Main content ──────────────────────────────────────────────────── -->
    <main class="shell-main" :class="{ 'shell-main--expanded': railExpanded }">
      <RouterView v-slot="{ Component }">
        <Transition name="page-fade" mode="out-in">
          <component :is="Component" :key="$route.path" />
        </Transition>
      </RouterView>
    </main>

    <!-- ── Bottom Tab Bar (mobile < 860px) ──────────────────────────────── -->
    <nav class="tab-bar" role="navigation" aria-label="Main navigation">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="tab-item"
        :class="{ 'tab-item--active': isActive(item.path) }"
      >
        <span class="tab-icon" v-html="item.icon" />
        <span class="tab-label t-mono">{{ item.label }}</span>
      </RouterLink>
    </nav>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import AuthAmbient from '@/components/auth/AuthAmbient.vue'

const route  = useRoute()
const router = useRouter()
const { user, logout, fetchMe } = useAuth()

const railExpanded = ref(false)

const userInitial = computed(() => {
  const name = user.value?.full_name || ''
  return name.split(' ').map((w: string) => w[0]).slice(0, 2).join('').toUpperCase() || 'V'
})

function isActive(path: string) {
  if (path === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(path)
}

async function handleLogout() {
  await logout()
}

onMounted(async () => {
  if (!user.value) await fetchMe()
})

const navItems = [
  {
    path: '/dashboard',
    label: 'Vault',
    icon: `<svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <rect x="2" y="2" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
      <rect x="10" y="2" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
      <rect x="2" y="10" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
      <rect x="10" y="10" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
    </svg>`,
  },
  {
    path: '/dashboard/transactions',
    label: 'Ledger',
    icon: `<svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <path d="M3 5h12M3 9h8M3 13h5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`,
  },
  {
    path: '/dashboard/budget',
    label: 'Budget',
    icon: `<svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.3"/>
      <path d="M9 5.5v7M6.5 7.5c0-1.1.9-2 2.5-2s2.5.9 2.5 2-1 1.6-2.5 2-2.5.9-2.5 2 .9 2 2.5 2 2.5-.9 2.5-2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
    </svg>`,
  },
  {
    path: '/dashboard/goals',
    label: 'Goals',
    icon: `<svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.3"/>
      <circle cx="9" cy="9" r="3" stroke="currentColor" stroke-width="1.3"/>
      <path d="M9 2v2M9 14v2M2 9h2M14 9h2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
    </svg>`,
  },
  {
    path: '/dashboard/settings',
    label: 'Profile',
    icon: `<svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="6.5" r="2.5" stroke="currentColor" stroke-width="1.3"/>
      <path d="M3 15c0-3.31 2.69-6 6-6s6 2.69 6 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`,
  },
]
</script>

<style scoped>
/* ── Shell root ── */
.shell {
  position: relative;
  height: 100vh;
  display: flex;
  background: var(--color-void, #080808);
  overflow: hidden;
}

/* ── Side Rail — hidden on mobile ── */
.rail { display: none; }

@media (min-width: 860px) {
  .rail {
    display: flex;
    flex-direction: column;
    position: fixed;
    left: 0; top: 0; bottom: 0;
    width: 64px;
    background: rgba(12, 12, 14, 0.95);
    border-right: 1px solid rgba(224, 224, 224, 0.06);
    z-index: 100;
    transition: width 0.28s cubic-bezier(0.22, 1, 0.36, 1);
    overflow: hidden;
  }
  .rail--expanded { width: 200px; }
}

/* ── Rail logo ── */
.rail-logo {
  display: flex; align-items: center; gap: 12px;
  padding: 20px 18px 16px;
  cursor: pointer;
  border-bottom: 1px solid rgba(224, 224, 224, 0.05);
  margin-bottom: 8px;
  min-height: 64px; flex-shrink: 0;
}
.rail-logo-mark {
  width: 28px; height: 28px; border-radius: 8px;
  background: rgba(128, 0, 32, 0.9);
  border: 1px solid rgba(128, 0, 32, 0.6);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 0 12px rgba(128, 0, 32, 0.4);
}
.rail-logo-r {
  font-family: var(--font-heading, 'Syne', sans-serif);
  font-size: 13px; font-weight: 800;
  color: rgba(224, 224, 224, 0.95); line-height: 1;
}
.rail-logo-name {
  font-size: 0.95rem; color: var(--color-plat, #E0E0E0);
  white-space: nowrap; letter-spacing: -0.02em;
}

/* ── Rail nav ── */
.rail-nav {
  flex: 1; display: flex; flex-direction: column;
  gap: 2px; padding: 0 8px; overflow-y: auto;
}
.rail-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px; border-radius: 10px;
  color: var(--color-gun, #757575);
  transition: all 0.18s; position: relative;
  text-decoration: none; min-height: 44px; white-space: nowrap;
  border: 1px solid transparent;
}
.rail-item:hover { background: rgba(224, 224, 224, 0.05); color: rgba(224, 224, 224, 0.7); }
.rail-item--active {
  background: rgba(128, 0, 32, 0.12);
  color: rgba(224, 224, 224, 0.9);
  border-color: rgba(128, 0, 32, 0.2);
}
.rail-item--active .rail-item-icon :deep(path),
.rail-item--active .rail-item-icon :deep(rect),
.rail-item--active .rail-item-icon :deep(circle) {
  stroke: var(--color-ox, #800020);
}
.rail-item-icon {
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.rail-item-label { font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase; }

/* ── Rail bottom ── */
.rail-bottom {
  padding: 12px 10px;
  border-top: 1px solid rgba(224, 224, 224, 0.05);
  display: flex; align-items: center; justify-content: space-between;
  gap: 8px; min-height: 64px;
}
.rail-user { display: flex; align-items: center; gap: 10px; overflow: hidden; }
.rail-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: rgba(128, 0, 32, 0.15);
  border: 1px solid rgba(128, 0, 32, 0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; color: rgba(224, 224, 224, 0.7);
  flex-shrink: 0; font-family: var(--font-mono, 'DM Mono', monospace);
}
.rail-user-info { display: flex; flex-direction: column; gap: 1px; overflow: hidden; }
.rail-user-name {
  font-size: 10px; letter-spacing: 0.5px; color: rgba(224, 224, 224, 0.7);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.rail-user-status { font-size: 8px; letter-spacing: 0.5px; text-transform: lowercase; }
.status--green { color: var(--color-grn, #4CAF50); }
.status--amber { color: var(--color-amb, #FB8C00); }

.rail-logout {
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px; color: var(--color-gun, #757575);
  background: rgba(224, 224, 224, 0.04);
  border: 1px solid rgba(224, 224, 224, 0.07);
  cursor: pointer; transition: all 0.18s; flex-shrink: 0;
}
.rail-logout:hover { color: #ef5350; background: rgba(239, 83, 80, 0.07); border-color: rgba(239, 83, 80, 0.2); }

/* ── Main content ── */
.shell-main {
  flex: 1; min-width: 0; min-height: 0;
  display: flex; flex-direction: column;
}
@media (min-width: 860px) {
  .shell-main {
    margin-left: 64px;
    transition: margin-left 0.28s cubic-bezier(0.22, 1, 0.36, 1);
  }
  .shell-main--expanded { margin-left: 200px; }
}

/* ── Bottom Tab Bar — mobile only ── */
.tab-bar {
  position: fixed; bottom: 0; left: 0; right: 0;
  height: 72px; display: flex; align-items: stretch;
  background: rgba(10, 10, 12, 0.96);
  border-top: 1px solid rgba(224, 224, 224, 0.07);
  backdrop-filter: blur(20px) saturate(1.4);
  -webkit-backdrop-filter: blur(20px) saturate(1.4);
  z-index: 200;
  padding-bottom: env(safe-area-inset-bottom);
}
@media (min-width: 860px) { .tab-bar { display: none; } }

.tab-item {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 4px; color: rgba(117, 117, 117, 0.7);
  text-decoration: none; transition: all 0.18s;
  position: relative; padding: 8px 4px 4px;
  -webkit-tap-highlight-color: transparent;
}
.tab-item:active { background: rgba(224, 224, 224, 0.04); }
.tab-item--active { color: rgba(224, 224, 224, 0.95); }
.tab-item--active .tab-icon :deep(path),
.tab-item--active .tab-icon :deep(rect),
.tab-item--active .tab-icon :deep(circle) {
  stroke: var(--color-ox, #800020);
}
.tab-item--active::before {
  content: '';
  position: absolute; top: 0; left: 50%;
  transform: translateX(-50%);
  width: 24px; height: 2px;
  background: var(--color-ox, #800020);
  border-radius: 0 0 2px 2px;
  box-shadow: 0 0 8px rgba(128, 0, 32, 0.8);
}
.tab-icon { width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; }
.tab-label { font-size: 8.5px; letter-spacing: 1px; text-transform: uppercase; }

/* ── Transitions ── */
.rail-label-enter-active, .rail-label-leave-active { transition: opacity 0.18s, transform 0.18s; }
.rail-label-enter-from, .rail-label-leave-to { opacity: 0; transform: translateX(-6px); }

.page-fade-enter-active, .page-fade-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.page-fade-enter-from, .page-fade-leave-to { opacity: 0; transform: translateY(6px); }
</style>