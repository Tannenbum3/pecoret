<script>
import AuthService from '@/service/AuthService';

export default {
    created() {
        // check dark theme
        const hasDarkPreference = window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (hasDarkPreference) {
            this.$primevue.changeTheme('lara-light-indigo', 'lara-dark-indigo', 'theme-css', () => {});
        }
        const authService = new AuthService();
        authService.checkAuth(this.$api);
    }
};
</script>

<template>
    <router-view />
</template>