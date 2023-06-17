<script>
import ContributorService from '@/service/ContributorService'
import ContributorCreateDialog from '../../../../components/dialogs/ContributorCreateDialog.vue'


export default {
    name: "ContributorList",
    data() {
        return {
            breadcrumbs: [
                {
                    label: "Team",
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            contributorService: new ContributorService()
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
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.contributorService.getContributors(this.$api, this.projectId, params).then((response) => {
                this.totalRecords = response.data.count;
                this.items = response.data.results;
            }).finally(() => { this.loading = false; });
        },
        confirmDialogDelete(contribId){
            this.$confirm.require({
                message: 'Do you want to delete this member?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteContributor(contribId)
                }
            })
        },
        deleteContributor(contribId){
            this.contributorService.deleteContributor(this.$api, this.projectId, contribId).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Deleted',
                    detail: 'Member removed from project!',
                    life: 3000
                })
                this.getItems()
            })
        },
    },
    components: { ContributorCreateDialog }
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
                <ContributorCreateDialog @object-created="getItems"></ContributorCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginatior lazy dataKey="pk" rowHover
                    :value="items" :rows="pagination.limit" :totalRecords="totalRecords"
                    filterDisplay="menu" :loading="loading" @page="onPage" @sort="onSort"
                    @filter="onFilter">
                    <Column field="user.username" header="User"></Column>
                    <Column field="role" header="Role"></Column>
                    <Column field="active_until" header="Membership Expiry">
                        <template #body="slotProps">
                            {{ slotProps.data.active_until || "Never" }}
                        </template>
                    </Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined severity="danger"
                                icon="fa fa-trash"
                                @click="confirmDialogDelete(slotProps.data.pk)"
                                ></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>



</template>