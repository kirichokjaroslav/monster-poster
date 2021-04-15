<template lang="html">
  <div class="modal-content">
      <button @click="$emit('close')" class="close">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M1 1L11 11M1 11L11 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <h4>You really want to remove an employee?</h4>
      <button @click="$root.$emit('deleteUser', id); $emit('close')" class="button-primary">Yes</button>
  </div>
</template>

<script>
export default {
    name: "ConfirmDeleteModal",
    props: ['id']
}
</script>

<style lang="css" scoped>
@import '../assets/style/config.less';

h4 {
  font-size: 18px;
  line-height: 27px;
  text-align: center;
  color: @global-color;
  font-weight: 700;
  margin-bottom: 40px;
}

.modal-content {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

.button-primary {
  min-width: 120px;
}
</style>
