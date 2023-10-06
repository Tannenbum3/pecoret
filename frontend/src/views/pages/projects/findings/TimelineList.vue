<script>
import FindingService from '@/service/FindingService'
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue'
import CustomBreadcrumb from "@/components/CustomBreadcrumb.vue";


export default {
    name: 'TimelineList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            findingService: new FindingService(),
            items: [],
            breadcrumbs: [
                {
                    label: 'Findings',
                    route: this.$router.resolve({
                        name: "FindingList",
                        params: { projectId: this.$route.params.projectId }
                    })
                },
                {
                    label: 'Finding Detail',
                    route: this.$router.resolve({
                        name: "FindingDetail",
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: 'Timeline',
                    disabled: true
                }
            ]
        }
    },
    methods: {
        getTimeline() {
            this.findingService.getTimeline(this.projectId, this.findingId).then((response) => {
                this.items = response.data.results
            })
        }
    },
    mounted() {
        this.getTimeline()
    },
    components: { FindingTabMenu, CustomBreadcrumb }
}
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <CustomBreadcrumb v-model="breadcrumbs"></CustomBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <Card class="border-noround-top">
                <template #content>

                    <Timeline :value="items" class="mt-3">
                        <template #opposite="slotProps">
                            <small class="p-text-secondary">{{ slotProps.item.date_created }}</small>
                        </template>
                        <template #content="slotProps">
                            {{ slotProps.item.title }}
                        </template>
                    </Timeline>
                </template>
            </Card>
        </div>
    </div>
</template>