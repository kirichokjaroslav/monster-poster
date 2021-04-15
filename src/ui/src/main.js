import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

import VModal from 'vue-js-modal'
Vue.use(VModal, { dynamic: true, injectModalsContainer: true })

import Notifications from 'vue-notification'
Vue.use(Notifications)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
