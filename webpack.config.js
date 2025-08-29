const path = require('path');
module.exports = {
  mode: process.env.NODE_ENV || 'production',
  entry: './src/index.js',
  output: { path: path.resolve(__dirname, 'dist'), filename: 'bundle.js', clean: true },
  module: { rules: [
    { test: /\.css$/i, use: ['style-loader','css-loader'] },
    { test: /\.(png|jpe?g|gif|svg)$/i, type: 'asset/resource' }
  ]},
  resolve: { extensions: ['.js'] }
};
