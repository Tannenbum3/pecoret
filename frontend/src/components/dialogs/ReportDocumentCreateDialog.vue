<script>
import ReportService from '@/service/ReportService'


export default {
    name: "ReportDocumentCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            model: {
                name: null,
                release_type: null
            },
            releaseTypeChoices: [
                { title: 'Draft', value: 'Draft' },
                { title: 'Final', value: 'Final' }
            ],
            reportService: new ReportService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        create() {
            let data = {
                name: this.model.name,
                release_type: this.model.release_type
            }
            this.reportService.createReportDocument(this.$api, this.projectId, this.reportId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "Document created!",
                    life: 3000,
                    detail: "New document created!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    },
}
</script>

<template>
    <Button icon="fa fa-plus" label="Document" outlined @click="open"></Button>

    <Dialog header="Create Document" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="name">Name</label>
            <InputText id="name" v-model="model.name"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="release_type">Release Type</label>
            <Dropdown v-model="model.release_type" id="release_type"
                :options="releaseTypeChoices" optionLabel="title"
                optionValue="value"
            ></Dropdown>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>