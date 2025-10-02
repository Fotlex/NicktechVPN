<script setup lang="ts">
import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();
const pageTitle = computed(() => (route.meta.title as string) || "");
</script>

<template>
  <div class="default-layout">
    <TopNav :title="pageTitle" />
    <main class="main-content">
      <router-view />
    </main>
    <BottomNav />
  </div>
</template>

<style scoped>
.default-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  overflow: hidden;
  background: linear-gradient(160deg, #4c2a4e 0%, #2c2c40 100%);; 
}

.main-content {
  flex-grow: 1;
  overflow-y: auto;
  padding-top: calc(50px + env(safe-area-inset-top));
  padding-bottom: calc(70px + env(safe-area-inset-bottom));
}
</style>
