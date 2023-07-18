<script>
import AuthService from "@/service/AuthService";
import { useAuthStore } from "@/store/auth";


const authService = new AuthService();
const authStore = useAuthStore();

export default {
    name: "Login",
    mounted() {
        authService.checkAuth(this.$api);
        if (authStore.me) {
            if (authStore.groups.isVendor === true) {
                this.$router.push({ name: "AdvisoryList" });
            } else {
                this.$router.push({ name: "ProjectList" });

            }
        }
    },
    data() {
        return {
            username: null,
            password: null,
            loading: false
        };
    },
    methods: {
        login() {
            this.loading = true;
            authService.login(this.$api, this.username, this.password).then((response) => {
                authStore.setAuthData(response.data);
                if (authStore.groups.isVendor === true) {
                    this.$router.push({ name: "AdvisoryList" });
                } else {
                    this.$router.push({ name: "ProjectList" });

                }
            }).finally(() => {
                this.loading = false;
            });
        }
    }
};
</script>

<template>
    <Toast></Toast>
    <div
        class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <img src="/images/logo-icon.svg" alt="PeCoReT logo" class="mb-5 w-6rem flex-shrink-0" />
            <div
                style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <div class="text-900 text-4xl font-medium mb-3">PeCoReT</div>
                        <div class="text-900 text-1xl font-medium mb-3">Pentest Collaboration and Reporting Tool!</div>
                        <span class="text-600 font-medium">Sign in to continue</span>
                    </div>

                    <div>
                        <label for="username" class="block text-900 text-xl font-medium mb-2">Username</label>
                        <InputText id="username" type="text" placeholder="Username" class="w-full md:w-30rem mb-5"
                                   style="padding: 1rem" v-model="username" />

                        <label for="password" class="block text-900 font-medium text-xl mb-2">Password</label>
                        <Password id="password" v-model="password" placeholder="Password" :feedback="false"
                                  v-on:keyup.enter="login"
                                  :toggleMask="true" class="w-full mb-3" inputClass="w-full"
                                  :inputStyle="{padding: '1rem'}"></Password>

                        <div class="flex align-items-center justify-content-between mb-5 gap-5">
                            <a class="font-medium no-underline ml-2 text-right cursor-pointer"
                               @click="this.$router.push({name: 'ResetPassword'})"
                               style="color: var(--primary-color)">Forgot password?</a>
                        </div>
                        <Button :loading=loading label="Sign In" class="w-full p-3 text-xl" @click="login"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
