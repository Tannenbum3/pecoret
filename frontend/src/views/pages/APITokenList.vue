<script>
import UserService from "@/service/UserService";
import BlankSlate from "@/components/BlankSlate.vue";
import APITokenCreate from "@/components/dialogs/APITokenCreate.vue";

export default {
    name: "APITokenList",
    components: { APITokenCreate, BlankSlate },
    data() {
        return {
            breadcrumbs: [],
            tokenKey: null,
            service: new UserService(),
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 }
        };
    },
    methods: {
        onSort() {
        },
        onFilter() {
        },
        onPage(event) {
            this.pagination.page = event.page + 1;
            this.getItems();
        },
        getItems() {
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service.getAPITokens(this.$api, params).then((response) => {
                this.items = response.data.results;
                this.totalRecords = response.data.count;
            });
        },
        showTokenKey(data) {
            this.tokenKey = data.token;
            this.getItems();
        },
        onDeleteConfirmDialog(id) {
            this.$confirm.require({
                message: "Do you want to delete this api token?",
                header: "Delete confirmation",
                icon: "fa fa-trash",
                acceptClass: "p-button-danger",
                accept: () => {
                    this.service.deleteAPIToken(this.$api, id).then(() => {
                        this.$toast.add({
                            severity: "info",
                            summary: "Deleted",
                            detail: "API Token was deleted!",
                            life: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    mounted() {
        this.getItems();
    }
};
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
                <APITokenCreate @object-created="showTokenKey"></APITokenCreate>
            </div>
        </div>
    </div>

    <div class="grid" v-if="tokenKey">
        <div class="col-12">
            <Message @close="() => {this.tokenKey = null}">{{ tokenKey }}</Message>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable :paginator="true" dataKey="pk"
                           :rowHover="items.length > 0"
                           :rows="pagination.limit"
                           :value="items" filterDisplay="menu"
                           :lazy="true" :loading="loading"
                           @sort="onSort" @filter="onFilter" @page="onPage"
                           :totalRecords="totalRecords">

                    <Column field="name" header="Name"></Column>
                    <Column field="prefix" header="Prefix"></Column>
                    <Column field="date_last_used" header="Last used"></Column>
                    <Column field="date_created" header="Date created"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-trash" severity="danger"
                                    @click="onDeleteConfirmDialog(slotProps.data.pk)">
                            </Button>
                        </template>
                    </Column>
                    <template #empty>
                        <BlankSlate icon="fa fa-fingerprint" title="No API-Tokens!"
                                    text="No API-Tokens found!"></BlankSlate>
                    </template>
                </DataTable>
            </div>
        </div>
    </div>
</template>