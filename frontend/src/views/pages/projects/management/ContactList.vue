<script>
import ProjectService from '@/service/ProjectService';
import ProjectContactCreateDialog from '../../../../components/dialogs/ProjectContactCreateDialog.vue';
import BlankSlate from '@/components/BlankSlate.vue';

export default {
    name: 'ContactList',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Contacts',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            projectService: new ProjectService()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onSort(event) {},
        onFilter(event) {},
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
            this.projectService
                .getContacts(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        confirmDialogDelete(contactId) {
            this.$confirm.require({
                message: 'Do you want to delete this contact?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.deleteContact(contactId);
                }
            });
        },
        deleteContact(contactId) {
            this.projectService.deleteContact(this.$api, this.projectId, contactId).then(() => {
                this.$toast.add({
                    severity: 'info',
                    summary: 'Contact Removed!',
                    detail: 'Removed contact from project!',
                    life: 3000
                });
                this.getItems();
            });
        }
    },
    components: { ProjectContactCreateDialog, BlankSlate }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ProjectContactCreateDialog @object-created="getItems"></ProjectContactCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginator lazy dataKey="pk" :rowHover="this.items.length > 0" :value="items" :rows="pagination.limit" :totalRecords="totalRecords" filterDisplay="menu" :loading="loading" @page="onPage" @sort="onSort" @filter="onFilter">
                    <template #empty>
                        <BlankSlate icon="fa fa-id-card" title="No contacts!" text="No contacts found!"></BlankSlate>
                    </template>
                    <Column field="name" header="Name">
                        <template #body="slotProps"> {{ slotProps.data.contact.first_name }} {{ slotProps.data.contact.last_name }} </template>
                    </Column>
                    <Column field="contact.email" header="E-Mail"></Column>
                    <Column field="contact.phone" header="Phone"></Column>
                    <Column field="contact.role" header="Role"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined severity="danger" icon="fa fa-trash" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>