<script>
import ProjectService from '@/service/ProjectService'
import CompanyService from '@/service/CompanyService'


export default {
    name: "ProjectContactCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            projectId: this.$route.params.projectId,
            companyId: null,
            model: {
                name: null,
                date_expire: null,
            },
            projectService: new ProjectService(),
            companyService: new CompanyService(),
            contactChoices: []
        };
    },
    mounted(){
        this.projectService.getProject(this.projectId).then((response) => {
            this.companyId = response.data.company
        })
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        getContactChoices(){
            if(this.contactChoices){
                return
            }
            this.companyService.getContacts(this.companyId).then((response) => {
                this.contactChoices = response.data.results
            })
        },
        onFilterContact(event){
            let params = {
                search: event.value
            }
            this.companyService.getContacts(this.companyId, params).then((response) => {
                this.contactChoices = response.data.results
            })
        },
        create() {
            let data = {
                contact: this.model.contact
            }
            this.projectService.createContact(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "Contact added!",
                    life: 3000,
                    detail: "Contact added to project!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    },
}
</script>

<template>
    <Button icon="fa fa-plus" label="Contact" outlined @click="open"></Button>

    <Dialog header="Add Contact" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="contact">Contact</label>
            <Dropdown id="contact" filter optionValue="pk"
                :optionLabel="(option) => option.first_name + ' ' + option.last_name"
                :options="contactChoices" v-model="model.contact"
                @filter="onFilterContact" @focus="getContactChoices"
            ></Dropdown>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>