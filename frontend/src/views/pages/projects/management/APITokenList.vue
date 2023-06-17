<script>
import APITokenService from '@/service/APITokenService'
import APITokenCreateDialog from '@/components/dialogs/APITokenCreateDialog.vue'
import BlankSlate from '@/components/BlankSlate.vue'


export default {
    name: "APITokenList",
    data() {
        return {
            breadcrumbs: [
                {
                    label: "API-Tokens",
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            apiTokenService: new APITokenService()
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
            this.apiTokenService.getTokens(this.$api, this.projectId, params).then((response) => {
                this.totalRecords = response.data.count;
                this.items = response.data.results;
            }).finally(() => { this.loading = false; });
        },
        confirmDialogDelete(tokenId){
            this.$confirm.require({
                message: 'Do you want to delete this member?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteToken(tokenId)
                }
            })
        },
        deleteToken(tokenId){
            this.apiTokenService.deleteToken(this.$api, this.projectId, tokenId).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Deleted',
                    detail: 'API-Token removed from project!',
                    life: 3000
                })
                this.getItems()
            })
        },
        copyToClipboard(token){
            navigator.clipboard.writeText(token)
            this.$toast.add({
                severity: 'info',
                summary: 'Copied',
                detail: 'Token copied to clipboard',
                life: 3000
            })
        }
    },
    components: { APITokenCreateDialog, BlankSlate }
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
                <APITokenCreateDialog @object-created="getItems"></APITokenCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginatior lazy dataKey="pk" rowHover
                    v-if="this.items.length > 0"
                    :value="items" :rows="pagination.limit" :totalRecords="totalRecords"
                    filterDisplay="menu" :loading="loading" @page="onPage" @sort="onSort"
                    @filter="onFilter">
                    <Column field="name" header="Name"></Column>
                    <Column field="date_expire" header="Date Expire"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-copy"
                                @click="copyToClipboard(slotProps.data.pk)"
                            ></Button>

                            <Button size="small" outlined severity="danger"
                                icon="fa fa-trash"
                                @click="confirmDialogDelete(slotProps.data.pk)"
                                ></Button>
                        </template>
                    </Column>
                </DataTable>
                <BlankSlate v-else icon="fa fa-key" title="No API-Tokens!" text="No API-Tokens found!"></BlankSlate>
            </div>
        </div>
    </div>



</template>