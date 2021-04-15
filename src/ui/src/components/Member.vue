<template lang="html">
  <div class="member">
      <span class="member-avatar"><img :src="userAvatar" alt="user"></span>
      <span class="member-name">{{ fullName }}</span>
      <span class="date">{{ in_company_from }}</span>
      <button @click="$emit('delete', id)" class="button-remove"></button>
  </div>
</template>

<script>
export default {
    name: 'Member',
    props: ['first_name', 'last_name', 'in_company_from', 'photography', 'id'],
    computed: {
      fullName() {
        return `${this.first_name} ${this.last_name}`
      },
      userAvatar() {
        return this.photography || require('../assets/images/default-avatar.jpg')
      }
    }
}
</script>

<style lang="less" scoped>
@import '../assets/style/config.less';

  .member {
    border: 1px solid #E9E9E9;
    box-sizing: border-box;
    border-radius: 8px;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    font-family: 'Proxima Nova', serif;
  }

  .member-avatar {
    margin-right: 12px;
    display: block;
    border-radius: 50%;
    overflow: hidden;

    img {
      width: 40px;
      height: 40px;
    }
  }

  .date {
    color: @secondary-color;
    margin-left: auto;
    margin-right: 20px;
  }

  .button-remove {
    background-color: @global-muted-background;
    width: 30px;
    height: 30px;
    display: block;
    border: none;
    border-radius: 50%;
    background-position: center center;
    background-repeat: no-repeat;
    transition: background-color .3s ease;
    background-image: url("data:image/svg+xml,%3Csvg width='12' height='16' viewBox='0 0 12 16' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1.83398 6.25H10.1673V13C10.1673 14.1046 9.27189 15 8.16732 15H3.83398C2.72942 15 1.83398 14.1046 1.83398 13V6.25Z' stroke='white' stroke-width='1.4'/%3E%3Cpath d='M4.75 8.875V12.375' stroke='white' stroke-width='1.4' stroke-linecap='round'/%3E%3Cpath d='M7.25 8.875V12.375' stroke='white' stroke-width='1.4' stroke-linecap='round'/%3E%3Cpath d='M4.33398 3.625H7.66732V2.66667C7.66732 1.74619 6.92113 1 6.00065 1V1C5.08018 1 4.33398 1.74619 4.33398 2.66667V3.625Z' stroke='white' stroke-width='1.4'/%3E%3Crect x='1' y='3.625' width='10' height='2.625' rx='1.3125' stroke='white' stroke-width='1.4'/%3E%3C/svg%3E%0A");

    &:hover,
    &:focus {
      background-color: @global-danger-background;
    }
  }
</style>
