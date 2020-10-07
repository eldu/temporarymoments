const path = require('path');
module.exports = {
  entry: path.join(__dirname, "src/entry"),
  output: {
    path: path.join(__dirname, 'build'),
    filename: "bundle.js"
  },
  mode: 'development', // TODO: 'production'
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel-loader',
        query: {
          presets: [['env', {
            targets: {
              browsers: ['> 1%', 'last 2 major versions'],
            },
            loose: true,
            modules: false,
          }]],
        }
      },
    ]
  },
  devtool: 'source-map',
}