<script>
import AssetService from '@/service/AssetService'
import HostCreateDialog from '../../../../components/dialogs/HostCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue'


export default {
    name: "HostList",
    data() {
        return {
            assetService: new AssetService(),
            projectId: this.$route.params.projectId,
            breadcrumbs: [
                {
                    label: "Projects",
                    to: this.$router.resolve({
                        name: "ProjectList"
                    })
                },
                {
                    label: "Project Detail",
                    to: this.$router.resolve({
                        name: "ProjectDetail",
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: "Hosts",
                    disabled: true
                }
            ],
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
    },
    methods: {
        onGlobalSearch(query) {
            this.loading = true
            let params = {
                search: query
            }
            this.assetService.getHosts(this.$api, this.projectId, params).then((response) => {
                this.totalRecords = response.data.count
                this.items = response.data.results
            }).finally(() => { this.loading = false })
        },
        getItems() {
            this.loading = true;
            let params = {
                page: this.pagination.page,
                limit: this.pagination.limit
            };
            this.assetService.getHosts(this.$api, this.projectId, params).then((response) => {
                this.totalRecords = response.data.count;
                this.items = response.data.results;
            }).finally(() => { this.loading = false; });
        },
        onSort(event) { },
        onFilter(event) { },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: 'Do you want to delete this host?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.assetService.deleteHost(this.$api, this.projectId, id).then(() => {
                        this.$toast.add({
                            severity: 'info',
                            summary: 'Deleted',
                            detail: 'Host was deleted!',
                            life: 3000
                        })
                        this.getItems()
                    })
                }
            })
        }
    },
    mounted() {
        this.getItems();
    },
    components: { HostCreateDialog, BlankSlate }
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
                <HostCreateDialog @object-created="getItems"></HostCreateDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginator rowHover dataKey="pk" lazy :rows="pagination.limit" :value="items" filterDisplay="menu"
                    responsiveLayout="scroll" @sort="onSort" @filter="onFilter" @page="onPage" :totalRecords="totalRecords"
                    :loading="loading" v-if="items.length > 0">
                    <template #header>
                        <div class="flex justify-content-between flex-column sm:flex-row">
                            <span class="p-input-icon-left mb-2">
                                <i class="pi pi-search" />
                                <InputText @update:modelValue="onGlobalSearch" placeholder="Keyword Search"
                                    style="width: 100%" />
                            </span>
                        </div>
                    </template>

                    <Column field="ip" header="IP"></Column>
                    <Column field="dns" header="DNS"></Column>
                    <Column field="operating_system" header="Operating System"></Column>
                    <Column field="environment" header="Environment"></Column>
                    <Column field="accessible" header="Accessible"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger"
                                @click="onDeleteConfirmDialog(slotProps.data.pk)">
                            </Button>
                        </template>
                    </Column>
                </DataTable>
                <BlankSlate v-else icon="fa fa-server" title="No hosts!" text="No hosts found!"></BlankSlate>
            </div>
        </div>
    </div>
</template>