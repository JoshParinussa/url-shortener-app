import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/UrlShortener.vue';
import URLShortener from '../components/UrlShortener.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'Home' }
  },
  {
    path: '/url-shortener',
    name: 'URLShortener',
    component: URLShortener,
    meta: { title: 'URL Shortener' }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// Navigation guard to update the document title
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Default Title';
  next();
});

export default router;
