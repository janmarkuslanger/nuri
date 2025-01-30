/** @type {import('tailwindcss').Config} */



module.exports = {
  content: ["../templates/**/*.html", "./src/**/*.{js,ts}"],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: ["retro"],
  },
  plugins: [
    require('daisyui')
  ],
};
