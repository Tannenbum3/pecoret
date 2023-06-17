<script>
import CompanyService from '@/service/CompanyService'
import ToastUIEditor from '@/components/elements/forms/ToastUIEditor.vue'


export default {
    name: 'CompanyInformationCreateDialog',
    props: {
        companyId: {
            required: true
        }
    },
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            companyService: new CompanyService(),
            text: ""
        }
    },
    methods: {
        close() {
            this.visible = false
        },
        open() {
            this.visible = true
        },
        create() {
            let data = {
                text: this.text,
                company: this.companyId
            }
            this.companyService.createCompanyInformation(data).then(() => {
                this.$toast.add(
                    { severity: 'success', summary: 'Created!', detail: 'Company Information created!', life: 3000 }
                )
                this.$emit('object-created')
                this.visible = false
            })
        }
    },
    components: { ToastUIEditor }
}
</script>

<template>
    <Button icon="fa fa-plus" label="Company Information" @click="open" outlined></Button>

    <Dialog header="Create Company Information" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <ToastUIEditor v-model="text" label="Text"></ToastUIEditor>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>