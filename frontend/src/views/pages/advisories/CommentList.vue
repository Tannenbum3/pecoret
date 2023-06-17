<script>
import AdvisoryService from '@/service/AdvisoryService'
import AdvisoryTabMenu from '../../../components/pages/AdvisoryTabMenu.vue';
import ToastUIEditor from '../../../components/elements/forms/ToastUIEditor.vue';


export default {
    name: "CommentList",
    data() {
        return {
            service: new AdvisoryService(),
            comment: "",
            breadcrumbs: [
                {
                    label: "Advisories",
                    to: this.$router.resolve({
                        name: "AdvisoryList"
                    })
                },
                {
                    label: "Advisory Detail",
                    to: this.$router.resolve({
                        name: "AdvisoryDetail",
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: "Comments",
                    disabled: true
                }
            ],
            advisoryId: this.$route.params.advisoryId,
            items: []
        };
    },
    mounted() {
        this.getItems()
    },
    methods: {
        getItems() {
            this.service.getComments(this.$api, this.advisoryId).then((response) => {
                this.items = response.data.results
            })
        },
        saveNewComment() {
            let data = {
                comment: this.comment
            }
            this.service.createComment(this.$api, this.advisoryId, data).then(() => {
                this.getItems()
                this.comment = ""
            })
        },
    },
    components: { AdvisoryTabMenu, ToastUIEditor }
}
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card">
                <Card v-for="comment in items" :key="comment.pk" class="surface-ground border-200 border-1 border-round">
                    <template #header>
                        <div class="col-12 surface-card border-200 border-1 border-round">
                            <div class="grid">
                                <div class="col-10">
                                    <div class="flex justify-content-start">
                                        {{ comment.user.username }} commented on {{ comment.date_created }}

                                    </div>
                                </div>
                                <div class="col-2">
                                    <div class="flex justify-content-end">

                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template #content>
                        <div class="grid">
                            <div class="col-12">
                                {{ comment.comment }}

                            </div>
                        </div>

                    </template>
                </Card>
            </div>
            <div class="card mt-3">
                <ToastUIEditor v-model="comment"></ToastUIEditor>
                <div class="flex justify-content-end">
                    <Button @click="saveNewComment" label="Save"></Button>
                </div>
            </div>
        </div>
    </div>
</template>