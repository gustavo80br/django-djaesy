import { createRouter, createWebHistory } from 'vue-router'
import TrackTime from '../components/views/TrackTime.vue'
import Login from '../components/views/Login.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/',
    name: 'Track Time',
    component: TrackTime,
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})
router.beforeEach((to, from, next) => {
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');
  if (authRequired && !loggedIn) {
    return next('/login');
  }
  if(loggedIn && to.path == '/login'){
    return next('/');
  }
  return next();
});

export default router
