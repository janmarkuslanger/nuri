/** @type {import('tailwindcss').Config} */



module.exports = {
  content: ["./index.html",  "./src/**/*.{js,ts}"],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: ["business"],
  },
  plugins: [
    require('daisyui')
  ],
};
