<script>
import markdown from '@/utils/markdown';
import FindingService from '@/service/FindingService';
import FindingTabMenu from '@/components/pages/FindingTabMenu.vue';
import MarkdownEditor from '@/components/elements/forms/MarkdownEditor.vue';

export default {
    name: 'FindingCommentList',
    data() {
        return {
            findingId: this.$route.params.findingId,
            projectId: this.$route.params.projectId,
            findingService: new FindingService(),
            loading: false,
            model: {
                comment: ''
            },
            items: [],
            breadcrumbs: [
                {
                    label: 'Findings',
                    to: this.$router.resolve({ name: 'FindingList', params: { projectId: this.$route.params.projectId } })
                },
                {
                    label: 'Finding Detail',
                    to: this.$router.resolve({ name: 'FindingDetail', params: { projectId: this.$route.params.projectId, findingId: this.$route.params.findingId } })
                },
                {
                    label: 'Comments',
                    disabled: true
                }
            ]
        };
    },
    methods: {
        renderMarkdown(text) {
            return markdown.renderMarkdown(text);
        },
        getComments() {
            this.loading = true;
            this.findingService
                .getComments(this.projectId, this.findingId)
                .then((response) => {
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        saveNewComment() {
            let data = {
                comment: this.model.comment
            };
            this.findingService.createComment(this.$api, this.projectId, this.findingId, data).then((response) => {
                this.model.comment = '';
                this.getComments();
            });
        }
    },
    mounted() {
        this.getComments();
    },
    components: { MarkdownEditor, FindingTabMenu }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <FindingTabMenu class="surface-card"></FindingTabMenu>
            <div class="card" v-if="items.length > 1">
                <div class="card" v-for="comment in items" :key="comment.pk">
                    {{ comment.comment }}
                </div>
            </div>
            <div class="card mt-3">
                <MarkdownEditor v-model="model.comment"></MarkdownEditor>
                <div class="flex justify-content-end">
                    <Button @click="saveNewComment" label="Save"></Button>
                </div>
            </div>
        </div>
    </div>
</template>