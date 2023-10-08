<script>
import AdminService from '@/service/AdminService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProjectTypeUpdateDialog',
    components: { MarkdownEditor },
    props: {
        pentestType: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.pentestType,
            service: new AdminService()
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch() {
            let data = {
                name: this.model.name,
                description: this.model.description
            };
            this.service.patchProjectType(this.$api, this.pentestType.pk, data).then(() => {
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        }
    },
    watch: {
        pentestType: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <Dialog header="Update Project Type" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="formgrid grid p-fluid">
            <div class="field col-12">
                <label for="name">Name</label>
                <InputText id="name" v-model="model.name"></InputText>
            </div>
            <div class="field col-12">
                <label for="description">Description</label>
                <MarkdownEditor v-model="model.description"></MarkdownEditor>
            </div>
        </div>

        <div class="flex flex-column gap-2"></div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>