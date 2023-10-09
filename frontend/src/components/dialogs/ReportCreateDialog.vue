<script>
import ReportService from '@/service/ReportService';

export default {
    name: 'ReportCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                template: null,
                variant: null,
                author: null
            },
            templateChoices: null,
            variantChoices: [
                { label: 'Vulnerability CSV', value: 'Vulnerability CSV' },
                { label: 'Pentest PDF Report', value: 'Pentest PDF' },
                { label: 'Pentest Excel', value: 'Pentest Excel' }
            ],
            authorChoices: null,
            loading: false,
            service: new ReportService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        getTemplates() {
            if (this.templateChoices) {
                return;
            }
            let url = '/report-templates/';
            this.$api.get(url).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        create() {
            this.loading = true;
            let data = {
                name: this.model.name,
                template: this.model.template.pk,
                variant: this.model.variant.value,
                author: this.model.author.pk
            };
            this.service
                .createReport(this.$api, this.projectId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Report created!',
                        life: 3000,
                        detail: 'New report created!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        getAuthors() {
            let url = '/projects/' + this.projectId + '/memberships/';
            this.$api.get(url).then((response) => {
                let authors = [];
                response.data.results.forEach(function (item) {
                    authors.push(item.user);
                });
                this.authorChoices = authors;
            });
        }
    },
    components: {}
};
</script>

<template>
    <Button icon="fa fa-plus" label="Report" outlined @click="open"></Button>

    <Dialog header="Create Report" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <label for="template">Template</label>
                <Dropdown v-model="model.template" id="template" @focus="getTemplates" optionLabel="name" :options="templateChoices"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="variant">Variant</label>
                <Dropdown v-model="model.variant" id="variant" optionLabel="label" :options="variantChoices"></Dropdown>
            </div>
            <div class="field col-12">
                <label for="author">Author</label>
                <Dropdown v-model="model.author" id="author" optionLabel="username" :options="authorChoices" @focus="getAuthors"></Dropdown>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" :loading="loading" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>