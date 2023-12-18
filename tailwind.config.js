/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'src/presentation/templates/**/*.html',
    'src/presentation/templates/**/*.html.jinja2',
  ],
  theme: {
    extend: {},
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      outline: '#ffffff',
      primary: {
        50: '#f3f1ff',
        100: '#ebe5ff',
        200: '#d9ceff',
        300: '#bea6ff',
        400: '#9f75ff',
        500: '#843dff',
        600: '#7916ff',
        700: '#6b04fd',
        800: '#5a03d5',
        900: '#4b05ad',
        950: '#2c0076',
      },
      onPrimary: '#000000',
      secondary: '#03dac6',
      onSecondary: '#000000',
      background: '#121212',
      onBackground: '#ffffff',
      surface: {
        50: '#ffffff1f',
        100: '#ffffff3d',
      },
      onSurface: '#ffffff',
      error: '#cf6679',
      onError: '#000000',
    },
  },
  plugins: [],
};
