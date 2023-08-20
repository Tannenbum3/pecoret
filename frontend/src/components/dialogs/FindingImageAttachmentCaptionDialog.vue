<script>
import FindingService from "@/service/FindingService";


export default {
    name: "FindingImageAttachmentCaptionDialog",
    props: {
        attachment: {
            required: true
        }
    },
    emits: ["object-updated"],
    data() {
        return {
            visible: false,
            model: this.attachment,
            service: new FindingService(),
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId
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
                caption: this.model.caption
            };
            this.service.findingImageAttachmentPatch(this.$api, this.projectId, this.findingId, this.attachment.pk, data).then((response) => {
                this.$emit("object-updated", response.data);
                this.visible = false;
            });
        }
    },
    watch: {
        attachment: {
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
    <Button label="Set Caption" class="p-0 m-0" link @click="open" v-tooltip="model.caption"></Button>

    <Dialog header="Attachment Caption" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="grid formgrid p-fluid">
            <div class="field col-12">
                <label for="caption">Caption</label>
                <InputText id="caption" v-model="model.caption"></InputText>
            </div>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>