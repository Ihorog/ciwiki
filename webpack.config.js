const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: process.env.NODE_ENV || 'production',
  entry: './src/index.js', // заміни, якщо маєш TS/React entry
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true,
  },
  module: {
    rules: [
      { test: /\.css$/i, use: ['style-loader','css-loader'] },
      { test: /\.(png|jpe?g|gif|svg)$/i, type: 'asset/resource' }
      // якщо потрібен TypeScript, додай:
      // { test: /\.tsx?$/, use: 'ts-loader', exclude: /node_modules/ }
    ]
  },
  resolve: { extensions: ['.js'] }, // для TS/React: ['.tsx','.ts','.js']
  plugins: [
    new HtmlWebpackPlugin({
      template: 'public/index.html',
      inject: 'body'
    })
  ]
};
