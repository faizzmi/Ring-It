import { createVuetify, type ThemeDefinition } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'
import '../styles/main.css'
import 'vuetify/styles'
const sovereign: ThemeDefinition = {
  dark: true,
  colors: {
    background: '#080808',
    surface:  '#121214',
    primary:  '#800020',
    secondary:  '#757575',
    accent:  '#E0E0E0',
    error:  '#B00020',
    success:  '#4CAF50',
    warning:  '#FB8C00',
    info:  '#2196F3',
    caution: '#FBC02D'
  },
}
export default createVuetify({
  theme: {
    defaultTheme: 'sovereign',
    themes: { sovereign },
  },
  display: {
    mobileBreakpoint: 'md',
    thresholds: { xs: 0, sm: 600, md: 840, lg: 1145, xl: 1545, xxl: 2138 },
  },
  defaults: {
    VCard:  { flat: true, rounded: 'sm', variant: 'flat', class: 'border-thin' },
    VBtn:  { rounded: 'xs', elevation: 0, class: 'text-uppercase letter-spacing-1' },
    VTextField: { variant: 'underlined', density: 'comfortable' },
  },
})