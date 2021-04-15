<template lang="html">
  <div class="">
    <Header />
    <MembersList />
  </div>
</template>

<script>
import Header from '../components/Header.vue'
import MembersList from '../components/MembersList.vue'


export default {
  name: 'MainPage',
  components: {
    Header,
    MembersList
  }
}
</script>

<style lang="less" scoped>
</style>
