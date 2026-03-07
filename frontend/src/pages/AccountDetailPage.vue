<template>
    <div class="detail-root">
      <div class="sov-ambient" aria-hidden="true">
        <div class="sov-orb sov-orb--1" />
        <div class="sov-orb sov-orb--2" />
        <div class="sov-grid-overlay" />
      </div>
  
      <div class="detail-scroll">
        <header class="detail-header">
          <div class="detail-hdr-mobile">
            <div class="detail-breadcrumb t-mono">
              <router-link to="/dashboard" class="breadcrumb-link">// VAULT</router-link>
              <span class="breadcrumb-sep">›</span>
              <router-link to="/dashboard/accounts" class="breadcrumb-link">ACCOUNTS</router-link>
              <span class="breadcrumb-sep">›</span>
              <span class="breadcrumb-cur">{{ account?.name ?? '...' }}</span>
            </div>
            <button class="notif-btn" @click="router.push('/dashboard/accounts')">
              <svg width="16" height="16" viewBox="0 0 18 18" fill="none">
                <path d="M11 4L6 9l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          <div class="detail-hdr-desktop">
            <div class="detail-breadcrumb t-mono">
              <router-link to="/dashboard" class="breadcrumb-link">// VAULT</router-link>
              <span class="breadcrumb-sep">›</span>
              <router-link to="/dashboard/accounts" class="breadcrumb-link">ACCOUNTS</router-link>
              <span class="breadcrumb-sep">›</span>
              <span class="breadcrumb-cur">{{ account?.name ?? '...' }}</span>
            </div>
            <div class="desk-right">
              <div class="desk-date t-mono">
                <svg width="11" height="11" viewBox="0 0 13 13" fill="none">
                  <rect x="1.5" y="2.5" width="10" height="9" rx="2" stroke="currentColor" stroke-width="1.1"/>
                  <path d="M4.5 1.5v2M8.5 1.5v2M1.5 5.5h10" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>
                </svg>
                {{ todayLabel }}
              </div>
              <div class="desk-avatar t-mono">{{ userInitial }}</div>
            </div>
          </div>
        </header>
  
        <div v-if="loading" class="page-loading">
          <div class="page-loading-inner">
            <div class="loading-ring" />
            <span class="t-mono loading-label">LOADING ACCOUNT</span>
          </div>
        </div>
  
        <template v-else-if="account">
          <!-- ── Hero card ── -->
          <section class="detail-section">
            <div class="hero-card sov-card">
              <div class="acct-bar-hero" :class="`bar--${account.theme}`" />
              <div class="hero-top">
                <div class="hero-left">
                  <div class="acct-badge" :class="`badge--${account.theme}`">
                    <span v-html="typeIcon(account.account_type)" />
                  </div>
                  <div>
                    <p class="hero-name t-mono">{{ account.name }}</p>
                    <p class="hero-meta t-mono">{{ account.institution || '—' }} <span class="acct-last4">•••• {{ account.last4 }}</span></p>
                  </div>
                </div>
                <div class="hero-chips">
                  <span class="sov-chip" :class="chipClass(account.account_type)">{{ account.account_type.toUpperCase() }}</span>
                  <span class="sov-chip sov-chip--ghost">{{ account.currency }}</span>
                </div>
              </div>
              <div class="hero-bal-row">
                <div>
                  <p class="sov-label">BALANCE</p>
                  <p class="hero-bal t-display">
                    <span class="hero-bal-ccy t-mono">{{ account.currency }}</span>{{ formatAmount(account.balance) }}
                  </p>
                </div>
                <div v-if="preferredCurrency !== account.currency" class="hero-converted">
                  <p class="sov-label">≈ {{ preferredCurrency }}</p>
                  <p class="hero-bal-conv t-mono">{{ preferredCurrency }} {{ convertedBalance }}</p>
                </div>
              </div>
              <div class="hero-footer">
                <span class="t-mono hero-since">SINCE {{ sinceLabel }}</span>
                <div class="hero-actions">
                  <button class="sov-btn sov-btn--ghost sov-btn--sm" @click="openEditModal">
                    <svg width="11" height="11" viewBox="0 0 13 13" fill="none">
                      <path d="M9.5 2.5l1 1-7 7-1.5.5.5-1.5 7-7Z" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    EDIT
                  </button>
                </div>
              </div>
            </div>
          </section>
  
          <!-- ── Balance chart ── -->
          <section class="detail-section">
            <div class="section-hdr">
              <span class="t-overline">// BALANCE HISTORY</span>
              <div class="chart-range-tabs">
                <button v-for="r in ranges" :key="r" class="range-tab t-mono" :class="{'range-tab--active': chartRange === r}" @click="chartRange = r">{{ r }}</button>
              </div>
            </div>
            <div class="chart-card sov-card">
              <div v-if="chartPoints.length < 2" class="chart-empty">
                <span class="t-mono" style="font-size:9px;letter-spacing:1.5px;color:var(--color-gun)">NO HISTORY YET</span>
              </div>
              <svg v-else class="chart-svg" :viewBox="`0 0 ${svgW} ${svgH}`" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="chart-grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="var(--color-ox)" stop-opacity="0.22"/>
                    <stop offset="100%" stop-color="var(--color-ox)" stop-opacity="0"/>
                  </linearGradient>
                </defs>
                <path :d="areaPath" fill="url(#chart-grad)" />
                <path :d="linePath" fill="none" stroke="var(--color-ox)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle v-for="(p, i) in chartPoints" :key="i" :cx="p.x" :cy="p.y" r="2.5" fill="var(--color-ox)" opacity="0.6"/>
              </svg>
              <div class="chart-labels">
                <span v-for="(p, i) in chartPoints" :key="i" class="chart-label t-mono">{{ p.label }}</span>
              </div>
            </div>
          </section>
  
          <!-- ── Stats strip ── -->
          <section class="detail-section">
            <div class="stats-strip sov-card">
              <div class="stat-item">
                <span class="stat-val t-display">{{ txnCount }}</span>
                <span class="sov-label">TRANSACTIONS</span>
              </div>
              <div class="summary-divider" />
              <div class="stat-item">
                <span class="stat-val t-display" :style="{color: totalIn > 0 ? 'var(--color-grn)' : 'inherit'}">{{ formatAmount(totalIn) }}</span>
                <span class="sov-label">TOTAL IN</span>
              </div>
              <div class="summary-divider" />
              <div class="stat-item">
                <span class="stat-val t-display" :style="{color: totalOut > 0 ? 'var(--color-red)' : 'inherit'}">{{ formatAmount(totalOut) }}</span>
                <span class="sov-label">TOTAL OUT</span>
              </div>
            </div>
          </section>
  
          <!-- ── Transactions ── -->
          <section class="detail-section">
            <div class="section-hdr">
              <span class="t-overline">// TRANSACTIONS</span>
              <button v-if="account" class="sov-btn sov-btn--ghost sov-btn--sm">
                <svg width="11" height="11" viewBox="0 0 13 13" fill="none">
                  <path d="M6.5 2v9M2 6.5h9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                </svg>
                ADD
              </button>
            </div>
            <div v-if="transactions.length === 0" class="empty-state sov-card">
              <div class="empty-icon-wrap">
                <svg width="26" height="26" viewBox="0 0 28 28" fill="none">
                  <path d="M4 14h20M4 9h20M4 19h12" stroke="rgba(224,224,224,0.15)" stroke-width="1.4" stroke-linecap="round"/>
                </svg>
              </div>
              <p class="t-mono empty-title">No transactions yet</p>
              <p class="t-mono" style="font-size:9.5px;color:var(--color-gun);line-height:1.7;text-align:center;max-width:220px">Transactions will appear here once added.</p>
            </div>
            <div v-else class="txn-list">
              <div v-for="txn in transactions" :key="txn.id" class="txn-row sov-card">
                <div class="txn-icon" :class="txn.amount > 0 ? 'txn-icon--in' : 'txn-icon--out'">
                  <svg width="12" height="12" viewBox="0 0 14 14" fill="none">
                    <path v-if="txn.amount > 0" d="M7 11V3M3 7l4-4 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path v-else d="M7 3v8M3 7l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="txn-info">
                  <span class="txn-desc t-mono">{{ txn.description }}</span>
                  <span class="txn-date t-mono">{{ formatDate(txn.date) }}</span>
                </div>
                <span class="txn-amt t-mono" :class="txn.amount > 0 ? 'txn-amt--in' : 'txn-amt--out'">
                  {{ txn.amount > 0 ? '+' : '' }}{{ account?.currency }} {{ formatAmount(Math.abs(txn.amount)) }}
                </span>
              </div>
            </div>
          </section>
        </template>
  
        <div v-else-if="!loading" class="page-loading">
          <p class="t-mono" style="font-size:10px;letter-spacing:1.5px;color:var(--color-gun)">ACCOUNT NOT FOUND</p>
        </div>
  
        <div style="height:48px" />
      </div>
  
      <!-- ── Edit modal ── -->
      <Transition name="modal-fade">
        <div v-if="modalOpen" class="modal-backdrop" @click.self="closeModal">
          <Transition name="modal-slide">
            <div v-if="modalOpen" class="modal-panel">
              <div class="modal-hdr">
                <div>
                  <span class="t-overline">// EDIT ACCOUNT</span>
                  <h2 class="modal-title t-display">Edit Account<span class="title-period">.</span></h2>
                </div>
                <button class="sov-btn sov-btn--icon sov-btn--ghost" @click="closeModal">
                  <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
                    <path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>
              <hr class="sov-divider" style="margin:0 0 24px" />
              <div class="modal-form">
                <div class="field-grp">
                  <label class="sov-label">ACCOUNT NAME <span class="req">*</span></label>
                  <input v-model="form.name" class="sov-input" type="text" maxlength="100" autofocus />
                  <span v-if="fErr.name" class="field-err t-mono">{{ fErr.name }}</span>
                </div>
                <div class="field-grp">
                  <label class="sov-label">ACCOUNT TYPE</label>
                  <div class="type-grid">
                    <button v-for="t in accountTypes" :key="t.value" type="button" class="type-btn t-mono" :class="{'type-btn--active': form.account_type === t.value}" @click="form.account_type = t.value">
                      <span v-html="t.icon" />{{ t.label }}
                    </button>
                  </div>
                </div>
                <div class="field-grp">
                  <label class="sov-label">INSTITUTION</label>
                  <input v-model="form.institution" class="sov-input" type="text" maxlength="100" />
                </div>
                <div class="field-grp">
                  <label class="sov-label">NOTES</label>
                  <textarea v-model="form.notes" class="sov-input sov-textarea" rows="2" />
                </div>
                <div v-if="submitErr" class="sov-nudge sov-nudge--warn">
                  <svg width="11" height="11" viewBox="0 0 12 12" fill="none">
                    <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.1"/>
                    <path d="M6 4v3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    <circle cx="6" cy="9" r=".6" fill="currentColor"/>
                  </svg>
                  {{ submitErr }}
                </div>
                <div class="modal-actions">
                  <button type="button" class="sov-btn sov-btn--ghost" style="flex:1" @click="closeModal">CANCEL</button>
                  <button type="button" class="sov-btn sov-btn--primary" style="flex:2" :disabled="submitting" @click="submitEdit">
                    <span v-if="submitting" class="btn-spin" />
                    SAVE CHANGES
                  </button>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, reactive, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useAuth } from '@/composables/useAuth'
  import { useAccount } from '@/composables/useAccounts'
  import type { IAccount } from '@/composables/useAccounts'
  
  const router = useRouter()
  const route  = useRoute()
  const { user } = useAuth()
  const { getAccount, updateAccount } = useAccount()
  
  const account    = ref<IAccount | null>(null)
  const loading    = ref(true)
  const modalOpen  = ref(false)
  const submitting = ref(false)
  const submitErr  = ref('')
  const chartRange = ref<'1W' | '1M' | '3M' | '1Y'>('1M')
  const ranges     = ['1W', '1M', '3M', '1Y'] as const
  
  // ── Mock transactions (replace with API when transactions endpoint is ready) ──
  const transactions = ref<{ id: string; description: string; amount: number; date: string }[]>([])
  
  const form = reactive({ name: '', account_type: 'bank', institution: '', notes: '' })
  const fErr = reactive({ name: '' })
  
  const accountTypes = [
    { value: 'bank',    label: 'Bank',     icon: `<svg width="14" height="14" viewBox="0 0 13 13" fill="none"><rect x="1.5" y="5" width="10" height="7" rx="2" stroke="currentColor" stroke-width="1.1"/><path d="M4 5V4a2.5 2.5 0 0 1 5 0v1" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/></svg>` },
    { value: 'ewallet', label: 'E-Wallet', icon: `<svg width="14" height="14" viewBox="0 0 13 13" fill="none"><rect x="1.5" y="3.5" width="10" height="7" rx="2" stroke="currentColor" stroke-width="1.1"/><circle cx="9" cy="7" r="1" fill="currentColor"/></svg>` },
    { value: 'cash',    label: 'Cash',     icon: `<svg width="14" height="14" viewBox="0 0 13 13" fill="none"><rect x="1.5" y="4" width="10" height="6" rx="1.5" stroke="currentColor" stroke-width="1.1"/><circle cx="6.5" cy="7" r="1.2" stroke="currentColor" stroke-width="1.1"/></svg>` },
  ]
  
  // ── Currency conversion (static rates — swap for live API when available) ────
  const FX: Record<string, Record<string, number>> = {
    MYR: { USD: 0.22, EUR: 0.20, SGD: 0.30, GBP: 0.17, MYR: 1 },
    USD: { MYR: 4.47, EUR: 0.92, SGD: 1.35, GBP: 0.79, USD: 1 },
    EUR: { MYR: 4.87, USD: 1.09, SGD: 1.47, GBP: 0.86, EUR: 1 },
    SGD: { MYR: 3.31, USD: 0.74, EUR: 0.68, GBP: 0.59, SGD: 1 },
    GBP: { MYR: 5.67, USD: 1.27, EUR: 1.16, SGD: 1.70, GBP: 1 },
  }
  
  const preferredCurrency = computed(() => user.value?.currency ?? 'MYR')
  const convertedBalance  = computed(() => {
    if (!account.value) return '0.00'
    const from = account.value.currency
    const to   = preferredCurrency.value
    const rate = FX[from]?.[to] ?? 1
    return formatAmount(account.value.balance * rate)
  })
  
  // ── Derived ───────────────────────────────────────────────────────────────────
  const todayLabel = computed(() =>
    new Date().toLocaleDateString('en-MY', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase()
  )
  const userInitial = computed(() => {
    const n = user.value?.full_name || ''
    return n.split(' ').map((w: string) => w[0]).slice(0, 2).join('').toUpperCase() || 'V'
  })
  const sinceLabel = computed(() => {
    if (!account.value) return ''
    return new Date(account.value.created_at).toLocaleDateString('en-MY', { day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase()
  })
  const txnCount = computed(() => transactions.value.length)
  const totalIn  = computed(() => transactions.value.filter(t => t.amount > 0).reduce((s, t) => s + t.amount, 0))
  const totalOut = computed(() => Math.abs(transactions.value.filter(t => t.amount < 0).reduce((s, t) => s + t.amount, 0)))
  
  // ── Chart ─────────────────────────────────────────────────────────────────────
  const svgW = 600
  const svgH = 120
  const padT = 12
  const padB = 8
  
  const chartPoints = computed(() => {
    if (!account.value) return []
    // Build mock history from current balance — replace with real ledger data
    const now     = Date.now()
    const days    = chartRange.value === '1W' ? 7 : chartRange.value === '1M' ? 30 : chartRange.value === '3M' ? 90 : 365
    const step    = Math.floor(days / 6)
    const pts     = []
    const bal     = account.value.balance
    for (let i = 0; i <= 6; i++) {
      const daysAgo = (6 - i) * step
      const date    = new Date(now - daysAgo * 86400000)
      const noise   = (Math.random() - 0.5) * bal * 0.08
      pts.push({
        val:   i === 6 ? bal : Math.max(0, bal + noise),
        label: date.toLocaleDateString('en-MY', { day: 'numeric', month: 'short' }).toUpperCase(),
        x:     0,
        y:     0,
      })
    }
    const min  = Math.min(...pts.map(p => p.val))
    const max  = Math.max(...pts.map(p => p.val))
    const rng  = max - min || 1
    const xStep = svgW / (pts.length - 1)
    pts.forEach((p, i) => {
      p.x = i * xStep
      p.y = padT + (1 - (p.val - min) / rng) * (svgH - padT - padB)
    })
    return pts
  })
  
  const linePath = computed(() => {
    if (chartPoints.value.length < 2) return ''
    return chartPoints.value.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ')
  })
  
  const areaPath = computed(() => {
    if (chartPoints.value.length < 2) return ''
    const pts = chartPoints.value
    const bottom = svgH - padB
    const first = pts[0]
    const last  = pts[pts.length - 1]
    if (!first || !last) return ''
    return `${linePath.value} L${last.x},${bottom} L${first.x},${bottom} Z`
  })
  
  // ── Helpers ───────────────────────────────────────────────────────────────────
  function formatAmount(v: number): string {
    if (!v && v !== 0) return '0.00'
    if (v >= 1_000_000) return (v / 1_000_000).toFixed(2) + 'M'
    if (v >= 1_000) return v.toLocaleString('en-MY', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
    return v.toFixed(2)
  }
  function formatDate(d: string): string {
    return new Date(d).toLocaleDateString('en-MY', { day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase()
  }
  function typeIcon(t: string) { return accountTypes.find(a => a.value === t)?.icon ?? '' }
  function chipClass(t: string) { return { bank: 'sov-chip--ox', ewallet: 'sov-chip--ghost', cash: 'sov-chip--amber' }[t] ?? 'sov-chip--ghost' }
  
  function openEditModal() {
    if (!account.value) return
    Object.assign(form, {
      name: account.value.name,
      account_type: account.value.account_type,
      institution: account.value.institution ?? '',
      notes: account.value.notes ?? '',
    })
    fErr.name = ''; submitErr.value = ''
    modalOpen.value = true
  }
  function closeModal() { modalOpen.value = false }
  
  async function submitEdit() {
    fErr.name = ''; submitErr.value = ''
    if (!form.name.trim()) { fErr.name = 'Account name is required.'; return }
    submitting.value = true
    try {
      const updated = await updateAccount(account.value!.id, {
        name:         form.name.trim(),
        account_type: form.account_type as IAccount['account_type'],
        institution:  form.institution || null,
        notes:        form.notes || null,
      })
      account.value = updated
      closeModal()
    } catch (e: any) {
      submitErr.value = e?.message ?? 'Something went wrong.'
    } finally {
      submitting.value = false
    }
  }
  
  onMounted(async () => {
    const id = route.params.id as string
    try {
        const raw = await getAccount(id)
        account.value = { ...raw, balance: Number(raw.balance) }
        // TODO: fetch transactions
    } catch {
        account.value = null
    } finally {
        loading.value = false
    }
    })
</script>
  
<style scoped>
  .detail-root { min-height:100vh; background:var(--color-void); position:relative; }
  .detail-scroll { position:relative; z-index:1; overflow-y:auto; -webkit-overflow-scrolling:touch; }
  .detail-header { padding:20px 20px 0; }
  @media(min-width:840px) { .detail-header { padding:36px 36px 0; } }
  .detail-hdr-mobile { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
  .detail-hdr-desktop { display:none; }
  @media(min-width:840px) {
    .detail-hdr-mobile { display:none; }
    .detail-hdr-desktop { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
    .desk-right { display:flex; align-items:center; gap:12px; }
  }
  .detail-breadcrumb { display:flex; align-items:center; gap:8px; font-size:9px; letter-spacing:2px; }
  .breadcrumb-link { color:var(--color-gun); text-decoration:none; transition:color .18s; }
  .breadcrumb-link:hover { color:var(--color-ox); }
  .breadcrumb-sep { color:rgba(224,224,224,.12); }
  .breadcrumb-cur { color:rgba(224,224,224,.45); }
  .desk-date { display:flex; align-items:center; gap:5px; font-size:9px; letter-spacing:1px; color:var(--color-gun); padding:5px 12px; background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:100px; }
  .desk-avatar { width:32px; height:32px; border-radius:50%; background:var(--color-ox-lo); border:1px solid var(--color-ox-md); display:flex; align-items:center; justify-content:center; font-size:9.5px; color:rgba(224,224,224,.7); font-family:var(--font-mono); }
  .notif-btn { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:rgba(224,224,224,.05); border:1px solid rgba(224,224,224,.08); color:var(--color-gun); cursor:pointer; transition:all .18s; }
  .notif-btn:hover { color:var(--color-plat); }
  .detail-section { padding:20px 20px 0; }
  @media(min-width:840px) { .detail-section { padding:24px 36px 0; } }
  .page-loading { display:flex; align-items:center; justify-content:center; padding:80px 20px; }
  .page-loading-inner { display:flex; flex-direction:column; align-items:center; gap:16px; }
  .loading-ring { width:28px; height:28px; border-radius:50%; border:2px solid var(--color-ox-lo); border-top-color:var(--color-ox-hi); animation:spin .8s linear infinite; }
  .loading-label { font-size:8.5px; letter-spacing:2.5px; color:var(--color-gun); }
  @keyframes spin { to { transform:rotate(360deg); } }
  .hero-card { padding:22px; position:relative; overflow:hidden; }
  .acct-bar-hero { position:absolute; left:0; top:0; bottom:0; width:3px; }
  .bar--ox { background:var(--color-ox); }
  .bar--tng { background:#1e90ff; }
  .bar--grab { background:#00b050; }
  .bar--slate { background:var(--color-gun); }
  .bar--bank { background:#6080c0; }
  .bar--ewallet { background:#1e90ff; }
  .bar--cash { background:#50a830; }
  .hero-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
  .hero-left { display:flex; align-items:center; gap:12px; }
  .acct-badge { width:40px; height:40px; border-radius:12px; flex-shrink:0; display:flex; align-items:center; justify-content:center; }
  .badge--ox { background:var(--color-ox-lo); border:1px solid var(--color-ox-md); color:rgba(200,60,80,.85); }
  .badge--tng { background:rgba(0,90,180,.12); border:1px solid rgba(0,100,200,.2); color:rgba(60,140,220,.85); }
  .badge--grab { background:rgba(0,130,60,.10); border:1px solid rgba(0,150,70,.2); color:rgba(0,180,80,.85); }
  .badge--slate { background:rgba(80,90,120,.12); border:1px solid rgba(100,110,160,.2); color:rgba(140,155,200,.8); }
  .badge--bank { background:rgba(80,100,180,.12); border:1px solid rgba(100,120,200,.2); color:rgba(140,160,220,.8); }
  .badge--ewallet { background:rgba(0,90,180,.12); border:1px solid rgba(0,100,200,.2); color:rgba(60,140,220,.85); }
  .badge--cash { background:rgba(60,140,40,.10); border:1px solid rgba(70,160,50,.2); color:rgba(80,180,60,.85); }
  .hero-name { font-size:13px; letter-spacing:.3px; color:rgba(224,224,224,.9); margin-bottom:3px; }
  .hero-meta { font-size:9px; letter-spacing:.3px; color:var(--color-gun); display:flex; align-items:center; gap:6px; }
  .acct-last4 { font-size:8.5px; letter-spacing:1.5px; color:rgba(224,224,224,.15); }
  .hero-chips { display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end; }
  .hero-bal-row { display:flex; align-items:flex-end; justify-content:space-between; margin-bottom:20px; }
  .hero-bal { font-size:clamp(1.8rem,6vw,2.8rem); color:var(--color-plat); line-height:1; letter-spacing:-.03em; }
  .hero-bal-ccy { font-size:11px; letter-spacing:.5px; color:var(--color-gun); margin-right:6px; vertical-align:super; }
  .hero-converted { text-align:right; }
  .hero-bal-conv { font-size:13px; letter-spacing:.2px; color:var(--color-gun); }
  .hero-footer { display:flex; align-items:center; justify-content:space-between; padding-top:16px; border-top:1px solid rgba(255,255,255,.05); }
  .hero-since { font-size:8.5px; letter-spacing:1.5px; color:rgba(224,224,224,.2); }
  .hero-actions { display:flex; gap:8px; }
  .section-hdr { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
  .chart-range-tabs { display:flex; gap:4px; }
  .range-tab { padding:4px 10px; font-size:8.5px; letter-spacing:1px; background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:6px; color:var(--color-gun); cursor:pointer; transition:all .18s; font-family:var(--font-mono); }
  .range-tab:hover { color:rgba(224,224,224,.6); }
  .range-tab--active { background:var(--color-ox-lo); border-color:var(--color-ox-md); color:rgba(200,80,100,.9); }
  .chart-card { padding:16px 16px 8px; }
  .chart-empty { height:120px; display:flex; align-items:center; justify-content:center; }
  .chart-svg { width:100%; height:120px; display:block; }
  .chart-labels { display:flex; justify-content:space-between; margin-top:6px; }
  .chart-label { font-size:7.5px; letter-spacing:.5px; color:var(--color-gun); }
  .stats-strip { display:flex; align-items:center; padding:18px 22px; overflow-x:auto; scrollbar-width:none; }
  .stats-strip::-webkit-scrollbar { display:none; }
  .stat-item { flex:1; display:flex; flex-direction:column; align-items:center; gap:5px; min-width:60px; }
  .stat-val { font-size:clamp(.9rem,3vw,1.3rem); color:var(--color-plat); line-height:1; letter-spacing:-.03em; }
  .summary-divider { width:1px; height:28px; flex-shrink:0; margin:0 4px; background:var(--color-glass-bo); }
  .txn-list { display:flex; flex-direction:column; gap:6px; }
  .txn-row { display:flex; align-items:center; gap:12px; padding:12px 16px; }
  .txn-icon { width:32px; height:32px; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
  .txn-icon--in { background:var(--color-grn-lo); border:1px solid rgba(76,175,80,.2); color:var(--color-grn); }
  .txn-icon--out { background:var(--color-red-lo); border:1px solid rgba(176,0,32,.2); color:var(--color-red); }
  .txn-info { flex:1; min-width:0; display:flex; flex-direction:column; gap:3px; }
  .txn-desc { font-size:11px; letter-spacing:.2px; color:rgba(224,224,224,.8); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .txn-date { font-size:8.5px; letter-spacing:.5px; color:var(--color-gun); }
  .txn-amt { font-size:11.5px; letter-spacing:.2px; flex-shrink:0; }
  .txn-amt--in { color:var(--color-grn); }
  .txn-amt--out { color:var(--color-red); }
  .empty-state { display:flex; flex-direction:column; align-items:center; gap:10px; padding:40px 24px; text-align:center; }
  .empty-icon-wrap { width:48px; height:48px; border-radius:14px; background:rgba(224,224,224,.03); border:1px solid var(--color-glass-bo); display:flex; align-items:center; justify-content:center; margin-bottom:4px; }
  .empty-title { font-size:10.5px; letter-spacing:1.2px; color:rgba(224,224,224,.4); text-transform:uppercase; }
  .sov-card { background:rgba(16,16,18,0.85); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); }
  .sov-label { font-size:8px; letter-spacing:1.8px; color:var(--color-gun); text-transform:uppercase; }
  .sov-chip { display:inline-flex; align-items:center; padding:2px 7px; border-radius:6px; font-size:7.5px; letter-spacing:1px; font-family:var(--font-mono); border:1px solid; }
  .sov-chip--ox { color:rgba(200,60,80,.8); background:var(--color-ox-lo); border-color:var(--color-ox-md); }
  .sov-chip--ghost { color:rgba(224,224,224,.4); background:rgba(255,255,255,.04); border-color:var(--color-glass-bo); }
  .sov-chip--amber { color:rgba(251,140,0,.8); background:var(--color-amb-lo); border-color:rgba(251,140,0,.18); }
  .sov-divider { border:none; border-top:1px solid var(--color-glass-bo); }
  .sov-btn { display:inline-flex; align-items:center; justify-content:center; gap:7px; border-radius:var(--radius-sm); font-family:var(--font-mono); font-size:11px; letter-spacing:1.4px; font-weight:500; text-transform:uppercase; cursor:pointer; transition:all .18s; padding:10px 20px; }
  .sov-btn--primary { background:var(--color-ox); border:1px solid var(--color-ox-md); color:rgba(255,255,255,.9); }
  .sov-btn--primary:hover:not(:disabled) { background:rgba(128,0,32,.9); }
  .sov-btn--primary:disabled { opacity:.5; cursor:not-allowed; }
  .sov-btn--ghost { background:rgba(255,255,255,.04); border:1px solid var(--color-glass-bo); color:rgba(224,224,224,.6); }
  .sov-btn--ghost:hover { border-color:rgba(255,255,255,.14); color:rgba(224,224,224,.85); }
  .sov-btn--icon { width:34px; height:34px; padding:0; border-radius:var(--radius-sm); }
  .sov-btn--sm { padding:7px 14px; font-size:9.5px; }
  .t-overline { font-size:8px; letter-spacing:2.5px; color:var(--color-gun); text-transform:uppercase; font-family:var(--font-mono); }
  .modal-backdrop { position:fixed; inset:0; z-index:200; background:rgba(8,8,8,.82); backdrop-filter:blur(8px); display:flex; align-items:flex-end; justify-content:center; }
  @media(min-width:600px) { .modal-backdrop { align-items:center; } }
  .modal-panel { background:var(--color-iron); border:1px solid var(--color-glass-bo); border-bottom:none; border-radius:28px 28px 0 0; width:100%; max-height:92vh; overflow-y:auto; padding:28px 24px 40px; }
  @media(min-width:600px) { .modal-panel { border-bottom:1px solid var(--color-glass-bo); border-radius:var(--radius-lg); max-width:460px; max-height:88vh; } }
  .modal-hdr { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:4px; gap:12px; }
  .modal-title { font-size:1.55rem; line-height:1; margin-top:5px; }
  .title-period { color:var(--color-ox); }
  .modal-form { display:flex; flex-direction:column; gap:20px; }
  .field-grp { display:flex; flex-direction:column; gap:8px; }
  .req { color:var(--color-ox); }
  .sov-input { background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); padding:10px 14px; color:rgba(224,224,224,.9); font-size:12px; letter-spacing:.3px; width:100%; outline:none; transition:border-color .18s; font-family:var(--font-mono); }
  .sov-input:focus { border-color:var(--color-ox-md); }
  .sov-textarea { resize:none; }
  .field-err { font-size:9px; letter-spacing:.5px; color:#ef5350; }
  .type-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; }
  .type-btn { display:flex; flex-direction:column; align-items:center; gap:7px; padding:12px 8px; font-size:9px; letter-spacing:1px; background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); color:var(--color-gun); cursor:pointer; transition:all .18s; }
  .type-btn:hover { border-color:rgba(255,255,255,.12); color:rgba(224,224,224,.6); }
  .type-btn--active { background:var(--color-ox-lo); border-color:var(--color-ox-md); color:rgba(200,80,100,.9); }
  .modal-actions { display:flex; gap:10px; margin-top:12px; }
  .sov-nudge { display:flex; align-items:center; gap:8px; padding:10px 14px; border-radius:10px; font-size:9.5px; letter-spacing:.3px; font-family:var(--font-mono); }
  .sov-nudge--warn { background:var(--color-amb-lo); border:1px solid rgba(251,140,0,.18); color:rgba(251,140,0,.8); }
  .btn-spin { width:11px; height:11px; border-radius:50%; flex-shrink:0; border:1.5px solid rgba(255,255,255,.18); border-top-color:rgba(255,255,255,.8); animation:spin .7s linear infinite; }
  .modal-fade-enter-active,.modal-fade-leave-active { transition:opacity .22s ease; }
  .modal-fade-enter-from,.modal-fade-leave-to { opacity:0; }
  .modal-slide-enter-active { transition:transform .3s var(--ease), opacity .22s ease; }
  .modal-slide-leave-active { transition:transform .2s ease, opacity .18s ease; }
  .modal-slide-enter-from { transform:translateY(40px); opacity:0; }
  .modal-slide-leave-to { transform:translateY(20px); opacity:0; }
  @media(min-width:600px) {
    .modal-slide-enter-from { transform:scale(.96) translateY(10px); }
    .modal-slide-leave-to { transform:scale(.97) translateY(6px); }
  }
</style>