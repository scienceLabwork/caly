/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    './templates/**/*.{html,js}',
    './static/**/*.js',
    './node_modules/tw-elements/dist/js/**/*.js',
    'node_modules/preline/dist/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'palcream':'#F9D3AA',
        'palpink':'#EE84D4',
        'pal1':'#D14D72',
        'pal2':'#FFABAB',
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('flowbite/plugin'),
    require("tw-elements/dist/plugin.cjs"),
  ],
};