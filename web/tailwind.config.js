/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          'linkedin': '#0072b1',
        }
      }
    },
    plugins: [
      require('tailwindcss-rtl'),
    ],
  }