<script>
export default {
    name: 'ReportTabMenu',
    data(){
        return {
            items: [
                {
                    label: 'Configuration',
                    to: this.$router.resolve({
                        name: 'ReportDetail',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Executive Summary',
                    to: this.$router.resolve({
                        name: 'ReportExecutiveSummaryDetail',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Version History',
                    to: this.$router.resolve({
                        name: 'ReportVersionHistoryList',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Documents',
                    to: this.$router.resolve({
                        name: 'ReportDocumentList',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                }
            ]
        }
    }
}
</script>

<template>
    <TabMenu :model="items"></TabMenu>
</template>