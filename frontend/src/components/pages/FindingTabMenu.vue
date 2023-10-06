<script>
export default {
    name: "FindingTabMenu",
    mounted() {
        this.activeItem = this.items.findIndex((item) => this.$route.path === this.$router.resolve(item.route).path);
    },
    data() {
        return {
            activeItem: null,
            items: [
                {
                    label: "Details",
                    route: this.$router.resolve({
                        name: "FindingDetail",
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: "Comments",
                    route: this.$router.resolve({
                        name: "FindingCommentList",
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })
                },
                {
                    label: "Timeline",
                    route: this.$router.resolve({
                        name: "FindingTimelineList",
                        params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId }
                    })

                },
                {
                    label: "Scores",
                    route: this.$router.resolve({
                        name: "FindingScoreList",
                        params: {
                            projectId: this.$route.params.projectId, findingId: this.$route.params.findingId
                        }
                    })

                }
            ]
        };
    }
};
</script>

<template>
    <TabMenu :model="items" v-model:activeIndex="activeItem">
        <template #item="{ label, item, props}">
            <router-link v-if="item.route" v-slot="routerProps" :to="item.route" custom>
                <a :href="routerProps.href" v-bind="props.action" @click="($event) => routerProps.navigate($event)"
                   @keydown.enter.space="($event) => routerProps.navigate($event)">
                    <span v-bind="props.icon" />
                    <span v-bind="props.label">{{ label }}</span>
                </a>
            </router-link>
        </template>
    </TabMenu>
</template>
