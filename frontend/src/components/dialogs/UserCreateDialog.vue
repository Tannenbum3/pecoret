<script>
import AdminService from '@/service/AdminService'


export default {
    name: "UserCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            model: {
                username: null,
                first_name: null,
                last_name: null,
                email: null,
                groups: []
            },
            service: new AdminService(),
            groupChoices: []
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
                username: this.model.username,
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                email: this.model.email,
                groups: this.model.groups
            }
            this.service.createUser(this.$api, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "User Created!",
                    life: 3000,
                    detail: "User created successfully!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        },
        getGroups(){
            this.service.getGroups(this.$api).then((response) => {
                this.groupChoices = response.data.results
            })
        }
    },
}
</script>

<template>
    <Button icon="fa fa-plus" label="User" outlined @click="open"></Button>

    <Dialog header="Create User" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="username">Username</label>
            <InputText id="username" v-model="model.username"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="first_name">First Name</label>
            <InputText id="first_name" v-model="model.first_name"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="last_name">Last Name</label>
            <InputText id="last_name" v-model="model.last_name"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="email">E-Mail</label>
            <InputText id="email" v-model="model.email"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="groups">Groups</label>
            <MultiSelect id="groups" v-model="model.groups" :options="groupChoices"
                @focus="getGroups" optionValue="pk"
                optionLabel="name"></MultiSelect>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>