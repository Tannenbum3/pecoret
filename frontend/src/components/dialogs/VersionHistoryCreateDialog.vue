<script>
import ReportService from '@/service/ReportService'
import ProjectService from '@/service/ProjectService'


export default {
    name: "VersionHistoryCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            model: {
                version: null,
                change: null,
                user: null,
                date: null
            },
            userChoices: [],
            reportService: new ReportService(),
            projectService: new ProjectService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        onFilterUser(event) {
            let params = {
                search: event.value
            }
            this.projectService.getProjectMemberships(this.$api, this.projectId, params).then((response) => {
                this.userChoices = response.data.results
            })
        },
        onFocusUser(){
            this.projectService.getProjectMemberships(this.$api, this.projectId).then((response) => {
                this.userChoices = response.data.results
            })
        },
        create() {
            let data = {
                user: this.model.user.user.pk,
                change: this.model.change,
                date: this.model.date.toISOString().split("T")[0],
                version: this.model.version
            }
            this.reportService.createVersionHistory(this.$api, this.projectId, this.reportId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "Version added!",
                    life: 3000,
                    detail: "Version added to report!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    },
}
</script>

<template>
    <Button icon="fa fa-plus" label="Change History" outlined @click="open"></Button>

    <Dialog header="Add Change" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="version">Version</label>
            <InputText id="version" v-model="model.version"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="change">Change</label>
            <InputText id="change" v-model="model.change"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="user">User</label>
            <Dropdown id="user" filter optionLabel="user.username"
                :options="userChoices" v-model="model.user"
                @filter="onFilterUser" @focus="onFocusUser"></Dropdown>
        </div>
        <div class="flex flex-column gap-2">
            <label for="date">Date</label>
            <Calendar id="date" v-model="model.date" showIcon></Calendar>
        </div>
        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>