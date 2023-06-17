<script>
import AdvisoryService from '@/service/AdvisoryService'
import AdvisoryTabMenu from '../../../components/pages/AdvisoryTabMenu.vue';
import AdvisoryMembershipCreateDialog from '@/components/dialogs/AdvisoryMembershipCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue'


export default {
    name: "MembershipList",
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            totalRecords: 0,
            pagination: { limit: 20, page: 1 },
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
                    label: "Memberships",
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
        onPage(event) {
            this.pagination.page = event.page + 1
            this.getItems()
        },
        onFilter(event) { },
        onSort(event) { },
        getItems() {
            this.loading = true
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page
            }
            this.service.getMemberships(this.$api, this.advisoryId, data).then((response) => {
                this.items = response.data.results
            }).finally(() => { this.loading = false })
        },
        confirmDialogDelete(id){
            this.$confirm.require({
                message: 'Do you want to remove this user from accessing advisory?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteMembership(this.$api, this.advisoryId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'User was removed from advisory',
                            life: 3000
                        })
                        this.getItems()
                    })
                }
            })
        }
    },
    components: { AdvisoryTabMenu, AdvisoryMembershipCreateDialog, BlankSlate }
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
            <div class="flex justify-content-start">
            </div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <AdvisoryMembershipCreateDialog @object-created="getItems"></AdvisoryMembershipCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card">
                <DataTable paginator lazy rowHover dataKey="pk" :totalRecords="totalRecords" :value="items"
                    v-if="items.length > 0"
                    :rows="pagination.limit" filterDisplay="menu" :loading="loading" @sort="onSort" @filter="onFilter"
                    @page="onPage">
                    <Column field="user.username" header="User"></Column>
                    <Column field="role" header="Role"></Column>
                    <Column field="active_until" header="Active Until">
                        <template #body="slotProps">
                            {{ slotProps.data.active_until || '-' }}
                        </template>
                    </Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger"
                                @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
                <BlankSlate icon="fa fa-users" title="No members!"
                    v-else
                    text="No members found! You may want to share the advisory with other users using the buttons above!"></BlankSlate>
            </div>
        </div>
    </div>
</template>