<script>
import ProjectCommandService from '@/service/ProjectCommandService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';

export default {
    name: 'CommandUpdate',
    props: {
        command: {
            required: true
        }
    },
    emits: ['object-updated'],
    data() {
        return {
            visible: false,
            model: this.command,
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
        patch() {
            let data = {
                command: this.model.command,
                output: this.model.output,
                date_run: this.model.date_run
            };
            this.service.patchCommand(this.$api, this.$route.params.projectId, this.command.pk, data).then(() => {
                this.$emit('object-updated', this.model);
                this.visible = false;
            });
        }
    },
    watch: {
        command: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: { MarkdownEditor }
};
</script>

<template>
    <Button icon="fa fa-pen-to-square" size="small" @click="open" outlined></Button>

    <Dialog header="Update Command" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
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
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>