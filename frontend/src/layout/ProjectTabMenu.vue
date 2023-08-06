<script>
import {useAuthStore} from '@/store/auth'
import ProjectService from '@/service/ProjectService'


export default {
    name: 'ProjectTabMenu',
    mounted() {
        if(!this.authStore.activeProject.name){
            this.projectService.getProject(this.$route.params.projectId).then((response) => {
                this.authStore.activateProject(response.data)
            })
        }
    },
    data() {
        return {
            authStore: useAuthStore(),
            projectService: new ProjectService(),
            items: [
                {
                    label: 'Dashboard',
                    icon: 'fa fa-chart-line',
                    to: this.$router.resolve({ name: 'ProjectDetail', params: { projectId: this.$route.params.projectId } }).path
                },
                {
                    label: 'Findings',
                    icon: 'fa fa-bug',
                    to: this.$router.resolve({ name: 'FindingList', params: { projectId: this.$route.params.projectId } }).path
                },
                {
                    label: 'Checklists',
                    icon: 'fa fa-circle-check',
                    to: this.$router.resolve({
                        name: 'ProjectChecklistList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Assets',
                    icon: 'fa fa-crosshairs',
                    items: [
                        {
                            label: 'Web Applications',
                            to: this.$router.resolve({
                                name: 'WebApplicationList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            }).path
                        },
                        {
                            label: 'Hosts',
                            to: this.$router.resolve({
                                name: 'HostList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            }).path
                        },
                        {
                            label: 'Services',
                            to: this.$router.resolve({
                                name: 'ServiceList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            }).path
                        },
                        {
                            label: 'Mobile Applications'
                        }
                    ]
                },
                {
                    label: 'Reports',
                    icon: 'fa fa-file',
                    to: this.$router.resolve({
                        name: 'ReportList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Management',
                    icon: 'fa fa-calendar',
                    items: [
                        {
                            label: 'Contributors',
                            to: this.$router.resolve({
                                name: 'ContributorList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'API-Tokens',
                            to: this.$router.resolve({
                                name: 'APITokenList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'User Accounts',
                            to: this.$router.resolve({
                                name: 'UserAccountList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: 'Contacts',
                            to: this.$router.resolve({
                                name: 'ContactList',
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        },
                        {
                            label: "Files",
                            to: this.$router.resolve({
                                name: "ProjectFileList",
                                params: {
                                    projectId: this.$route.params.projectId
                                }
                            })
                        }
                    ]
                },
                {
                    label: 'Vulnerabilities',
                    icon: 'fa fa-bolt',
                    to: this.$router.resolve({
                        name: 'VulnerabilityList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                }
            ]
        }
    }
}
</script>

<template>
    <Menubar :model="items" class="surface-card"></Menubar>
</template>