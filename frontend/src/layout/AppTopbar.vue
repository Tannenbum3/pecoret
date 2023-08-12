<script>
import { useAuthStore } from "@/store/auth";
import ProjectTabMenu from "./ProjectTabMenu.vue";
import AuthService from "../service/AuthService";

export default {
    name: "AppTopbar",
    data() {
        return {
            topbarMenuActive: null,
            authStore: useAuthStore(),
            userMenuItems: [
                {
                    label: "Settings",
                    icon: "fa fa-gear",
                    to: this.$router.resolve({
                        name: "UserSettingsDetail"
                    })
                },
                {
                    separator: true
                },
                {
                    label: "Logout",
                    icon: "fa fa-right-from-bracket",
                    command: this.onLogout
                }
            ],
            adminMenuItems: [
                {
                    label: "Users",
                    to: this.$router.resolve({
                        name: "UserList"
                    })
                },
                {
                    label: "Report Templates",
                    to: this.$router.resolve({
                        name: "ReportTemplateList"
                    })
                },
                {
                    label: "Project Types",
                    to: this.$router.resolve({
                        name: "ProjectTypeList"
                    })
                }
            ]
        };

    },
    computed: {
        showCompanyButton() {
            if (this.authStore.groups.isVendor === true) {
                return false;
            }
            return true;
        },
        showVulnerabilityTemplatesButton() {
            if (this.authStore.groups.isVendor === true) {
                return false;
            }
            return true;
        },
        showProjectButton() {
            if (this.authStore.groups.isVendor === true) {
                return false;
            }
            return true;
        },
        topbarMenuClasses() {
            return {
                "layout-topbar-menu-mobile-active": this.topbarMenuActive
            };
        },
        advisoryMenuItems() {
            let items = [
                {
                    label: "My Advisories",
                    to: this.$router.resolve({
                        name: "AdvisoryList"
                    })
                }
            ];
            if (this.authStore.groups.isAdvisoryManagement === true) {
                items.push({
                    label: "Inbox",
                    to: this.$router.resolve({
                        name: "AdvisoryInbox"
                    })
                });
                items.push({
                    label: "Labels",
                    to: this.$router.resolve({
                        name: "AdvisoryManagementLabelList"
                    })
                });
            }
            return items;
        }
    },
    methods: {

        onLogout() {
            const authService = new AuthService();
            authService.logout(this.$api).then(() => {
                this.$router.push({ name: "Login" });
            });
        },
        toggleMenu(event) {
            this.$refs.menu.toggle(event);
        },
        onTopBarMenuButton() {
            this.topbarMenuActive = !this.topbarMenuActive;
        },
        toggleAdvisoryMenu(event) {
            this.$refs.advisoryMenu.toggle(event);
        },
        toggleAdminMenu(event) {
            this.$refs.adminMenu.toggle(event);
        }
    },
    components: { ProjectTabMenu }
};
</script>

<template>
    <div class="layout-topbar">
        <router-link to="/" class="layout-topbar-logo">
            <img src="/images/logo-icon.svg" alt="logo" />
            <span>PeCoReT</span>
        </router-link>

        <button class="p-link layout-topbar-menu-button layout-topbar-button" @click="onTopBarMenuButton()">
            <i class="pi pi-ellipsis-v"></i>
        </button>

        <div class="layout-topbar-menu" :class="topbarMenuClasses">
            <Button label="Projects" class="p-link layout-topbar-button"
                    v-if="showProjectButton === true"
                    @click="this.$router.push({ name: 'ProjectList' })">
            </Button>
            <Button label="Companies" class="p-link layout-topbar-button"
                    v-if="showCompanyButton === true"
                    @click="this.$router.push({ name: 'CompanyList' })">
            </Button>
            <Button label="Vulnerability Templates" class="p-link layout-topbar-button"
                    v-if="showVulnerabilityTemplatesButton === true"
                    @click="this.$router.push({ name: 'VulnerabilityTemplateList' })">
            </Button>
            <Menu ref="advisoryMenu" :model="advisoryMenuItems" :popup="true"></Menu>
            <Button type="button" label="Advisories" icon="pi pi-angle-down" @click="toggleAdvisoryMenu"
                    class="p-link layout-topbar-button"></Button>
            <Button if="authStore.groups.isAdmin" label="Admin" v-if="this.authStore.groups.isAdmin"
                    icon="pi pi-angle-down"
                    @click="toggleAdminMenu" class="p-link layout-topbar-button"></Button>
            <Menu ref="adminMenu" :model="adminMenuItems" v-if="this.authStore.groups.isAdmin" :popup="true"
                  if="authStore.groups.isAdmin"></Menu>

            <div v-if="authStore.isAuthenticated">
                <Menu ref="menu" :model="userMenuItems" :popup="true"></Menu>
                <Button type="button" :label="authStore.me.username" icon="pi pi-angle-down" @click="toggleMenu"
                        class="p-link layout-topbar-button"></Button>
            </div>
        </div>
    </div>
    <ProjectTabMenu v-if="this.$route.params.projectId"></ProjectTabMenu>
</template>
