<template>
	<transition name="fade">
		<button v-if="showBtn" class="back-to-top" @click="scrollToTop" aria-label="Back to top">
			<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16">
				<path
					fill-rule="evenodd"
					d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5"
				/>
			</svg>
		</button>
	</transition>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const showBtn = ref(false);

const scrollToTop = () => {
	window.scrollTo({ top: 0, behavior: "smooth" });
};

const handleScroll = () => {
	showBtn.value = window.scrollY > 200;
};

onMounted(() => {
	window.addEventListener("scroll", handleScroll);
});

onBeforeUnmount(() => {
	window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
.back-to-top {
	position: fixed;
	bottom: 2rem;
	right: 2rem;
	width: 48px;
	height: 48px;
	background-color: rgba(72, 160, 120, 0.85); /* 淺綠 + 半透明 */
	color: white;
	border: none;
	border-radius: 12px; /* 圓角 */
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 柔陰影 */
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.3s ease;
	z-index: 9999;
}

.back-to-top:hover {
	background-color: rgba(72, 160, 120, 1); /* hover 更深一點 */
	box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
}

/* Vue Transition 淡入淡出 */
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>
