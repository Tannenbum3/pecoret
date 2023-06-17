<script>
import AdvisoryService from '@/service/AdvisoryService'


export default {
    name: "AdvisoryTimelineCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            advisoryId: this.$route.params.advisoryId,
            model: {
                text: null,
                date: null
            },
            service: new AdvisoryService()
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
            let data = {
                text: this.model.text,
                date: this.model.date.toISOString().split("T")[0]
            }
            this.service.createTimeline(this.$api, this.advisoryId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "Timeline added!",
                    life: 3000,
                    detail: "Timeline added to Advisory!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    },
}
</script>

<template>
    <Button icon="fa fa-plus" label="Timeline" outlined @click="open"></Button>

    <Dialog header="Create Timeline Entry" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="text">Text</label>
            <InputText id="text" v-model="model.text"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="date">Date</label>
            <Calendar v-model="model.date" id="date"></Calendar>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>