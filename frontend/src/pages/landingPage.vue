<template>
  <div class="page-root">

    <!-- AMBIENT -->
    <div class="sov-ambient" aria-hidden="true">
      <div class="sov-orb sov-orb--1" />
      <div class="sov-orb sov-orb--2" />
      <div class="sov-grid-overlay" />
    </div>

    <!-- NAV -->
    <nav class="glass-nav" :class="{ scrolled }">
      <div class="nav-inner sov-container">
        <a class="nav-brand" href="#">
          <img src="@/assets/ring-it.png" alt="Ring-It Logo" class="brand-logo-img">
          <div>
            <p class="brand-name t-mono">RING-IT</p>
            <p class="brand-sub t-mono">// vault · v1.0</p>
          </div>
        </a>
        <div class="nav-end">
          <a href="#features" class="sov-nav-link">Features</a>
          <a href="#ai"       class="sov-nav-link">Behavioral Brain</a>
          <a href="#compliance" class="sov-nav-link">Compliance</a>
          <RouterLink to="/login" class="sov-btn sov-btn--primary sov-btn--sm">Enter Vault →</RouterLink>
        </div>
        <button class="hamburger" @click="mobileOpen = !mobileOpen" :class="{ open: mobileOpen }">
          <span /><span /><span />
        </button>
      </div>
      <div class="mobile-drawer" :class="{ active: mobileOpen }">
        <a href="#features"   class="mobile-link" @click="mobileOpen=false">Features</a>
        <a href="#ai"         class="mobile-link" @click="mobileOpen=false">Behavioral Brain</a>
        <a href="#compliance" class="mobile-link" @click="mobileOpen=false">Compliance</a>
        <RouterLink to="/login" class="sov-btn sov-btn--primary" style="text-align:center;margin-top:14px" @click="mobileOpen=false">Enter Vault →</RouterLink>
      </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
      <div class="sov-container">
        <div class="hero-layout">

          <div class="hero-copy">
            <div class="eyebrow">
              <span class="sov-pulse" />
              Behavioral Finance · Malaysian Compliance · v1.0
            </div>

            <h1 class="hero-h1 t-display">
              Not a Budgeting App.<br />
              <span class="t-accent">A Wealth System.</span>
            </h1>

            <blockquote class="hero-quote">
              <span class="qm">"</span>You do not rise to the level of your goals.
              You fall to the level of your systems.
              <footer>— James Clear, Atomic Habits</footer>
            </blockquote>

            <RouterLink to="/login" class="sov-btn sov-btn--primary sov-btn--lg hero-cta">
              Open the Vault
              <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                <path d="M2.5 6.5h8M6.5 2.5l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </RouterLink>
          </div>

          <!-- Dashboard mock -->
          <div class="hero-visual" aria-hidden="true">
            <div class="mock-shell">

              <div class="mock-topbar">
                <div class="mock-brand-row">
                  <span class="mock-dot sov-pulse" style="animation:none" />
                  <span class="t-mono mock-mono">RING-IT // VAULT DASHBOARD</span>
                </div>
                <span class="sov-chip sov-chip--green">DSR 42% ●</span>
              </div>

              <div class="mock-nw">
                <span class="t-label">// NET WORTH</span>
                <div class="mock-nw-amt">
                  <span class="mock-ccy t-gun t-mono">RM</span>
                  <span class="mock-big t-display">24,500.00</span>
                </div>
                <div class="mock-nw-sub t-mono">
                  <span class="t-green">▲ Assets 32,000</span>
                  <span class="t-gun">·</span>
                  <span class="t-red">▼ Liabilities 7,500</span>
                </div>
              </div>

              <div class="mock-widgets">
                <div class="mock-widget">
                  <span class="t-label">// TODAY</span>
                  <div class="gauge-wrap">
                    <svg viewBox="0 0 72 72" class="gauge-svg">
                      <circle cx="36" cy="36" r="26" fill="none" stroke="#1A1A1E" stroke-width="5"/>
                      <circle cx="36" cy="36" r="26" fill="none" stroke="#4CAF50"
                              stroke-width="5" stroke-linecap="round"
                              stroke-dasharray="63.4 163.4"
                              transform="rotate(-90 36 36)"/>
                    </svg>
                    <div class="gauge-center">
                      <span class="gauge-pct t-mono">38%</span>
                      <span class="gauge-sub t-mono t-gun">used</span>
                    </div>
                  </div>
                  <span class="t-label t-green">RM 74.20 left</span>
                </div>
                <div class="mock-widget">
                  <span class="t-label">// EMERGENCY</span>
                  <div class="ef-row">
                    <span class="ef-num t-display">5</span>
                    <span class="ef-unit t-mono t-gun">months</span>
                  </div>
                  <div class="sov-track"><div class="sov-track__fill sov-track__fill--green" style="width:83%" /></div>
                  <span class="t-label t-amber" style="margin-top:4px">Target: 6 months</span>
                </div>
              </div>

              <div class="mock-txns">
                <span class="t-label">// RECENT LEDGER</span>
                <div v-for="t in mockTxns" :key="t.id" class="mock-txn">
                  <div class="txn-ico" :class="`txn-ico--${t.type}`">{{ t.icon }}</div>
                  <div class="txn-info">
                    <span class="txn-cat t-mono">{{ t.cat }}</span>
                    <span class="txn-acc t-mono t-gun">{{ t.acc }}</span>
                  </div>
                  <span class="txn-amt t-mono" :class="t.type === 'income' ? 't-green' : ''">
                    {{ t.type === 'income' ? '+' : '-' }}RM {{ t.amt }}
                  </span>
                </div>
              </div>

              <div class="sov-nudge sov-nudge--warn">
                <span>⚠</span>
                <span class="t-mono">NO-BUY · DSR headroom thin. Justify before RM 150 purchase.</span>
              </div>

            </div>

            <div class="float-tag sov-float">
              <span class="float-dot float-dot-g" />10yr: RM 12,793
            </div>
            <div class="float-tag float-tag-r sov-float sov-float--slow">
              <span class="float-dot float-dot-r" />LHDN 82% filled
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Trust strip -->
    <div class="trust-strip">
      <div class="trust-inner">
        <span v-for="t in trust" :key="t" class="trust-item t-mono">
          <svg width="7" height="7" viewBox="0 0 7 7"><circle cx="3.5" cy="3.5" r="3" fill="#4CAF50"/></svg>
          {{ t }}
        </span>
      </div>
    </div>

    <!-- 3 BEHAVIORAL LEVERS -->
    <section class="sov-section" id="features">
      <div class="sov-container">
        <div class="sec-head">
          <span class="t-overline">// Personal Finance Application</span>
          <h2 class="sec-h2 t-display">Ring-It</h2>
          <p class="t-body">
            Ring-It is a behavioral architecture for wealth accumulation — built
            specifically for the Malaysian financial ecosystem. Every design
            decision makes good habits effortless and bad ones deliberately hard.
          </p>
        </div>
        <div class="lever-grid">
          <div v-for="l in levers" :key="l.num" class="sov-card sov-card--hover lever-card">
            <span class="lever-num t-mono">{{ l.num }}</span>
            <span class="lever-emoji">{{ l.emoji }}</span>
            <h3 class="lever-title t-display">{{ l.title }}</h3>
            <p class="lever-desc t-body">{{ l.desc }}</p>
            <span class="sov-chip sov-chip--ox lever-tag">{{ l.tag }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- KEY CAPABILITIES -->
    <section class="sov-section sov-section--alt">
      <div class="sov-container">
        <div class="sec-head">
          <span class="t-overline">// CORE MODULES</span>
          <h2 class="sec-h2 t-display">Built for the Malaysian<br />Financial Reality.</h2>
        </div>
        <div class="cap-grid">
          <div v-for="c in caps" :key="c.id"
               class="sov-card sov-card--hover cap-card"
               :class="{ 'sov-card--ox': c.hi }">
            <div class="cap-top">
              <span class="t-overline" style="margin-bottom:0">{{ c.id }}</span>
              <span class="cap-icon">{{ c.icon }}</span>
            </div>
            <h3 class="cap-title t-display">{{ c.title }}</h3>
            <p class="cap-desc t-body">{{ c.desc }}</p>
            <div class="cap-tags">
              <span v-for="tag in c.tags" :key="tag" class="sov-chip sov-chip--ghost">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- BEHAVIORAL BRAIN -->
    <section class="sov-section" id="ai">
      <div class="sov-container">
        <div class="ai-layout">

          <div class="sov-card ai-flow-card">
            <p class="t-overline" style="margin-bottom:14px">// MOD-09 · DECISION FLOW</p>

            <div class="flow-step flow-step-input">
              <span class="sov-chip sov-chip--ox">WANT</span>
              <span class="t-mono flow-text">Purchase &gt; RM 50 detected</span>
            </div>
            <div class="flow-arrow t-mono">↓</div>

            <div class="flow-checks">
              <div class="flow-check">
                <span class="fc-dot fc-g" /><span class="t-mono t-gun">DSR 42% · Green ✓</span>
              </div>
              <div class="flow-check">
                <span class="fc-dot fc-g" /><span class="t-mono t-gun">Daily allowance OK ✓</span>
              </div>
              <div class="flow-check">
                <span class="fc-dot fc-a" /><span class="t-mono t-gun">Emergency Fund 5mo ⚠</span>
              </div>
            </div>
            <div class="flow-arrow t-mono">↓</div>

            <div class="flow-verdict">
              <span class="t-green" style="font-size:14px">✓</span>
              <span class="t-mono t-green" style="font-weight:500;letter-spacing:2px">BUY APPROVED</span>
            </div>
            <div class="flow-arrow t-mono">↓</div>

            <div class="flow-step flow-step-justify">
              <span class="sov-chip sov-chip--amber">REQUIRED</span>
              <span class="t-mono flow-text">Type your justification to save</span>
            </div>
            <div class="justify-input-mock">
              <span class="t-mono t-accent sov-blink">|</span>
              <span class="t-mono justify-ph">Why are you buying this?</span>
            </div>

            <div class="compound-row">
              <div>
                <p class="t-overline" style="margin-bottom:4px">10-YR PROJECTION</p>
                <p class="compound-amt t-display t-green">RM 12,793</p>
                <p class="t-mono t-gun" style="font-size:8.5px">RM 6,500 saved @ 7% p.a.</p>
              </div>
              <div class="compound-bars">
                <div v-for="(h,i) in [18,28,38,49,60,70,80,88,95,100]" :key="i"
                     class="cbar" :style="{ height: h+'%', opacity: i===9 ? 1 : 0.35+(i*0.065) }" />
              </div>
            </div>
          </div>

          <div class="ai-copy">
            <span class="t-overline">// BEHAVIORAL BRAIN</span>
            <h2 class="sec-h2 t-display" style="text-align:left">Spend with<br />Intention.</h2>
            <p class="t-body ai-body">
              Before any "Want" purchase over RM 50, Ring-It checks your DSR,
              daily budget, and emergency fund — then issues a Buy or No-Buy
              recommendation with hard numbers. You still proceed if you want,
              but only after writing <em>why</em>.
            </p>
            <div class="ai-feats">
              <div v-for="f in aiFeats" :key="f.title" class="ai-feat">
                <span class="ai-feat-icon">{{ f.icon }}</span>
                <div>
                  <p class="ai-feat-title t-plat">{{ f.title }}</p>
                  <p class="ai-feat-desc t-body">{{ f.desc }}</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- COMPLIANCE -->
    <section class="sov-section sov-section--alt" id="compliance">
      <div class="sov-container">
        <div class="sec-head">
          <span class="t-overline">// MALAYSIAN REGULATORY COMPLIANCE</span>
          <h2 class="sec-h2 t-display">Government<br />Dependencies.</h2>
        </div>
        <div class="comp-grid">
          <div v-for="c in compliance" :key="c.law" class="sov-card sov-card--hover comp-card">
            <div class="comp-top">
              <span class="t-label">{{ c.law }}</span>
              <span class="sov-chip" :class="`sov-chip--${c.color}`">{{ c.status }}</span>
            </div>
            <p class="comp-title t-plat">{{ c.title }}</p>
            <p class="comp-desc t-body">{{ c.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="sov-section">
      <div class="sov-container">
        <div class="sov-card cta-card">
          <div class="cta-glow" />
          <span class="t-overline">// THE VAULT IS OPEN</span>
          <h2 class="cta-h2 t-display">Your Ledger Awaits.</h2>
          <p class="t-body cta-body">Free to start. Built to last. Zero compromise.</p>
          <a href="#" class="sov-btn sov-btn--primary sov-btn--lg">Create Account →</a>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="site-footer">
      <div class="sov-container">
        <div class="footer-inner">
          <div>
            <div class="nav-brand" style="margin-bottom:10px">
              <img src="@/assets/ring-it.png" alt="Ring-It Logo" class="brand-logo-img">
              <div><p class="brand-name t-mono">RING-IT</p></div>
            </div>
            <p class="footer-tag t-body">Personal Finance · Behavioral Wealth System<br/>Sontiqo &amp; Co · Muhammad Faiz bin Azmi · 2026</p>
          </div>
          <div v-for="col in footerCols" :key="col.title" class="footer-col">
            <p class="footer-col-title t-mono">{{ col.title }}</p>
            <button
              v-for="l in col.links"
              :key="l"
              class="footer-link footer-link--btn"
              @click="openModal(l)"
            >{{ l }}</button>
          </div>
        </div>
        <div class="footer-bottom t-mono">
          <span>© 2026 Sontiqo &amp; Co · MIT License</span>
        </div>
      </div>
    </footer>

    <!-- ── MODALS ── -->
    <teleport to="body">
      <transition name="modal-fade">
        <div v-if="activeModal" class="modal-backdrop" @click.self="activeModal = null">
          <div class="modal-shell" role="dialog" :aria-label="activeModal.title">

            <div class="modal-topbar">
              <div class="modal-brand-row">
                <span class="modal-dot" />
                <span class="t-mono modal-overline">{{ activeModal.id }}</span>
              </div>
              <button class="modal-close" @click="activeModal = null" aria-label="Close">✕</button>
            </div>

            <h2 class="modal-title t-display">{{ activeModal.title }}</h2>
            <p class="modal-sub t-mono">{{ activeModal.sub }}</p>

            <div class="modal-body">
              <div v-for="section in activeModal.sections" :key="section.heading" class="modal-section">
                <div class="modal-sec-head">
                  <span class="modal-sec-num t-mono">{{ section.num }}</span>
                  <h3 class="modal-sec-title t-plat">{{ section.heading }}</h3>
                </div>
                <p class="t-body modal-sec-body">{{ section.body }}</p>
              </div>
            </div>

            <div class="modal-footer-bar">
              <span class="sov-chip sov-chip--green">Ring-It v1.0</span>
              <span class="t-mono t-gun" style="font-size:9px">Sontiqo &amp; Co · 2026</span>
            </div>

          </div>
        </div>
      </transition>
    </teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'

const mobileOpen = ref(false)
const scrolled    = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 40 }
onMounted(()   => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const trust = ['PDPA 2010', 'LHDN 2026/2027', 'BNM RMIT']

const mockTxns = [
  { id: '1', type: 'income',  icon: '↓', cat: 'Salary',           acc: 'Maybank Savings', amt: '6,500.00' },
  { id: '2', type: 'expense', icon: '↑', cat: 'Dining · WANT',    acc: 'TnG eWallet',     amt: '45.80'    },
  { id: '3', type: 'expense', icon: '↑', cat: 'Transport · NEED', acc: 'TnG eWallet',     amt: '12.50'    },
]

const levers = [
  { num: '01', emoji: '🛡', title: 'Friction by Design',
    desc: '"Want" purchases over RM 50 trigger a live DSR + budget check. You must type a justification note before the transaction saves.',
    tag: 'Mandatory Friction' },
  { num: '02', emoji: '📈', title: 'Immediate Reward',
    desc: 'Every savings log instantly shows the 10-year compounded projection at 7% annual return. Your future wealth is visible now.',
    tag: 'Habit Loop' },
  { num: '03', emoji: '🔄', title: 'Habit Anchoring',
    desc: 'The Daily Gauge resets every midnight — the Fresh Start Effect on repeat. Your vault starts clean each morning.',
    tag: 'Fresh Start Effect' },
]

const caps = [
  { id: 'MOD-01', icon: '🏦', hi: false, title: 'Account & Ledger',
    desc: 'Multi-account real-time ledger — Bank, E-Wallet, Cash. Zero-sum transfers. IOU tracking. Live net worth snapshot.',
    tags: ['Double-Entry', 'Net Worth'] },
  { id: 'MOD-05', icon: '🧾', hi: true,  title: 'LHDN Receipt Vault',
    desc: 'Encrypted receipts with 7-year retention. Real-time cap tracking for 2026/2027 LHDN relief categories.',
    tags: ['LHDN 2026', '7yr Retention'] },
  { id: 'MOD-06', icon: '🕌', hi: false, title: 'EPF & Zakat',
    desc: 'Internal EPF RIA benchmarking across 3 tiers (RM 390K / 650K / 1.3M).',
    tags: ['EPF RIA', 'Zakat', 'Internal'] },
  { id: 'MOD-07', icon: '🏛', hi: true,  title: 'Banking Readiness',
    desc: 'Real-time DSR calculator with Malaysian bank grading. CCRIS payment streak gamification. Snowball / Avalanche debt payoff toggle.',
    tags: ['DSR', 'CCRIS', 'BNM'] },
  { id: 'MOD-08', icon: '🌍', hi: false, title: 'Exchange Rates & Goals',
    desc: 'Live Exchange Rates API with 150+ pairs refreshed every 15 min. Foreign-currency goals auto-buffered with 2–5% volatility protection.',
    tags: ['150+ Pairs', 'Volatility Buffer'] },
  { id: 'MOD-10', icon: '⚙️', hi: false, title: 'Policy Config',
    desc: 'Auto-migrates Jan 1st with immutable audit trail.',
    tags: ['Versioned'] },
]

const aiFeats = [
  { icon: '🔴', title: 'Buy / No-Buy Advisor',   desc: 'Live check of DSR, daily allowance, and emergency fund before every Want purchase.' },
  { icon: '✍️', title: 'Mandatory Justification', desc: 'Cannot save a Want >RM 50 without typing your reason — friction that actually works.' },
  { icon: '📊', title: '10-Year Compounding',     desc: 'Every saving instantly projects future wealth at a configurable annual return rate.' },
  { icon: '🔔', title: 'Subscription Audit',      desc: 'Detects recurring charges and alerts on any price increase exceeding 5%.' },
]

const compliance = [
  { law: 'PDPA 2010 (Act 709)', status: 'Compliant', color: 'green',
    title: 'Personal Data Protection', desc: '7-year receipt retention.' },
  { law: 'LHDN 2026/2027',      status: 'Internal',  color: 'amber',
    title: 'Tax Relief Tracking',      desc: 'All brackets and relief caps.' },
  { law: 'EPF / Zakat',         status: 'Internal',  color: 'amber',
    title: 'Retirement & Zakat',       desc: 'EPF RIA tiers and Zakat Nisab computed entirely.' },
  { law: 'BNM RMIT',            status: 'Compliant', color: 'green',
    title: 'Financial Security',       desc: 'Rate limiting.' },
]

const footerCols = [
  { title: '// LEGAL',      links: ['MIT License', 'Terms of Service', 'Risk Disclosure'] },
  { title: '// GOVERNANCE', links: ['Compliance Framework', 'Privacy Policy', 'PDPA Notice', 'Data Encryption'] },
]

// ── MODAL ──
interface ModalSection { num: string; heading: string; body: string }
interface ModalContent { id: string; title: string; sub: string; sections: ModalSection[] }

const activeModal = ref<ModalContent | null>(null)

const modalContent: Record<string, ModalContent> = {
  'MIT License': {
    id: '// LEGAL · LIC-01',
    title: 'MIT License',
    sub: 'Open-source · Permissive · Free forever',
    sections: [
      { num: '§1', heading: 'Grant of Rights', body: 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files ("Ring-It"), to deal in the software without restriction — including the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software — and to permit persons to whom the software is furnished to do so.' },
      { num: '§2', heading: 'Conditions', body: 'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software. Attribution to Sontiqo & Co and Muhammad Faiz bin Azmi must be preserved in any redistribution.' },
      { num: '§3', heading: 'Disclaimer', body: 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM OR IN CONNECTION WITH THE SOFTWARE.' },
      { num: '§4', heading: 'Jurisdiction', body: 'This license shall be governed by and construed under the laws of Malaysia. Any disputes arising from this license shall be subject to the jurisdiction of Malaysian courts.' },
    ],
  },
  'Terms of Service': {
    id: '// LEGAL · TOS-01',
    title: 'Terms of Service',
    sub: 'Effective 1 January 2026 · Ring-It v1.0',
    sections: [
      { num: '§1', heading: 'Acceptance', body: 'By accessing or using Ring-It ("the App"), you agree to be bound by these Terms. If you do not agree, discontinue use immediately. These Terms form a binding legal agreement between you and Sontiqo & Co.' },
      { num: '§2', heading: 'Financial Disclaimer', body: 'Ring-It is a personal finance management tool and does NOT constitute financial advice, investment advice, or professional consultation. All projections (e.g., 10-year compound estimates) are illustrative only. Always consult a licensed financial planner for investment decisions.' },
      { num: '§3', heading: 'User Responsibilities', body: 'You are responsible for maintaining the accuracy of data you enter. Ring-It stores your financial data locally and encrypted. You must not use the App for any unlawful purpose or in violation of Malaysian law, including the PDPA 2010 (Act 709).' },
      { num: '§4', heading: 'Modifications', body: 'Sontiqo & Co reserves the right to modify these Terms at any time. Continued use after modifications constitutes acceptance. Material changes will be notified via in-app notification at least 14 days in advance.' },
      { num: '§5', heading: 'Termination', body: 'We reserve the right to terminate or suspend access for breach of these Terms. Upon termination, your data export will be made available for 30 days before permanent deletion, in compliance with PDPA obligations.' },
    ],
  },
  'Risk Disclosure': {
    id: '// LEGAL · RSK-01',
    title: 'Risk Disclosure',
    sub: 'Read carefully before using financial projections',
    sections: [
      { num: '§1', heading: 'Projection Accuracy', body: 'All compound growth projections displayed in Ring-It (default: 7% p.a.) are hypothetical and based on historical averages. Past performance of any asset class does not guarantee future results. Actual returns may be significantly higher or lower.' },
      { num: '§2', heading: 'Exchange Rate Risk', body: 'Live exchange rates are sourced from third-party APIs and refreshed every 15 minutes. Rates displayed may differ from interbank rates. Foreign currency goals include a 2–5% volatility buffer, but this does not eliminate currency risk.' },
      { num: '§3', heading: 'DSR & Credit Risk', body: "The Debt Service Ratio (DSR) calculator uses data you provide and BNM guidelines. Ring-It's credit readiness assessment is indicative only and does not guarantee loan approval or reflect actual bank underwriting criteria." },
      { num: '§4', heading: 'Tax Guidance Limitation', body: "LHDN relief tracking is based on publicly available 2026/2027 LHDN guidelines. Tax law is subject to change. Ring-It's calculations do not constitute tax advice. Consult a licensed tax agent for official filings." },
    ],
  },
  'Compliance Framework': {
    id: '// GOVERNANCE · GOV-01',
    title: 'Compliance Framework',
    sub: 'Malaysian regulatory alignment · Ring-It v1.0',
    sections: [
      { num: '§1', heading: 'PDPA 2010 (Act 709)', body: "Ring-It is designed for full compliance with Malaysia's Personal Data Protection Act 2010. User financial data is processed only for the stated purpose of personal finance management. Data is encrypted at rest using AES-256 and never sold to third parties." },
      { num: '§2', heading: 'BNM RMIT Guidelines', body: "Our financial security architecture aligns with Bank Negara Malaysia's Risk Management in Technology (RMIT) framework. This includes rate limiting on all API endpoints, audit trails for sensitive operations, and session management controls." },
      { num: '§3', heading: 'LHDN Compliance', body: 'Receipt vault retention is set to 7 years in line with LHDN audit requirements. All relief category caps reflect the official 2026/2027 assessment year guidelines published by Lembaga Hasil Dalam Negeri Malaysia.' },
      { num: '§4', heading: 'EPF Act 1991', body: "EPF RIA benchmark tiers (RM 390K / RM 650K / RM 1.3M) are sourced from EPF's Retirement Income Adequacy framework. Calculations are for self-assessment only and do not represent official EPF projections." },
    ],
  },
  'Privacy Policy': {
    id: '// GOVERNANCE · PRV-01',
    title: 'Privacy Policy',
    sub: 'How Ring-It handles your personal financial data',
    sections: [
      { num: '§1', heading: 'Data We Collect', body: "Ring-It collects financial data you voluntarily enter: account balances, transactions, income, expenses, and uploaded receipts. We do not collect biometric data, location data (beyond your stated currency region), or device identifiers beyond what is necessary for app function." },
      { num: '§2', heading: 'How We Use Your Data', body: "Your data is used solely to power Ring-It's features: ledger tracking, budget calculations, DSR analysis, LHDN relief tracking, and EPF benchmarking. We do not use your data for advertising, profiling, or any purpose beyond the stated app function." },
      { num: '§3', heading: 'Data Storage & Security', body: 'All data is encrypted at rest (AES-256) and in transit (TLS 1.3). Receipt vault data is retained for 7 years per LHDN requirements. Other data is retained for the duration of your account. You may export or delete your data at any time from Settings.' },
      { num: '§4', heading: 'Third-Party Services', body: 'Ring-It uses a third-party exchange rate API for live FX data. Only your selected currency pairs are queried — no personal or financial data is transmitted. No other third-party data processors have access to your financial records.' },
      { num: '§5', heading: 'Your Rights (PDPA)', body: 'Under PDPA 2010, you have the right to access, correct, and withdraw consent for processing of your personal data. To exercise these rights or submit a complaint, contact privacy@sontiqo.co. We will respond within 21 days as required by law.' },
    ],
  },
  'PDPA Notice': {
    id: '// GOVERNANCE · PDPA-01',
    title: 'PDPA Notice',
    sub: 'Personal Data Protection Act 2010 (Act 709) · Malaysia',
    sections: [
      { num: '§1', heading: 'Data Controller', body: 'The data controller for Ring-It is Sontiqo & Co, operated by Muhammad Faiz bin Azmi. For all data protection enquiries, contact: privacy@sontiqo.co or write to our registered address in Kuala Lumpur, Malaysia.' },
      { num: '§2', heading: 'Purpose of Processing', body: 'Your personal and financial data is collected and processed for the purpose of providing personal finance management services through Ring-It. This includes ledger management, budgeting, tax relief tracking, and financial goal setting.' },
      { num: '§3', heading: 'Consent', body: 'By creating a Ring-It account, you provide explicit consent for the processing described in this notice. You may withdraw consent at any time by deleting your account. Withdrawal of consent will not affect the lawfulness of processing prior to withdrawal.' },
      { num: '§4', heading: 'Data Retention', body: 'Receipt and tax-related data is retained for 7 years as required by LHDN. All other personal data is retained for the duration of your account plus 90 days after account closure to allow for data export. Anonymised aggregate data may be retained indefinitely.' },
      { num: '§5', heading: 'Cross-Border Transfer', body: 'Ring-It does not transfer your personal data outside of Malaysia except where necessary for exchange rate API queries (currency pair data only, no personal identifiers). All such transfers comply with PDPA Section 129 requirements.' },
    ],
  },
  'Data Encryption': {
    id: '// GOVERNANCE · SEC-01',
    title: 'Data Encryption',
    sub: 'Security architecture · Ring-It Vault',
    sections: [
      { num: '§1', heading: 'Encryption at Rest', body: 'All user financial data stored in the Ring-It Vault is encrypted using AES-256-GCM, the current gold standard for symmetric encryption. Encryption keys are derived using PBKDF2 with a unique salt per user, ensuring no two users share encryption parameters.' },
      { num: '§2', heading: 'Encryption in Transit', body: 'All data transmitted between your device and Ring-It servers uses TLS 1.3 with perfect forward secrecy (PFS). Older TLS versions (1.0, 1.1) are explicitly disabled. Certificate pinning is enforced on mobile clients to prevent MITM attacks.' },
      { num: '§3', heading: 'Receipt Vault Security', body: "Uploaded receipts in the LHDN vault are stored with client-side encryption before upload. This means even Ring-It's servers cannot read the raw content of your receipts — only you hold the decryption key derived from your account credentials." },
      { num: '§4', heading: 'BNM RMIT Alignment', body: "Our security posture aligns with Bank Negara Malaysia's RMIT framework. This includes: API rate limiting to prevent brute force, immutable audit logs for all financial mutations, session timeout after 15 minutes of inactivity, and regular penetration testing." },
    ],
  },
}

function openModal(label: string) {
  const content = modalContent[label]
  if (content) activeModal.value = content
}

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') activeModal.value = null
}
onMounted(()   => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<style scoped>
.page-root { position: relative; min-height: 100vh; overflow-x: hidden; }

/* NAV */
.glass-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(8,8,8,.65); backdrop-filter: blur(26px) saturate(1.8); -webkit-backdrop-filter: blur(26px) saturate(1.8); border-bottom: 1px solid transparent; transition: border-color .3s, background .3s; }
.glass-nav.scrolled { border-bottom-color: var(--color-glass-bo); background: rgba(8,8,8,.88); }
.nav-inner { height: 60px; display: flex; align-items: center; }
.nav-brand { display: flex; align-items: center; gap: 9px; flex-shrink: 0; }
.brand-logo-img { width: 32px; height: 32px; object-fit: contain; filter: drop-shadow(0 0 8px rgba(255,255,255,0.2)); margin-right: 10px; }
.brand-name { font-size: 12px; font-weight: 500; letter-spacing: 4px; color: var(--color-plat); line-height: 1; }
.brand-sub  { font-size: 9px; letter-spacing: 2px; color: var(--color-gun); margin-top: 2px; }
.nav-end { display: none; margin-left: auto; gap: 4px; align-items: center; }
@media (min-width: 860px) { .nav-end { display: flex; } }
.hamburger { display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 5px; width: 36px; height: 36px; background: rgba(224,224,224,.04); border: 1px solid var(--color-glass-bo); border-radius: 8px; margin-left: auto; flex-shrink: 0; }
@media (min-width: 860px) { .hamburger { display: none; } }
.hamburger span { display: block; width: 15px; height: 1.5px; background: rgba(224,224,224,.7); border-radius: 2px; transition: all .24s ease; transform-origin: center; }
.hamburger.open span:nth-child(1) { transform: translateY(6.5px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; }
.hamburger.open span:nth-child(3) { transform: translateY(-6.5px) rotate(-45deg); }
.mobile-drawer { max-height: 0; overflow: hidden; transition: max-height .35s ease, padding .3s; padding: 0 20px; }
.mobile-drawer.active { max-height: 380px; padding: 14px 20px 22px; border-top: 1px solid var(--color-glass-bo); }
.mobile-link { display: block; font-size: 15px; color: rgba(224,224,224,.7); padding: 10px 0; border-bottom: 1px solid rgba(224,224,224,.05); transition: color .18s; }
.mobile-link:hover { color: var(--color-plat); }

/* HERO */
.hero { padding-top: calc(60px + 52px); padding-bottom: 80px; min-height: 100svh; display: flex; align-items: center; }
@media (min-width: 900px) { .hero { padding-top: calc(60px + 72px); padding-bottom: 100px; } }
.hero-layout { display: grid; grid-template-columns: 1fr; gap: 60px; align-items: start; }
@media (min-width: 1020px) { .hero-layout { grid-template-columns: 1fr 440px; align-items: center; gap: 68px; } }
.hero-copy { display: flex; flex-direction: column; }
.eyebrow { display: inline-flex; align-items: center; gap: 8px; padding: 5px 14px; background: rgba(224,224,224,.04); border: 1px solid rgba(224,224,224,.08); border-radius: 100px; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: var(--color-gun); margin-bottom: 20px; width: fit-content; }
.hero-h1 { font-size: clamp(2.2rem, 5.5vw, 3.8rem); margin-bottom: 18px; }
.hero-quote { font-size: 10.5px; font-style: italic; line-height: 1.75; color: rgba(117,117,117,.7); border-left: 2px solid var(--color-ox); padding-left: 14px; margin: 0 0 28px; max-width: 400px; }
.qm { font-size: 16px; color: var(--color-ox); font-style: normal; vertical-align: -3px; margin-right: 1px; }
.hero-quote footer { color: rgba(117,117,117,.45); margin-top: 4px; font-size: 9.5px; }
.hero-cta { margin-top: 4px; }

/* MOCK DASHBOARD */
.hero-visual { position: relative; display: none; }
@media (min-width: 1020px) { .hero-visual { display: block; } }
.mock-shell { background: rgba(12,12,14,.88); backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px); border: 1px solid rgba(224,224,224,.1); border-radius: var(--radius-lg); padding: 18px; box-shadow: 0 40px 90px rgba(0,0,0,.6), inset 0 0 0 1px rgba(255,255,255,.04); position: relative; z-index: 1; }
.mock-shell::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,.22) 50%, transparent); border-radius: var(--radius-lg) var(--radius-lg) 0 0; }
.mock-topbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.mock-brand-row { display: flex; align-items: center; gap: 6px; }
.mock-dot { width: 7px; height: 7px; background: var(--color-ox); border-radius: 50%; box-shadow: 0 0 8px rgba(128,0,32,.9); }
.mock-mono { font-size: 9px; letter-spacing: 2.5px; }
.mock-nw { margin-bottom: 14px; }
.mock-nw-amt { display: flex; align-items: baseline; gap: 4px; margin-bottom: 5px; }
.mock-ccy { font-size: 11px; }
.mock-big { font-size: 1.85rem; font-weight: 700; letter-spacing: -.03em; line-height: 1; }
.mock-nw-sub { display: flex; gap: 7px; font-size: 10px; }
.mock-widgets { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; margin-bottom: 12px; }
.mock-widget { background: rgba(8,8,8,.5); border: 1px solid rgba(224,224,224,.06); border-radius: 11px; padding: 10px; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.gauge-wrap { position: relative; width: 58px; height: 58px; }
.gauge-svg { width: 100%; height: 100%; }
.gauge-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.gauge-pct { font-size: 12px; font-weight: 500; line-height: 1; }
.gauge-sub { font-size: 7px; }
.ef-row { display: flex; align-items: baseline; gap: 4px; margin: 3px 0; }
.ef-num { font-size: 1.7rem; font-weight: 700; line-height: 1; }
.ef-unit { font-size: 9px; }
.mock-txns { margin-bottom: 10px; }
.mock-txn { display: flex; align-items: center; gap: 9px; padding: 7px 0; border-bottom: 1px solid rgba(224,224,224,.05); }
.mock-txn:last-child { border-bottom: none; }
.txn-ico { width: 26px; height: 26px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; flex-shrink: 0; }
.txn-ico--income  { background: rgba(76,175,80,.1);  color: var(--color-grn); }
.txn-ico--expense { background: rgba(128,0,32,.1);   color: #ef5350; }
.txn-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.txn-cat { font-size: 9.5px; }
.txn-acc { font-size: 8px; }
.txn-amt { font-size: 10.5px; font-weight: 500; white-space: nowrap; }
.float-tag { position: absolute; display: flex; align-items: center; gap: 6px; padding: 6px 11px; background: rgba(12,12,14,.92); border: 1px solid rgba(224,224,224,.09); border-radius: 100px; font-size: 9px; color: var(--color-gun); backdrop-filter: blur(18px); white-space: nowrap; z-index: 2; top: 12px; left: -52px; }
.float-tag-r { top: auto; left: auto; bottom: 50px; right: -44px; }
.float-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.float-dot-g { background: var(--color-grn); box-shadow: 0 0 5px var(--color-grn); }
.float-dot-r { background: var(--color-ox);  box-shadow: 0 0 5px var(--color-ox); }

/* TRUST STRIP */
.trust-strip { position: relative; z-index: 1; border-top: 1px solid var(--color-glass-bo); border-bottom: 1px solid var(--color-glass-bo); background: rgba(18,18,20,.5); backdrop-filter: blur(10px); padding: 12px 0; }
.trust-inner { display: flex; justify-content: center; flex-wrap: wrap; gap: 5px 18px; padding: 0 20px; }
.trust-item { display: flex; align-items: center; gap: 5px; font-size: 8.5px; letter-spacing: 1.5px; text-transform: uppercase; color: rgba(117,117,117,.7); }

/* SECTION HEADS */
.sec-head { text-align: center; max-width: 560px; margin: 0 auto 52px; }
.sec-h2 { font-size: clamp(1.6rem, 3.8vw, 2.3rem); margin-bottom: 13px; }

/* LEVERS */
.lever-grid { display: grid; grid-template-columns: 1fr; gap: 14px; }
@media (min-width: 640px) { .lever-grid { grid-template-columns: repeat(3, 1fr); } }
.lever-card { padding: 26px 22px; }
.lever-num   { display: block; font-size: 2.2rem; color: rgba(128,0,32,.28); line-height: 1; margin-bottom: 8px; }
.lever-emoji { display: block; font-size: 1.3rem; margin-bottom: 10px; }
.lever-title { font-size: .95rem; font-weight: 700; margin-bottom: 9px; }
.lever-desc  { font-size: .8rem; margin-bottom: 14px; }

/* CAPS */
.cap-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
@media (min-width: 640px) { .cap-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 960px) { .cap-grid { grid-template-columns: repeat(3, 1fr); } }
.cap-card { padding: 22px; }
.cap-top   { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.cap-icon  { font-size: 1.1rem; }
.cap-title { font-size: .9rem; font-weight: 700; margin-bottom: 7px; }
.cap-desc  { font-size: .78rem; margin-bottom: 13px; }
.cap-tags  { display: flex; flex-wrap: wrap; gap: 5px; }

/* AI SECTION */
.ai-layout { display: grid; grid-template-columns: 1fr; gap: 52px; align-items: start; }
@media (min-width: 960px) { .ai-layout { grid-template-columns: 420px 1fr; align-items: center; } }
.ai-flow-card { padding: 22px; }
.flow-step  { display: flex; align-items: center; gap: 8px; padding: 9px 11px; border-radius: 8px; }
.flow-step-input   { background: rgba(224,224,224,.04); border: 1px solid rgba(224,224,224,.08); }
.flow-step-justify { background: rgba(251,140,0,.06);  border: 1px solid rgba(251,140,0,.14); }
.flow-text   { font-size: 10px; color: var(--color-gun); }
.flow-arrow  { font-size: 15px; color: rgba(224,224,224,.13); text-align: center; margin: 4px 0; }
.flow-checks { display: flex; flex-direction: column; gap: 5px; padding: 9px 11px; background: rgba(8,8,8,.45); border-radius: 8px; }
.flow-check  { display: flex; align-items: center; gap: 8px; }
.fc-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.fc-g   { background: var(--color-grn); box-shadow: 0 0 5px var(--color-grn); }
.fc-a   { background: var(--color-amb); box-shadow: 0 0 5px var(--color-amb); }
.flow-verdict { display: flex; align-items: center; gap: 8px; padding: 9px 13px; border-radius: 8px; background: rgba(76,175,80,.08); border: 1px solid rgba(76,175,80,.18); }
.justify-input-mock { display: flex; align-items: center; gap: 4px; padding: 9px 11px; background: rgba(8,8,8,.5); border: 1px solid rgba(224,224,224,.05); border-radius: 7px; margin-top: 8px; margin-bottom: 16px; }
.justify-ph { font-size: 10px; color: rgba(117,117,117,.35); font-style: italic; }
.compound-row { display: flex; align-items: flex-end; justify-content: space-between; padding-top: 14px; border-top: 1px solid rgba(224,224,224,.06); }
.compound-amt { font-size: 1.3rem; letter-spacing: -.02em; margin-bottom: 3px; }
.compound-bars { display: flex; align-items: flex-end; gap: 3px; height: 38px; }
.cbar { width: 9px; background: var(--color-grn); border-radius: 2px 2px 0 0; }
.ai-body  { max-width: 440px; margin: 14px 0 24px; }
.ai-body em { color: rgba(224,224,224,.7); font-style: normal; }
.ai-feats { display: flex; flex-direction: column; gap: 14px; }
.ai-feat  { display: flex; align-items: flex-start; gap: 11px; }
.ai-feat-icon  { font-size: .95rem; flex-shrink: 0; margin-top: 1px; }
.ai-feat-title { font-size: .84rem; font-weight: 600; margin-bottom: 2px; }
.ai-feat-desc  { font-size: .77rem; line-height: 1.6; }

/* COMPLIANCE */
.comp-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
@media (min-width: 640px) { .comp-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 960px) { .comp-grid { grid-template-columns: repeat(4, 1fr); } }
.comp-card  { padding: 18px 20px; }
.comp-top   { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 9px; }
.comp-title { font-size: .84rem; font-weight: 600; margin-bottom: 5px; }
.comp-desc  { font-size: .76rem; line-height: 1.62; }

/* CTA */
.cta-card { max-width: 660px; margin: 0 auto; padding: 56px 36px; text-align: center; }
@media (max-width: 600px) { .cta-card { padding: 36px 22px; } }
.cta-glow { position: absolute; width: 420px; height: 420px; background: rgba(128,0,32,.1); border-radius: 50%; filter: blur(80px); top: 50%; left: 50%; transform: translate(-50%,-50%); pointer-events: none; }
.cta-h2   { font-size: clamp(1.8rem, 4.2vw, 2.8rem); margin-bottom: 11px; position: relative; }
.cta-body { font-size: .88rem; margin-bottom: 26px; position: relative; }

/* FOOTER */
.site-footer { position: relative; z-index: 1; border-top: 1px solid var(--color-glass-bo); padding: 48px 0 28px; background: rgba(8,8,8,.85); }
.footer-inner { display: grid; grid-template-columns: 1fr; gap: 32px; margin-bottom: 32px; }
@media (min-width: 640px) { .footer-inner { grid-template-columns: 2fr 1fr 1fr; } }
.footer-tag { font-size: .75rem; line-height: 1.8; color: rgba(117,117,117,.58); margin-top: 2px; max-width: 220px; }
.footer-col { display: flex; flex-direction: column; gap: 10px; }
.footer-col-title { font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(224,224,224,.5); margin-bottom: 2px; }
.footer-link { font-size: .78rem; color: rgba(117,117,117,.7); transition: color .18s; }
.footer-link:hover { color: rgba(224,224,224,.9); }
.footer-link--btn { background: none; border: none; padding: 0; cursor: pointer; text-align: left; font-family: inherit; }
.footer-bottom { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px; padding-top: 22px; border-top: 1px solid rgba(224,224,224,.05); font-size: .7rem; color: rgba(117,117,117,.4); }

/* ── MODAL BACKDROP ── */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999;
  background: rgba(4, 4, 6, 0.72);
  backdrop-filter: blur(14px) saturate(1.4);
  -webkit-backdrop-filter: blur(14px) saturate(1.4);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* ── MODAL SHELL ── */
.modal-shell {
  position: relative;
  width: 100%;
  max-width: 640px;
  max-height: 85svh;
  overflow-y: auto;
  background: rgba(12, 12, 14, 0.92);
  backdrop-filter: blur(40px) saturate(2);
  -webkit-backdrop-filter: blur(40px) saturate(2);
  border: 1px solid rgba(224, 224, 224, 0.11);
  border-radius: 18px;
  padding: 24px 28px 28px;
  box-shadow:
    0 60px 120px rgba(0, 0, 0, 0.7),
    0 0 0 1px rgba(255, 255, 255, 0.04) inset,
    0 1px 0 rgba(255, 255, 255, 0.14) inset;
  scrollbar-width: thin;
  scrollbar-color: rgba(224,224,224,0.08) transparent;
}
.modal-shell::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2) 50%, transparent);
  border-radius: 18px 18px 0 0;
  pointer-events: none;
}

/* ── MODAL TOP BAR ── */
.modal-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.modal-brand-row {
  display: flex;
  align-items: center;
  gap: 7px;
}
.modal-dot {
  width: 7px;
  height: 7px;
  background: var(--color-ox);
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(128, 0, 32, 0.9);
  flex-shrink: 0;
}
.modal-overline {
  font-size: 8.5px;
  letter-spacing: 2.5px;
  color: var(--color-gun);
}
.modal-close {
  width: 30px;
  height: 30px;
  background: rgba(224, 224, 224, 0.04);
  border: 1px solid rgba(224, 224, 224, 0.08);
  border-radius: 8px;
  color: rgba(224, 224, 224, 0.45);
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.18s, color 0.18s, border-color 0.18s;
  flex-shrink: 0;
}
.modal-close:hover {
  background: rgba(128, 0, 32, 0.15);
  color: rgba(224, 224, 224, 0.9);
  border-color: rgba(128, 0, 32, 0.3);
}

/* ── MODAL HEADER ── */
.modal-title {
  font-size: clamp(1.3rem, 3vw, 1.8rem);
  margin-bottom: 5px;
}
.modal-sub {
  font-size: 9px;
  letter-spacing: 1.5px;
  color: var(--color-gun);
  margin-bottom: 24px;
}

/* ── MODAL BODY ── */
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}
.modal-section {
  padding: 15px 16px;
  background: rgba(8, 8, 8, 0.5);
  border: 1px solid rgba(224, 224, 224, 0.06);
  border-radius: 10px;
  transition: border-color 0.2s;
}
.modal-section:hover {
  border-color: rgba(224, 224, 224, 0.11);
}
.modal-sec-head {
  display: flex;
  align-items: baseline;
  gap: 9px;
  margin-bottom: 8px;
}
.modal-sec-num {
  font-size: 9px;
  color: var(--color-ox);
  letter-spacing: 1px;
  flex-shrink: 0;
}
.modal-sec-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-plat);
}
.modal-sec-body {
  font-size: 0.76rem;
  line-height: 1.72;
  color: rgba(117, 117, 117, 0.85);
}

/* ── MODAL FOOTER BAR ── */
.modal-footer-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 18px;
  border-top: 1px solid rgba(224, 224, 224, 0.06);
}

/* ── TRANSITIONS ── */
.modal-fade-enter-active { transition: opacity 0.22s ease; }
.modal-fade-leave-active { transition: opacity 0.18s ease; }
.modal-fade-enter-active .modal-shell { transition: transform 0.26s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.22s ease; }
.modal-fade-leave-active .modal-shell { transition: transform 0.18s ease, opacity 0.18s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }
.modal-fade-enter-from .modal-shell { transform: scale(0.95) translateY(14px); opacity: 0; }
.modal-fade-leave-to .modal-shell   { transform: scale(0.97) translateY(6px);  opacity: 0; }
</style>