import { createApp } from "vue";
import App from "./App.vue";

// Bootstrap 引入（可選）
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// Router 設定
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./components/HomePage.vue";
import AboutPage from "./components/AboutPage.vue";

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: "/", component: HomePage }, // 預設首頁
		{ path: "/homepage", component: HomePage }, // 預設首頁
		{ path: "/aboutpage", component: AboutPage }, // 預設首頁
	],
	linkActiveClass: "router-link-activate",
});

const app = createApp(App);
app.use(router);
app.mount("#app");
