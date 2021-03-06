import Vue from 'vue'
import App from './App.vue'
import SuiVue from 'semantic-ui-vue'
import 'semantic-ui-css/semantic.min.css'
import router from './router'
import VueResource from 'vue-resource'

Vue.config.productionTip = false
Vue.use(SuiVue);
Vue.use(VueResource);

Vue.directive('scroll', {
    inserted: function (el, binding) {
        let f = function (evt) {
            if (binding.value(evt, el)) {
                window.removeEventListener('scroll', f)
            }
        }
        window.addEventListener('scroll', f)
    }
})

new Vue({
    router: router,
    render: h => h(App),
    mounted: function () {
        console.log(this.$http);
    }
}).$mount('#app')
