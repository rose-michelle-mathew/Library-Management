import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

const app = createApp(App);
const pinia = createPinia();


router.beforeEach((to, from, next) => {
    const isFirstLoad = !sessionStorage.getItem('visited');
    if (isFirstLoad) {
      sessionStorage.setItem('visited', 'true');
      if (to.path !== '/') {
        return next({ path: '/' });
      }
    }
    next();
  });

  

app.use(pinia);
app.use(router);

app.mount('#app');
