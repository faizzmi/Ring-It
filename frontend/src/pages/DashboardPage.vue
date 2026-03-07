<template>
  <div class="dash">
    <div class="dash-scroll">
      <header class="dash-header">
        <div class="dash-header-mobile">
          <div>
            <p class="dash-greeting t-mono">{{ greeting }}</p>
            <h1 class="dash-name t-display">{{ firstName }}<span class="dash-period">.</span></h1>
          </div>
          <button class="notif-btn" :class="{ 'notif-btn--dot': true }">
            <svg width="19" height="19" viewBox="0 0 19 19" fill="none">
              <path d="M9.5 2.5a5.5 5.5 0 0 1 5.5 5.5v2.5l1.5 3H3L4.5 10.5V8a5.5 5.5 0 0 1 5-5.5" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7.5 15.5a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.35" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <div class="dash-header-desktop">
          <div class="desk-header-left">
            <p class="dash-greeting t-mono">{{ greeting }}</p>
            <h1 class="dash-name t-display">{{ firstName }}<span class="dash-period">.</span></h1>
          </div>
          <div class="desk-header-right">
            <div class="desk-date t-mono">
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                <rect x="1.5" y="2.5" width="10" height="9" rx="2" stroke="currentColor" stroke-width="1.1"/>
                <path d="M4.5 1.5v2M8.5 1.5v2M1.5 5.5h10" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>
              </svg>
              {{ todayLabel }}
            </div>
            <button class="notif-btn" :class="{ 'notif-btn--dot': true }">
              <svg width="18" height="18" viewBox="0 0 19 19" fill="none">
                <path d="M9.5 2.5a5.5 5.5 0 0 1 5.5 5.5v2.5l1.5 3H3L4.5 10.5V8a5.5 5.5 0 0 1 5-5.5" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7.5 15.5a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.35" stroke-linecap="round"/>
              </svg>
            </button>
            <div class="desk-avatar t-mono">{{ userInitial }}</div>
          </div>
        </div>
        <div v-if="user && !user.is_verified" class="verify-banner">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.1"/>
            <path d="M6 4v3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
            <circle cx="6" cy="9" r=".6" fill="currentColor"/>
          </svg>
          <span class="t-mono" style="font-size:10px">Verify your email to unlock full access.</span>
          <a href="/verify-email" class="verify-link t-mono">Verify →</a>
        </div>
      </header>

      <div v-if="loading" class="dash-loading">
        <div class="dash-loading-inner">
          <div class="loading-pulse" />
          <span class="t-mono" style="font-size:9px;letter-spacing:2px;color:var(--color-gun)">LOADING VAULT</span>
        </div>
      </div>

      <template v-else>
        <section class="dash-section">
          <div class="nw-card">
            <div class="nw-glow" />
            <div class="nw-top">
              <span class="t-mono nw-label">// NET WORTH</span>
              <button class="eye-btn" @click="hideBalance = !hideBalance">
                <svg v-if="!hideBalance" width="15" height="15" viewBox="0 0 15 15" fill="none">
                  <ellipse cx="7.5" cy="7.5" rx="6" ry="4" stroke="currentColor" stroke-width="1.2"/>
                  <circle cx="7.5" cy="7.5" r="1.8" stroke="currentColor" stroke-width="1.2"/>
                </svg>
                <svg v-else width="15" height="15" viewBox="0 0 15 15" fill="none">
                  <path d="M2 2l11 11M5.5 4.8A6 6 0 0 1 7.5 4.5c3 0 5.5 2.8 5.5 3s-.6 1.2-1.5 2.1M9.5 10.2C8.9 10.6 8.2 10.8 7.5 10.8c-3 0-5.5-2.8-5.5-3 0-.2.5-1.1 1.5-2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <div class="nw-amount-row">
              <span class="nw-ccy t-mono">{{ user?.currency || 'MYR' }}</span>
              <span class="nw-amount t-display">{{ hideBalance ? '••••••' : formatAmount(summary.netWorth) }}</span>
            </div>
            <div class="nw-meta-row">
              <div class="nw-delta" :class="summary.netWorthDelta >= 0 ? 'delta--pos' : 'delta--neg'">
                <svg width="9" height="9" viewBox="0 0 9 9" fill="none">
                  <path :d="summary.netWorthDelta >= 0 ? 'M4.5 7.5V1.5M1.5 4.5l3-3 3 3' : 'M4.5 1.5v6M1.5 4.5l3 3 3-3'" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span class="t-mono">{{ summary.netWorthDelta >= 0 ? '+' : '' }}{{ formatAmount(Math.abs(summary.netWorthDelta)) }} this month</span>
              </div>
              <div class="dsr-pill" :style="{ borderColor: dsrColor, color: dsrColor }">
                <span class="t-mono">DSR {{ summary.dsr }}%</span>
                <span class="t-mono dsr-status-label">{{ dsrLabel }}</span>
              </div>
            </div>
          </div>
        </section>

        <section class="dash-section">
          <div class="section-hdr">
            <span class="t-mono section-tag">// ACCOUNTS & WALLETS</span>
            <a href="/dashboard/accounts" class="section-link t-mono">Manage →</a>
          </div>
          <div v-if="activeAccounts.length === 0" class="empty-card">
            <span class="t-mono empty-label">No accounts yet</span>
            <a href="/dashboard/accounts" class="t-mono empty-link">Add one →</a>
          </div>
          <template v-else>
            <div class="cards-scroll">
              <div v-for="(card, i) in activeAccounts" :key="card.id" class="bank-card" :class="`bank-card--${card.theme}`" @click="activeCard = i">
                <div class="card-shine" />
                <div class="card-noise" />
                <div class="card-top">
                  <div class="card-type-badge t-mono">{{ card.account_type.toUpperCase() }}</div>
                  <div class="card-network" v-html="networkIcon(card.account_type)" />
                </div>
                <div class="card-mid">
                  <span class="card-bal-label t-mono">Available Balance</span>
                  <div class="card-bal-row">
                    <span class="card-ccy t-mono">{{ card.currency }}</span>
                    <span class="card-bal t-display">{{ hideBalance ? '••••••' : formatAmount(card.balance) }}</span>
                  </div>
                </div>
                <div class="card-bottom">
                  <div class="card-holder">
                    <span class="card-holder-label t-mono">ACCOUNT</span>
                    <span class="card-holder-name t-mono">{{ card.name }}</span>
                  </div>
                  <div class="card-number-end">
                    <span class="card-dots t-mono">•••• ••••</span>
                    <span class="card-last4 t-mono">{{ card.last4 }}</span>
                  </div>
                </div>
                <div v-if="activeCard === i" class="card-active-ring" />
              </div>
              <div class="bank-card bank-card--add" @click="$router.push('/dashboard/accounts')">
                <div class="card-add-inner">
                  <div class="card-add-icon">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <span class="t-mono card-add-label">ADD ACCOUNT</span>
                </div>
              </div>
            </div>
            <div class="cards-dots">
              <span v-for="(_, i) in activeAccounts" :key="i" class="cards-dot" :class="{ 'cards-dot--active': activeCard === i }" @click="activeCard = i" />
            </div>
          </template>
        </section>

        <section class="dash-section">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-card-top">
                <div class="stat-icon stat-icon--green">
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <path d="M2 9L5.5 5.5l3 3 4-5" stroke="var(--color-grn)" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="stat-trend t-mono" :class="summary.incomeTrend >= 0 ? 'trend--pos' : 'trend--neg'">{{ summary.incomeTrend >= 0 ? '▲' : '▼' }} {{ Math.abs(summary.incomeTrend) }}%</span>
              </div>
              <span class="stat-val t-display">{{ hideBalance ? '••••' : formatAmount(summary.income) }}</span>
              <span class="stat-label t-mono">Income</span>
            </div>
            <div class="stat-card">
              <div class="stat-card-top">
                <div class="stat-icon stat-icon--red">
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <path d="M2 4L5.5 7.5l3-3 4 5" stroke="#ef5350" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="stat-trend t-mono" :class="summary.expenseTrend <= 0 ? 'trend--pos' : 'trend--neg'">{{ summary.expenseTrend >= 0 ? '▲' : '▼' }} {{ Math.abs(summary.expenseTrend) }}%</span>
              </div>
              <span class="stat-val t-display">{{ hideBalance ? '••••' : formatAmount(summary.expenses) }}</span>
              <span class="stat-label t-mono">Expenses</span>
            </div>
            <div class="stat-card stat-card--wide">
              <div class="stat-card-top">
                <div class="stat-icon stat-icon--ox">
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                    <path d="M6.5 2v9M4 7l2.5 3 2.5-3" stroke="var(--color-ox)" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="stat-trend t-mono" :class="summary.savingsTrend >= 0 ? 'trend--pos' : 'trend--neg'">{{ summary.savingsTrend >= 0 ? '▲' : '▼' }} {{ Math.abs(summary.savingsTrend) }}%</span>
              </div>
              <span class="stat-val t-display">{{ hideBalance ? '••••' : formatAmount(summary.savings) }}</span>
              <span class="stat-label t-mono">Savings</span>
            </div>
          </div>
        </section>

        <section class="dash-section">
          <div class="section-hdr">
            <span class="t-mono section-tag">// MONTHLY BUDGET</span>
            <span class="section-meta t-mono">{{ budgetDaysLeft }}d left</span>
          </div>
          <div v-if="budgets.length === 0" class="empty-card">
            <span class="t-mono empty-label">No budgets yet</span>
            <a href="/dashboard/budget" class="t-mono empty-link">Set one up →</a>
          </div>
          <div v-else class="budget-card sov-card">
            <div v-for="b in budgets" :key="b.label" class="budget-row">
              <div class="budget-row-top">
                <div class="budget-row-left">
                  <span class="budget-dot" :style="{ background: b.color }" />
                  <span class="budget-name t-mono">{{ b.label }}</span>
                </div>
                <span class="budget-amt t-mono">
                  <span class="budget-spent">{{ formatAmount(b.spent) }}</span>
                  <span style="color:rgba(224,224,224,0.15)"> / </span>
                  <span style="color:var(--color-gun)">{{ formatAmount(b.total) }}</span>
                </span>
              </div>
              <div class="sov-track" style="margin-top:7px">
                <div class="sov-track__fill" :style="{ width: Math.min((b.spent / b.total) * 100, 100) + '%', background: b.color, boxShadow: `0 0 6px ${b.color}55` }" />
              </div>
            </div>
          </div>
        </section>

        <section class="dash-section">
          <div class="section-hdr">
            <span class="t-mono section-tag">// WEALTH GOALS</span>
            <a href="/dashboard/goals" class="section-link t-mono">All →</a>
          </div>
          <div v-if="goals.length === 0" class="empty-card">
            <span class="t-mono empty-label">No goals yet</span>
            <a href="/dashboard/goals" class="t-mono empty-link">Add a goal →</a>
          </div>
          <div v-else class="goals-scroll">
            <div v-for="g in goals" :key="g.label" class="goal-card sov-card">
              <div class="goal-top">
                <span class="goal-icon" v-html="g.icon" />
                <span class="goal-pct t-mono" :class="g.pct >= 100 ? 't-green' : ''">{{ g.pct }}%</span>
              </div>
              <p class="goal-name t-mono">{{ g.label }}</p>
              <p class="goal-target t-display">{{ formatAmount(g.current) }}</p>
              <p class="goal-sub t-mono">of {{ formatAmount(g.target) }}</p>
              <div class="sov-track" style="margin-top:10px">
                <div class="sov-track__fill" :style="{ width: Math.min(g.pct, 100) + '%', background: g.pct >= 100 ? 'var(--color-grn)' : 'var(--color-ox)' }" />
              </div>
            </div>
            <div class="goal-card goal-card--add" @click="$router.push('/dashboard/goals')">
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                <circle cx="11" cy="11" r="9" stroke="rgba(224,224,224,0.12)" stroke-width="1.3"/>
                <path d="M11 7v8M7 11h8" stroke="rgba(224,224,224,0.2)" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span class="t-mono" style="font-size:8px;letter-spacing:1.5px;color:rgba(224,224,224,0.18);margin-top:8px">NEW GOAL</span>
            </div>
          </div>
        </section>

        <section class="dash-section" style="padding-bottom:12px">
          <div class="section-hdr">
            <span class="t-mono section-tag">// RECENT LEDGER</span>
            <a href="/dashboard/transactions" class="section-link t-mono">All →</a>
          </div>
          <div v-if="recentTxns.length === 0" class="empty-card">
            <span class="t-mono empty-label">No transactions yet</span>
            <a href="/dashboard/transactions?new=1" class="t-mono empty-link">Log your first →</a>
          </div>
          <div v-else class="txn-list sov-card">
            <div v-for="(txn, i) in recentTxns" :key="i" class="txn-row">
              <div class="txn-icon-wrap" :style="{ background: txn.bg }">
                <span v-html="txn.icon" />
              </div>
              <div class="txn-info">
                <span class="txn-name t-mono">{{ txn.name }}</span>
                <span class="txn-date t-mono">{{ txn.date }}</span>
              </div>
              <span class="txn-amt t-mono" :class="txn.type === 'credit' ? 't-green' : 't-red'">{{ txn.type === 'credit' ? '+' : '-' }}{{ formatAmount(txn.amount) }}</span>
            </div>
          </div>
        </section>
      </template>
      <div style="height:40px" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useAccount } from '@/composables/useAccounts'

const { user } = useAuth()
const { activeAccounts, loading: acctLoading, fetchAccounts } = useAccount()

const hideBalance = ref(false)
const loading = ref(true)
const activeCard = ref(0)

function networkIcon(type: string): string {
  if (type === 'bank') return `<svg width="36" height="22" viewBox="0 0 36 22" fill="none"><circle cx="13" cy="11" r="9" fill="rgba(255,255,255,0.18)"/><circle cx="23" cy="11" r="9" fill="rgba(255,255,255,0.1)"/></svg>`
  if (type === 'ewallet') return `<svg width="36" height="22" viewBox="0 0 36 22" fill="none"><path d="M6 11 L18 4 L30 11 L18 18 Z" fill="rgba(255,255,255,0.12)"/><circle cx="18" cy="11" r="4" fill="rgba(255,255,255,0.15)"/></svg>`
  return `<svg width="36" height="22" viewBox="0 0 36 22" fill="none"><rect x="4" y="7" width="28" height="8" rx="4" fill="rgba(255,255,255,0.12)"/></svg>`
}

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return '// GOOD MORNING'
  if (h < 17) return '// GOOD AFTERNOON'
  return '// GOOD EVENING'
})
const firstName = computed(() => user.value?.full_name?.split(' ')[0] || 'Vault')
const userInitial = computed(() => {
  const name = user.value?.full_name || ''
  return name.split(' ').map((w: string) => w[0]).slice(0, 2).join('').toUpperCase() || 'V'
})
const todayLabel = computed(() =>
  new Date().toLocaleDateString('en-MY', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase()
)

const summary = ref({ netWorth: 0, netWorthDelta: 0, dsr: 0, income: 0, expenses: 0, savings: 0, incomeTrend: 0, expenseTrend: 0, savingsTrend: 0 })
const budgets = ref<any[]>([])
const goals = ref<any[]>([])
const recentTxns = ref<any[]>([])

const dsrColor = computed(() => {
  const d = summary.value.dsr
  return d <= 30 ? 'var(--color-grn)' : d <= 40 ? 'var(--color-amb)' : '#ef5350'
})
const dsrLabel = computed(() => {
  const d = summary.value.dsr
  return d <= 30 ? 'HEALTHY' : d <= 40 ? 'CAUTION' : 'HIGH RISK'
})
const budgetDaysLeft = computed(() => {
  const now = new Date()
  const end = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  return end.getDate() - now.getDate()
})

function formatAmount(v: number): string {
  if (!v && v !== 0) return '0.00'
  if (v >= 1_000_000) return (v / 1_000_000).toFixed(2) + 'M'
  if (v >= 1_000) return v.toLocaleString('en-MY', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
  return v.toFixed(2)
}

onMounted(async () => {
  try {
    await fetchAccounts()
    // TODO: fetch summary, budgets, goals, recentTxns from API
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dash { height:100%; min-height:100vh; background:var(--color-void); }
.dash-scroll { height:100%; overflow-y:auto; -webkit-overflow-scrolling:touch; }
.dash-header { padding:20px 20px 16px; }
.dash-header-mobile { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:14px; }
.dash-header-desktop { display:none; }
@media(min-width:860px) {
  .dash-header { padding:36px 36px 20px; }
  .dash-header-mobile { display:none; }
  .dash-header-desktop { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
  .desk-header-left { display:flex; flex-direction:column; gap:4px; }
  .desk-header-right { display:flex; align-items:center; gap:12px; }
  .desk-date { display:flex; align-items:center; gap:6px; font-size:9.5px; letter-spacing:1px; color:var(--color-gun); padding:6px 12px; background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); border-radius:100px; }
  .desk-avatar { width:34px; height:34px; border-radius:50%; background:var(--color-ox-lo); border:1px solid var(--color-ox-md); display:flex; align-items:center; justify-content:center; font-size:10px; color:rgba(224,224,224,0.75); font-family:var(--font-mono); cursor:pointer; }
  .dash-name { font-size:clamp(1.8rem,3vw,2.4rem); }
}
.dash-greeting { font-size:8.5px; letter-spacing:2.5px; color:var(--color-gun); text-transform:uppercase; margin-bottom:4px; }
.dash-name { font-size:clamp(2rem,8vw,2.8rem); color:var(--color-plat); line-height:1; }
.dash-period { color:var(--color-ox); }
.notif-btn { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:rgba(224,224,224,0.05); border:1px solid rgba(224,224,224,0.08); color:var(--color-gun); cursor:pointer; position:relative; transition:all .18s; }
.notif-btn:hover { color:var(--color-plat); }
.notif-btn--dot::after { content:''; position:absolute; top:8px; right:9px; width:5px; height:5px; background:var(--color-ox); border-radius:50%; box-shadow:0 0 5px var(--color-ox-hi); }
.verify-banner { display:flex; align-items:center; gap:8px; padding:9px 14px; background:var(--color-amb-lo); border:1px solid rgba(251,140,0,0.18); border-radius:10px; color:rgba(251,140,0,0.8); }
.verify-link { margin-left:auto; font-size:9.5px; letter-spacing:0.5px; color:rgba(251,140,0,0.9); text-decoration:none; }
.dash-loading { display:flex; align-items:center; justify-content:center; padding:80px 20px; }
.dash-loading-inner { display:flex; flex-direction:column; align-items:center; gap:16px; }
.loading-pulse { width:32px; height:32px; border-radius:50%; border:2px solid var(--color-ox-lo); border-top-color:var(--color-ox-hi); animation:spin .8s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }
.dash-section { padding:0 16px 20px; }
@media(min-width:860px) { .dash-section { padding:0 36px 24px; } }
.nw-card { background:rgba(16,16,18,0.9); border:1px solid var(--color-glass-bo); border-radius:var(--radius-lg); padding:22px 20px 18px; position:relative; overflow:hidden; }
.nw-glow { position:absolute; top:-40px; right:-40px; width:160px; height:160px; background:radial-gradient(circle, var(--color-ox-md) 0%, transparent 70%); pointer-events:none; }
.nw-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.nw-label { font-size:8.5px; letter-spacing:2px; color:var(--color-gun); text-transform:uppercase; }
.eye-btn { width:26px; height:26px; display:flex; align-items:center; justify-content:center; border-radius:50%; background:rgba(224,224,224,0.05); border:1px solid var(--color-glass-bo); color:var(--color-gun); cursor:pointer; transition:all .18s; }
.eye-btn:hover { color:var(--color-plat); }
.nw-amount-row { display:flex; align-items:baseline; gap:6px; margin-bottom:14px; }
.nw-ccy { font-size:12px; letter-spacing:1px; color:var(--color-gun); }
.nw-amount { font-size:clamp(2rem,8vw,2.8rem); color:var(--color-plat); letter-spacing:-0.04em; line-height:1; }
.nw-meta-row { display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; }
.nw-delta { display:inline-flex; align-items:center; gap:5px; font-size:9.5px; letter-spacing:0.3px; font-family:var(--font-mono); padding:4px 10px; border-radius:100px; }
.delta--pos { color:var(--color-grn); background:var(--color-grn-lo); }
.delta--neg { color:#ef5350; background:var(--color-red-lo); }
.dsr-pill { display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:100px; border-width:1px; border-style:solid; background:rgba(0,0,0,0.2); }
.dsr-pill .t-mono { font-size:9px; letter-spacing:1px; }
.dsr-status-label { opacity:0.7; }
.stats-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.stat-card { background:rgba(16,16,18,0.85); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); padding:14px 14px 12px; display:flex; flex-direction:column; gap:4px; }
.stat-card--wide { grid-column:1 / -1; flex-direction:row; align-items:center; gap:0; }
.stat-card--wide .stat-val { margin-left:auto; }
.stat-card--wide .stat-label { margin-left:8px; align-self:flex-end; padding-bottom:2px; }
.stat-card--wide .stat-card-top { margin-bottom:0; }
.stat-card-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:6px; }
.stat-icon { width:24px; height:24px; border-radius:8px; display:flex; align-items:center; justify-content:center; }
.stat-icon--green { background:var(--color-grn-lo); }
.stat-icon--red { background:var(--color-red-lo); }
.stat-icon--ox { background:var(--color-ox-lo); }
.stat-val { font-size:1.05rem; color:var(--color-plat); letter-spacing:-0.02em; line-height:1; }
.stat-label { font-size:8.5px; letter-spacing:1.2px; color:var(--color-gun); text-transform:uppercase; }
.stat-trend { font-size:8.5px; letter-spacing:0.3px; }
.trend--pos { color:var(--color-grn); }
.trend--neg { color:#ef5350; }
.section-hdr { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.section-tag { font-size:8.5px; letter-spacing:2px; color:var(--color-gun); text-transform:uppercase; }
.section-meta { font-size:8.5px; letter-spacing:1px; color:var(--color-gun); }
.section-link { font-size:9.5px; letter-spacing:0.5px; color:var(--color-ox); text-decoration:none; transition:color .18s; }
.section-link:hover { color:rgba(200,50,80,0.9); }
.empty-card { display:flex; align-items:center; justify-content:space-between; padding:20px 18px; background:rgba(16,16,18,0.6); border:1px dashed var(--color-glass-bo); border-radius:var(--radius-sm); }
.empty-label { font-size:10px; letter-spacing:0.5px; color:var(--color-gun); }
.empty-link { font-size:9.5px; letter-spacing:0.5px; color:var(--color-ox); text-decoration:none; }
.budget-card { padding:16px 18px; display:flex; flex-direction:column; gap:14px; }
.budget-row-top { display:flex; align-items:center; justify-content:space-between; }
.budget-row-left { display:flex; align-items:center; gap:8px; }
.budget-dot { width:6px; height:6px; border-radius:50%; flex-shrink:0; }
.budget-name { font-size:10px; letter-spacing:0.8px; color:rgba(224,224,224,0.65); text-transform:uppercase; }
.budget-amt { font-size:10px; }
.budget-spent { color:rgba(224,224,224,0.8); font-family:var(--font-mono); }
.goals-scroll { display:flex; gap:12px; overflow-x:auto; -webkit-overflow-scrolling:touch; padding-bottom:4px; scrollbar-width:none; }
.goals-scroll::-webkit-scrollbar { display:none; }
.goal-card { flex-shrink:0; width:148px; padding:14px 13px; display:flex; flex-direction:column; }
.goal-card--add { display:flex; flex-direction:column; align-items:center; justify-content:center; background:rgba(224,224,224,0.02); border:1px dashed rgba(224,224,224,0.07) !important; cursor:pointer; transition:border-color .18s; }
.goal-card--add:hover { border-color:var(--color-ox-md) !important; }
.goal-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; }
.goal-icon { width:18px; height:18px; display:flex; align-items:center; justify-content:center; }
.goal-pct { font-size:9px; letter-spacing:0.5px; color:var(--color-gun); }
.goal-name { font-size:8px; letter-spacing:1px; color:var(--color-gun); text-transform:uppercase; margin-bottom:6px; }
.goal-target { font-size:1.05rem; color:var(--color-plat); letter-spacing:-0.02em; line-height:1.1; margin-bottom:2px; }
.goal-sub { font-size:8.5px; color:var(--color-gun); }
.txn-list { padding:4px 0; }
.txn-row { display:flex; align-items:center; gap:12px; padding:12px 16px; border-bottom:1px solid rgba(224,224,224,0.04); transition:background .18s; }
.txn-row:last-child { border-bottom:none; }
.txn-icon-wrap { width:34px; height:34px; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.txn-info { flex:1; display:flex; flex-direction:column; gap:2px; min-width:0; }
.txn-name { font-size:11px; letter-spacing:0.3px; color:rgba(224,224,224,0.8); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.txn-date { font-size:8.5px; letter-spacing:0.5px; color:var(--color-gun); }
.txn-amt { font-size:11px; letter-spacing:0.3px; flex-shrink:0; }
.t-green { color:var(--color-grn); }
.t-red { color:#ef5350; }
.sov-card { background:rgba(16,16,18,0.85); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); }
.sov-track { width:100%; height:3px; background:rgba(224,224,224,0.07); border-radius:2px; overflow:hidden; }
.sov-track__fill { height:100%; border-radius:2px; transition:width .5s var(--ease); }
.cards-scroll { display:flex; gap:14px; overflow-x:auto; -webkit-overflow-scrolling:touch; padding:4px 2px 8px; scrollbar-width:none; scroll-snap-type:x mandatory; }
.cards-scroll::-webkit-scrollbar { display:none; }
.bank-card { flex-shrink:0; width:288px; height:168px; border-radius:20px; padding:18px 20px 16px; display:flex; flex-direction:column; justify-content:space-between; position:relative; overflow:hidden; cursor:pointer; scroll-snap-align:start; transition:transform .22s var(--ease), box-shadow .22s; user-select:none; }
.bank-card:active { transform:scale(0.97); }
.card-shine { position:absolute; inset:0; background:linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.04) 40%, transparent 60%); pointer-events:none; border-radius:inherit; }
.card-noise { position:absolute; inset:0; opacity:0.04; background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); background-size:128px; pointer-events:none; border-radius:inherit; }
.bank-card--ox { background:linear-gradient(135deg, #6b0019 0%, #3a000d 55%, #1a0008 100%); border:1px solid rgba(180,20,50,0.35); box-shadow:0 12px 40px var(--color-ox-hi), 0 2px 8px rgba(0,0,0,0.5); }
.bank-card--slate { background:linear-gradient(135deg, #1e2130 0%, #131720 55%, #0c0f18 100%); border:1px solid rgba(100,120,180,0.2); box-shadow:0 12px 40px rgba(20,30,70,0.5), 0 2px 8px rgba(0,0,0,0.5); }
.bank-card--tng { background:linear-gradient(135deg, #003d6b 0%, #001e38 55%, #000e1e 100%); border:1px solid rgba(0,120,200,0.25); box-shadow:0 12px 40px rgba(0,60,120,0.45), 0 2px 8px rgba(0,0,0,0.5); }
.bank-card--grab { background:linear-gradient(135deg, #0a3320 0%, #041a10 55%, #020e09 100%); border:1px solid rgba(0,180,80,0.2); box-shadow:0 12px 40px rgba(0,100,40,0.4), 0 2px 8px rgba(0,0,0,0.5); }
.bank-card--bank { background:linear-gradient(135deg, #1e2130 0%, #131720 55%, #0c0f18 100%); border:1px solid rgba(100,120,180,0.2); box-shadow:0 12px 40px rgba(20,30,70,0.5), 0 2px 8px rgba(0,0,0,0.5); }
.bank-card--ewallet { background:linear-gradient(135deg, #003d6b 0%, #001e38 55%, #000e1e 100%); border:1px solid rgba(0,120,200,0.25); box-shadow:0 12px 40px rgba(0,60,120,0.45), 0 2px 8px rgba(0,0,0,0.5); }
.bank-card--cash { background:linear-gradient(135deg, #1a2010 0%, #0e1508 55%, #080b04 100%); border:1px solid rgba(80,160,50,0.2); box-shadow:0 12px 40px rgba(40,80,20,0.4), 0 2px 8px rgba(0,0,0,0.5); }
.bank-card--add { background:rgba(224,224,224,0.02); border:1.5px dashed rgba(224,224,224,0.1); box-shadow:none; align-items:center; justify-content:center; transition:border-color .2s, background .2s; }
.bank-card--add:hover { border-color:var(--color-ox-md); background:var(--color-ox-lo); }
.card-add-inner { display:flex; flex-direction:column; align-items:center; gap:10px; }
.card-add-icon { width:40px; height:40px; border-radius:50%; background:rgba(224,224,224,0.06); border:1px solid rgba(224,224,224,0.1); display:flex; align-items:center; justify-content:center; color:rgba(224,224,224,0.3); }
.card-add-label { font-size:8.5px; letter-spacing:2px; color:rgba(224,224,224,0.2); }
.card-top { display:flex; align-items:center; justify-content:space-between; }
.card-type-badge { font-size:8px; letter-spacing:2.5px; color:rgba(255,255,255,0.45); background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.1); padding:3px 8px; border-radius:100px; }
.card-network { display:flex; align-items:center; opacity:0.9; }
.card-mid { display:flex; flex-direction:column; gap:4px; }
.card-bal-label { font-size:8px; letter-spacing:1.5px; color:rgba(255,255,255,0.35); text-transform:uppercase; }
.card-bal-row { display:flex; align-items:baseline; gap:5px; }
.card-ccy { font-size:11px; letter-spacing:1px; color:rgba(255,255,255,0.45); }
.card-bal { font-size:1.75rem; letter-spacing:-0.04em; line-height:1; color:rgba(255,255,255,0.95); }
.card-bottom { display:flex; align-items:flex-end; justify-content:space-between; }
.card-holder { display:flex; flex-direction:column; gap:2px; }
.card-holder-label { font-size:7px; letter-spacing:2px; color:rgba(255,255,255,0.3); text-transform:uppercase; }
.card-holder-name { font-size:10.5px; letter-spacing:0.5px; color:rgba(255,255,255,0.75); }
.card-number-end { display:flex; align-items:baseline; gap:5px; }
.card-dots { font-size:9px; letter-spacing:2px; color:rgba(255,255,255,0.3); }
.card-last4 { font-size:13px; letter-spacing:2px; color:rgba(255,255,255,0.7); font-weight:500; }
.card-active-ring { position:absolute; inset:0; border-radius:20px; border:1.5px solid rgba(255,255,255,0.35); pointer-events:none; }
.cards-dots { display:flex; align-items:center; justify-content:center; gap:6px; margin-top:10px; }
.cards-dot { width:5px; height:5px; border-radius:50%; background:rgba(224,224,224,0.15); cursor:pointer; transition:all .22s var(--ease); }
.cards-dot--active { width:18px; border-radius:3px; background:var(--color-ox); box-shadow:0 0 6px var(--color-ox-hi); }
</style>