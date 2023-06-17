<script>
export default {
    name: 'FindingTabMenu',
    data(){
        return {
            items: [
                {
                    label: 'Details',
                    to: this.$router.resolve({name: 'FindingDetail', params: {projectId: this.$route.params.projectId, findingId: this.$route.params.findingId}})
                },
                {
                    label: 'Comments',
                    to: this.$router.resolve({name: 'FindingCommentList',  params: {projectId: this.$route.params.projectId, findingId: this.$route.params.findingId}})
                },
                {
                    label: 'Timeline',
                    to: this.$router.resolve({name: 'FindingTimelineList',  params: {projectId: this.$route.params.projectId, findingId: this.$route.params.findingId}})

                },
                {
                    label: 'Scores',
                    to: this.$router.resolve({
                        name: 'FindingScoreList', 
                        params: {projectId: this.$route.params.projectId, findingId: this.$route.params.findingId
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