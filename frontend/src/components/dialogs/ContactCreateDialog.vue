<script>
import CompanyService from '@/service/CompanyService'
import ToastUIEditor from '@/components/elements/forms/ToastUIEditor.vue'


export default {
    name: 'ContactCreateDialog',
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            companyService: new CompanyService(),
            companyId: this.$route.params.companyId,
            model: {
                first_name: null,
                last_name: null,
                phone: null,
                role: null,
                pgp_public_key: null,
                email: null
            }
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
                first_name: this.model.first_name,
                last_name: this.model.last_name,
                phone: this.model.phone,
                pgp_public_key: this.model.pgp_public_key,
                email: this.model.email,
                role: this.model.role
            }
            this.companyService.createContact(this.$api, this.companyId, data).then(() => {
                this.$toast.add(
                    { severity: 'success', summary: 'Created!', detail: 'Contact created for company!', life: 3000 }
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
    <Button icon="fa fa-plus" label="Contact" @click="open" outlined></Button>

    <Dialog header="Create Contact" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="first_name">First Name</label>
            <InputText id="first_name" v-model="model.first_name"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="last_name">Last Name</label>
            <InputText id="last_name" v-model="model.last_name"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="email">E-Mail</label>
            <InputText id="email" v-model="model.email" type="email"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="phone">Phone</label>
            <InputText id="phone" v-model="model.phone"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="role">Role</label>
            <InputText id="role" v-model="model.role"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="pgp_public_key">PGP Public Key</label>
            <Textarea id="pgp_public_key" v-model="model.pgp_public_key"></Textarea>
        </div>



        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>