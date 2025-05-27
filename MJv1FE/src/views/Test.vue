<template>
  <table border="1" width="20%">
    <tr>
      <th>id</th>
      <th>姓名</th>
      <th>年龄</th>
    </tr>
      <tr>
        <td>1</td>
        <td>廖仁俊</td>
        <td>21</td>
      </tr>
  </table>
</template>

<script setup>
defineOptions({ name: 'TestPage' });
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