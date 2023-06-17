<script>
import ContributorService from '@/service/ContributorService';

export default {
    name: 'ContributorCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                user: null,
                role: null,
                active_until: null
            },
            userChoices: [],
            roleChoices: [{ label: 'Project Leader' }, { label: 'Owner' }, { label: 'Read Only' }, { label: 'Contributor' }],
            contributorService: new ContributorService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        onFocusUser(event){
            let url = "/users/"
            this.$api.get(url).then((response) => {
                this.userChoices = response.data.results
            })
        },
        onFilterUser(event){
            let url = "/users/"
            let config = {
                search: event.value
            }
            this.$api.get(url).then((response) => {
                this.userChoices = response.data.results
            })
        },
        create() {
            let data = {
                role: this.model.role,
                active_until: this.model.active_until,
                user: this.model.user
            };
            this.contributorService.createContributor(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'User added!',
                    life: 3000,
                    detail: 'User added to project!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Member" outlined @click="open"></Button>

    <Dialog header="Add Member to Project" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="user">User</label>
                <Dropdown v-model="model.user" optionLabel="username" id="user" :options="userChoices" optionValue="pk"
                    @focus="onFocusUser" filter
                    @filter="onFilterUser"
                ></Dropdown>
            </div>
            <div class="field col-12">
                <label for="role">Role</label>
                <Dropdown v-model="model.role" :options="roleChoices" optionValue="label" optionLabel="label"
                ></Dropdown>
            </div>
            <div class="field col-12">
                <label for="active_until">Membership Expiry?</label>
                <Calendar v-model="model.active_until"></Calendar>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>
