<script>
import AdminService from '@/service/AdminService'
import UserCreateDialog from '../../../components/dialogs/UserCreateDialog.vue'
import UserUpdateDialog from '../../../components/dialogs/UserUpdateDialog.vue';


export default {
    name: "UserList",
    data() {
        return {
            breadcrumbs: [
                {
                    label: "Users",
                    disabled: true
                }
            ],
            service: new AdminService(),
            loading: false,
            pagination: { page: 1, limit: 20 },
            totalRecords: 0,
            items: []
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onSort(event) { },
        onFilter(event) { },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems() {
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.service.getUsers(this.$api, params).then((response) => {
                this.totalRecords = response.data.count;
                this.items = response.data.results;
            }).finally(() => { this.loading = false; });
        },
        confirmDialogDelete(userId) {
            this.$confirm.require({
                message: "Do you want to delete this user?",
                header: "Delete Confirmation",
                icon: "fa fa-trash",
                acceptClass: "p-button-danger",
                accept: () => {
                    this.service.deleteUser(this.$api, userId).then(() => {
                        this.$toast.add({
                            severity: "success",
                            summary: "Deleted",
                            detail: "User was deleted successfully!",
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        },
    },
    components: { UserCreateDialog, UserUpdateDialog }
}
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-6">
            <div class="justify-content-start flex"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <UserCreateDialog @object-created="getItems"></UserCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <Card>
                <template #content>
                    <DataTable paginator dataKey rowHover :rows="pagination.limit" :value="items" filterDisplay="menu" lazy
                        responsiveLayout="scroll" :totalRecords="totalRecords" :loading="loading" @page="onPage"
                        @sort="onSort" @filter="onFilter">

                        <Column field="username" header="Username"></Column>
                        <Column field="first_name" header="First Name"></Column>
                        <Column field="last_name" header="Last Name"></Column>
                        <Column field="email" header="E-Mail"></Column>
                        <Column field="is_active" header="Is Active?"></Column>
                        <Column header="Actions">
                            <template #body="slotProps">
                                <UserUpdateDialog :user="slotProps.data"></UserUpdateDialog>
                                <Button size="small" outlined icon="fa fa-trash" severity="danger"
                                    @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                            </template>
                        </Column>
                    </DataTable>
                </template>
            </Card>
        </div>
    </div>
</template>