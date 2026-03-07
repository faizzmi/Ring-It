<template>
  <div class="accts-root">
    <div class="sov-ambient" aria-hidden="true">
      <div class="sov-orb sov-orb--1" />
      <div class="sov-orb sov-orb--2" />
      <div class="sov-grid-overlay" />
    </div>
    <div class="accts-scroll">
      <header class="accts-header">
        <div class="accts-hdr-mobile">
          <div class="accts-breadcrumb t-mono">
            <router-link to="/dashboard" class="breadcrumb-link">// VAULT</router-link>
            <span class="breadcrumb-sep">›</span>
            <span class="breadcrumb-cur">ACCOUNTS</span>
          </div>
          <button class="notif-btn">
            <svg width="18" height="18" viewBox="0 0 19 19" fill="none">
              <path d="M9.5 2.5a5.5 5.5 0 0 1 5.5 5.5v2.5l1.5 3H3L4.5 10.5V8a5.5 5.5 0 0 1 5-5.5" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7.5 15.5a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.35" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <div class="accts-hdr-desktop">
          <div class="accts-breadcrumb t-mono">
            <router-link to="/dashboard" class="breadcrumb-link">// VAULT</router-link>
            <span class="breadcrumb-sep">›</span>
            <span class="breadcrumb-cur">ACCOUNTS</span>
          </div>
          <div class="desk-right">
            <div class="desk-date t-mono">
              <svg width="11" height="11" viewBox="0 0 13 13" fill="none">
                <rect x="1.5" y="2.5" width="10" height="9" rx="2" stroke="currentColor" stroke-width="1.1"/>
                <path d="M4.5 1.5v2M8.5 1.5v2M1.5 5.5h10" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>
              </svg>
              {{ todayLabel }}
            </div>
            <button class="notif-btn">
              <svg width="18" height="18" viewBox="0 0 19 19" fill="none">
                <path d="M9.5 2.5a5.5 5.5 0 0 1 5.5 5.5v2.5l1.5 3H3L4.5 10.5V8a5.5 5.5 0 0 1 5-5.5" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7.5 15.5a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.35" stroke-linecap="round"/>
              </svg>
            </button>
            <div class="desk-avatar t-mono">{{ userInitial }}</div>
          </div>
        </div>
        <div class="accts-title-row">
          <div>
            <h1 class="accts-title t-display">Accounts<span class="title-period">.</span></h1>
            <p class="accts-subtitle t-mono">{{ activeCount }} active <span class="subtitle-sep">·</span> MYR {{ formatAmount(totalBalance) }}</p>
          </div>
          <button class="sov-btn sov-btn--primary" @click="openCreateModal">
            <svg width="12" height="12" viewBox="0 0 13 13" fill="none">
              <path d="M6.5 2v9M2 6.5h9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
            NEW ACCOUNT
          </button>
        </div>
      </header>

      <div v-if="loading" class="page-loading">
        <div class="page-loading-inner">
          <div class="loading-ring" />
          <span class="t-mono loading-label">LOADING VAULT</span>
        </div>
      </div>

      <template v-else>
        <section class="accts-section">
          <div class="summary-strip sov-card">
            <div class="summary-item">
              <span class="summary-val t-display">{{ activeCount }}</span>
              <span class="sov-label">ACCOUNTS</span>
            </div>
            <div class="summary-divider" />
            <div class="summary-item">
              <span class="summary-val t-display">{{ formatAmount(totalBalance) }}</span>
              <span class="sov-label">TOTAL · MYR</span>
            </div>
            <div class="summary-divider" />
            <div class="summary-item">
              <span class="summary-val t-display">{{ bankAccounts.length }}</span>
              <span class="sov-label">BANKS</span>
            </div>
            <div class="summary-divider" />
            <div class="summary-item">
              <span class="summary-val t-display">{{ ewalletAccounts.length }}</span>
              <span class="sov-label">WALLETS</span>
            </div>
          </div>
        </section>

        <section class="accts-section accts-section--nb">
          <div class="filter-tabs">
            <button v-for="tab in tabs" :key="tab.value" class="filter-tab t-mono" :class="{ 'filter-tab--active': activeTab === tab.value }" @click="activeTab = tab.value">
              {{ tab.label }}
              <span class="tab-badge">{{ tab.count }}</span>
            </button>
          </div>
        </section>

        <section v-if="error" class="accts-section">
          <div class="sov-nudge sov-nudge--warn">
            <svg width="11" height="11" viewBox="0 0 12 12" fill="none">
              <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.1"/>
              <path d="M6 4v3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
              <circle cx="6" cy="9" r=".6" fill="currentColor"/>
            </svg>
            {{ error }}
          </div>
        </section>

        <section class="accts-section">
          <div v-if="filteredAccounts.length === 0" class="empty-state sov-card">
            <div class="empty-icon-wrap">
              <svg width="26" height="26" viewBox="0 0 28 28" fill="none">
                <rect x="3" y="7" width="22" height="16" rx="4" stroke="rgba(224,224,224,0.15)" stroke-width="1.4"/>
                <path d="M3 12h22" stroke="rgba(224,224,224,0.15)" stroke-width="1.4"/>
                <circle cx="8" cy="17.5" r="1.5" fill="rgba(224,224,224,0.08)"/>
              </svg>
            </div>
            <p class="t-mono empty-title">No {{ activeTab === 'all' ? '' : activeTab + ' ' }}accounts yet</p>
            <p class="t-mono" style="font-size:9.5px;color:var(--color-gun);line-height:1.7;text-align:center;max-width:220px">Add your first account to start tracking your wealth vault.</p>
            <button class="sov-btn sov-btn--ghost sov-btn--sm" style="margin-top:4px" @click="openCreateModal">
              <svg width="11" height="11" viewBox="0 0 13 13" fill="none">
                <path d="M6.5 2v9M2 6.5h9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              </svg>
              ADD ACCOUNT
            </button>
          </div>
          <div v-else class="accts-list">
            <div v-for="account in filteredAccounts" :key="account.id" class="acct-row sov-card" @click="goToAccount(account)">
              <div class="acct-bar" :class="`bar--${account.theme}`" />
              <div class="acct-badge" :class="`badge--${account.theme}`">
                <span v-html="typeIcon(account.account_type)" />
              </div>
              <div class="acct-info">
                <div class="acct-name-row">
                  <span class="acct-name t-mono">{{ account.name }}</span>
                  <span class="sov-chip" :class="chipClass(account.account_type)">{{ account.account_type.toUpperCase() }}</span>
                </div>
                <span class="acct-meta t-mono">{{ account.institution || '—' }} <span class="acct-last4">•••• {{ account.last4 }}</span></span>
              </div>
              <div class="acct-bal">
                <span class="sov-amount"><span class="sov-amount__ccy">{{ account.currency }}</span>{{ formatAmount(account.balance) }}</span>
              </div>
              <div class="acct-actions" @click.stop>
                <button class="sov-btn sov-btn--icon sov-btn--ghost action-btn" title="Edit" @click="openEditModal(account)">
                  <svg width="12" height="12" viewBox="0 0 13 13" fill="none">
                    <path d="M9.5 2.5l1 1-7 7-1.5.5.5-1.5 7-7Z" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button class="sov-btn sov-btn--icon action-btn action-btn--del" title="Delete" @click="confirmDelete(account)">
                  <svg width="12" height="12" viewBox="0 0 13 13" fill="none">
                    <path d="M2.5 4h8M5 4V2.5h3V4M10 4l-.5 7h-6L3 4" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              <svg width="13" height="13" viewBox="0 0 14 14" fill="none" class="acct-caret">
                <path d="M5 3.5l3.5 3.5L5 10.5" stroke="rgba(224,224,224,0.18)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="acct-row acct-row--add" @click="openCreateModal">
              <div class="add-inner">
                <div class="add-icon">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                    <path d="M8 3v10M3 8h10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
                  </svg>
                </div>
                <span class="t-mono" style="font-size:9px;letter-spacing:2px;color:rgba(224,224,224,0.2)">ADD NEW ACCOUNT</span>
              </div>
            </div>
          </div>
        </section>
      </template>
      <div style="height:48px" />
    </div>

    <Transition name="modal-fade">
      <div v-if="modalOpen" class="modal-backdrop" @click.self="closeModal">
        <Transition name="modal-slide">
          <div v-if="modalOpen" class="modal-panel">
            <div class="modal-hdr">
              <div>
                <span class="t-overline">{{ isEdit ? '// EDIT ACCOUNT' : '// NEW ACCOUNT' }}</span>
                <h2 class="modal-title t-display">{{ isEdit ? 'Edit' : 'New' }} Account<span class="title-period">.</span></h2>
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
                <input v-model="form.name" class="sov-input" type="text" placeholder="e.g. Maybank Savings" maxlength="100" autofocus />
                <span v-if="fErr.name" class="field-err t-mono">{{ fErr.name }}</span>
              </div>
              <div class="field-grp">
                <label class="sov-label">ACCOUNT TYPE <span class="req">*</span></label>
                <div class="type-grid">
                  <button v-for="t in accountTypes" :key="t.value" type="button" class="type-btn t-mono" :class="{ 'type-btn--active': form.account_type === t.value }" @click="form.account_type = t.value as IAccount['account_type']">
                    <span v-html="t.icon" />{{ t.label }}
                  </button>
                </div>
              </div>
              <div class="field-grp">
                <label class="sov-label">INSTITUTION</label>
                <input v-model="form.institution" class="sov-input" type="text" :placeholder="instPlaceholder" maxlength="100" />
              </div>
              <div class="field-grp">
                <label class="sov-label">CURRENCY</label>
                <div class="ccy-row">
                  <button v-for="c in currencies" :key="c" type="button" class="ccy-btn t-mono" :class="{ 'ccy-btn--active': form.currency === c }" @click="form.currency = c">{{ c }}</button>
                </div>
              </div>
              <div v-if="!isEdit" class="field-grp">
                <label class="sov-label">OPENING BALANCE</label>
                <div class="amt-wrap">
                  <span class="amt-prefix t-mono">{{ form.currency }}</span>
                  <input v-model="form.opening_balance" class="sov-input sov-input--amt" type="number" min="0" step="0.01" placeholder="0.00" />
                </div>
                <span class="field-hint t-mono">Current balance in this account right now.</span>
              </div>
              <div class="field-grp">
                <label class="sov-label">NOTES</label>
                <textarea v-model="form.notes" class="sov-input sov-textarea" rows="2" placeholder="Optional notes…" />
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
                <button type="button" class="sov-btn sov-btn--primary" style="flex:2" :disabled="submitting" @click="submitForm">
                  <span v-if="submitting" class="btn-spin" />
                  {{ isEdit ? 'SAVE CHANGES' : 'CREATE ACCOUNT' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>

    <Transition name="modal-fade">
      <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null">
        <Transition name="modal-slide">
          <div v-if="deleteTarget" class="modal-panel modal-panel--sm">
            <div class="modal-hdr">
              <div>
                <span class="t-overline" style="color:#ef5350">// CONFIRM DELETE</span>
                <h2 class="modal-title t-display" style="font-size:1.3rem">Remove Account<span class="title-period" style="color:#ef5350">.</span></h2>
              </div>
              <button class="sov-btn sov-btn--icon sov-btn--ghost" @click="deleteTarget = null">
                <svg width="13" height="13" viewBox="0 0 14 14" fill="none">
                  <path d="M2 2l10 10M12 2L2 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
            <hr class="sov-divider" style="margin:0 0 20px" />
            <div class="del-preview sov-card">
              <div class="acct-badge" :class="`badge--${deleteTarget.theme}`">
                <span v-html="typeIcon(deleteTarget.account_type)" />
              </div>
              <div>
                <p class="t-mono" style="font-size:11px;color:rgba(224,224,224,.8);margin-bottom:3px">{{ deleteTarget.name }}</p>
                <p class="t-mono" style="font-size:9px;color:var(--color-gun)">{{ deleteTarget.currency }} {{ formatAmount(deleteTarget.balance) }}</p>
              </div>
            </div>
            <p class="del-warn t-mono">{{ deleteTarget.balance > 0 ? 'This account has a balance — it will be deactivated and hidden. Transaction history is preserved.' : 'This account has no transactions and will be permanently removed from the vault.' }}</p>
            <div class="modal-actions" style="margin-top:0">
              <button class="sov-btn sov-btn--ghost" style="flex:1" @click="deleteTarget = null">CANCEL</button>
              <button class="btn-danger" style="flex:2" :disabled="deleting" @click="executeDelete">
                <span v-if="deleting" class="btn-spin" />
                {{ deleting ? 'REMOVING...' : 'CONFIRM DELETE' }}
              </button>
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
const route = useRoute()
const { user } = useAuth()
const {
  accounts, loading, error,
  totalBalance, activeCount,
  activeAccounts, bankAccounts, ewalletAccounts,
  fetchAccounts, createAccount, updateAccount, deleteAccount,
} = useAccount()

type TabValue = 'all' | 'bank' | 'ewallet' | 'cash'
const activeTab = ref<TabValue>('all')
const modalOpen = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const submitErr = ref('')
const editingId = ref<string | null>(null)
const deleteTarget = ref<IAccount | null>(null)
const deleting = ref(false)

const form = reactive({ name: '', account_type: 'bank' as IAccount['account_type'], currency: 'MYR' as 'MYR'|'USD'|'EUR'|'SGD'|'GBP', institution: '', notes: '', opening_balance: '' })
const fErr = reactive({ name: '' })

const accountTypes = [
  { value: 'bank', label: 'Bank', icon: `<svg width="14" height="14" viewBox="0 0 13 13" fill="none"><rect x="1.5" y="5" width="10" height="7" rx="2" stroke="currentColor" stroke-width="1.1"/><path d="M4 5V4a2.5 2.5 0 0 1 5 0v1" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/></svg>` },
  { value: 'ewallet', label: 'E-Wallet', icon: `<svg width="14" height="14" viewBox="0 0 13 13" fill="none"><rect x="1.5" y="3.5" width="10" height="7" rx="2" stroke="currentColor" stroke-width="1.1"/><circle cx="9" cy="7" r="1" fill="currentColor"/></svg>` },
  { value: 'cash', label: 'Cash', icon: `<svg width="14" height="14" viewBox="0 0 13 13" fill="none"><rect x="1.5" y="4" width="10" height="6" rx="1.5" stroke="currentColor" stroke-width="1.1"/><circle cx="6.5" cy="7" r="1.2" stroke="currentColor" stroke-width="1.1"/></svg>` },
]
const currencies = ['MYR', 'USD', 'EUR', 'SGD', 'GBP'] as const

const tabs = computed((): { value: TabValue; label: string; count: number }[] => [
  { value: 'all', label: 'ALL', count: activeAccounts.value.length },
  { value: 'bank', label: 'BANKS', count: bankAccounts.value.length },
  { value: 'ewallet', label: 'WALLETS', count: ewalletAccounts.value.length },
  { value: 'cash', label: 'CASH', count: accounts.value.filter((a: IAccount) => a.is_active && a.account_type === 'cash').length },
])
const filteredAccounts = computed(() =>
  activeTab.value === 'all' ? activeAccounts.value : activeAccounts.value.filter(a => a.account_type === activeTab.value)
)
const instPlaceholder = computed(() =>
  form.account_type === 'bank' ? 'e.g. Maybank, CIMB, RHB' : form.account_type === 'ewallet' ? "e.g. Touch 'n Go, GrabPay" : 'Optional'
)
const todayLabel = computed(() =>
  new Date().toLocaleDateString('en-MY', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase()
)
const userInitial = computed(() => {
  const n = user.value?.full_name || ''
  return n.split(' ').map((w: string) => w[0]).slice(0, 2).join('').toUpperCase() || 'V'
})

function formatAmount(v: number): string {
  if (!v && v !== 0) return '0.00'
  if (v >= 1_000_000) return (v / 1_000_000).toFixed(2) + 'M'
  if (v >= 1_000) return v.toLocaleString('en-MY', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
  return v.toFixed(2)
}
function typeIcon(t: string) { return accountTypes.find(a => a.value === t)?.icon ?? '' }
function chipClass(t: string) { return { bank: 'sov-chip--ox', ewallet: 'sov-chip--ghost', cash: 'sov-chip--amber' }[t] ?? 'sov-chip--ghost' }
function resetForm() {
  Object.assign(form, { name: '', account_type: 'bank', currency: 'MYR', institution: '', notes: '', opening_balance: '' })
  fErr.name = ''; submitErr.value = ''; editingId.value = null
}
function openCreateModal() { resetForm(); isEdit.value = false; modalOpen.value = true }
function openEditModal(a: IAccount) {
  resetForm(); isEdit.value = true; editingId.value = a.id
  Object.assign(form, { name: a.name, account_type: a.account_type, currency: a.currency, institution: a.institution ?? '', notes: a.notes ?? '' })
  modalOpen.value = true
}
function closeModal() { modalOpen.value = false; setTimeout(resetForm, 300) }
function goToAccount(a: IAccount) { router.push(`/dashboard/accounts/${a.id}`) }

async function submitForm() {
  fErr.name = ''; submitErr.value = ''
  if (!form.name.trim()) { fErr.name = 'Account name is required.'; return }
  submitting.value = true
  try {
    if (isEdit.value && editingId.value) {
      await updateAccount(editingId.value, { name: form.name.trim(), account_type: form.account_type, currency: form.currency, institution: form.institution || null, notes: form.notes || null })
    } else {
      await createAccount({ name: form.name.trim(), account_type: form.account_type, currency: form.currency, institution: form.institution || null, notes: form.notes || null, opening_balance: parseFloat(form.opening_balance || '0') || 0 })
    }
    closeModal()
  } catch (e: any) {
    submitErr.value = e?.response?.data?.detail ?? 'Something went wrong. Please try again.'
  } finally { submitting.value = false }
}

function confirmDelete(a: IAccount) { deleteTarget.value = a }
async function executeDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try { await deleteAccount(deleteTarget.value.id); deleteTarget.value = null }
  catch { deleteTarget.value = null }
  finally { deleting.value = false }
}

onMounted(async () => {
  await fetchAccounts()
  if (route.query.new === '1') openCreateModal()
})
</script>

<style scoped>
.accts-root { min-height:100vh; background:var(--color-void); position:relative; }
.accts-scroll { position:relative; z-index:1; overflow-y:auto; -webkit-overflow-scrolling:touch; }
.accts-header { padding:20px 20px 0; }
@media(min-width:840px) { .accts-header { padding:36px 36px 0; } }
.accts-hdr-mobile { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
.accts-hdr-desktop { display:none; }
@media(min-width:840px) {
  .accts-hdr-mobile { display:none; }
  .accts-hdr-desktop { display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }
  .desk-right { display:flex; align-items:center; gap:12px; }
}
.accts-breadcrumb { display:flex; align-items:center; gap:8px; font-size:9px; letter-spacing:2px; }
.breadcrumb-link { color:var(--color-gun); text-decoration:none; transition:color .18s; }
.breadcrumb-link:hover { color:var(--color-ox); }
.breadcrumb-sep { color:rgba(224,224,224,.12); }
.breadcrumb-cur { color:rgba(224,224,224,.45); }
.desk-date { display:flex; align-items:center; gap:5px; font-size:9px; letter-spacing:1px; color:var(--color-gun); padding:5px 12px; background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:100px; }
.desk-avatar { width:32px; height:32px; border-radius:50%; background:var(--color-ox-lo); border:1px solid var(--color-ox-md); display:flex; align-items:center; justify-content:center; font-size:9.5px; color:rgba(224,224,224,.7); font-family:var(--font-mono); }
.notif-btn { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:rgba(224,224,224,.05); border:1px solid rgba(224,224,224,.08); color:var(--color-gun); cursor:pointer; transition:all .18s; }
.notif-btn:hover { color:var(--color-plat); }
.accts-title-row { display:flex; align-items:flex-end; justify-content:space-between; padding:16px 0 22px; border-bottom:1px solid rgba(255,255,255,.05); }
.accts-title { font-size:clamp(2rem,7vw,2.6rem); color:var(--color-plat); line-height:1; margin-bottom:6px; }
.title-period { color:var(--color-ox); }
.accts-subtitle { font-size:9.5px; letter-spacing:1.2px; color:var(--color-gun); }
.subtitle-sep { opacity:.4; margin:0 4px; }
.accts-section { padding:20px 20px 0; }
.accts-section--nb { padding-bottom:0; }
@media(min-width:840px) { .accts-section { padding:24px 36px 0; } }
.page-loading { display:flex; align-items:center; justify-content:center; padding:80px 20px; }
.page-loading-inner { display:flex; flex-direction:column; align-items:center; gap:16px; }
.loading-ring { width:28px; height:28px; border-radius:50%; border:2px solid var(--color-ox-lo); border-top-color:var(--color-ox-hi); animation:spin .8s linear infinite; }
.loading-label { font-size:8.5px; letter-spacing:2.5px; color:var(--color-gun); }
@keyframes spin { to { transform:rotate(360deg); } }
.summary-strip { display:flex; align-items:center; padding:18px 22px; overflow-x:auto; scrollbar-width:none; }
.summary-strip::-webkit-scrollbar { display:none; }
.summary-item { flex:1; display:flex; flex-direction:column; align-items:center; gap:5px; min-width:60px; }
.summary-val { font-size:clamp(.95rem,3.5vw,1.4rem); color:var(--color-plat); line-height:1; letter-spacing:-.03em; }
.summary-divider { width:1px; height:28px; flex-shrink:0; margin:0 4px; background:var(--color-glass-bo); }
.filter-tabs { display:flex; gap:4px; overflow-x:auto; scrollbar-width:none; padding:16px 0 0; }
.filter-tabs::-webkit-scrollbar { display:none; }
.filter-tab { display:inline-flex; align-items:center; gap:6px; padding:6px 14px; font-size:9px; letter-spacing:1.5px; color:var(--color-gun); background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:100px; cursor:pointer; transition:all .18s; white-space:nowrap; }
.filter-tab:hover { color:rgba(224,224,224,.6); border-color:rgba(255,255,255,.1); }
.filter-tab--active { color:rgba(224,224,224,.9); background:var(--color-ox-lo); border-color:var(--color-ox-md); }
.tab-badge { display:inline-flex; align-items:center; justify-content:center; width:16px; height:16px; border-radius:50%; font-size:7.5px; background:rgba(224,224,224,.07); }
.filter-tab--active .tab-badge { background:var(--color-ox-lo); color:rgba(200,80,100,.9); }
.accts-list { display:flex; flex-direction:column; gap:8px; }
.acct-row { display:flex; align-items:center; gap:12px; padding:14px 18px; cursor:pointer; position:relative; transition:transform 220ms var(--ease), box-shadow 220ms var(--ease); }
.acct-row:hover { transform:translateX(4px); box-shadow:-3px 0 0 0 var(--color-ox), 0 8px 28px rgba(0,0,0,.3); }
.acct-bar { position:absolute; left:0; top:8px; bottom:8px; width:3px; border-radius:2px; opacity:0; transition:opacity .18s; }
.acct-row:hover .acct-bar { opacity:1; }
.bar--ox { background:var(--color-ox); }
.bar--tng { background:#1e90ff; }
.bar--grab { background:#00b050; }
.bar--slate { background:var(--color-gun); }
.bar--bank { background:#6080c0; }
.bar--ewallet { background:#1e90ff; }
.bar--cash { background:#50a830; }
.acct-badge { width:36px; height:36px; border-radius:11px; flex-shrink:0; display:flex; align-items:center; justify-content:center; }
.badge--ox { background:var(--color-ox-lo); border:1px solid var(--color-ox-md); color:rgba(200,60,80,.85); }
.badge--tng { background:rgba(0,90,180,.12); border:1px solid rgba(0,100,200,.2); color:rgba(60,140,220,.85); }
.badge--grab { background:rgba(0,130,60,.10); border:1px solid rgba(0,150,70,.2); color:rgba(0,180,80,.85); }
.badge--slate { background:rgba(80,90,120,.12); border:1px solid rgba(100,110,160,.2); color:rgba(140,155,200,.8); }
.badge--bank { background:rgba(80,100,180,.12); border:1px solid rgba(100,120,200,.2); color:rgba(140,160,220,.8); }
.badge--ewallet { background:rgba(0,90,180,.12); border:1px solid rgba(0,100,200,.2); color:rgba(60,140,220,.85); }
.badge--cash { background:rgba(60,140,40,.10); border:1px solid rgba(70,160,50,.2); color:rgba(80,180,60,.85); }
.acct-info { flex:1; min-width:0; display:flex; flex-direction:column; gap:4px; }
.acct-name-row { display:flex; align-items:center; gap:8px; }
.acct-name { font-size:11.5px; letter-spacing:.3px; color:rgba(224,224,224,.85); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.acct-meta { font-size:9px; letter-spacing:.3px; color:var(--color-gun); display:flex; align-items:center; gap:6px; }
.acct-last4 { font-size:8.5px; letter-spacing:1.5px; color:rgba(224,224,224,.15); }
.acct-bal { flex-shrink:0; }
.acct-actions { display:flex; gap:4px; flex-shrink:0; }
.action-btn { width:28px!important; height:28px!important; padding:0!important; border-radius:8px!important; }
.action-btn--del { background:rgba(239,83,80,.05)!important; border-color:rgba(239,83,80,.1)!important; color:rgba(239,83,80,.35)!important; }
.action-btn--del:hover { color:#ef5350!important; border-color:rgba(239,83,80,.28)!important; background:rgba(239,83,80,.1)!important; }
.acct-caret { flex-shrink:0; }
.acct-row--add { border:1.5px dashed var(--color-glass-bo)!important; background:rgba(224,224,224,.01)!important; justify-content:center; padding:18px; cursor:pointer; }
.acct-row--add:hover { border-color:var(--color-ox-md)!important; background:var(--color-ox-lo)!important; transform:none!important; box-shadow:none!important; }
.add-inner { display:flex; align-items:center; gap:12px; }
.add-icon { width:30px; height:30px; border-radius:50%; background:rgba(224,224,224,.04); border:1px solid rgba(224,224,224,.09); display:flex; align-items:center; justify-content:center; color:rgba(224,224,224,.2); }
.empty-state { display:flex; flex-direction:column; align-items:center; gap:10px; padding:52px 24px; text-align:center; }
.empty-icon-wrap { width:52px; height:52px; border-radius:14px; background:rgba(224,224,224,.03); border:1px solid var(--color-glass-bo); display:flex; align-items:center; justify-content:center; margin-bottom:6px; }
.empty-title { font-size:10.5px; letter-spacing:1.2px; color:rgba(224,224,224,.4); text-transform:uppercase; }
.sov-card { background:rgba(16,16,18,0.85); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); }
.sov-label { font-size:8px; letter-spacing:1.8px; color:var(--color-gun); text-transform:uppercase; }
.sov-chip { display:inline-flex; align-items:center; padding:2px 7px; border-radius:6px; font-size:7.5px; letter-spacing:1px; font-family:var(--font-mono); border:1px solid; }
.sov-chip--ox { color:rgba(200,60,80,.8); background:var(--color-ox-lo); border-color:var(--color-ox-md); }
.sov-chip--ghost { color:rgba(224,224,224,.4); background:rgba(255,255,255,.04); border-color:var(--color-glass-bo); }
.sov-chip--amber { color:rgba(251,140,0,.8); background:var(--color-amb-lo); border-color:rgba(251,140,0,.18); }
.sov-amount { font-size:13px; letter-spacing:-.02em; color:rgba(224,224,224,.9); font-family:var(--font-heading); }
.sov-amount__ccy { font-size:9px; letter-spacing:.5px; color:var(--color-gun); margin-right:3px; font-family:var(--font-mono); }
.sov-nudge { display:flex; align-items:center; gap:8px; padding:10px 14px; border-radius:10px; font-size:9.5px; letter-spacing:.3px; font-family:var(--font-mono); }
.sov-nudge--warn { background:var(--color-amb-lo); border:1px solid rgba(251,140,0,.18); color:rgba(251,140,0,.8); }
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
.modal-panel--sm { max-height:unset; overflow:visible; }
.modal-hdr { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:4px; gap:12px; }
.modal-title { font-size:1.55rem; line-height:1; margin-top:5px; }
.modal-form { display:flex; flex-direction:column; gap:20px; }
.field-grp { display:flex; flex-direction:column; gap:8px; }
.req { color:var(--color-ox); }
.sov-input { background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); padding:10px 14px; color:rgba(224,224,224,.9); font-size:12px; letter-spacing:.3px; width:100%; outline:none; transition:border-color .18s; font-family:var(--font-mono); }
.sov-input:focus { border-color:var(--color-ox-md); }
.sov-input--amt { padding-left:46px; }
.sov-textarea { resize:none; }
.field-err { font-size:9px; letter-spacing:.5px; color:#ef5350; }
.field-hint { font-size:9px; letter-spacing:.3px; color:rgba(117,117,117,.7); }
.type-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; }
.type-btn { display:flex; flex-direction:column; align-items:center; gap:7px; padding:12px 8px; font-size:9px; letter-spacing:1px; background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); color:var(--color-gun); cursor:pointer; transition:all .18s; }
.type-btn:hover { border-color:rgba(255,255,255,.12); color:rgba(224,224,224,.6); }
.type-btn--active { background:var(--color-ox-lo); border-color:var(--color-ox-md); color:rgba(200,80,100,.9); }
.ccy-row { display:flex; gap:6px; flex-wrap:wrap; }
.ccy-btn { padding:6px 13px; font-size:9px; letter-spacing:1px; background:rgba(255,255,255,.03); border:1px solid var(--color-glass-bo); border-radius:8px; color:var(--color-gun); cursor:pointer; transition:all .18s; }
.ccy-btn:hover { border-color:rgba(255,255,255,.12); color:rgba(224,224,224,.6); }
.ccy-btn--active { background:var(--color-ox-lo); border-color:var(--color-ox-md); color:rgba(200,80,100,.9); }
.amt-wrap { position:relative; }
.amt-prefix { position:absolute; left:14px; top:50%; transform:translateY(-50%); font-size:9.5px; letter-spacing:.5px; color:var(--color-gun); pointer-events:none; }
.modal-actions { display:flex; gap:10px; margin-top:12px; }
.btn-danger { display:inline-flex; align-items:center; justify-content:center; gap:8px; background:var(--color-red-lo); border:1px solid rgba(239,83,80,.28); border-radius:var(--radius-sm); color:#ef5350; font-family:var(--font-mono); font-size:11px; letter-spacing:1.4px; font-weight:500; text-transform:uppercase; cursor:pointer; transition:all .18s; padding:10px 20px; }
.btn-danger:hover:not(:disabled) { background:rgba(239,83,80,.18); }
.btn-danger:disabled { opacity:.5; cursor:not-allowed; }
.btn-spin { width:11px; height:11px; border-radius:50%; flex-shrink:0; border:1.5px solid rgba(255,255,255,.18); border-top-color:rgba(255,255,255,.8); animation:spin .7s linear infinite; }
.del-preview { display:flex; align-items:center; gap:12px; padding:13px 15px; margin-bottom:14px; }
.del-warn { font-size:10px; letter-spacing:.2px; color:rgba(239,83,80,.65); line-height:1.7; margin-bottom:20px; }
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