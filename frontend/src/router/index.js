import {createRouter, createWebHistory} from 'vue-router';
import LoginView from '@/views/LoginView.vue';
import {createPinia} from 'pinia'
import SensorSettingsView from "@/views/SensorSettingsView.vue";
import MeasurementListView from "@/views/MeasurementListView.vue";
import {useUserStore} from "@/store/UserStore";

export const pinia = createPinia()

const routes = [
    {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: {forbidsAuth: true}
    },
    {
        path: '/',
        name: 'measurement-list',
        component: MeasurementListView,
        meta: {requiresAuth: true}
    },
    {
        path: '/sensor-settings',
        name: 'sensor-settings',
        component: SensorSettingsView,
        meta: {requiresAuth: true}
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const userStore = useUserStore()

    if (to.meta.requiresAuth && !userStore.isAuthenticated) {
        next('/login');
    } else if (to.meta.forbidsAuth && userStore.isAuthenticated) {
        next("/")
    } else {
        next();
    }
});

export default router;
