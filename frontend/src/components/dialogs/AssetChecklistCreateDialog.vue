<script>
import ChecklistService from '@/service/ChecklistService'
import AssetSelectField from '@/components/elements/forms/AssetSelectField.vue'


export default {
    name: 'AssetChecklistCreateDialog',
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            model: {
                asset: null,
                checklist: null
            },
            projectId: this.$route.params.projectId,
            checklistChoices: [],
            service: new ChecklistService(),
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
                asset: this.model.asset,
                checklist_id: this.model.checklist
            }
            this.service.createAssetChecklist(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created',
                    life: 3000,
                    detail: 'Checklist created successfully!'
                })
                this.$emit('object-created', response.data)
                this.visible = false
            })
        },
        onFocusChecklist(){
            this.service.getChecklists(this.$api).then((response) => {
                this.checklistChoices = response.data.results
            })
        },
        onFilterChecklist(event){
            let params = {
                search: event.value
            }
            this.service.getChecklists(this.$api, params).then((response) => {
                this.checklistChoices = response.data.results
            })
        }
    },
    components: { AssetSelectField }
}

</script>

<template>
    <Button icon="fa fa-plus" label="Checklist" @click="open()" outlined></Button>

    <Dialog header="Create Checklist" v-model:visible="visible" :breakpoints="{ '960px': '75vw' }" :style="{ width: '70vw' }"
        :modal="true">

        <div class="p-fluid formgrid grid">
            <AssetSelectField v-model="model.asset"></AssetSelectField>
            <div class="field col-12">
                <label for="test_method">Checklist</label>
                <Dropdown v-model="model.checklist"
                    :options="checklistChoices" filter
                    @focus="onFocusChecklist"
                    @filter="onFilterChecklist"
                    optionLabel="name" optionValue="checklist_id"></Dropdown>
            </div>
            
        </div>


        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>