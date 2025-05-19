<template>
  <div class="test">
    <div class="sb">sb</div>
  </div>
</template>

<script setup>
</script>

<style scoped lang="scss">
.sb {
  backdrop-filter: blur(10px) brightness(90%);
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  height: 100px;
  width: 100px;
}

.test {
  display: flex;
  
  justify-content: center;
  align-items: center;
  height: calc(100vh - 100px);
}
</style>