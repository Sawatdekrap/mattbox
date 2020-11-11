const path = require("path");

module.exports = {
  entry: {
    chat_server: "./src/chat/index.ts"
  },
  module: {
    rules: [
      {
        test: /\.(ts)$/,
        exclude: /node_modules/,
        use: {
          loader: "ts-loader",
        },
      },
    ],
  },
  resolve: {
    alias: {
      common: path.resolve(__dirname, "src/common/"),
    },
    extensions: [".ts"],
  }
};
