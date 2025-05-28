const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
	transpileDependencies: true,
	publicPath: "./", // GitHub Pages 建議用相對路徑，避免資源抓不到
});
