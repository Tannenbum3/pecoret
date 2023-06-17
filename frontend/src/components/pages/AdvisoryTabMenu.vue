<script>
export default {
    name: 'AdvisoryTabMenu',
    data(){
        return {
            items: [
                {
                    label: 'Details',
                    to: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId,
                        }
                    })
                },
                {
                    label: 'Proofs',
                    to: this.$router.resolve({
                        name: 'AdvisoryProofList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Timeline',
                    to: this.$router.resolve({
                        name: 'AdvisoryTimelineList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Comments',
                    to: this.$router.resolve({
                        name: 'AdvisoryCommentList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Memberships',
                    to: this.$router.resolve({
                        name: 'AdvisoryMembershipList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
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