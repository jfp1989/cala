import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Person from './components/Person.vue'
import Login from './components/Login.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/persons',
      name: 'persons',
      component: Person
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }      
  ]
})
