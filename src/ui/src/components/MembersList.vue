<template lang="html">
  <div class="container">
      <div class="members-list-header">
        <h1>Employees</h1>
        <button @click="openAddMember" class="button-primary">Add employee</button>
      </div>
      <div class="members-list">
          <div v-if="loadingList" :class="[{ 'minimal-spinner': members.length }, 'spinner-wrapper']">
            <div class="lds-dual-ring"></div>
            <span>Updating...</span>
          </div>
          <Member v-for="member in members" @delete="showDeleteConfimModal" v-bind="member" :key="member.id" class="member"/>
          <p v-if="isListEmpty && !loadingList" class="default-text">Employee list is empty</p>
      </div>
  </div>
</template>

<script>
import Member from './Member.vue'
import AddMemberModal from './AddMemberModal.vue'
import ConfirmDeleteModal from './ConfirmDeleteModal.vue'

import { getList, deleteUser, baseURL } from '../services/members'

const modalSetting = { width: 420, height: 'auto', styles: 'overflow: visible' }

export default {
  name: "MembersList",
  data() {
    return {
      loadingList: false,
      members: []
    }
  },
  computed: {
    isListEmpty() {
      return !this.members.length
    }
  },
  created(){
    this.fetchMemberList()
    this.$root.$on('deleteUser', this.deleteMember)
    this.$root.$on('triggerUpdateList', this.fetchMemberList)
  },
  methods: {
    async fetchMemberList(){
      this.loadingList = true
      try {
        let response = await getList()
        this.members = response.payload
        this.members = this.members.map(member => {
          return {
            ...member,
            photography: member.photography ? `${baseURL}${ member.photography }` : ''
          }
        })
      } catch(e) {
        this.$notify({ title: 'Щось пішло не так', type: 'error' });
      }
      this.loadingList = false
    },
    showDeleteConfimModal(id){
      this.$modal.show(ConfirmDeleteModal, { id }, modalSetting)
    },
    async deleteMember(id) {
      try {
        await deleteUser(id)
        this.fetchMemberList()
        this.$notify({ title: 'Employee removed', type: 'success' });
      } catch (e) {
        this.$notify({ title: 'Something went wrong', type: 'error' });
      }
    },
    openAddMember() {
      this.$modal.show(AddMemberModal, null, modalSetting)
    }
  },
  components: {
    Member
  }
}
</script>

<style lang="less" scoped>
@import '../assets/style/config.less';

  h1 {
    color: @global-color;
    font-family: Proxima Nova, sans-serif;
    font-style: normal;
    font-weight: 800;
    font-size: 24px;
    line-height: 29px;
  }

  .default-text {
    text-align: center;
    color: @secondary-color;
  }

  .container {
    max-width: 1000px;
    margin: 70px auto;
  }

  .members-list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .members-list {
    margin-top: 40px;
    background: #fff;
    box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 40px;
    position: relative;
  }


  .minimal-spinner {
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
  }

  .spinner-wrapper {
    display: flex;
    font-size: 12px;
    color: @secondary-color;
    justify-content: center;
    align-items: center;
  }

  .lds-dual-ring {
    display: block;
    margin-right: 10px;
  }

  .lds-dual-ring:after {
    border-color: @secondary-color transparent @secondary-color transparent;
  }

  .member {
    margin-bottom: 10px;
  }
</style>
