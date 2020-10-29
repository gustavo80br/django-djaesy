
const webpack = require('webpack'); //to access built-in plugins
const path = require('path');

const TerserJSPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const devMode = process.env.NODE_ENV !== 'production';

module.exports = {
  watch: devMode,
  entry: './app/main.js',
  output: {
    filename: 'djaesy.js',
    path: path.resolve(__dirname, '../static/'),
  },
  module: {
    rules: [
      { test: /\.tsx?$/, loader: "ts-loader" },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
        ],
      },
      {
        test: /\.s[ac]ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              hmr: process.env.NODE_ENV === 'development',
              reloadAll: true,
            },
          },
          'css-loader',
          'sass-loader',
        ],
      },
      {
        test: /\.less$/,
        loader: 'less-loader', // compiles Less to CSS
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        loader: 'file-loader?name=djaesy/images/[contenthash].[ext]'
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf|html)$/,
        loader: 'file-loader?name=djaesy/fonts/[contenthash].[ext]',
        // options: {
        //   outputPath: (url, resourcePath, context) => {
        //     return `/app_panel/fonts/${url}`;
        //   }
        // },
      },
      // Expose jquery globally for inline/legacy use
      {
          test: require.resolve('jquery'),
          use: [
              { loader: 'expose-loader', options: 'jQuery' },
              { loader: 'expose-loader', options: '$' }
          ]
      },
    ],
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
  optimization: {
    minimizer: [new TerserJSPlugin({}), new OptimizeCSSAssetsPlugin({})],
  },
  plugins: [
      new webpack.ProvidePlugin({ moment:'moment' }),
      new webpack.ProvidePlugin({ Raphael: 'raphael', toastr: 'toastr/toastr.js' }),
      new webpack.ProvidePlugin({ $: 'jquery', jQuery: 'jquery', jquery: 'jquery', 'window.jQuery': 'jquery' }),
      new MiniCssExtractPlugin({
        // Options similar to the same options in webpackOptions.output
        // both options are optional
        filename: devMode ? '[name].css' : '[name].[hash].css',
        chunkFilename: devMode ? '[id].css' : '[id].[hash].css',
      }),
  ]
};