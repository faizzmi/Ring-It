/**
 * plugins/vuetify.ts
 */

import { createVuetify, type ThemeDefinition } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'
import '../styles/layers.css'
import 'vuetify/styles'

// Define the "Millionaire Minimalist" Theme
const sovereign: ThemeDefinition = {
  dark: true,
  colors: {
    background: '#080808', // Deepest Obsidian void
    surface: '#121214',    // Matte Iron (Vault surface)
    primary: '#800020',    // Flat Oxblood Red
    secondary: '#757575',  // Muted Gunmetal
    accent: '#E0E0E0',     // Platinum Silver for highlights
    error: '#B00020',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'sovereign',
    themes: {
      sovereign,
    },
  },
  // Maintain your specific breakpoints
  display: {
    mobileBreakpoint: 'md',
    thresholds: {
      xs: 0,
      sm: 600,
      md: 840,
      lg: 1145,
      xl: 1545,
      xxl: 2138,
    },
  },
  // Modern defaults to remove "shiny" shadows and add precision borders
  defaults: {
    VCard: {
      flat: true,
      rounded: 'sm', // Sharp, machined corners
      variant: 'flat',
      class: 'border-thin', // Use a 1px border instead of shadow
    },
    VBtn: {
      rounded: 'xs',
      elevation: 0,
      class: 'text-uppercase letter-spacing-1', // Professional bank-ledger style
    },
    VTextField: {
      variant: 'underlined', // Cleaner, more minimalist
      density: 'comfortable',
    }
  }
})