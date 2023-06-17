import { defineStore } from 'pinia';

export const useAuthStore = defineStore('authStore', {
  state: () => ({
    authToken: '',
    isAuthenticated: false,
    me: null,
    csrfToken: null,
    groups: { isAdmin: false, isManagement: false, isAdvisoryManagement: false },
    activeProject: {}
  }),
  getters: {
  },
  actions: {
    activateProject(project) {
      this.activeProject = project
    },
    deactivateProject(project) {
      this.activeProject = {}
    },
    setAuthData(responseData) {
      this.csrfToken = responseData.csrf_token
      if (responseData.user) {
        this.me = responseData.user
        this.groups.isAdmin = responseData.user.is_superuser
        let data = responseData.user
        data.groups.forEach((item) => {
          if (item.name === "Management") {
            this.groups.isManagement = true
          }
          if (item.name === "Advisory Management") {
            this.groups.isAdvisoryManagement = true
          }
        })
        this.isAuthenticated = true
      }
    },
    unsetMe() {
      this.me = null
      this.isAuthenticated = false
    },
    setMe(data) {
      this.me = data
      this.groups.isAdmin = data.is_superuser
      data.groups.forEach((item) => {
        if (item.name === "Management") {
          this.groups.isManagement = true
        }
        if (item.name === "Advisory Management") {
          this.groups.isAdvisoryManagement = true
        }
      })
    }
  },
});
