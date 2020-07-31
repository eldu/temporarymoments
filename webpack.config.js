const path = require('path');
module.exports = {
  entry: path.join(__dirname, "src/main"),
  output: {
    path: path.join(__dirname, 'build'),
    filename: "bundle.js"
  },
  mode: 'development',
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
  devServer: {
    port: 8000,
    publicPath: '/build/'
  },
}