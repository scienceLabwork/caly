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
        'pallight':'#f66ca5',
        'palpink':'#EE84D4',
        'pal1':'#D14D72',
        'pal2':'#FFABAB',
        'pal3':'#B22F59',
        'pal4':'#FFBCBC',
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('flowbite/plugin'),
    require("tw-elements/dist/plugin.cjs"),
    require('flowbite/plugin')
  ],
};