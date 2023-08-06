<script>
import ProjectService from "@/service/ProjectService";


export default {
    name: "ProjectFileCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                file: null,
                name: null
            },
            service: new ProjectService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        getFileObject(event) {
            this.model.file = event.files[0];
        },
        create() {
            let data = {
                name: this.model.name,
                file: this.model.file
            };
            this.service.createProjectFile(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "File added!",
                    life: 3000,
                    detail: "New file was added!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="File" outlined @click="open"></Button>

    <Dialog header="Create File" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="col-12 field">
                <label for="name">Name</label>
                <InputText id="name" v-model="model.name"></InputText>
            </div>
            <div class="col-12 field">
                <label for="file">File</label>
                <FileUpload mode="basic" id="file" @select="this.getFileObject"></FileUpload>
            </div>
        </div>


        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>