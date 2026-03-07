<template>
  <div class="shell">
    <AuthAmbient />
    <AppNavBar />

    <main class="shell-main">
      <RouterView v-slot="{ Component }">
        <Transition name="page-fade" mode="out-in">
          <component :is="Component" :key="$route.path" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import AuthAmbient from '@/components/auth/AuthAmbient.vue'
import AppNavBar   from '@/components/layout/AppNavBar.vue'

const { user, fetchMe } = useAuth()

onMounted(async () => {
  if (!user.value) await fetchMe()
})
</script>

<style scoped>
.shell {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--void, #080808);
  overflow-x: hidden;
}

/* Mobile: pad bottom so content isn't hidden under pill nav */
.shell-main {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 110px;
}

/* Desktop: pad top to clear the fixed top navbar (52px height) */
@media (min-width: 860px) {
  .shell-main {
    padding-top: 84px; /* 14px offset + 52px nav + 18px breathing room */
    padding-bottom: 40px;
    max-width: 960px;
    margin: 0 auto;
    width: 100%;
  }
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(6px);
}
</style>