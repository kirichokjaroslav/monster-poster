<template>
  <div class="custom-select" :tabindex="tabindex" @blur="open = false">
    <div class="selected" :class="{open: open}" @click="open = !open">{{ selected.label }}</div>
    <div class="items" :class="{selectHide: !open}">
      <div
        class="item"
        v-for="(option, i) of options"
        :key="i"
        @click="selected = option; open=false; $emit('input', option)"
      >{{ option.label }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    options: {
      type: Array,
      required: true
    },
    value: {
      type: Object,
      required: false
    },
    tabindex: {
      type: Number,
      required: false,
      default: 0
    }
  },
  watch: {
    value: {
      handler(value){
        this.selected = value
      },
      immediate: true
    }
  },
  data() {
    return {
      selected: this.options.length > 0 ? this.options[0] : {},
      open: false
    };
  },
  mounted() {
    this.$emit("input", this.selected);
  }
};
</script>

<style scoped lang="less">
@import '../assets/style/config.less';

.custom-select {
  position: relative;
  width: 100%;
  text-align: left;
  outline: none;
  height: 47px;
  line-height: 47px;
}

.selected {
  color: @global-color;
  cursor: pointer;
  user-select: none;
  line-height: 1;
  padding-bottom: 14px;
  padding-top: 5px;
  border-bottom: #D1D1D1 1px solid;
}

.selected.open {
  border-radius: 6px 6px 0px 0px;
}

.selected:after {
  position: absolute;
  content: "";
  top: 10px;
  right: 0;
  width: 9px;
  height: 5px;
  transform-origin: 50% 50%;
  background-repeat: no-repeat;
  transition: transform .2s;
  background-image: url("data:image/svg+xml,%3Csvg width='8' height='5' viewBox='0 0 8 5' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L4 4L7 1' stroke='%232C3346' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E%0A");
}

.open.selected:after {
  transform: rotate(180deg);
}

.items {
  color: @global-color;
  border-radius: 0px 0px 6px 6px;
  position: absolute;
  background-color: #fff;
  box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.1);
  left: 0;
  right: 0;
  height: 200px;
  overflow: auto;
  z-index: 10;
}

.item {
  color: @global-color;
  padding-left: 8px;
  cursor: pointer;
  user-select: none;
}

.item:hover {
  background-color: lighten(@global-primary-background, 30%);
}

.selectHide {
  display: none;
}
</style>
