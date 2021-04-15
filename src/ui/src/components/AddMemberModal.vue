<template lang="html">
  <div class="modal-content">
      <button @click="$emit('close')" class="close">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M1 1L11 11M1 11L11 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <h4>Новий співробітник</h4>
      <AddMemberForm @close="$emit('close')" />
  </div>
</template>

<script>
import AddMemberForm from './AddMembersForm.vue'

export default {
  name: "AddMemberModal",
  components: {
    AddMemberForm
  }
}
</script>

<style lang="less" scoped>

h4 {
  font-size: 24/16rem;
  text-align: center;
  margin-bottom: 40px;
}

</style>
