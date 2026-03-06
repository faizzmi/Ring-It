<template>
  <div class="dash">

    <!-- ── Scroll container ──────────────────────────────────────────────── -->
    <div class="dash-scroll">

      <!-- ── Hero header ─────────────────────────────────────────────────── -->
      <header class="dash-header">
        <div class="dash-header-top">
          <div>
            <p class="dash-greeting t-mono">{{ greeting }}</p>
            <h1 class="dash-name t-display">{{ firstName }}<span class="dash-period">.</span></h1>
          </div>
          <div class="dash-header-right">
            <button class="dash-notif-btn" :class="{ 'has-dot': true }">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 2a5 5 0 0 1 5 5v2.5l1.5 2.5H2.5L4 9.5V7a5 5 0 0 1 5-5Z"
                      stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 14.5a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Verification banner -->
        <div v-if="user && !user.is_verified" class="dash-verify-banner">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.1"/>
            <path d="M6 4v3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
            <circle cx="6" cy="9" r=".6" fill="currentColor"/>
          </svg>
          <span class="t-mono">Verify your email to unlock full access.</span>
          <a href="/verify-email" class="verify-link t-mono">Verify →</a>
        </div>
      </header>

      <!-- ── Net Worth card ─────────────────────────────────────────────── -->
      <section class="dash-section">
        <div class="nw-card">
          <div class="nw-card-inner">
            <div class="nw-top">
              <span class="t-mono nw-label">// NET WORTH</span>
              <button class="nw-eye-btn" @click="hideBalance = !hideBalance">
                <svg v-if="!hideBalance" width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <ellipse cx="7" cy="7" rx="5.5" ry="3.5" stroke="currentColor" stroke-width="1.2"/>
                  <circle cx="7" cy="7" r="1.5" stroke="currentColor" stroke-width="1.2"/>
                </svg>
                <svg v-else width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2 2l10 10M5 4.5A5.4 5.4 0 0 1 7 4c2.76 0 5 2.5 5 3s-.5 1.1-1.3 1.9M9 9.5C8.4 9.83 7.72 10 7 10c-2.76 0-5-2.5-5-3s.5-1.1 1.3-1.9" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <div class="nw-amount-row">
              <span class="nw-ccy t-mono">{{ user?.currency || 'MYR' }}</span>
              <span class="nw-amount t-display">
                {{ hideBalance ? '••••••' : formatAmount(netWorth) }}
              </span>
            </div>
            <div class="nw-delta" :class="deltaPositive ? 'delta--pos' : 'delta--neg'">
              <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                <path :d="deltaPositive ? 'M5 8V2M2 5l3-3 3 3' : 'M5 2v6M2 5l3 3 3-3'"
                      stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span class="t-mono">{{ deltaPositive ? '+' : '' }}{{ formatAmount(Math.abs(netWorthDelta)) }} this month</span>
            </div>
          </div>

          <!-- DSR gauge -->
          <div class="nw-dsr">
            <div class="dsr-track-wrap">
              <svg class="dsr-arc" viewBox="0 0 60 36" fill="none">
                <path d="M5 35 A25 25 0 0 1 55 35" stroke="rgba(224,224,224,0.07)" stroke-width="5" stroke-linecap="round" fill="none"/>
                <path d="M5 35 A25 25 0 0 1 55 35"
                  :stroke="dsrColor" stroke-width="5" stroke-linecap="round" fill="none"
                  :stroke-dasharray="`${dsrDash} 100`" />
              </svg>
              <div class="dsr-label">
                <span class="dsr-pct t-display" :style="{ color: dsrColor }">{{ dsr }}%</span>
                <span class="dsr-sub t-mono">DSR</span>
              </div>
            </div>
            <span class="dsr-status t-mono" :style="{ color: dsrColor }">{{ dsrLabel }}</span>
          </div>
        </div>
      </section>

      <!-- ── Quick stats ────────────────────────────────────────────────── -->
      <section class="dash-section">
        <div class="stats-row">
          <div v-for="stat in quickStats" :key="stat.label" class="stat-pill">
            <span class="stat-pill-icon" v-html="stat.icon" />
            <span class="stat-pill-val t-display">
              {{ hideBalance ? '••••' : formatAmount(stat.value) }}
            </span>
            <span class="stat-pill-label t-mono">{{ stat.label }}</span>
            <span class="stat-pill-trend t-mono" :class="stat.trendPos ? 'trend--pos' : 'trend--neg'">
              {{ stat.trendPos ? '▲' : '▼' }} {{ stat.trend }}%
            </span>
          </div>
        </div>
      </section>

      <!-- ── Budget ─────────────────────────────────────────────────────── -->
      <section class="dash-section">
        <div class="section-header">
          <span class="t-mono section-tag">// MONTHLY BUDGET</span>
          <span class="section-meta t-mono">{{ budgetDaysLeft }}d left</span>
        </div>
        <div class="budget-card sov-card">
          <div v-for="b in budgetItems" :key="b.label" class="budget-row">
            <div class="budget-row-top">
              <div class="budget-row-left">
                <span class="budget-dot" :style="{ background: b.color }" />
                <span class="budget-name t-mono">{{ b.label }}</span>
              </div>
              <span class="budget-amt t-mono">
                <span class="budget-spent">{{ formatAmount(b.spent) }}</span>
                <span class="budget-sep"> / </span>
                <span class="budget-total">{{ formatAmount(b.total) }}</span>
              </span>
            </div>
            <div class="sov-track" style="margin-top:7px">
              <div class="sov-track__fill"
                :style="{
                  width: Math.min((b.spent / b.total) * 100, 100) + '%',
                  background: b.color,
                  boxShadow: `0 0 6px ${b.color}55`
                }" />
            </div>
          </div>
        </div>
      </section>

      <!-- ── Goals ─────────────────────────────────────────────────────── -->
      <section class="dash-section">
        <div class="section-header">
          <span class="t-mono section-tag">// WEALTH GOALS</span>
          <a href="/dashboard/goals" class="section-link t-mono">All →</a>
        </div>
        <div class="goals-scroll">
          <div v-for="g in goals" :key="g.label" class="goal-card sov-card">
            <div class="goal-top">
              <span class="goal-icon" v-html="g.icon" />
              <span class="goal-pct t-mono" :class="g.pct >= 100 ? 't-green' : ''">{{ g.pct }}%</span>
            </div>
            <p class="goal-name t-mono">{{ g.label }}</p>
            <p class="goal-target t-display">{{ formatAmount(g.current) }}</p>
            <p class="goal-sub t-mono">of {{ formatAmount(g.target) }}</p>
            <div class="sov-track" style="margin-top:10px">
              <div class="sov-track__fill"
                :style="{ width: Math.min(g.pct, 100) + '%', background: g.pct >= 100 ? '#4CAF50' : 'var(--color-ox,#800020)' }" />
            </div>
          </div>
          <div class="goal-card goal-card--add" @click="$router.push('/dashboard/goals')">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="rgba(224,224,224,0.12)" stroke-width="1.3"/>
              <path d="M12 8v8M8 12h8" stroke="rgba(224,224,224,0.25)" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <span class="t-mono" style="font-size:9px;letter-spacing:1.5px;color:rgba(224,224,224,0.2);margin-top:8px">NEW GOAL</span>
          </div>
        </div>
      </section>

      <!-- ── Recent Ledger ──────────────────────────────────────────────── -->
      <section class="dash-section" style="padding-bottom:20px">
        <div class="section-header">
          <span class="t-mono section-tag">// RECENT LEDGER</span>
          <a href="/dashboard/transactions" class="section-link t-mono">All →</a>
        </div>
        <div class="txn-list sov-card">
          <div v-for="(txn, i) in recentTxns" :key="i" class="txn-row">
            <div class="txn-icon-wrap" :style="{ background: txn.bg }">
              <span v-html="txn.icon" />
            </div>
            <div class="txn-info">
              <span class="txn-name t-mono">{{ txn.name }}</span>
              <span class="txn-date t-mono">{{ txn.date }}</span>
            </div>
            <span class="txn-amt t-mono" :class="txn.type === 'credit' ? 't-green' : 't-red'">
              {{ txn.type === 'credit' ? '+' : '-' }}{{ formatAmount(txn.amount) }}
            </span>
          </div>
          <div v-if="!recentTxns.length" class="txn-empty">
            <span class="t-mono" style="font-size:9px;color:var(--color-gun);letter-spacing:1.5px">
              NO TRANSACTIONS YET
            </span>
          </div>
        </div>
      </section>

      <!-- bottom breathing room above tab bar -->
      <div style="height:100px" />
    </div>

    <!-- ── FAB ───────────────────────────────────────────────────────────── -->
    <button class="dash-fab" @click="$router.push('/dashboard/transactions?new=1')" aria-label="Add transaction">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'

const { user } = useAuth()

const hideBalance = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return '// GOOD MORNING'
  if (h < 17) return '// GOOD AFTERNOON'
  return '// GOOD EVENING'
})

const firstName = computed(() => {
  return user.value?.full_name?.split(' ')[0] || 'Vault'
})

const netWorth      = ref(247_830)
const netWorthDelta = ref(4_210)
const deltaPositive = computed(() => netWorthDelta.value >= 0)
const dsr           = ref(28)
const dsrDash       = computed(() => (dsr.value / 100) * 78.5)
const dsrColor      = computed(() => dsr.value <= 30 ? '#4CAF50' : dsr.value <= 40 ? '#FB8C00' : '#ef5350')
const dsrLabel      = computed(() => dsr.value <= 30 ? 'HEALTHY' : dsr.value <= 40 ? 'CAUTION' : 'HIGH RISK')

const quickStats = [
  {
    label: 'Income', value: 8_500, trend: 3.2, trendPos: true,
    icon: `<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 10L6 6l3 3 4-5" stroke="#4CAF50" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  },
  {
    label: 'Expenses', value: 3_240, trend: 1.8, trendPos: false,
    icon: `<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 4l4 4 3-3 4 5" stroke="#ef5350" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  },
  {
    label: 'Savings', value: 5_260, trend: 12.5, trendPos: true,
    icon: `<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 2v10M4 8.5l3 3.5 3-3.5" stroke="#800020" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  },
]

const budgetDaysLeft = computed(() => {
  const now = new Date()
  const end = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  return end.getDate() - now.getDate()
})

const budgetItems = [
  { label: 'Housing',   spent: 1_800, total: 2_000, color: '#800020' },
  { label: 'Food',      spent: 640,   total: 800,   color: '#FB8C00' },
  { label: 'Transport', spent: 280,   total: 400,   color: '#2196F3' },
  { label: 'Lifestyle', spent: 520,   total: 500,   color: '#ef5350' },
]

const goals = [
  {
    label: 'Emergency Fund', current: 18_000, target: 25_500, pct: 71,
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2L3 5v4c0 3 2.5 5 5 5s5-2 5-5V5L8 2Z" stroke="#4CAF50" stroke-width="1.2" stroke-linejoin="round"/></svg>`,
  },
  {
    label: 'Car Fund', current: 9_200, target: 30_000, pct: 31,
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="6" width="12" height="6" rx="2" stroke="#FB8C00" stroke-width="1.2"/><path d="M4 6L5.5 3h5L12 6" stroke="#FB8C00" stroke-width="1.2" stroke-linejoin="round"/><circle cx="5" cy="12" r="1.2" stroke="#FB8C00" stroke-width="1"/><circle cx="11" cy="12" r="1.2" stroke="#FB8C00" stroke-width="1"/></svg>`,
  },
  {
    label: 'Vacation', current: 4_800, target: 5_000, pct: 96,
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="#2196F3" stroke-width="1.2"/><path d="M2 8h12M8 2c-1.5 2-2.5 4-2.5 6s1 4 2.5 6M8 2c1.5 2 2.5 4 2.5 6S9.5 12 8 14" stroke="#2196F3" stroke-width="1.2" stroke-linecap="round"/></svg>`,
  },
]

const recentTxns = [
  { name: 'Grab Food', date: 'Today, 12:30', amount: 24.50, type: 'debit', bg: 'rgba(128,0,32,0.1)', icon: `<svg width="13" height="13" viewBox="0 0 13 13" fill="none"><circle cx="6.5" cy="6.5" r="5.5" stroke="rgba(128,0,32,0.6)" stroke-width="1.1"/><path d="M4 7.5c.5 1 1.3 1.5 2.5 1.5s2-.5 2.5-1.5" stroke="rgba(128,0,32,0.6)" stroke-width="1" stroke-linecap="round"/></svg>` },
  { name: 'Salary — Acme Corp', date: 'Yesterday', amount: 8_500, type: 'credit', bg: 'rgba(76,175,80,0.08)', icon: `<svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M2 9L6 5l3 3 4-5" stroke="#4CAF50" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>` },
  { name: 'TNB Electricity', date: '2 days ago', amount: 145, type: 'debit', bg: 'rgba(33,150,243,0.08)', icon: `<svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M7.5 1.5L3 7.5h3.5L5.5 12l5.5-6H7.5L7.5 1.5Z" stroke="#2196F3" stroke-width="1.1" stroke-linejoin="round"/></svg>` },
  { name: 'Aeon Mall', date: '3 days ago', amount: 312.80, type: 'debit', bg: 'rgba(251,140,0,0.07)', icon: `<svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M2 4.5h9L9.5 10h-6L2 4.5Z" stroke="#FB8C00" stroke-width="1.1" stroke-linejoin="round"/><path d="M4 4.5V3a2 2 0 0 1 4 0v1.5" stroke="#FB8C00" stroke-width="1.1" stroke-linecap="round"/></svg>` },
]

function formatAmount(v: number): string {
  if (v >= 1_000_000) return (v / 1_000_000).toFixed(2) + 'M'
  if (v >= 1_000) return v.toLocaleString('en-MY', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
  return v.toFixed(2)
}
</script>

<style scoped>
/* ── Root: fill the shell-main area ── */
.dash {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 100vh;
  position: relative;
  background: var(--color-void, #080808);
}

/* ── Scroll: takes all remaining height, scrolls internally ── */
.dash-scroll {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

/* ── Header ── */
.dash-header {
  padding: 28px 20px 16px;
}
@media (min-width: 860px) {
  .dash-header { padding: 36px 32px 20px; }
}

.dash-header-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 14px;
}
.dash-greeting {
  font-size: 8.5px;
  letter-spacing: 2.5px;
  color: var(--color-gun, #757575);
  text-transform: uppercase;
  margin-bottom: 4px;
}
.dash-name {
  font-size: clamp(1.8rem, 7vw, 2.6rem);
  color: var(--color-plat, #E0E0E0);
  line-height: 1;
}
.dash-period { color: var(--color-ox, #800020); }

.dash-header-right { padding-top: 4px; }
.dash-notif-btn {
  width: 36px; height: 36px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: rgba(224,224,224,0.05);
  border: 1px solid rgba(224,224,224,0.08);
  color: var(--color-gun, #757575);
  cursor: pointer;
  position: relative;
  transition: all 0.18s;
}
.dash-notif-btn:hover { color: var(--color-plat); background: rgba(224,224,224,0.09); }
.dash-notif-btn.has-dot::after {
  content: '';
  position: absolute; top: 8px; right: 9px;
  width: 5px; height: 5px;
  background: var(--color-ox, #800020);
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(128,0,32,0.9);
}

.dash-verify-banner {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 14px;
  background: rgba(251,140,0,0.06);
  border: 1px solid rgba(251,140,0,0.18);
  border-radius: 8px;
  font-size: 9.5px; letter-spacing: 0.3px;
  color: rgba(251,140,0,0.75);
}
.verify-link {
  margin-left: auto;
  color: rgba(251,140,0,0.9);
  font-size: 9.5px; letter-spacing: 0.5px;
  text-decoration: none;
}

/* ── Sections ── */
.dash-section {
  padding: 0 20px 20px;
}
@media (min-width: 860px) {
  .dash-section { padding: 0 32px 24px; }
}

/* ── Net Worth card ── */
.nw-card {
  background: rgba(18,18,20,0.8);
  border: 1px solid rgba(224,224,224,0.07);
  border-radius: 18px;
  padding: 22px 20px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  position: relative;
  overflow: hidden;
}
.nw-card::before {
  content: '';
  position: absolute; top: -30px; right: -30px;
  width: 140px; height: 140px;
  background: radial-gradient(circle, rgba(128,0,32,0.18) 0%, transparent 70%);
  pointer-events: none;
}
.nw-card-inner { flex: 1; min-width: 0; }
.nw-top { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.nw-label { font-size: 8.5px; letter-spacing: 2px; color: var(--color-gun,#757575); text-transform: uppercase; }
.nw-eye-btn {
  width: 24px; height: 24px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%;
  background: rgba(224,224,224,0.05);
  border: 1px solid rgba(224,224,224,0.08);
  color: var(--color-gun,#757575);
  cursor: pointer; transition: all 0.18s;
}
.nw-eye-btn:hover { color: var(--color-plat); }
.nw-amount-row { display: flex; align-items: baseline; gap: 6px; margin-bottom: 8px; }
.nw-ccy { font-size: 11px; letter-spacing: 1px; color: var(--color-gun,#757575); }
.nw-amount { font-size: clamp(1.7rem,6vw,2.4rem); color: var(--color-plat,#E0E0E0); letter-spacing: -0.04em; line-height: 1; }
.nw-delta {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 9px; letter-spacing: 0.5px;
  font-family: var(--font-mono,'DM Mono',monospace);
  padding: 3px 8px; border-radius: 100px;
}
.delta--pos { color: var(--color-grn,#4CAF50); background: rgba(76,175,80,0.08); }
.delta--neg { color: #ef5350; background: rgba(239,83,80,0.08); }

/* DSR */
.nw-dsr { display: flex; flex-direction: column; align-items: center; gap: 4px; flex-shrink: 0; }
.dsr-track-wrap { position: relative; width: 70px; }
.dsr-arc { width: 70px; height: 42px; }
.dsr-label {
  position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center;
}
.dsr-pct { font-size: 0.9rem; letter-spacing: -0.03em; line-height: 1; transition: color 0.4s; }
.dsr-sub { font-size: 6.5px; letter-spacing: 1.5px; color: var(--color-gun,#757575); }
.dsr-status { font-size: 7.5px; letter-spacing: 1.5px; text-transform: uppercase; transition: color 0.4s; }

/* ── Stats ── */
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.stat-pill {
  background: rgba(18,18,20,0.7);
  border: 1px solid rgba(224,224,224,0.07);
  border-radius: 14px;
  padding: 14px 12px;
  display: flex; flex-direction: column; gap: 4px;
}
.stat-pill-icon { width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; margin-bottom: 4px; }
.stat-pill-val { font-size: 0.95rem; color: var(--color-plat,#E0E0E0); letter-spacing: -0.02em; line-height: 1; }
.stat-pill-label { font-size: 7.5px; letter-spacing: 1.2px; color: var(--color-gun,#757575); text-transform: uppercase; }
.stat-pill-trend { font-size: 7.5px; letter-spacing: 0.5px; margin-top: 2px; }
.trend--pos { color: var(--color-grn,#4CAF50); }
.trend--neg { color: #ef5350; }

/* ── Section header ── */
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.section-tag { font-size: 8.5px; letter-spacing: 2px; color: var(--color-gun,#757575); text-transform: uppercase; }
.section-meta { font-size: 8.5px; letter-spacing: 1px; color: var(--color-gun,#757575); }
.section-link { font-size: 9px; letter-spacing: 1px; color: var(--color-ox,#800020); text-decoration: none; transition: color 0.18s; }
.section-link:hover { color: rgba(200,50,80,0.9); }

/* ── Budget ── */
.budget-card { padding: 16px 18px; display: flex; flex-direction: column; gap: 14px; }
.budget-row-top { display: flex; align-items: center; justify-content: space-between; }
.budget-row-left { display: flex; align-items: center; gap: 8px; }
.budget-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.budget-name { font-size: 10px; letter-spacing: 0.8px; color: rgba(224,224,224,0.7); text-transform: uppercase; }
.budget-amt { font-size: 10px; }
.budget-spent { color: rgba(224,224,224,0.8); font-family: var(--font-mono); }
.budget-sep { color: rgba(224,224,224,0.2); font-family: var(--font-mono); }
.budget-total { color: var(--color-gun,#757575); font-family: var(--font-mono); }

/* ── Goals ── */
.goals-scroll { display: flex; gap: 12px; overflow-x: auto; -webkit-overflow-scrolling: touch; padding-bottom: 4px; scrollbar-width: none; }
.goals-scroll::-webkit-scrollbar { display: none; }
.goal-card { flex-shrink: 0; width: 150px; padding: 16px 14px; display: flex; flex-direction: column; }
@media (min-width: 500px) { .goal-card { width: 165px; } }
.goal-card--add {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  background: rgba(224,224,224,0.02);
  border: 1px dashed rgba(224,224,224,0.08);
  cursor: pointer; transition: border-color 0.18s;
}
.goal-card--add:hover { border-color: rgba(128,0,32,0.25); }
.goal-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.goal-icon { width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; }
.goal-pct { font-size: 9px; letter-spacing: 0.5px; color: var(--color-gun,#757575); }
.goal-name { font-size: 8.5px; letter-spacing: 1px; color: var(--color-gun,#757575); text-transform: uppercase; margin-bottom: 6px; }
.goal-target { font-size: 1.05rem; color: var(--color-plat,#E0E0E0); letter-spacing: -0.02em; line-height: 1.1; margin-bottom: 2px; }
.goal-sub { font-size: 8.5px; letter-spacing: 0.3px; color: var(--color-gun,#757575); margin-bottom: 0; }
.t-green { color: var(--color-grn,#4CAF50); }

/* ── Transactions ── */
.txn-list { padding: 4px 0; }
.txn-row { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-bottom: 1px solid rgba(224,224,224,0.04); transition: background 0.18s; }
.txn-row:last-child { border-bottom: none; }
.txn-row:active { background: rgba(224,224,224,0.03); }
.txn-icon-wrap { width: 34px; height: 34px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.txn-info { flex: 1; display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.txn-name { font-size: 11px; letter-spacing: 0.3px; color: rgba(224,224,224,0.8); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.txn-date { font-size: 8.5px; letter-spacing: 0.5px; color: var(--color-gun,#757575); }
.txn-amt { font-size: 11px; letter-spacing: 0.5px; flex-shrink: 0; }
.t-red { color: #ef5350; }
.txn-empty { padding: 28px 16px; text-align: center; }

/* ── FAB ── */
.dash-fab {
  position: fixed;
  bottom: 90px; right: 20px;
  width: 50px; height: 50px;
  border-radius: 50%;
  background: rgba(128,0,32,0.9);
  border: 1px solid rgba(128,0,32,0.6);
  color: rgba(224,224,224,0.95);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  box-shadow: 0 6px 24px rgba(128,0,32,0.4), 0 0 0 1px rgba(255,255,255,0.05) inset;
  transition: all 0.2s cubic-bezier(0.22,1,0.36,1);
  z-index: 150;
}
.dash-fab:hover { transform: scale(1.08); box-shadow: 0 8px 32px rgba(128,0,32,0.55); }
.dash-fab:active { transform: scale(0.95); }
@media (min-width: 860px) { .dash-fab { bottom: 32px; right: 32px; } }
</style>