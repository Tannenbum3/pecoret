<script>
import BlankSlate from '@/components/BlankSlate.vue';
import ProjectService from '@/service/ProjectService';
import ProjectFileCreateDialog from '@/components/dialogs/ProjectFileCreateDialog.vue';
import forceFileDownload from '@/utils/file';

export default {
    name: 'ProjectFileList',
    components: { BlankSlate, ProjectFileCreateDialog },
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Project Files',
                    disabled: true
                }
            ],
            projectId: this.$route.params.projectId,
            items: [],
            loading: false,
            totalRecords: 0,
            pagination: { page: 1, limit: 20 },
            service: new ProjectService()
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        onSort() {},
        onFilter() {},
        onPage(event) {},
        getItems() {
            this.loading = true;
            let params = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service
                .getProjectFiles(this.$api, this.projectId, params)
                .then((response) => {
                    this.totalRecords = response.data.count;
                    this.items = response.data.results;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        downloadFile(file_id) {
            this.service.downloadProjectFile(this.$api, this.projectId, file_id).then((response) => {
                forceFileDownload(response);
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Dou you want to delete this file?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteProjectFile(this.$api, this.projectId, id).then(() => {
                        this.getItems();
                    });
                }
            });
        }
    }
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
                <ProjectFileCreateDialog @object-created="this.getItems"></ProjectFileCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <DataTable paginator lazy dataKey="pk" :value="items" :rows="pagination.limit" :rowHover="this.items.length > 0" :totalRecords="totalRecords" filterDisplay="menu" :loading="loading" @page="onPage" @sort="onSort" @filter="onFilter">
                    <template #empty>
                        <BlankSlate icon="fa fa-file" title="No files!" text="No project files found!"></BlankSlate>
                    </template>
                    <Column field="name" header="Name"></Column>

                    <Column field="date_created" header="Date created"></Column>
                    <Column header="Actions">
                        <template #body="slotProps">
                            <Button size="small" outlined icon="fa fa-download" @click="downloadFile(slotProps.data.pk)"></Button>
                            <Button size="small" outlined severity="danger" icon="fa fa-trash" @click="confirmDialogDelete(slotProps.data.pk)"></Button>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>