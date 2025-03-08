module.exports = {
  content: [
    "./src/**/*.{html,js,jsx,ts,tsx}",
    // include your paths to JSX or TSX files if you're using React
  ],
  theme: {
    extend: {
      fontFamily: {
        "SourceSans": ["SourceSans", "sans-serif"] // Replace 'Inter' with your font
      },
    },
  },
  plugins: [],
};