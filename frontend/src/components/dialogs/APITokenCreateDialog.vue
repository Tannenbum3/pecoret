<script>
import APITokenService from '@/service/APITokenService'


export default {
    name: "APITokenCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                date_expire: null,
            },
            tokenService: new APITokenService()
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
                date_expire: this.model.date_expire
            }
            this.tokenService.createToken(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "Token added!",
                    life: 3000,
                    detail: "API-Token added to project!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    },
}
</script>

<template>
    <Button icon="fa fa-plus" label="API-Token" outlined @click="open"></Button>

    <Dialog header="Create API-Token" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="name">Name</label>
            <InputText id="name" v-model="model.name"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="date_expire">Date Expire</label>
            <Calendar v-model="model.date_expire" showTime hourFormat="24" id="date_expire"></Calendar>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>