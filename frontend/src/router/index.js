import {createRouter, createWebHistory} from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'Home',
                    component: () => import('@/views/Home.vue')
                },
                {
                    path: '/admin',
                    children: [
                        {
                            path: '/admin/users',
                            name: 'UserList',
                            component: () => import('@/views/pages/admin/UserList.vue')
                        },
                        {
                            path: '/admin/report-templates',
                            name: 'ReportTemplateList',
                            component: () => import('@/views/pages/admin/ReportTemplateList.vue')
                        },
                        {
                            path: '/admins/project-types',
                            name: 'ProjectTypeList',
                            component: () => import('@/views/pages/admin/ProjectTypeList.vue')
                        }
                    ]
                },
                {
                    path: '/projects',
                    children: [
                        {
                            path: '/projects',
                            name: 'ProjectList',
                            component: () => import('@/views/pages/projects/ProjectList.vue'),
                        },
                        {
                            path: '/projects/:projectId',
                            children: [
                                {
                                    path: '/projects/:projectId',
                                    name: 'ProjectDetail',
                                    component: () => import('@/views/pages/projects/ProjectDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings',
                                    name: 'FindingList',
                                    component: () => import('@/views/pages/projects/findings/FindingList.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/create',
                                    name: 'FindingCreate',
                                    component: () => import('@/views/pages/projects/findings/FindingCreate.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/proofs/create',
                                    name: 'FindingProofCreate',
                                    component: () => import('@/views/pages/projects/findings/ProofCreate.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/proofs/:proofId/update',
                                    name: 'FindingProofUpdate',
                                    component: () => import('@/views/pages/projects/findings/ProofUpdate.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId',
                                    name: 'FindingDetail',
                                    component: () => import('@/views/pages/projects/findings/FindingDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/comments',
                                    name: 'FindingCommentList',
                                    component: () => import('@/views/pages/projects/findings/CommentList.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/scores',
                                    name: 'FindingScoreList',
                                    component: () => import('@/views/pages/projects/findings/ScoreList.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/timelines',
                                    name: 'FindingTimelineList',
                                    component: () => import('@/views/pages/projects/findings/TimelineList.vue')
                                },
                                {
                                    path: '/projects/:projectId/web-applications',
                                    name: 'WebApplicationList',
                                    component: () => import('@/views/pages/projects/assets/WebApplicationList.vue')
                                },
                                {
                                    path: '/projects/:projectId/web-applications/:assetId',
                                    name: 'WebApplicationDetail',
                                    component: () => import('@/views/pages/projects/assets/WebApplicationDetail.vue')

                                },
                                {
                                    path: '/projects/:projectId/hosts',
                                    name: 'HostList',
                                    component: () => import('@/views/pages/projects/assets/HostList.vue')
                                },
                                {
                                    path: '/projects/:projectId/hosts/:assetId',
                                    name: 'HostDetail',
                                    component: () => import('@/views/pages/projects/assets/HostDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/team',
                                    name: 'ContributorList',
                                    component: () => import('@/views/pages/projects/management/ContributorList.vue')
                                },
                                {
                                    path: '/projects/:projectId/contacts',
                                    name: 'ContactList',
                                    component: () => import('@/views/pages/projects/management/ContactList.vue')
                                },
                                {
                                    path: '/projects/:projectId/user-accounts',
                                    name: 'UserAccountList',
                                    component: () => import('@/views/pages/projects/management/UserAccountList.vue')
                                },
                                {
                                    path: '/projects/:projectId/api-tokens',
                                    name: 'APITokenList',
                                    component: () => import('@/views/pages/projects/management/APITokenList.vue')
                                },
                                {
                                    path: '/projects/:projectId/vulnerabilities',
                                    name: 'VulnerabilityList',
                                    component: () => import('@/views/pages/projects/vulnerabilities/VulnerabilityList.vue')
                                },
                                {
                                    path: '/projects/:projectId/vulnerabilities/create',
                                    name: 'VulnerabilityCreate',
                                    component: () => import('@/views/pages/projects/vulnerabilities/VulnerabilityCreate.vue')
                                },
                                {
                                    path: '/projects/:projectId/vulnerabilities/:vulnerabilityId/update',
                                    name: 'VulnerabilityUpdate',
                                    component: () => import('@/views/pages/projects/vulnerabilities/VulnerabilityUpdate.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports',
                                    name: 'ReportList',
                                    component: () => import('@/views/pages/projects/reports/ReportList.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports/:reportId',
                                    name: 'ReportDetail',
                                    component: () => import('@/views/pages/projects/reports/ReportDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports/:reportId/executive-summary',
                                    name: 'ReportExecutiveSummaryDetail',
                                    component: () => import('@/views/pages/projects/reports/ExecutiveSummary.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports/:reportId/version-history',
                                    name: 'ReportVersionHistoryList',
                                    component: () => import('@/views/pages/projects/reports/VersionHistoryList.vue')
                                },
                                {
                                    path: '/projects/:projectId/reports/:reportId/documents',
                                    name: 'ReportDocumentList',
                                    component: () => import('@/views/pages/projects/reports/ReportDocumentList.vue')
                                },
                                {
                                    path: '/projects/:projectId/services',
                                    name: 'ServiceList',
                                    component: () => import('@/views/pages/projects/assets/ServiceList.vue')
                                },
                                {
                                    path: '/projects/:projectId/services/:assetId',
                                    name: 'ServiceDetail',
                                    component: () => import('@/views/pages/projects/assets/ServiceDetail.vue')
                                },
                                {
                                    path: '/projects/:projectId/findings/:findingId/update',
                                    name: 'FindingUpdate',
                                    component: () => import('@/views/pages/projects/findings/FindingUpdate.vue')
                                },
                                {
                                    path: '/projects/:projectId/checklists',
                                    name: 'ProjectChecklistList',
                                    component: () => import('@/views/pages/projects/checklists/ChecklistList.vue')
                                },
                            ]
                        }
                    ]
                },
                {
                    path: '/advisory-management',
                    children: [
                        {
                            name: 'AdvisoryManagementLabelList',
                            path: '/advisory-management/labels',
                            component: () => import('@/views/pages/advisories/LabelList.vue')
                        }
                    ]
                },
                {
                    path: '/advisories',
                    children: [
                        {
                            name: 'AdvisoryList',
                            path: '/advisories',
                            component: () => import('@/views/pages/advisories/AdvisoryList.vue')
                        },
                        {
                            name: 'AdvisoryInbox',
                            path: '/advisories/inbox',
                            component: () => import('@/views/pages/advisories/AdvisoryInbox.vue')
                        },
                        {
                            name: 'AdvisoryCreate',
                            path: '/advisories/create',
                            component: () => import('@/views/pages/advisories/AdvisoryCreate.vue')
                        },
                        {
                            name: 'AdvisoryDetail',
                            path: '/advisories/:advisoryId',
                            component: () => import('@/views/pages/advisories/AdvisoryDetail.vue')
                        },
                        {
                            name: 'AdvisoryUpdate',
                            path: '/advisories/:advisoryId/update',
                            component: () => import('@/views/pages/advisories/AdvisoryUpdate.vue')
                        },
                        {
                            name: 'AdvisoryTimelineList',
                            path: '/advisories/:advisoryId/timeline',
                            component: () => import('@/views/pages/advisories/TimelineList.vue')
                        },
                        {
                            name: 'AdvisoryCommentList',
                            path: '/advisories/:advisoryId/comments',
                            component: () => import('@/views/pages/advisories/CommentList.vue')
                        },
                        {
                            name: 'AdvisoryMembershipList',
                            path: '/advisories/:advisoryId/memberships',
                            component: () => import('@/views/pages/advisories/MembershipList.vue')
                        },
                        {
                            name: 'AdvisoryProofList',
                            path: '/advisories/:advisoryId/proofs',
                            component: () => import('@/views/pages/advisories/ProofList.vue')
                        },
                        {
                            name: 'AdvisoryProofCreate',
                            path: '/advisories/:advisoryId/proofs/create',
                            component: () => import('@/views/pages/advisories/ProofCreate.vue')
                        },
                        {
                            name: 'AdvisoryProofUpdate',
                            path: '/advisories/:advisoryId/proofs/:proofId/update',
                            component: () => import('@/views/pages/advisories/ProofUpdate.vue')
                        }
                    ]
                },

                {
                    path: '/vulnerability-templates',
                    name: 'VulnerabilityTemplateList',
                    component: () => import('@/views/pages/vulnerability_templates/VulnerabilityTemplateList.vue')
                },


                {
                    path: '/companies',
                    children: [
                        {
                            path: '/companies',
                            name: 'CompanyList',
                            component: () => import('@/views/pages/companies/CompanyList.vue')
                        },
                        {
                            path: '/companies/:companyId',
                            name: 'CompanyDetail',
                            component: () => import('@/views/pages/companies/CompanyDetail.vue')
                        },
                        {
                            path: '/companies/:companyId/contacts',
                            name: 'CompanyContactList',
                            component: () => import('@/views/pages/companies/CompanyContactList.vue')
                        }
                    ]
                },
                {
                    path: '/user/settings',
                    name: 'UserSettingsDetail',
                    component: () => import('@/views/pages/settings/UserSettingsDetail.vue')
                }

            ]
        },

        {
            path: '/login',
            name: 'Login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/reset_password',
            name: 'ResetPassword',
            component: () => import('@/views/pages/auth/ResetPassword.vue')
        },
        {
            path: '/account-activation/:uid/:token',
            name: 'AccountActivation',
            component: () => import('@/views/pages/auth/AccountActivation.vue')
        }
    ]
});

export default router;
