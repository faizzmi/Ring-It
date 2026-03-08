<template>
  <div class="txns">
    <div class="txns-scroll">

      <header class="txns-header">
        <div class="txns-header-inner">
          <div>
            <p class="t-mono txns-sup">// LEDGER</p>
            <h1 class="t-display txns-title">Transactions<span class="txns-period">.</span></h1>
          </div>
          <div class="header-actions">
            <button class="import-btn" @click="openImportModal" title="Import CSV/XLSX">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 1v8M4 6l3 3 3-3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 10v1.5A1.5 1.5 0 003.5 13h7a1.5 1.5 0 001.5-1.5V10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              </svg>
              <span class="t-mono">IMPORT</span>
            </button>
            <button class="add-fab" @click="openModal()">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M9 3v12M3 9h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Segment Control -->
        <div class="segment-wrap">
          <div class="segment">
            <button class="segment-btn" :class="{ 'segment-btn--active': activeTab === 'ledger' }" @click="activeTab = 'ledger'">
              <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                <rect x="1" y="1" width="9" height="9" rx="1.5" stroke="currentColor" stroke-width="1.1"/>
                <path d="M3 4h5M3 6h5M3 8h3" stroke="currentColor" stroke-width="1" stroke-linecap="round"/>
              </svg>
              <span class="t-mono">LEDGER</span>
            </button>
            <button class="segment-btn" :class="{ 'segment-btn--active': activeTab === 'analytics' }" @click="activeTab = 'analytics'">
              <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                <path d="M1 9L3.5 6l2.5 2 3-5" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span class="t-mono">ANALYTICS</span>
            </button>
          </div>
        </div>
      </header>

      <!-- ══ LEDGER TAB ══ -->
      <template v-if="activeTab === 'ledger'">

        <!-- Summary -->
        <section class="txns-section">
          <div class="summary-grid">
            <div class="summary-stat">
              <div class="summary-stat-top">
                <div class="summary-icon summary-icon--green">
                  <svg width="11" height="11" viewBox="0 0 11 11" fill="none"><path d="M1 8L4 5l2.5 2.5L10 3" stroke="var(--color-grn)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <span class="t-mono summary-label">Income</span>
              </div>
              <span class="t-display summary-val">{{ formatAmount(calMonthIncome) }}</span>
              <span class="t-mono summary-sub">{{ calMonthLabel }}</span>
            </div>
            <div class="summary-stat">
              <div class="summary-stat-top">
                <div class="summary-icon summary-icon--red">
                  <svg width="11" height="11" viewBox="0 0 11 11" fill="none"><path d="M1 3L4 6l2.5-2.5L10 8" stroke="#ef5350" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <span class="t-mono summary-label">Expenses</span>
              </div>
              <span class="t-display summary-val">{{ formatAmount(calMonthExpenses) }}</span>
              <span class="t-mono summary-sub">{{ calMonthLabel }}</span>
            </div>
            <div class="summary-stat summary-stat--net">
              <div class="summary-stat-top">
                <div class="summary-icon" :class="calMonthNet >= 0 ? 'summary-icon--ox' : 'summary-icon--red'">
                  <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                    <path :d="calMonthNet >= 0 ? 'M5.5 9V2M2 5l3.5-3 3.5 3' : 'M5.5 2v7M2 6l3.5 3 3.5-3'" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="t-mono summary-label">Net</span>
              </div>
              <span class="t-display summary-val" :class="calMonthNet >= 0 ? 't-green' : 't-red'">
                {{ calMonthNet >= 0 ? '+' : '' }}{{ formatAmount(Math.abs(calMonthNet)) }}
              </span>
              <span class="t-mono summary-sub">{{ calTxnCount }} transactions</span>
            </div>
          </div>
        </section>

        <!-- Calendar -->
        <section class="txns-section" style="padding-top:0">
          <div class="cal-card sov-card">
            <div class="cal-hdr">
              <button class="cal-nav" @click="calPrev">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M7.5 2.5L4 6l3.5 3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
              <span class="t-mono cal-month-label">{{ calMonthLabel }}</span>
              <button class="cal-nav" @click="calNext">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M4.5 2.5L8 6l-3.5 3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
            </div>
            <div class="cal-grid">
              <div v-for="d in calDayHeaders" :key="d" class="cal-dow t-mono">{{ d }}</div>
              <div
                v-for="(cell, i) in calCells"
                :key="i"
                class="cal-cell"
                :class="{
                  'cal-cell--empty': cell.empty,
                  'cal-cell--today': cell.today,
                  'cal-cell--active': !cell.empty && cell.count > 0,
                }"
              >
                <template v-if="!cell.empty">
                  <span class="cal-day-num t-mono" :class="cell.today ? 'cal-day-num--today' : ''">{{ cell.day }}</span>
                  <span v-if="cell.income > 0" class="cal-inc t-mono">+{{ formatAmount(cell.income) }}</span>
                  <span v-if="cell.expense > 0" class="cal-exp t-mono">-{{ formatAmount(cell.expense) }}</span>
                  <span v-if="cell.count > 0" class="cal-count t-mono">{{ cell.count }}</span>
                </template>
              </div>
            </div>
          </div>
        </section>

        <!-- Chart -->
        <section class="txns-section">
          <div class="chart-card sov-card">
            <div class="chart-hdr">
              <span class="t-mono chart-title">// DAILY SPEND</span>
              <div class="chart-legend">
                <span class="legend-dot legend-dot--credit" /><span class="t-mono legend-label">Income</span>
                <span class="legend-dot legend-dot--debit" /><span class="t-mono legend-label">Expense</span>
              </div>
            </div>
            <div class="chart-wrap">
              <div class="chart-bars">
                <div v-for="bar in chartBars" :key="bar.day" class="chart-bar-group"
                  :class="{ 'chart-bar-group--active': bar.day === hoveredDay }"
                  @mouseenter="hoveredDay = bar.day" @mouseleave="hoveredDay = null">
                  <Transition name="tip">
                    <div v-if="hoveredDay === bar.day" class="bar-tip">
                      <span class="t-mono bar-tip-day">{{ bar.label }}</span>
                      <span v-if="bar.credit > 0" class="t-mono bar-tip-credit">+{{ formatAmount(bar.credit) }}</span>
                      <span v-if="bar.debit > 0" class="t-mono bar-tip-debit">-{{ formatAmount(bar.debit) }}</span>
                    </div>
                  </Transition>
                  <div class="bar-col">
                    <div class="bar-stack">
                      <div class="bar bar--credit" :style="{ height: barH(bar.credit) + 'px', opacity: bar.credit > 0 ? 1 : 0 }" />
                      <div class="bar bar--debit" :style="{ height: barH(bar.debit) + 'px', opacity: bar.debit > 0 ? 1 : 0 }" />
                    </div>
                    <span class="bar-day t-mono">{{ bar.shortDay }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Search + Filters -->
        <section class="txns-section" style="padding-bottom:12px">
          <div class="search-row">
            <div class="search-wrap">
              <svg class="search-icon" width="13" height="13" viewBox="0 0 13 13" fill="none">
                <circle cx="5.5" cy="5.5" r="4" stroke="currentColor" stroke-width="1.2"/>
                <path d="M8.5 8.5l3 3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
              </svg>
              <input v-model="searchQ" class="search-input t-mono" placeholder="Search transactions..." type="text"/>
              <button v-if="searchQ" class="search-clear" @click="searchQ = ''">
                <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
              </button>
            </div>
            <button class="filter-btn" :class="{ 'filter-btn--active': filtersOpen }" @click="filtersOpen = !filtersOpen">
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M1.5 3.5h10M3.5 6.5h6M5.5 9.5h2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
              <span class="t-mono" style="font-size:9px;letter-spacing:1px">FILTER</span>
              <span v-if="activeFilterCount > 0" class="filter-count">{{ activeFilterCount }}</span>
            </button>
          </div>
          <Transition name="drawer">
            <div v-if="filtersOpen" class="filter-drawer">
              <div class="filter-group">
                <span class="t-mono filter-group-label">TYPE</span>
                <div class="filter-pills">
                  <button v-for="opt in typeOpts" :key="opt.value" class="filter-pill t-mono"
                    :class="{ 'filter-pill--active': filterType === opt.value }"
                    @click="filterType = filterType === opt.value ? null : opt.value">{{ opt.label }}</button>
                </div>
              </div>
              <div class="filter-group">
                <span class="t-mono filter-group-label">ACCOUNT</span>
                <div class="filter-pills">
                  <button class="filter-pill t-mono" :class="{ 'filter-pill--active': filterAccount === null }" @click="filterAccount = null">All</button>
                  <button v-for="acc in activeAccounts" :key="acc.id" class="filter-pill t-mono"
                    :class="{ 'filter-pill--active': filterAccount === acc.id }"
                    @click="filterAccount = filterAccount === acc.id ? null : acc.id">{{ acc.name }}</button>
                </div>
              </div>
              <button v-if="activeFilterCount > 0" class="filter-reset t-mono" @click="resetFilters">Reset all filters</button>
            </div>
          </Transition>
        </section>

        <!-- Transaction List -->
        <section class="txns-section" style="padding-top:0;padding-bottom:40px">
          <div v-if="filteredTxns.length === 0" class="txns-empty">
            <div class="txns-empty-icon">
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                <circle cx="11" cy="11" r="9" stroke="rgba(224,224,224,0.1)" stroke-width="1.3"/>
                <path d="M7 11h8M11 7v8" stroke="rgba(224,224,224,0.12)" stroke-width="1.3" stroke-linecap="round"/>
              </svg>
            </div>
            <p class="t-mono" style="font-size:10px;color:var(--color-gun)">No transactions found</p>
            <button class="t-mono txns-empty-cta" @click="openModal()">+ Log one →</button>
          </div>
          <template v-else>
            <div v-for="group in groupedTxns" :key="group.date" class="txn-group">
              <div class="txn-group-hdr">
                <span class="t-mono txn-group-date">{{ group.label }}</span>
                <span class="t-mono txn-group-net" :class="group.net >= 0 ? 't-green' : 't-red'">
                  {{ group.net >= 0 ? '+' : '' }}{{ formatAmount(Math.abs(group.net)) }}
                </span>
              </div>
              <div class="txn-list sov-card">
                <div v-for="(txn, i) in group.items" :key="txn.id"
                  class="txn-row" :class="{ 'txn-row--last': i === group.items.length - 1 }"
                  @click="openModal(txn)">
                  <div class="txn-icon-wrap" :style="{ background: txnBg(txn) }">
                    <span v-html="txnIconSvg(txn)" />
                  </div>
                  <div class="txn-info">
                    <span class="txn-name t-mono">{{ txn.description }}</span>
                    <div class="txn-meta">
                      <span v-if="txn.subcategory" class="txn-chip t-mono">{{ txn.subcategory }}</span>
                      <span v-else-if="txn.category" class="txn-chip t-mono">{{ txn.category }}</span>
                      <span v-if="txn.account" class="txn-chip txn-chip--ghost t-mono">{{ txn.account.name }}</span>
                      <span v-if="txn.store" class="txn-chip txn-chip--ghost t-mono">{{ txn.store }}</span>
                    </div>
                  </div>
                  <div class="txn-right">
                    <span class="txn-amt t-mono" :class="txn.txn_type === 'income' ? 't-green' : 't-red'">
                      {{ txn.txn_type === 'income' ? '+' : '-' }}{{ formatAmount(parseFloat(txn.amount)) }}
                    </span>
                    <div class="txn-indicators">
                      <span v-if="txn.cloudinary_url" class="txn-ind" title="Receipt">
                        <svg width="8" height="8" viewBox="0 0 10 10" fill="none"><rect x="1" y="1" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.1"/><path d="M3 4h4M3 6h2.5" stroke="currentColor" stroke-width="1" stroke-linecap="round"/></svg>
                      </span>
                      <span v-if="txn.notes" class="txn-ind" title="Notes">
                        <svg width="8" height="8" viewBox="0 0 10 10" fill="none"><path d="M2 3h6M2 5h6M2 7h4" stroke="currentColor" stroke-width="1" stroke-linecap="round"/></svg>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </section>

      </template>

      <!-- ══ ANALYTICS TAB ══ -->
      <template v-else>

        <!-- Month context banner -->
        <section class="txns-section" style="padding-bottom:0">
          <div class="analytics-month-banner">
            <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
              <rect x="1" y="1.5" width="9" height="8" rx="1.5" stroke="currentColor" stroke-width="1.1"/>
              <path d="M3.5 1v1.5M7.5 1v1.5M1 4.5h9" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>
            </svg>
            <span class="t-mono">Showing analytics for <strong>{{ calMonthLabel }}</strong></span>
            <span class="t-mono analytics-month-hint">← Use calendar in Ledger tab to change month</span>
          </div>
        </section>

        <!-- Summary tiles -->
        <section class="txns-section">
          <div class="an-summary-row">
            <div class="an-tile">
              <span class="t-mono an-tile-label">INCOME</span>
              <span class="t-display an-tile-val t-green">{{ formatAmount(calMonthIncome) }}</span>
            </div>
            <div class="an-tile-div"/>
            <div class="an-tile">
              <span class="t-mono an-tile-label">EXPENSES</span>
              <span class="t-display an-tile-val t-red">{{ formatAmount(calMonthExpenses) }}</span>
            </div>
            <div class="an-tile-div"/>
            <div class="an-tile">
              <span class="t-mono an-tile-label">NET</span>
              <span class="t-display an-tile-val" :class="calMonthNet >= 0 ? 't-green' : 't-red'">
                {{ calMonthNet >= 0 ? '+' : '' }}{{ formatAmount(Math.abs(calMonthNet)) }}
              </span>
            </div>
          </div>
        </section>

        <!-- Spending by Division — Donut -->
        <section class="txns-section">
          <div class="an-hdr">
            <span class="t-mono section-tag">// SPENDING BY DIVISION</span>
            <span class="t-mono section-meta">{{ formatAmount(calMonthExpenses) }} total</span>
          </div>
          <div class="sov-card an-card">
            <div v-if="divisionData.length === 0" class="an-empty">
              <span class="t-mono">No expense data for {{ calMonthLabel }}</span>
            </div>
            <div v-else class="donut-layout">
              <div class="donut-wrap">
                <svg viewBox="0 0 120 120" class="donut-svg">
                  <circle cx="60" cy="60" r="46" fill="none" stroke="rgba(224,224,224,0.05)" stroke-width="14"/>
                  <circle
                    v-for="(seg, i) in donutSegments"
                    :key="i"
                    cx="60" cy="60" r="46"
                    fill="none"
                    :stroke="seg.color"
                    stroke-width="14"
                    stroke-linecap="butt"
                    :stroke-dasharray="`${seg.dash} ${seg.gap}`"
                    :stroke-dashoffset="seg.offset"
                  />
                  <text x="60" y="56" text-anchor="middle" font-size="7" fill="rgba(224,224,224,0.3)" font-family="var(--font-mono)" letter-spacing="1">EXPENSES</text>
                  <text x="60" y="68" text-anchor="middle" font-size="10" fill="rgba(224,224,224,0.85)" font-family="var(--font-display)" letter-spacing="-0.5">{{ formatAmount(calMonthExpenses) }}</text>
                </svg>
              </div>
              <div class="donut-legend">
                <div v-for="d in divisionData" :key="d.label" class="donut-legend-row">
                  <div class="donut-legend-left">
                    <span class="donut-dot" :style="{ background: d.color }"/>
                    <span class="t-mono donut-legend-label">{{ d.label.toUpperCase() }}</span>
                  </div>
                  <div class="donut-legend-right">
                    <span class="t-mono donut-legend-val">{{ formatAmount(d.amount) }}</span>
                    <span class="t-mono donut-legend-pct">{{ d.pct }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Spending by Subcategory -->
        <section class="txns-section">
          <div class="an-hdr">
            <span class="t-mono section-tag">// BY SUBCATEGORY</span>
            <span class="t-mono section-meta">Top {{ subcategoryData.length }}</span>
          </div>
          <div class="sov-card an-card">
            <div v-if="subcategoryData.length === 0" class="an-empty">
              <span class="t-mono">No subcategory data for {{ calMonthLabel }}</span>
            </div>
            <div v-else class="hbar-list">
              <div v-for="(item, i) in subcategoryData" :key="item.label" class="hbar-row">
                <div class="hbar-meta">
                  <div class="hbar-rank-wrap">
                    <span class="t-mono hbar-rank">{{ String(i + 1).padStart(2, '0') }}</span>
                    <span class="t-mono hbar-label">{{ item.label }}</span>
                  </div>
                  <div class="hbar-vals">
                    <span class="t-mono hbar-amt">{{ formatAmount(item.amount) }}</span>
                    <span class="t-mono hbar-pct">{{ item.pct }}%</span>
                  </div>
                </div>
                <div class="hbar-track">
                  <div class="hbar-fill" :style="{
                    width: item.pct + '%',
                    background: divisionColorFor(item.division),
                    boxShadow: `0 0 8px ${divisionColorFor(item.division)}44`,
                    transitionDelay: `${i * 40}ms`
                  }"/>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Top Merchants -->
        <section class="txns-section" style="padding-bottom:40px">
          <div class="an-hdr">
            <span class="t-mono section-tag">// TOP MERCHANTS</span>
            <span class="t-mono section-meta">Top {{ storeData.length }}</span>
          </div>
          <div class="sov-card an-card">
            <div v-if="storeData.length === 0" class="an-empty">
              <span class="t-mono">No merchant data for {{ calMonthLabel }}</span>
            </div>
            <div v-else class="hbar-list">
              <div v-for="(item, i) in storeData" :key="item.label" class="hbar-row">
                <div class="hbar-meta">
                  <div class="hbar-rank-wrap">
                    <span class="t-mono hbar-rank">{{ String(i + 1).padStart(2, '0') }}</span>
                    <span class="t-mono hbar-label">{{ item.label }}</span>
                  </div>
                  <div class="hbar-vals">
                    <span class="t-mono hbar-amt">{{ formatAmount(item.amount) }}</span>
                    <span class="t-mono hbar-count">{{ item.count }}x</span>
                  </div>
                </div>
                <div class="hbar-track">
                  <div class="hbar-fill hbar-fill--store" :style="{ width: item.pct + '%', transitionDelay: `${i * 40}ms` }"/>
                </div>
              </div>
            </div>
          </div>
        </section>

      </template>

    </div>

    <!-- ══ Transaction Modal ══ -->
    <Transition name="modal-fade">
      <div v-if="modalOpen" class="modal-overlay" @click.self="closeModal">
        <Transition name="modal-slide">
          <div v-if="modalOpen" class="modal">
            <div class="modal-hdr">
              <div>
                <p class="t-mono modal-sup">{{ isEditing ? '// EDIT' : '// NEW' }}</p>
                <h2 class="t-display modal-title">{{ isEditing ? 'Transaction' : 'Log Entry' }}</h2>
              </div>
              <button class="modal-close" @click="closeModal">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="type-toggle">
                <button class="type-btn" :class="{ 'type-btn--active type-btn--debit': form.txn_type === 'expense' }"
                  @click="form.txn_type = 'expense'; form.category = 'commitment'; form.subcategory = ''">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 3L5 6l2.5-2.5L11 8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <span class="t-mono">EXPENSE</span>
                </button>
                <button class="type-btn" :class="{ 'type-btn--active type-btn--credit': form.txn_type === 'income' }"
                  @click="form.txn_type = 'income'; form.category = 'income'; form.subcategory = ''">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 9L5 6l2.5 2.5L11 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <span class="t-mono">INCOME</span>
                </button>
              </div>
              <div class="field-group">
                <label class="field-label t-mono">AMOUNT</label>
                <div class="amount-wrap">
                  <span class="amount-ccy t-mono">{{ selectedAccountCurrency }}</span>
                  <input v-model="form.amount" class="amount-input t-display" type="number" min="0" step="0.01" placeholder="0.00" inputmode="decimal"/>
                </div>
                <div class="amount-underline" :class="form.txn_type === 'income' ? 'amount-underline--credit' : 'amount-underline--debit'" />
              </div>
              <div class="field-group">
                <label class="field-label t-mono">DESCRIPTION</label>
                <input v-model="form.description" class="field-input t-mono" type="text" placeholder="What was this for?"/>
              </div>
              <div class="field-row">
                <div class="field-group field-group--half">
                  <label class="field-label t-mono">ACCOUNT</label>
                  <div class="select-wrap">
                    <select v-model="form.account_id" class="field-select t-mono">
                      <option value="" disabled>Select...</option>
                      <option v-for="acc in activeAccounts" :key="acc.id" :value="acc.id">{{ acc.name }}</option>
                    </select>
                    <svg class="select-arrow" width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 4l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </div>
                </div>
                <div class="field-group field-group--half">
                  <label class="field-label t-mono">CATEGORY</label>
                  <div class="select-wrap">
                    <select v-model="form.category" class="field-select t-mono" @change="form.subcategory = ''">
                      <option v-for="cat in availableCategoryOpts" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
                    </select>
                    <svg class="select-arrow" width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 4l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </div>
                </div>
              </div>
              <div class="field-group">
                <label class="field-label t-mono">SUBCATEGORY</label>
                <div class="select-wrap">
                  <select v-model="form.subcategory" class="field-select t-mono">
                    <option value="">None</option>
                    <option v-for="sub in currentSubcategories" :key="sub.value" :value="sub.value">{{ sub.label }}</option>
                  </select>
                  <svg class="select-arrow" width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 4l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>
              <div class="field-row">
                <div class="field-group field-group--half">
                  <label class="field-label t-mono">STORE / MERCHANT</label>
                  <input v-model="form.store" class="field-input t-mono" type="text" placeholder="Optional"/>
                </div>
                <div class="field-group field-group--half">
                  <label class="field-label t-mono">DATE</label>
                  <input v-model="form.txn_date" class="field-input t-mono" type="date"/>
                </div>
              </div>
              <div class="field-group">
                <label class="field-label t-mono">NOTES</label>
                <input v-model="form.notes" class="field-input t-mono" type="text" placeholder="Optional"/>
              </div>
              <div class="field-group">
                <label class="field-label t-mono">RECEIPT</label>
                <div v-if="form.cloudinary_url" class="receipt-preview">
                  <a :href="form.cloudinary_url" target="_blank" rel="noopener" class="receipt-link t-mono">
                    <svg width="11" height="11" viewBox="0 0 10 10" fill="none"><rect x="1" y="1" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.1"/><path d="M3 4h4M3 6h2.5" stroke="currentColor" stroke-width="1" stroke-linecap="round"/></svg>
                    View receipt
                  </a>
                  <button class="receipt-remove t-mono" @click="form.cloudinary_url = null">Remove</button>
                </div>
                <label v-else class="receipt-drop" :class="{ 'receipt-drop--loading': uploadingReceipt }">
                  <input type="file" accept="image/*,application/pdf" style="display:none" :disabled="uploadingReceipt" @change="onReceiptPick"/>
                  <template v-if="uploadingReceipt">
                    <div class="btn-spinner" />
                    <span class="t-mono" style="font-size:9px;color:var(--color-gun)">Uploading {{ uploadProgress }}%</span>
                  </template>
                  <template v-else>
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1v8M4 6l3 3 3-3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 10v1.5A1.5 1.5 0 003.5 13h7a1.5 1.5 0 001.5-1.5V10" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
                    <span class="t-mono" style="font-size:9px;color:var(--color-gun)">Upload receipt (JPG, PNG, PDF · max 10MB)</span>
                  </template>
                </label>
                <p v-if="receiptError" class="receipt-error t-mono">{{ receiptError }}</p>
              </div>
              <div v-if="formError" class="form-error t-mono">
                <svg width="11" height="11" viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="currentColor" stroke-width="1"/><path d="M5.5 3.5v2.5" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/><circle cx="5.5" cy="8" r=".5" fill="currentColor"/></svg>
                {{ formError }}
              </div>
              <div class="modal-actions">
                <button v-if="isEditing" class="modal-btn modal-btn--delete" :disabled="submitting" @click="handleDelete">
                  <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M2 3.5h9M5 3.5V2.5h3v1M5.5 6v3.5M7.5 6v3.5M3 3.5l.5 7h6l.5-7" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  <span class="t-mono">{{ confirmDelete ? 'CONFIRM?' : 'DELETE' }}</span>
                </button>
                <button class="modal-btn modal-btn--submit" :disabled="submitting || !formValid" @click="handleSubmit">
                  <div v-if="submitting" class="btn-spinner" />
                  <span class="t-mono">{{ isEditing ? 'SAVE CHANGES' : 'LOG ENTRY' }}</span>
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>

    <!-- ══ Import Modal ══ -->
    <Transition name="modal-fade">
      <div v-if="importModalOpen" class="modal-overlay" @click.self="closeImportModal">
        <Transition name="modal-slide">
          <div v-if="importModalOpen" class="modal">
            <div class="modal-hdr">
              <div>
                <p class="t-mono modal-sup">// BULK</p>
                <h2 class="t-display modal-title">Import</h2>
              </div>
              <button class="modal-close" @click="closeImportModal">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="col-guide sov-card">
                <div class="col-guide-hdr">
                  <span class="t-mono col-guide-title">// COLUMN REFERENCE</span>
                  <button class="col-guide-toggle t-mono" @click="guideOpen = !guideOpen">
                    {{ guideOpen ? 'HIDE' : 'SHOW' }}
                    <svg width="8" height="8" viewBox="0 0 8 8" fill="none" :style="{ transform: guideOpen ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform .2s' }">
                      <path d="M1 2.5l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
                <Transition name="guide">
                  <div v-if="guideOpen" class="col-table-wrap">
                    <table class="col-table">
                      <thead>
                        <tr>
                          <th class="t-mono">COLUMN</th>
                          <th class="t-mono">REQ</th>
                          <th class="t-mono">ACCEPTED VALUES</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="col in importColumns" :key="col.name">
                          <td class="col-name t-mono">{{ col.name }}</td>
                          <td class="col-req">
                            <span class="req-badge t-mono" :class="col.required ? 'req-badge--yes' : 'req-badge--no'">
                              {{ col.required ? 'YES' : 'NO' }}
                            </span>
                          </td>
                          <td class="col-vals t-mono">{{ col.values }}</td>
                        </tr>
                      </tbody>
                    </table>
                    <div class="col-note">
                      <svg width="10" height="10" viewBox="0 0 10 10" fill="none" style="flex-shrink:0;margin-top:1px">
                        <circle cx="5" cy="5" r="4" stroke="var(--color-gun)" stroke-width="1"/>
                        <path d="M5 4v3" stroke="var(--color-gun)" stroke-width="1" stroke-linecap="round"/>
                        <circle cx="5" cy="3" r=".4" fill="var(--color-gun)"/>
                      </svg>
                      <span class="t-mono col-note-text">
                        Rows missing <strong>Date</strong> or <strong>Amount</strong> are skipped.
                        Unrecognised Type/Division fall back to defaults.
                        Column headers are case-insensitive.
                      </span>
                    </div>
                  </div>
                </Transition>
              </div>
              <div class="field-group">
                <label class="field-label t-mono">FILE</label>
                <label class="receipt-drop import-drop" :class="{ 'receipt-drop--loading': importLoading, 'import-drop--has-file': !!importFile }">
                  <input type="file" accept=".csv,.xlsx,.xls" style="display:none" :disabled="importLoading" @change="onImportFilePick"/>
                  <template v-if="importLoading"><div class="btn-spinner" /><span class="t-mono" style="font-size:9px;color:var(--color-gun)">Importing…</span></template>
                  <template v-else-if="importFile">
                    <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M2 6.5l3 3 6-6" stroke="var(--color-grn)" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <span class="t-mono" style="font-size:9px;color:rgba(224,224,224,0.7)">{{ importFile.name }}</span>
                  </template>
                  <template v-else>
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1v8M4 6l3 3 3-3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 10v1.5A1.5 1.5 0 003.5 13h7a1.5 1.5 0 001.5-1.5V10" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
                    <span class="t-mono" style="font-size:9px;color:var(--color-gun)">Choose CSV or XLSX file</span>
                  </template>
                </label>
              </div>
              <div class="field-group">
                <label class="field-label t-mono">DEFAULT ACCOUNT</label>
                <div class="select-wrap">
                  <select v-model="importAccountId" class="field-select t-mono">
                    <option value="" disabled>Select fallback account…</option>
                    <option v-for="acc in activeAccounts" :key="acc.id" :value="acc.id">{{ acc.name }}</option>
                  </select>
                  <svg class="select-arrow" width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 4l3 3 3-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
              </div>
              <div v-if="importResult" class="import-result">
                <div class="import-result-row">
                  <span class="t-mono import-result-ok">✓ {{ importResult.imported }} imported</span>
                  <span v-if="importResult.skipped > 0" class="t-mono import-result-skip">{{ importResult.skipped }} skipped</span>
                  <span v-if="importResult.errors.length > 0" class="t-mono import-result-err">{{ importResult.errors.length }} errors</span>
                </div>
                <div v-if="importResult.errors.length" class="import-errors">
                  <p v-for="r in importResult.errors.slice(0, 5)" :key="r.row" class="t-mono import-error-row">Row {{ r.row }}: {{ r.reason }}</p>
                </div>
              </div>
              <div v-if="importError" class="form-error t-mono">
                <svg width="11" height="11" viewBox="0 0 11 11" fill="none"><circle cx="5.5" cy="5.5" r="4.5" stroke="currentColor" stroke-width="1"/><path d="M5.5 3.5v2.5" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/><circle cx="5.5" cy="8" r=".5" fill="currentColor"/></svg>
                {{ importError }}
              </div>
              <div class="modal-actions">
                <button class="modal-btn modal-btn--submit" :disabled="!importFile || !importAccountId || importLoading" @click="handleImport">
                  <div v-if="importLoading" class="btn-spinner" />
                  <span class="t-mono">{{ importResult ? 'IMPORT ANOTHER' : 'RUN IMPORT' }}</span>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useAccount } from '@/composables/useAccounts'
import { useTransactions, type ITransaction, type ITransactionCreate, type ITransactionUpdate, type IBulkImportResponse } from '@/composables/useTransactions'
import { useCloudinaryUpload } from '@/composables/useCloudinaryUpload'

const route = useRoute()
const { user } = useAuth()
const { activeAccounts, fetchAccounts } = useAccount() as any
const {
  transactions,
  fetchTransactions, createTransaction, updateTransaction, deleteTransaction, importTransactions,
} = useTransactions()
const { uploadReceipt, uploading: uploadingReceipt, uploadProgress, error: uploadError } = useCloudinaryUpload()

// ── Tab ───────────────────────────────────────────────────────────────────────
const activeTab = ref<'ledger' | 'analytics'>('ledger')

// ── Category / subcategory definitions ───────────────────────────────────────
const allCategoryOpts = [
  { value: 'commitment', label: '🏠 Commitment', txnType: 'expense' },
  { value: 'want',       label: '🛍️ Want',       txnType: 'expense' },
  { value: 'savings',    label: '💰 Savings',    txnType: 'expense' },
  { value: 'income',     label: '💼 Income',     txnType: 'income'  },
]

const subcategoryMap: Record<string, { value: string; label: string }[]> = {
  commitment: [
    { value: 'Rent',             label: 'Rent'             },
    { value: 'Utilities',        label: 'Utilities'        },
    { value: 'Water',            label: 'Water'            },
    { value: 'Electric',         label: 'Electric'         },
    { value: 'Wifi',             label: 'Wifi'             },
    { value: 'Prepaid',          label: 'Prepaid'          },
    { value: 'Public Transport', label: 'Public Transport/Toll' },
    { value: 'Grab',             label: 'Grab'             },
    { value: 'Car Loan',         label: 'Car Loan'         },
    { value: 'Parking',          label: 'Parking'          },
    { value: 'Maintenance',      label: 'Maintenance'      },
    { value: 'Fuel',             label: 'Fuel'             },
    { value: 'Groceries',        label: 'Groceries'        },
    { value: 'Toiletries',       label: 'Toiletries'       },
    { value: 'Home Supplies',    label: 'Home Supplies'    },
    { value: 'Food',             label: 'Food'             },
    { value: 'Medical Card',     label: 'Medical Card'     },
    { value: 'PTPTN',            label: 'PTPTN'            },
    { value: 'Installment',      label: 'Installment'      },
    { value: 'Parent',           label: 'Parent'           },
  ],
  want: [
    { value: 'Self Rewards',     label: 'Self Rewards'     },
    { value: 'Gadget',           label: 'Gadget'           },
    { value: 'Fashion',          label: 'Fashion'          },
    { value: 'Self Care',        label: 'Self Care'        },
    { value: 'Trip',             label: 'Trip'             },
    { value: 'Craving',          label: 'Craving'          },
    { value: 'Treat',            label: 'Treat'            },
    { value: 'Home Appliances',  label: 'Home Appliances'  },
    { value: 'Subscription',     label: 'Subscription'     },
    { value: 'Movie',            label: 'Movie'            },
    { value: 'Entertainment',    label: 'Entertainment'    },
    { value: 'Haircuts',         label: 'Haircuts'         },
    { value: 'Cert',             label: 'Cert'             },
    { value: 'Misc',             label: 'Misc'             },
  ],
  savings: [
    { value: 'Hajj/Umrah',       label: 'Hajj/Umrah'      },
    { value: 'Emergency',        label: 'Emergency'        },
    { value: 'Goals',            label: 'Goals'            },
    { value: 'House',            label: 'House'            },
    { value: 'ASB',              label: 'ASB'              },
    { value: 'Gold',             label: 'Gold'             },
    { value: 'Wishlist Saving',  label: 'Wishlist Saving'  },
    { value: 'Sadaqah',          label: 'Sadaqah'          },
    { value: 'Investment',       label: 'Investment'       },
  ],
  income: [
    { value: 'Salary',           label: 'Salary'           },
    { value: 'Pocket Money',     label: 'Pocket Money'     },
    { value: 'Government Aid',   label: 'Government Aid'   },
    { value: 'Gift',             label: 'Gift'             },
  ],
}

const availableCategoryOpts = computed(() =>
  allCategoryOpts.filter(c => c.txnType === form.value.txn_type)
)
const currentSubcategories = computed(() => subcategoryMap[form.value.category] ?? [])

// ── Calendar ──────────────────────────────────────────────────────────────────
const calYear  = ref(new Date().getFullYear())
const calMonth = ref(new Date().getMonth())
const calDayHeaders = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

const calMonthLabel = computed(() =>
  new Date(calYear.value, calMonth.value, 1)
    .toLocaleDateString('en-MY', { month: 'long', year: 'numeric' })
)

function calPrev() {
  if (calMonth.value === 0) { calMonth.value = 11; calYear.value-- }
  else calMonth.value--
}
function calNext() {
  if (calMonth.value === 11) { calMonth.value = 0; calYear.value++ }
  else calMonth.value++
}

const calCells = computed(() => {
  const y = calYear.value
  const m = calMonth.value
  const firstDow = new Date(y, m, 1).getDay()
  const offset   = (firstDow + 6) % 7
  const daysInMonth = new Date(y, m + 1, 0).getDate()
  const today = new Date().toISOString().slice(0, 10)
  const dayMap = new Map<number, { income: number; expense: number; count: number }>()
  for (const txn of transactions.value) {
    const d = new Date(txn.txn_date + 'T00:00:00')
    if (d.getFullYear() !== y || d.getMonth() !== m) continue
    const day = d.getDate()
    const entry = dayMap.get(day) ?? { income: 0, expense: 0, count: 0 }
    const amt = parseFloat(txn.amount)
    if (txn.txn_type === 'income') entry.income += amt
    else entry.expense += amt
    entry.count++
    dayMap.set(day, entry)
  }
  const cells: { day: number; income: number; expense: number; count: number; empty: boolean; today: boolean }[] = []
  for (let i = 0; i < offset; i++)
    cells.push({ day: 0, income: 0, expense: 0, count: 0, empty: true, today: false })
  for (let d = 1; d <= daysInMonth; d++) {
    const iso = `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`
    const data = dayMap.get(d) ?? { income: 0, expense: 0, count: 0 }
    cells.push({ day: d, ...data, empty: false, today: iso === today })
  }
  return cells
})

// ── Filters ───────────────────────────────────────────────────────────────────
const searchQ       = ref('')
const filtersOpen   = ref(false)
const filterType    = ref<'income' | 'expense' | 'transfer' | null>(null)
const filterAccount = ref<string | null>(null)
const hoveredDay    = ref<string | null>(null)
const typeOpts = [{ label: 'Income', value: 'income' as const }, { label: 'Expense', value: 'expense' as const }, { label: 'Transfer', value: 'transfer' as const }]
const activeFilterCount = computed(() => (filterType.value ? 1 : 0) + (filterAccount.value ? 1 : 0))
function resetFilters() { filterType.value = null; filterAccount.value = null; searchQ.value = '' }

const filteredTxns = computed(() => {
  const y = calYear.value
  const m = calMonth.value
  const from = `${y}-${String(m + 1).padStart(2, '0')}-01`
  const to   = `${y}-${String(m + 1).padStart(2, '0')}-${String(new Date(y, m + 1, 0).getDate()).padStart(2, '0')}`
  let list = transactions.value.filter(t => t.txn_date >= from && t.txn_date <= to)
  if (filterType.value)    list = list.filter(t => t.txn_type === filterType.value)
  if (filterAccount.value) list = list.filter(t => t.account_id === filterAccount.value)
  const q = searchQ.value.toLowerCase().trim()
  if (q) list = list.filter(t =>
    (t.description ?? '').toLowerCase().includes(q) ||
    (t.store ?? '').toLowerCase().includes(q) ||
    ((t as any).subcategory ?? '').toLowerCase().includes(q) ||
    (t.category ?? '').toLowerCase().includes(q) ||
    (t.account?.name ?? '').toLowerCase().includes(q)
  )
  return [...list].sort((a, b) => { const d = b.txn_date.localeCompare(a.txn_date); return d !== 0 ? d : b.created_at.localeCompare(a.created_at) })
})

const groupedTxns = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10)
  const map = new Map<string, ITransaction[]>()
  for (const t of filteredTxns.value) { const arr = map.get(t.txn_date) ?? []; arr.push(t); map.set(t.txn_date, arr) }
  return [...map.entries()].map(([date, items]) => {
    const net = items.reduce((s, t) => { const a = parseFloat(t.amount); return t.txn_type === 'income' ? s + a : s - a }, 0)
    const label = date === today ? 'Today' : date === yesterday ? 'Yesterday' : new Date(date).toLocaleDateString('en-MY', { weekday: 'short', day: 'numeric', month: 'short' })
    return { date, label, items, net }
  })
})

// Month stats (shared between tabs)
const calMonthTxns     = computed(() => transactions.value.filter(t => { const d = new Date(t.txn_date + 'T00:00:00'); return d.getFullYear() === calYear.value && d.getMonth() === calMonth.value }))
const calMonthIncome   = computed(() => calMonthTxns.value.filter(t => t.txn_type === 'income').reduce((s, t) => s + parseFloat(t.amount), 0))
const calMonthExpenses = computed(() => calMonthTxns.value.filter(t => t.txn_type !== 'income').reduce((s, t) => s + parseFloat(t.amount), 0))
const calMonthNet      = computed(() => calMonthIncome.value - calMonthExpenses.value)
const calTxnCount      = computed(() => calMonthTxns.value.length)

// ── Chart ─────────────────────────────────────────────────────────────────────
const BAR_MAX_H = 52
const chartBars = computed(() => {
  const days: { day: string; date: string; label: string; shortDay: string; credit: number; debit: number }[] = []
  for (let i = 13; i >= 0; i--) {
    const d = new Date(Date.now() - i * 86_400_000); const iso = d.toISOString().slice(0, 10)
    days.push({ day: iso, date: iso, label: d.toLocaleDateString('en-MY', { weekday: 'short', day: 'numeric', month: 'short' }), shortDay: String(d.getDate()), credit: 0, debit: 0 })
  }
  for (const txn of transactions.value) {
    const bar = days.find(d => d.date === txn.txn_date); if (!bar) continue
    const amt = parseFloat(txn.amount)
    if (txn.txn_type === 'income') bar.credit += amt; else bar.debit += amt
  }
  return days
})
const chartMax = computed(() => Math.max(1, ...chartBars.value.map(b => Math.max(b.credit, b.debit))))
function barH(val: number) { return Math.round((val / chartMax.value) * BAR_MAX_H) }

// ── Analytics computed ────────────────────────────────────────────────────────
const DIVISION_COLORS: Record<string, string> = {
  commitment: '#800020',
  comitmment: '#800020',
  want:       '#FB8C00',
  savings:    '#4CAF50',
  income:     '#2196F3',
}
const DIVISION_DISPLAY: Record<string, string> = {
  commitment: 'Commitment',
  comitmment: 'Commitment',
  want:       'Want',
  savings:    'Savings',
  income:     'Income',
}

function divisionColorFor(div?: string): string {
  return DIVISION_COLORS[(div ?? '').toLowerCase()] ?? 'rgba(224,224,224,0.3)'
}

const expenseTxns = computed(() => calMonthTxns.value.filter(t => t.txn_type !== 'income'))

const divisionData = computed(() => {
  const map = new Map<string, number>()
  for (const t of expenseTxns.value) {
    const key = (t.category ?? 'other').toLowerCase()
    map.set(key, (map.get(key) ?? 0) + parseFloat(t.amount))
  }
  const total = calMonthExpenses.value || 1
  return [...map.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([key, amount]) => ({
      label: DIVISION_DISPLAY[key] ?? key,
      amount,
      pct: Math.round((amount / total) * 100),
      color: DIVISION_COLORS[key] ?? 'rgba(224,224,224,0.3)',
    }))
})

const CIRCUMFERENCE = 2 * Math.PI * 46
const donutSegments = computed(() => {
  const total = calMonthExpenses.value || 1
  let offset = CIRCUMFERENCE * 0.25
  return divisionData.value.map(d => {
    const dash = (d.amount / total) * CIRCUMFERENCE
    const gap  = CIRCUMFERENCE - dash
    const seg  = { color: d.color, dash, gap, offset: -offset + CIRCUMFERENCE }
    offset += dash
    return seg
  })
})

const subcategoryData = computed(() => {
  const map = new Map<string, { amount: number; division: string }>()
  for (const t of expenseTxns.value) {
    const key = (t as any).subcategory || t.category || 'Other'
    const existing = map.get(key) ?? { amount: 0, division: t.category ?? '' }
    existing.amount += parseFloat(t.amount)
    map.set(key, existing)
  }
  const sorted = [...map.entries()].sort((a, b) => b[1].amount - a[1].amount).slice(0, 10)
  const max = sorted[0]?.[1].amount || 1
  return sorted.map(([label, { amount, division }]) => ({
    label, amount, division,
    pct: Math.round((amount / max) * 100),
  }))
})

const storeData = computed(() => {
  const map = new Map<string, { amount: number; count: number }>()
  for (const t of expenseTxns.value) {
    const key = t.store || t.description || 'Unknown'
    const existing = map.get(key) ?? { amount: 0, count: 0 }
    existing.amount += parseFloat(t.amount)
    existing.count++
    map.set(key, existing)
  }
  const sorted = [...map.entries()].sort((a, b) => b[1].amount - a[1].amount).slice(0, 10)
  const max = sorted[0]?.[1].amount || 1
  return sorted.map(([label, { amount, count }]) => ({
    label, amount, count,
    pct: Math.round((amount / max) * 100),
  }))
})

// ── Transaction modal ─────────────────────────────────────────────────────────
const modalOpen     = ref(false)
const isEditing     = ref(false)
const editingId     = ref<string | null>(null)
const submitting    = ref(false)
const formError     = ref<string | null>(null)
const confirmDelete = ref(false)
const receiptError  = ref<string | null>(null)

interface FormShape {
  account_id: string; category: string; subcategory: string
  amount: number | string; txn_type: 'income' | 'expense' | 'transfer'
  description: string; store: string | null; cloudinary_url: string | null
  notes: string | null; txn_date: string
}

const blankForm = (): FormShape => ({
  account_id: activeAccounts.value?.[0]?.id ?? '',
  category: 'commitment', subcategory: '',
  amount: 0, txn_type: 'expense',
  description: '', store: null, cloudinary_url: null, notes: null,
  txn_date: new Date().toISOString().slice(0, 10),
})

const form = ref<FormShape>(blankForm())
const formValid = computed(() => !!form.value.account_id && !!form.value.description.trim() && Number(form.value.amount) > 0)
const selectedAccountCurrency = computed(() => {
  const acc = activeAccounts.value?.find((a: any) => a.id === form.value.account_id)
  return acc?.currency ?? user.value?.currency ?? 'MYR'
})

function openModal(txn?: ITransaction) {
  formError.value = null; receiptError.value = null; confirmDelete.value = false
  if (txn) {
    isEditing.value = true; editingId.value = txn.id
    form.value = {
      account_id: txn.account_id, category: txn.category ?? 'commitment',
      subcategory: (txn as any).subcategory ?? '',
      amount: parseFloat(txn.amount), txn_type: txn.txn_type,
      description: txn.description ?? '', store: txn.store ?? null,
      cloudinary_url: txn.cloudinary_url ?? null, notes: txn.notes ?? null,
      txn_date: txn.txn_date,
    }
  } else {
    isEditing.value = false; editingId.value = null; form.value = blankForm()
  }
  modalOpen.value = true; document.body.style.overflow = 'hidden'
}

function closeModal() {
  modalOpen.value = false; document.body.style.overflow = ''
  setTimeout(() => { formError.value = null; receiptError.value = null; confirmDelete.value = false }, 300)
}

async function onReceiptPick(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]; if (!file) return
  receiptError.value = null
  try { form.value.cloudinary_url = await uploadReceipt(file) }
  catch { receiptError.value = uploadError.value ?? 'Upload failed.' }
  finally { (e.target as HTMLInputElement).value = '' }
}

async function handleSubmit() {
  if (!formValid.value) return
  formError.value = null; submitting.value = true
  try {
    if (isEditing.value && editingId.value) {
      await updateTransaction(editingId.value, {
        description: form.value.description || null,
        store: form.value.store, notes: form.value.notes,
        cloudinary_url: form.value.cloudinary_url,
        category: form.value.category as ITransactionUpdate['category'],
        subcategory: form.value.subcategory || undefined,
      } as ITransactionUpdate)
    } else {
      await createTransaction({
        account_id: form.value.account_id,
        amount: Number(form.value.amount),
        txn_type: form.value.txn_type,
        category: form.value.category as ITransactionCreate['category'],
        subcategory: form.value.subcategory || undefined,
        division: form.value.category as ITransactionCreate['division'],
        txn_date: form.value.txn_date,
        description: form.value.description || null,
        store: form.value.store, notes: form.value.notes,
        cloudinary_url: form.value.cloudinary_url,
        idempotency_key: crypto.randomUUID(),
      } as ITransactionCreate)
    }
    closeModal()
  } catch (e: unknown) {
    formError.value = e instanceof Error ? e.message : 'Something went wrong.'
  } finally {
    submitting.value = false
  }
}

async function handleDelete() {
  if (!editingId.value) return
  if (!confirmDelete.value) { confirmDelete.value = true; setTimeout(() => { confirmDelete.value = false }, 3000); return }
  submitting.value = true
  try { await deleteTransaction(editingId.value); closeModal() }
  catch (e: unknown) { formError.value = e instanceof Error ? e.message : 'Delete failed.' }
  finally { submitting.value = false }
}

// ── Import modal ──────────────────────────────────────────────────────────────
const importModalOpen = ref(false)
const importFile      = ref<File | null>(null)
const importAccountId = ref('')
const importLoading   = ref(false)
const importError     = ref<string | null>(null)
const importResult    = ref<IBulkImportResponse | null>(null)
const guideOpen       = ref(true)

const importColumns = [
  { name: 'Date',           required: true,  values: 'DD/MM/YYYY or YYYY-MM-DD  e.g. 26/2/2026' },
  { name: 'Amount (RM)',    required: true,  values: 'Positive number  e.g. 61.20 or 2000' },
  { name: 'Type',           required: false, values: 'Income · Expenses  (default: Expenses)' },
  { name: 'Division',       required: false, values: 'Commitment · Want · Savings · Income  (default: Commitment)' },
  { name: 'Category',       required: false, values: 'Subcategory name  e.g. Grab, Salary, Gold, Treat' },
  { name: 'Description',    required: false, values: 'Free text  e.g. "Nasi Ayam Sayur"' },
  { name: 'Account',        required: false, values: 'Must match your account name  e.g. GX Bank · Bank Islam · TNG' },
  { name: 'Payment Method', required: false, values: 'E-Wallet · Debit · Online · Cash  (informational)' },
  { name: 'Store',          required: false, values: 'Merchant name  e.g. "NSK Grocer"' },
  { name: 'Notes',          required: false, values: 'Any free text' },
]

function openImportModal() {
  importFile.value = null; importAccountId.value = activeAccounts.value?.[0]?.id ?? ''
  importError.value = null; importResult.value = null
  importModalOpen.value = true; document.body.style.overflow = 'hidden'
}
function closeImportModal() { importModalOpen.value = false; document.body.style.overflow = '' }
function onImportFilePick(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]; if (!file) return
  importFile.value = file; importError.value = null; importResult.value = null
}
async function handleImport() {
  if (!importFile.value || !importAccountId.value) return
  importLoading.value = true; importError.value = null; importResult.value = null
  try { importResult.value = await importTransactions(importFile.value, importAccountId.value); importFile.value = null }
  catch (e: unknown) { importError.value = e instanceof Error ? e.message : 'Import failed.' }
  finally { importLoading.value = false }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function formatAmount(v: number): string {
  if (!v && v !== 0) return '0.00'
  if (v >= 1_000_000) return (v / 1_000_000).toFixed(2) + 'M'
  if (v >= 1_000) return v.toLocaleString('en-MY', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
  return v.toFixed(2)
}
function txnIconSvg(txn: Partial<ITransaction>): string {
  const c = txn.txn_type === 'income' ? '#4CAF50' : '#800020'
  return txn.txn_type === 'income'
    ? `<svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M2 9L6 5l3 3 4-5" stroke="${c}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
    : `<svg width="13" height="13" viewBox="0 0 13 13" fill="none"><circle cx="6.5" cy="6.5" r="5.5" stroke="${c}99" stroke-width="1.1"/><path d="M4 7.5c.5 1 1.3 1.5 2.5 1.5s2-.5 2.5-1.5" stroke="${c}99" stroke-width="1" stroke-linecap="round"/></svg>`
}
function txnBg(txn: Partial<ITransaction>): string { return `${txn.txn_type === 'income' ? '#4CAF50' : '#800020'}18` }

onMounted(async () => {
  await fetchAccounts()
  await fetchTransactions({ limit: 1000 })
  if (route.query.new === '1') openModal()
})
</script>

<style scoped>
.txns { height:100%; min-height:100vh; background:var(--color-void); position:relative; }
.txns-scroll { height:100%; overflow-y:auto; -webkit-overflow-scrolling:touch; }
.txns-header { padding:20px 20px 0; }
@media(min-width:860px) { .txns-header { padding:36px 36px 0; } }
.txns-header-inner { display:flex; align-items:flex-start; justify-content:space-between; }
.txns-sup { font-size:8.5px; letter-spacing:2.5px; color:var(--color-gun); margin-bottom:4px; }
.txns-title { font-size:clamp(1.8rem,7vw,2.6rem); color:var(--color-plat); line-height:1; }
.txns-period { color:var(--color-ox); }
.header-actions { display:flex; align-items:center; gap:8px; }
.import-btn { display:flex; align-items:center; gap:6px; padding:0 12px; height:42px; border-radius:14px; background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); color:var(--color-gun); cursor:pointer; transition:all .18s; }
.import-btn:hover { border-color:var(--color-ox-md); color:var(--color-plat); background:var(--color-ox-lo); }
.import-btn span { font-size:9px; letter-spacing:1px; }
.add-fab { width:42px; height:42px; border-radius:14px; flex-shrink:0; background:linear-gradient(150deg, rgba(170,10,45,0.95), rgba(90,0,18,0.92)); border:1px solid rgba(180,20,50,0.4); display:flex; align-items:center; justify-content:center; color:rgba(224,224,224,0.95); cursor:pointer; box-shadow:0 6px 22px var(--color-ox-hi), 0 0 0 1px rgba(255,255,255,0.06) inset; transition:all .2s var(--ease); }
.add-fab:hover { transform:translateY(-2px); box-shadow:0 10px 30px var(--color-ox-hi); }
.add-fab:active { transform:scale(0.93); }
/* ── Segment ── */
.segment-wrap { padding:14px 0 0; }
.segment { display:inline-flex; background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); border-radius:12px; padding:3px; gap:3px; }
.segment-btn { display:flex; align-items:center; gap:6px; padding:8px 16px; border-radius:9px; color:var(--color-gun); cursor:pointer; transition:all .18s; }
.segment-btn span { font-size:9px; letter-spacing:1.5px; }
.segment-btn--active { background:rgba(128,0,32,0.18); border:1px solid var(--color-ox-md); color:var(--color-plat); box-shadow:0 2px 10px var(--color-ox-hi); }
/* ── Analytics banner ── */
.analytics-month-banner { display:flex; align-items:center; gap:8px; padding:10px 14px; background:rgba(128,0,32,0.06); border:1px solid var(--color-ox-md); border-radius:var(--radius-sm); color:rgba(224,224,224,0.5); flex-wrap:wrap; }
.analytics-month-banner strong { color:rgba(224,224,224,0.85); font-style:normal; }
.analytics-month-banner .t-mono { font-size:9px; letter-spacing:0.5px; }
.analytics-month-hint { margin-left:auto; color:var(--color-gun); font-size:8px; letter-spacing:0.3px; }
/* ── Analytics summary row ── */
.an-summary-row { display:flex; align-items:stretch; background:rgba(16,16,18,0.85); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); overflow:hidden; }
.an-tile { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:5px; padding:16px 10px; }
.an-tile-div { width:1px; background:var(--color-glass-bo); flex-shrink:0; }
.an-tile-label { font-size:7.5px; letter-spacing:2px; color:var(--color-gun); }
.an-tile-val { font-size:clamp(0.9rem,3vw,1.2rem); letter-spacing:-0.03em; line-height:1; }
/* ── Analytics sections ── */
.an-hdr { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.section-tag { font-size:8.5px; letter-spacing:2px; color:var(--color-gun); }
.section-meta { font-size:8.5px; letter-spacing:1px; color:var(--color-gun); }
.an-card { padding:18px; }
.an-empty { display:flex; align-items:center; justify-content:center; padding:28px; }
.an-empty .t-mono { font-size:10px; color:var(--color-gun); }
/* ── Donut ── */
.donut-layout { display:flex; align-items:center; gap:20px; flex-wrap:wrap; }
.donut-wrap { flex-shrink:0; width:130px; height:130px; }
.donut-svg { width:100%; height:100%; transform:rotate(-90deg); }
.donut-legend { flex:1; min-width:150px; display:flex; flex-direction:column; gap:10px; }
.donut-legend-row { display:flex; align-items:center; justify-content:space-between; gap:8px; }
.donut-legend-left { display:flex; align-items:center; gap:8px; }
.donut-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.donut-legend-label { font-size:9px; letter-spacing:1px; color:rgba(224,224,224,0.65); }
.donut-legend-right { display:flex; align-items:center; gap:8px; }
.donut-legend-val { font-size:10px; color:rgba(224,224,224,0.85); font-family:var(--font-mono); }
.donut-legend-pct { font-size:8.5px; color:var(--color-gun); min-width:28px; text-align:right; font-family:var(--font-mono); }
/* ── Horizontal bars ── */
.hbar-list { display:flex; flex-direction:column; gap:14px; }
.hbar-row { display:flex; flex-direction:column; gap:5px; }
.hbar-meta { display:flex; align-items:center; justify-content:space-between; gap:8px; }
.hbar-rank-wrap { display:flex; align-items:center; gap:8px; min-width:0; }
.hbar-rank { font-size:8px; letter-spacing:1px; color:var(--color-gun); flex-shrink:0; }
.hbar-label { font-size:10px; color:rgba(224,224,224,0.75); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.hbar-vals { display:flex; align-items:center; gap:10px; flex-shrink:0; }
.hbar-amt { font-size:10px; color:rgba(224,224,224,0.85); }
.hbar-pct { font-size:8.5px; color:var(--color-gun); min-width:30px; text-align:right; }
.hbar-count { font-size:8.5px; color:var(--color-gun); }
.hbar-track { width:100%; height:3px; background:rgba(224,224,224,0.06); border-radius:2px; overflow:hidden; }
.hbar-fill { height:100%; border-radius:2px; width:0; transition:width 0.6s cubic-bezier(0.4,0,0.2,1); }
.hbar-fill--store { background:var(--color-ox); box-shadow:0 0 8px var(--color-ox-hi); }
/* ── rest of original styles ── */
.txns-section { padding:20px 16px; }
@media(min-width:860px) { .txns-section { padding:24px 36px; } }
.summary-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.summary-stat { background:rgba(16,16,18,0.85); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); padding:14px 14px 12px; display:flex; flex-direction:column; gap:4px; }
.summary-stat--net { grid-column:1 / -1; flex-direction:row; align-items:center; justify-content:space-between; }
.summary-stat--net .summary-val { font-size:1.1rem; }
.summary-stat-top { display:flex; align-items:center; gap:7px; margin-bottom:4px; }
.summary-icon { width:22px; height:22px; border-radius:7px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.summary-icon--green { background:var(--color-grn-lo); color:var(--color-grn); }
.summary-icon--red { background:var(--color-red-lo); color:#ef5350; }
.summary-icon--ox { background:var(--color-ox-lo); color:var(--color-ox); }
.summary-label { font-size:8.5px; letter-spacing:1.5px; color:var(--color-gun); text-transform:uppercase; }
.summary-val { font-size:1rem; color:var(--color-plat); letter-spacing:-0.02em; line-height:1; }
.summary-sub { font-size:8px; letter-spacing:0.5px; color:var(--color-gun); }
.cal-card { overflow:hidden; }
.cal-hdr { display:flex; align-items:center; justify-content:space-between; padding:11px 14px; border-bottom:1px solid var(--color-glass-bo); }
.cal-month-label { font-size:9px; letter-spacing:2px; color:var(--color-plat); text-transform:uppercase; }
.cal-nav { width:26px; height:26px; display:flex; align-items:center; justify-content:center; border-radius:8px; background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); color:var(--color-gun); cursor:pointer; transition:all .15s; }
.cal-nav:hover { color:var(--color-plat); border-color:rgba(224,224,224,0.15); background:rgba(255,255,255,0.07); }
.cal-grid { display:grid; grid-template-columns:repeat(7,1fr); }
.cal-dow { font-size:7px; letter-spacing:1px; color:var(--color-gun); text-align:center; padding:7px 0 5px; border-bottom:1px solid rgba(224,224,224,0.04); }
.cal-cell { display:flex; flex-direction:column; align-items:center; gap:1px; padding:5px 2px 5px; border-right:1px solid rgba(224,224,224,0.03); border-bottom:1px solid rgba(224,224,224,0.03); min-height:52px; position:relative; transition:background .12s; }
.cal-cell:nth-child(7n) { border-right:none; }
.cal-cell--empty { pointer-events:none; }
.cal-cell--active { background:rgba(255,255,255,0.015); }
.cal-cell--today { background:rgba(128,0,32,0.08); }
.cal-cell--today::after { content:''; position:absolute; inset:0; border:1px solid rgba(128,0,32,0.25); pointer-events:none; }
.cal-day-num { font-size:8.5px; letter-spacing:0.3px; color:var(--color-gun); line-height:1; margin-bottom:2px; }
.cal-day-num--today { color:var(--color-ox); font-weight:600; }
.cal-inc { font-size:6.5px; color:var(--color-grn); line-height:1; }
.cal-exp { font-size:6.5px; color:#ef5350; line-height:1; }
.cal-count { font-size:6px; color:var(--color-gun); margin-top:1px; background:rgba(255,255,255,0.06); border-radius:100px; padding:1px 4px; line-height:1.4; }
.chart-card { padding:16px 16px 12px; }
.chart-hdr { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
.chart-title { font-size:8px; letter-spacing:2px; color:var(--color-gun); }
.chart-legend { display:flex; align-items:center; gap:10px; }
.legend-dot { width:6px; height:6px; border-radius:50%; flex-shrink:0; }
.legend-dot--credit { background:var(--color-grn); box-shadow:0 0 5px rgba(76,175,80,0.5); }
.legend-dot--debit { background:var(--color-ox); box-shadow:0 0 5px var(--color-ox-hi); }
.legend-label { font-size:8px; letter-spacing:0.5px; color:var(--color-gun); }
.chart-wrap { overflow-x:auto; scrollbar-width:none; padding-bottom:2px; }
.chart-wrap::-webkit-scrollbar { display:none; }
.chart-bars { display:flex; align-items:flex-end; gap:6px; min-width:max-content; padding:0 4px; }
.chart-bar-group { display:flex; flex-direction:column; align-items:center; position:relative; cursor:pointer; }
.chart-bar-group--active .bar-day { color:var(--color-plat); }
.bar-col { display:flex; flex-direction:column; align-items:center; gap:5px; }
.bar-stack { display:flex; gap:2px; align-items:flex-end; height:52px; }
.bar { width:10px; border-radius:3px 3px 0 0; transition:height .4s var(--ease), opacity .3s; min-height:2px; }
.bar--credit { background:var(--color-grn); box-shadow:0 0 6px rgba(76,175,80,0.3); }
.bar--debit { background:var(--color-ox); box-shadow:0 0 6px var(--color-ox-hi); }
.bar-day { font-family:var(--font-mono); font-size:7.5px; color:var(--color-gun); transition:color .15s; width:22px; text-align:center; }
.bar-tip { position:absolute; bottom:calc(100% + 6px); left:50%; transform:translateX(-50%); background:rgba(18,18,20,0.98); border:1px solid var(--color-glass-bo); border-radius:8px; padding:7px 10px; z-index:10; white-space:nowrap; display:flex; flex-direction:column; gap:2px; }
.bar-tip-day { font-size:7.5px; color:var(--color-gun); margin-bottom:2px; }
.bar-tip-credit { font-size:9px; color:var(--color-grn); }
.bar-tip-debit { font-size:9px; color:#ef5350; }
.tip-enter-active, .tip-leave-active { transition:opacity .12s, transform .12s; }
.tip-enter-from, .tip-leave-to { opacity:0; transform:translateX(-50%) translateY(4px); }
.search-row { display:flex; align-items:center; gap:10px; }
.search-wrap { flex:1; display:flex; align-items:center; gap:8px; background:rgba(18,18,20,0.8); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); padding:0 12px; height:38px; transition:border-color .18s; }
.search-wrap:focus-within { border-color:var(--color-ox-md); }
.search-icon { color:var(--color-gun); flex-shrink:0; }
.search-input { flex:1; background:none; border:none; outline:none; font-size:11px; color:var(--color-plat); }
.search-input::placeholder { color:var(--color-gun); }
.search-clear { color:var(--color-gun); display:flex; align-items:center; justify-content:center; transition:color .15s; }
.search-clear:hover { color:var(--color-plat); }
.filter-btn { display:flex; align-items:center; gap:6px; padding:0 12px; height:38px; background:rgba(18,18,20,0.8); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); color:var(--color-gun); cursor:pointer; transition:all .18s; position:relative; white-space:nowrap; }
.filter-btn:hover, .filter-btn--active { border-color:var(--color-ox-md); color:var(--color-plat); background:var(--color-ox-lo); }
.filter-count { position:absolute; top:-5px; right:-5px; width:16px; height:16px; border-radius:50%; background:var(--color-ox); color:#fff; font-family:var(--font-mono); font-size:8px; display:flex; align-items:center; justify-content:center; }
.filter-drawer { margin-top:10px; padding:14px 16px; background:rgba(16,16,18,0.95); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); display:flex; flex-direction:column; gap:14px; }
.filter-group { display:flex; flex-direction:column; gap:8px; }
.filter-group-label { font-size:7.5px; letter-spacing:2px; color:var(--color-gun); }
.filter-pills { display:flex; flex-wrap:wrap; gap:6px; }
.filter-pill { padding:5px 12px; border-radius:100px; border:1px solid var(--color-glass-bo); background:rgba(255,255,255,0.03); color:var(--color-gun); font-size:9px; letter-spacing:0.8px; cursor:pointer; transition:all .15s; }
.filter-pill:hover { color:var(--color-plat); border-color:rgba(224,224,224,0.15); }
.filter-pill--active { background:var(--color-ox-lo); border-color:var(--color-ox-md); color:var(--color-plat); }
.filter-reset { font-size:8.5px; color:var(--color-gun); align-self:flex-start; padding:4px 0; transition:color .15s; }
.filter-reset:hover { color:#ef5350; }
.drawer-enter-active, .drawer-leave-active { transition:opacity .2s, transform .2s var(--ease); }
.drawer-enter-from, .drawer-leave-to { opacity:0; transform:translateY(-6px); }
.txns-empty { display:flex; flex-direction:column; align-items:center; gap:10px; padding:48px 20px; }
.txns-empty-icon { width:52px; height:52px; border-radius:16px; background:rgba(224,224,224,0.03); border:1px dashed rgba(224,224,224,0.08); display:flex; align-items:center; justify-content:center; }
.txns-empty-cta { font-size:9.5px; color:var(--color-ox); margin-top:4px; }
.txn-group { margin-bottom:20px; }
.txn-group-hdr { display:flex; align-items:center; justify-content:space-between; padding:0 4px; margin-bottom:8px; }
.txn-group-date { font-size:8.5px; letter-spacing:1.5px; color:var(--color-gun); text-transform:uppercase; }
.txn-group-net { font-size:9.5px; }
.txn-list { overflow:hidden; }
.txn-row { display:flex; align-items:center; gap:12px; padding:13px 16px; border-bottom:1px solid rgba(224,224,224,0.04); cursor:pointer; transition:background .15s; }
.txn-row:hover { background:rgba(255,255,255,0.025); }
.txn-row--last { border-bottom:none; }
.txn-icon-wrap { width:36px; height:36px; border-radius:11px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.txn-info { flex:1; min-width:0; display:flex; flex-direction:column; gap:4px; }
.txn-name { font-size:11px; color:rgba(224,224,224,0.85); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.txn-meta { display:flex; flex-wrap:wrap; gap:4px; }
.txn-chip { font-size:8px; padding:2px 7px; border-radius:100px; background:rgba(128,0,32,0.12); border:1px solid var(--color-ox-md); color:rgba(224,224,224,0.5); }
.txn-chip--ghost { background:rgba(255,255,255,0.04); border-color:var(--color-glass-bo); }
.txn-right { display:flex; flex-direction:column; align-items:flex-end; gap:4px; flex-shrink:0; }
.txn-amt { font-size:11.5px; font-weight:500; }
.txn-indicators { display:flex; gap:4px; }
.txn-ind { color:var(--color-gun); display:flex; opacity:0.5; }
.t-green { color:var(--color-grn); }
.t-red { color:#ef5350; }
.sov-card { background:rgba(16,16,18,0.85); border:1px solid var(--color-glass-bo); border-radius:var(--radius-md); }
.receipt-drop { display:flex; align-items:center; justify-content:center; gap:8px; padding:14px; border-radius:var(--radius-sm); border:1px dashed var(--color-glass-bo); background:rgba(255,255,255,0.02); cursor:pointer; transition:all .18s; }
.receipt-drop:hover { border-color:var(--color-ox-md); background:var(--color-ox-lo); }
.receipt-drop--loading { pointer-events:none; opacity:0.7; }
.receipt-preview { display:flex; align-items:center; justify-content:space-between; padding:10px 12px; background:rgba(76,175,80,0.06); border:1px solid rgba(76,175,80,0.2); border-radius:var(--radius-sm); }
.receipt-link { display:flex; align-items:center; gap:6px; font-size:10px; color:var(--color-grn); text-decoration:none; }
.receipt-link:hover { text-decoration:underline; }
.receipt-remove { font-size:9px; color:var(--color-gun); transition:color .15s; }
.receipt-remove:hover { color:#ef5350; }
.receipt-error { font-size:9px; color:#ef5350; margin-top:4px; }
.import-drop { min-height:64px; }
.import-drop--has-file { border-color:rgba(76,175,80,0.3); background:rgba(76,175,80,0.04); }
.import-result { padding:12px 14px; background:rgba(76,175,80,0.06); border:1px solid rgba(76,175,80,0.2); border-radius:var(--radius-sm); display:flex; flex-direction:column; gap:8px; }
.import-result-row { display:flex; align-items:center; gap:14px; }
.import-result-ok { font-size:10px; color:var(--color-grn); }
.import-result-skip { font-size:10px; color:var(--color-gun); }
.import-result-err { font-size:10px; color:#ef5350; }
.import-errors { display:flex; flex-direction:column; gap:3px; }
.import-error-row { font-size:8.5px; color:#ef5350; }
.modal-overlay { position:fixed; inset:0; z-index:400; background:rgba(8,8,8,0.75); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); display:flex; align-items:flex-end; justify-content:center; }
@media(min-width:600px) { .modal-overlay { align-items:center; } }
.modal { width:100%; max-width:480px; background:rgba(14,14,16,0.98); border:1px solid var(--color-glass-bo); border-bottom:none; border-radius:var(--radius-xl) var(--radius-xl) 0 0; overflow:hidden; }
@media(min-width:600px) { .modal { border-radius:var(--radius-xl); border-bottom:1px solid var(--color-glass-bo); } }
.modal-hdr { display:flex; align-items:flex-start; justify-content:space-between; padding:24px 24px 0; }
.modal-sup { font-size:8px; letter-spacing:2.5px; color:var(--color-gun); margin-bottom:3px; }
.modal-title { font-size:1.6rem; color:var(--color-plat); line-height:1; }
.modal-close { width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:rgba(224,224,224,0.06); border:1px solid var(--color-glass-bo); color:var(--color-gun); cursor:pointer; transition:all .15s; flex-shrink:0; margin-top:4px; }
.modal-close:hover { color:var(--color-plat); background:rgba(224,224,224,0.1); }
.modal-body { padding:20px 24px 32px; display:flex; flex-direction:column; gap:18px; overflow-y:auto; max-height:80vh; }
@media(max-height:700px) { .modal-body { padding-bottom:20px; } }
.type-toggle { display:grid; grid-template-columns:1fr 1fr; gap:6px; background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); padding:4px; }
.type-btn { display:flex; align-items:center; justify-content:center; gap:6px; padding:9px 12px; border-radius:8px; color:var(--color-gun); cursor:pointer; transition:all .18s; }
.type-btn span { font-size:9px; letter-spacing:1.5px; }
.type-btn--debit { background:rgba(176,0,32,0.12); border:1px solid rgba(176,0,32,0.25); color:#ef5350; }
.type-btn--credit { background:rgba(76,175,80,0.12); border:1px solid rgba(76,175,80,0.25); color:var(--color-grn); }
.field-group { display:flex; flex-direction:column; gap:6px; }
.field-group--half { flex:1; min-width:0; }
.field-row { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.field-label { font-size:8px; letter-spacing:2px; color:var(--color-gun); }
.field-input { width:100%; background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); padding:10px 12px; font-size:12px; color:var(--color-plat); outline:none; transition:border-color .18s; box-sizing:border-box; }
.field-input:focus { border-color:var(--color-ox-md); }
.field-input::placeholder { color:var(--color-gun); }
.amount-wrap { display:flex; align-items:baseline; gap:8px; padding-bottom:4px; }
.amount-ccy { font-size:13px; color:var(--color-gun); flex-shrink:0; }
.amount-input { flex:1; background:none; border:none; outline:none; font-size:2rem; letter-spacing:-0.04em; color:var(--color-plat); padding:0; }
.amount-input::placeholder { color:rgba(117,117,117,0.4); }
.amount-input::-webkit-inner-spin-button, .amount-input::-webkit-outer-spin-button { -webkit-appearance:none; }
.amount-underline { height:1.5px; border-radius:1px; transition:background .2s; }
.amount-underline--debit { background:linear-gradient(90deg, #ef5350, transparent); }
.amount-underline--credit { background:linear-gradient(90deg, var(--color-grn), transparent); }
.select-wrap { position:relative; }
.field-select { width:100%; background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); border-radius:var(--radius-sm); padding:10px 32px 10px 12px; font-size:11px; color:var(--color-plat); outline:none; appearance:none; -webkit-appearance:none; cursor:pointer; transition:border-color .18s; }
.field-select:focus { border-color:var(--color-ox-md); }
.field-select option { background:#0f0f11; }
.select-arrow { position:absolute; right:10px; top:50%; transform:translateY(-50%); pointer-events:none; color:var(--color-gun); }
input[type="date"].field-input { color-scheme:dark; }
input[type="date"].field-input::-webkit-calendar-picker-indicator { filter:invert(0.4); cursor:pointer; }
.form-error { display:flex; align-items:center; gap:8px; padding:9px 12px; background:var(--color-red-lo); border:1px solid rgba(176,0,32,0.25); border-radius:var(--radius-sm); font-size:10px; color:#ef5350; }
.modal-actions { display:flex; gap:10px; padding-top:4px; }
.modal-btn { flex:1; display:flex; align-items:center; justify-content:center; gap:8px; padding:13px 18px; border-radius:var(--radius-sm); cursor:pointer; transition:all .18s; }
.modal-btn span { font-size:10px; letter-spacing:1.5px; }
.modal-btn:disabled { opacity:0.45; cursor:not-allowed; }
.modal-btn--submit { background:linear-gradient(135deg, var(--color-ox-hi), rgba(90,0,18,0.9)); border:1px solid var(--color-ox-md); color:var(--color-plat); box-shadow:0 4px 18px var(--color-ox-hi); flex:2; }
.modal-btn--submit:not(:disabled):hover { box-shadow:0 6px 26px var(--color-ox-hi); transform:translateY(-1px); }
.modal-btn--delete { background:rgba(239,83,80,0.08); border:1px solid rgba(239,83,80,0.2); color:#ef5350; flex:0 0 auto; padding:13px 16px; }
.modal-btn--delete:hover { background:rgba(239,83,80,0.15); border-color:rgba(239,83,80,0.35); }
.btn-spinner { width:13px; height:13px; border-radius:50%; border:1.5px solid rgba(224,224,224,0.2); border-top-color:rgba(224,224,224,0.8); animation:spin .7s linear infinite; flex-shrink:0; }
@keyframes spin { to { transform:rotate(360deg); } }
.modal-fade-enter-active, .modal-fade-leave-active { transition:opacity .2s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity:0; }
.modal-slide-enter-active { transition:transform .28s var(--ease), opacity .2s; }
.modal-slide-leave-active { transition:transform .2s ease-in, opacity .15s; }
.modal-slide-enter-from { transform:translateY(40px); opacity:0; }
.modal-slide-leave-to { transform:translateY(20px); opacity:0; }
@media(min-width:600px) {
  .modal-slide-enter-from { transform:scale(0.96) translateY(10px); }
  .modal-slide-leave-to { transform:scale(0.97) translateY(5px); }
}
.col-guide { overflow:hidden; }
.col-guide-hdr { display:flex; align-items:center; justify-content:space-between; padding:11px 14px; border-bottom:1px solid var(--color-glass-bo); }
.col-guide-title { font-size:7.5px; letter-spacing:2px; color:var(--color-gun); }
.col-guide-toggle { display:flex; align-items:center; gap:5px; font-size:8px; letter-spacing:1px; color:var(--color-gun); cursor:pointer; transition:color .15s; padding:4px 8px; border-radius:6px; border:1px solid var(--color-glass-bo); background:rgba(255,255,255,0.03); }
.col-guide-toggle:hover { color:var(--color-plat); border-color:rgba(224,224,224,0.15); }
.col-table-wrap { padding:0 0 10px; }
.col-table { width:100%; border-collapse:collapse; table-layout:fixed; }
.col-table thead tr { border-bottom:1px solid var(--color-glass-bo); }
.col-table th { font-size:7px; letter-spacing:1.5px; color:var(--color-gun); padding:7px 12px; text-align:left; font-weight:400; }
.col-table th:nth-child(1) { width:30%; }
.col-table th:nth-child(2) { width:12%; }
.col-table th:nth-child(3) { width:58%; }
.col-table tbody tr { border-bottom:1px solid rgba(224,224,224,0.03); transition:background .12s; }
.col-table tbody tr:last-child { border-bottom:none; }
.col-table tbody tr:hover { background:rgba(255,255,255,0.02); }
.col-table td { padding:7px 12px; vertical-align:top; }
.col-name { font-size:9px; color:rgba(224,224,224,0.75); }
.req-badge { display:inline-block; font-size:7px; letter-spacing:1px; padding:2px 6px; border-radius:100px; }
.req-badge--yes { background:rgba(176,0,32,0.15); border:1px solid var(--color-ox-md); color:var(--color-ox); }
.req-badge--no { background:rgba(255,255,255,0.04); border:1px solid var(--color-glass-bo); color:var(--color-gun); }
.col-vals { font-size:8px; color:rgba(224,224,224,0.38); line-height:1.65; word-break:break-word; }
.col-note { display:flex; align-items:flex-start; gap:7px; margin:8px 12px 0; padding:8px 10px; background:rgba(255,255,255,0.02); border:1px solid var(--color-glass-bo); border-radius:8px; }
.col-note-text { font-size:7.5px; color:var(--color-gun); line-height:1.7; }
.col-note-text strong { color:rgba(224,224,224,0.5); font-weight:500; }
.guide-enter-active { transition:opacity .2s; overflow:hidden; }
.guide-leave-active { transition:opacity .15s; overflow:hidden; }
.guide-enter-from, .guide-leave-to { opacity:0; }
</style>