<script>
import UserAccountService from '@/service/UserAccountService';

export default {
    name: 'UserAccountUpdateDialog',
    props: {
        account: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            loading: false,
            model: this.account,
            service: new UserAccountService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            this.loading = true;
            let data = {
                username: this.model.username,
                password: this.model.password,
                role: this.model.role,
                compromised: this.model.compromised,
                description: this.model.description
            };
            this.service
                .patchAccount(this.$api, this.$route.params.projectId, this.account.pk, data)
                .then(() => {
                    this.$emit('object-updated', this.model);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    watch: {
        account: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <Dialog header="Update User Account" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="field col-12">
                <label for="username">Username</label>
                <InputText id="username" v-model="model.username"></InputText>
            </div>
            <div class="field col-12">
                <label for="password">Password</label>
                <Password id="password" v-model="model.password" :feedback="false" toggleMask></Password>
            </div>
            <div class="field col-12">
                <label for="rolel">Role</label>
                <InputText id="role" v-model="model.role"></InputText>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <InputText v-model="model.description"></InputText>
            </div>
            <div class="field col-12">
                <div class="flex align-items-center">
                    <Checkbox v-model="model.compromised" inputId="compromised" :binary="true" />
                    <label for="compromised" class="ml-2"> Compromised?</label>
                </div>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" :loading="loading" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>