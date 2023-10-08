<script>
import AdvisoryService from '@/service/AdvisoryService';
import VulnerabilityTemplateService from '@/service/VulnerabilityTemplateService';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'AdvisoryCreate',
    data() {
        return {
            service: new AdvisoryService(),
            templateService: new VulnerabilityTemplateService(),
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            model: {
                internal_name: null,
                template: null,
                product: null,
                affected_versions: null,
                fixed_version: null,
                severity: null,
                vendor_name: null,
                vendor_url: null
            },
            templateChoices: []
        };
    },
    methods: {
        create() {
            let data = {
                internal_name: this.model.internal_name,
                vulnerability_id: this.model.template,
                product: this.model.product,
                description: this.model.description,
                affected_versions: this.model.affected_versions,
                fixed_version: this.model.fixed_version,
                severity: this.model.severity,
                vendor_name: this.model.vendor_name,
                vendor_url: this.model.vendor_url
            };
            this.service.createAdvisory(this.$api, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Advisory created!',
                    life: 3000,
                    detail: 'Advisory was created successfully!'
                });
                this.$router.push({
                    name: 'AdvisoryDetail',
                    params: {
                        advisoryId: response.data.pk
                    }
                });
            });
        },
        preSelectTemplateValues(obj) {
            this.templateChoices.forEach((item) => {
                if (item.vulnerability_id === this.model.template) {
                    this.model.severity = item.severity;
                    this.model.recommendation = item.recommendation;
                }
            });
        },
        onFocusTemplate() {
            this.templateService.getTemplates(this.$api).then((response) => {
                this.templateChoices = response.data.results;
            });
        },
        onFilterTemplate(event) {
            let params = {
                search: event.value
            };
            this.templateService.getTemplates(this.$api, params).then((response) => {
                this.templateChoices = response.data.results;
            });
        }
    },
    mounted() {},
    components: { SeveritySelectField, MarkdownEditor }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="p-fluid formgrid grid">
                    <div class="field col-12">
                        <label for="name">Internal Name</label>
                        <InputText id="name" v-model="model.internal_name"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="template">Vulnerability Template</label>
                        <Dropdown :options="templateChoices" optionLabel="name" optionValue="vulnerability_id" @change="preSelectTemplateValues" @focus="onFocusTemplate" filter @filter="onFilterTemplate" v-model="model.template"></Dropdown>
                    </div>
                    <div class="field col-12 md:col-6">
                        <SeveritySelectField v-model="model.severity"></SeveritySelectField>
                    </div>
                    <div class="field col-12">
                        <label for="product">Product</label>
                        <InputText id="product" v-model="model.product"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="affected_versions">Affected Versions</label>
                        <InputText id="affected_versions" v-model="model.affected_versions"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="fixed_versions">Fixed Version</label>
                        <InputText id="fixed_version" v-model="model.fixed_version"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_name">Vendor</label>
                        <InputText id="vendor_name" v-model="model.vendor_name"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_url">Vendor URL</label>
                        <InputText id="vendor_url" v-model="model.vendor_url"></InputText>
                    </div>
                    <div class="field col-12">
                        <label for="description">Description</label>
                        <MarkdownEditor v-model="model.description"></MarkdownEditor>
                    </div>
                    <div class="field col-12">
                        <label for="recommendation">Recommendation</label>
                        <MarkdownEditor v-model="model.recommendation"></MarkdownEditor>
                    </div>
                    <div class="mt-3 col-12">
                        <div class="justify-content-end flex">
                            <Button label="Save" @click="create"></Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>