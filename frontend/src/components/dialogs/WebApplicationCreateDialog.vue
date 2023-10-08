<script>
import AssetService from '@/service/AssetService';
import AssetEnvironmentSelectField from '../elements/forms/AssetEnvironmentSelectField.vue';
import AssetAccessibleSelectField from '../elements/forms/AssetAccessibleSelectField.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'WebApplicationCreateDialog',
    emits: ['object-created'],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                name: null,
                base_url: null,
                environment: 'Unknown',
                accessible: 'Unknown',
                description: ''
            },
            assetService: new AssetService()
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
            this.assetService.createWebApplication(this.$api, this.projectId, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Web application created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    },
    components: { AssetEnvironmentSelectField, AssetAccessibleSelectField, MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Web Application" outlined @click="open"></Button>

    <Dialog header="Create Web Application" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="formgrid grid p-fluid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" type="text" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <label for="base_url">Base URL</label>
                <InputText id="base_url" type="text" v-model="model.base_url"></InputText>
            </div>
            <div class="field col-12 md:col-6">
                <AssetEnvironmentSelectField v-model="model.environment"></AssetEnvironmentSelectField>
            </div>
            <div class="field col-12 md:col-6">
                <AssetAccessibleSelectField v-model="model.accessible"></AssetAccessibleSelectField>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>