<script>
import ProjectCommandService from '@/service/ProjectCommandService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'ProjectCommandCreate',
    emits: ['object-created'],
    components: { MarkdownEditor },
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            model: {
                command: null,
                output: null,
                date_run: null
            },
            service: new ProjectCommandService()
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
            this.service.createCommand(this.$api, this.projectId, this.model).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created!',
                    life: 3000,
                    detail: 'Command created!'
                });
                this.$emit('object-created', response.data);
                this.visible = false;
            });
        }
    }
};
</script>

<template>
    <Button icon="fa fa-plus" label="Command" outlined @click="open"></Button>

    <Dialog header="Create Command" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="p-fluid formgrid grid">
            <div class="field col-12">
                <label for="command">Command</label>
                <InputText id="name" type="text" v-model="model.command"></InputText>
            </div>
            <div class="field col-12">
                <label for="output">Output</label>
                <MarkdownEditor v-model="model.output"></MarkdownEditor>
            </div>
            <div class="field col-12">
                <label for="date_expire">Date run?</label>
                <Calendar v-model="model.date_run" id="date_expire"></Calendar>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>