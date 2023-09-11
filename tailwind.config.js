/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**"],
  theme: {
    extend: {
      screens: {
        'phone': '360px',
      },
      colors: {
        'site-black': '#242F36',
        'menu-construart': '#041E37',
        'laranja-construart': '#D6480A',
      },
    },
  },
  plugins: [],
}