<script>
import AssetService from '@/service/AssetService'
import BlankSlate from '@/components/BlankSlate.vue'


export default {
    name: "ServiceList",
    components: {BlankSlate},
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
                    label: "Services",
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
            this.assetService.getServices(this.$api, this.projectId, params).then((response) => {
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
            this.assetService.getServices(this.$api, this.projectId, params).then((response) => {
                this.totalRecords = response.data.count;
                this.items = response.data.results;
            }).finally(() => { this.loading = false; });
        },
        onSort(event) { },
        onFilter(event) { },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        }
    },
    mounted() {
        this.getItems();
    },
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

                    <Column field="name" header="Name"></Column>
                    <Column field="port" header="Port"></Column>
                    <Column field="protocol" header="Protocol"></Column>
                    <Column field="state" header="State"></Column>
                    <Column field="host.name" header="Host"></Column>
                    <Column header="Actions"></Column>
                </DataTable>
                <BlankSlate icon="fa fa-network-wired" v-else text="No services found!" title="No services!"></BlankSlate>
            </div>
        </div>
    </div>
</template>