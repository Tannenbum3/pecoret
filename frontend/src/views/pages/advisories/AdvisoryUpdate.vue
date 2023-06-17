<script>
import AdvisoryService from '@/service/AdvisoryService';
import VulnerabilityTemplateService from '@/service/VulnerabilityTemplateService';
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue';

export default {
    name: 'AdvisoryUpdate',
    data() {
        return {
            service: new AdvisoryService(),
            templateService: new VulnerabilityTemplateService(),
            advisoryId: this.$route.params.advisoryId,
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Advisory Detail',
                    to: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Update',
                    disabled: true
                }
            ],
            model: {},
            templateChoices: [],
            loaded: false
        };
    },
    methods: {
        update() {
            let data = {
                internal_name: this.model.internal_name,
                product: this.model.product,
                affected_versions: this.model.affected_versions,
                fixed_versions: this.model.fixed_versions,
                vendor_name: this.model.vendor_name,
                vendor_url: this.model.vendor_url
            };
            this.service.patchAdvisory(this.$api, this.advisoryId, data).then((response) => {
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
        getAdvisory() {
            this.service.getAdvisory(this.$api, this.advisoryId).then((response) => {
                this.model = response.data;
                this.model.template = response.data.vulnerability.vulnerability_id
                this.templateChoices.push(response.data.vulnerability);
                this.loaded = true;
            });
        },
    },
    mounted() {
        this.getAdvisory();
    },
    components: { SeveritySelectField }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="p-fluid formgrid grid" v-if="loaded">
                    <div class="field col-12">
                        <label for="name">Internal Name</label>
                        <InputText id="name" v-model="model.internal_name"></InputText>
                    </div>
                    <div class="field col-12">
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
                        <label for="fixed_versions">Fixed Versions</label>
                        <InputText id="fixed_versions" v-model="model.fixed_versions"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_name">Vendor</label>
                        <InputText id="vendor_name" v-model="model.vendor_name"></InputText>
                    </div>
                    <div class="field col-12 md:col-6">
                        <label for="vendor_url">Vendor URL</label>
                        <InputText id="vendor_url" v-model="model.vendor_url"></InputText>
                    </div>
                    <div class="mt-3 col-12">
                        <div class="justify-content-end flex">
                            <Button label="Save" @click="update"></Button>
                        </div>
                    </div>
                </div>

                <div v-else class="grid w-full">
                    <Skeleton class="mb-2"></Skeleton>
                    <Skeleton width="10rem" class="mb-2"></Skeleton>
                    <Skeleton width="5rem" class="mb-2"></Skeleton>
                    <Skeleton height="2rem" class="mb-2"></Skeleton>
                    <Skeleton width="10rem" height="4rem"></Skeleton>
                </div>
            </div>
        </div>
    </div>
</template>
