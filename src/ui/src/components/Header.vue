<template lang="html">
  <header>
      <router-link :to="{ name: 'Main' }">
        <img src="../assets/images/logo.svg" alt="Logo" class="img-logo">
      </router-link>
  </header>
</template>

<script>
export default {
    name: "Header",

}
</script>

<style lang="less" scoped>
@import '../assets/style/config.less';

  header {
    background-color: @global-color;
    height: 90px;
    display: flex;
    justify-content: center;
    align-items: center;


    .img-logo {
        height: 53px;
        width: auto;
    }
  }
</style>
