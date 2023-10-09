<script>
import FindingService from '@/service/FindingService';

export default {
    name: 'FindingAsAdvisoryDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            loading: false,
            model: {
                product: null,
                affected_versions: null,
                vendor_name: null,
                vendor_url: null
            },
            service: new FindingService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        create() {
            this.loading = true;
            let data = {
                product: this.model.product,
                affected_versions: this.model.affected_versions,
                affected_product: this.model.affected_product,
                vendor_name: this.model.vendor_name,
                vendor_url: this.model.vendor_url
            };
            this.service
                .findingAsAdvisory(this.$api, this.projectId, this.findingId, data)
                .then((response) => {
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Finding copies as advisory!',
                        life: 3000,
                        detail: 'Finding was successfully copied as advisory!'
                    });
                    this.$emit('object-created', response.data);
                    this.visible = false;
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    components: {}
};
</script>

<template>
    <Button icon="fa fa-plus" label="Finding As Advisory" outlined @click="open"></Button>

    <Dialog header="Create Advisory from Finding" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="product">Product</label>
                <InputText id="product" v-model="model.product"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="vendor">Vendor</label>
                <InputText id="vendor" v-model="model.vendor_name"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <label for="vendor_url">Vendor-URL</label>
                <InputText type="url" v-model="model.vendor_url"></InputText>
            </div>
            <div class="field col-12">
                <label for="versions">Affected Versions</label>
                <InputText v-model="model.affected_versions" id="versions"></InputText>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" :loading="loading" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>