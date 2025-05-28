<template>
	<nav class="navbar navbar-expand-lg bg-light border-bottom sticky-top shadow">
		<div class="container d-flex">
			<!-- 🔽 左：Logo & 標題組合 -->
			<router-link class="navbar-brand d-flex align-items-center" to="/">
				<img src="./image/榮總醫院 台南分院 logo.png" alt="logo" class="img-fluid" style="max-height: 40px" />
			</router-link>
			<h3 class="fw-bold">南榮樂活學苑</h3>

			<!-- 🔽 手機收合按鈕 -->
			<button
				class="navbar-toggler"
				type="button"
				data-bs-toggle="collapse"
				data-bs-target="#navbarNav"
				aria-controls="navbarNav"
				aria-expanded="false"
				aria-label="Toggle navigation"
			>
				<span class="navbar-toggler-icon"></span>
			</button>

			<!-- 🔽 導覽列 -->
			<div class="collapse navbar-collapse justify-content-end" id="navbarNav">
				<ul class="navbar-nav text-center text-lg-start">
					<li class="nav-item">
						<router-link class="nav-link" to="/homepage">首頁</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/aboutpage">關於我們</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/aboutpage">我們的理念</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/aboutpage">我們的服務</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/aboutpage">聯絡我們</router-link>
					</li>
				</ul>
			</div>
		</div>
	</nav>
	<!-- 這邊一定要放 router-view 才會顯示頁面 -->
	<router-view />
</template>

<style scoped>
/* 全域 Reset 樣式 */
* {
	padding: 0;
	margin: 0;
	box-sizing: border-box;
}

/* 啟用時的樣式 */
.router-link-activate {
	font-weight: bold;
	color: green;
}
</style>
