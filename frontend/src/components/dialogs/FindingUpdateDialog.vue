<script>
import FindingService from '@/service/FindingService'
import ProjectVulnerabilityAutocompleteField from '../elements/forms/ProjectVulnerabilityAutocompleteField.vue'
import ToastUIEditor from '@/components/elements/forms/ToastUIEditor.vue'


export default {
    name: "FindingUpdateDialog",
    props: {
        finding: {
            required: true
        }
    },
    emits: ["object-updated"],
    data() {
        return {
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            visible: false,
            model: this.finding,
            findingService: new FindingService(),
            severityChoices: [
                { name: "Critical", value: "Critical" },
                { name: "High", value: "High" },
                { name: "Medium", value: "Medium" },
                { name: "Low", value: "Low" },
                { name: "Informational", value: "Informational" }
            ]
        };
    },
    methods: {
        close() {
            this.visible = false;
        },
        open() {
            this.visible = true;
        },
        patch(){
            if (typeof this.model.vulnerability === 'object'){
                delete this.model.vulnerability
            }
            if (typeof this.model.user_account === 'object'){
                delete this.model.user_account
            }
            // always delete asset, since we dont want to change asset yet
            delete this.model.asset
            let data = {
                user_account: this.model.user_account.pk,
                recommendation: this.model.recommendation,
                name: this.model.name,
                asset: this.model.asset,
                retest_results: this.model.retest_results,
                date_retest: this.model.date_retest,
                exclude_from_report: this.model.exclude_from_report
            }

            this.findingService.patchFinding(this.projectId, this.findingId, data).then((response) => {
                this.$emit('object-updated', this.model)
                this.visible = false
            })
        },
    },
    watch: {
        finding: {
            immediate: true,
            deep: true,
            handler(value) {
                this.model = value;
            }
        }
    },
    components: { ProjectVulnerabilityAutocompleteField, ToastUIEditor }
}

</script>

<template>
    <Button icon="fa fa-pen-to-square" label="Edit" @click="open" outlined></Button>

    <Dialog header="Update Finding" v-model:visible="visible" :modal="true" :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <ProjectVulnerabilityAutocompleteField v-model="finding.vulnerability"></ProjectVulnerabilityAutocompleteField>
        </div>
        <div class="flex flex-column gap-2 mt-3">
            <label for="name">Name</label>
            <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
        </div>
        <div class="flex flex-column gap-2 mt-3">
            <label for="severity">Severity</label>
            <Dropdown v-model="model.severity" :options="severityChoices" optionLabel="name" optionValue="value"
                id="severity">
            </Dropdown>
        </div>
        <div class="flex flex-column gap-2 mt-3">
            <div class="flex align-items-center">
                <Checkbox v-model="model.exclude_from_report" binary id="exclude_from_report"></Checkbox>
                <label for="exclude_from_report" class="ml-2"> Exclude From Report?</label>
            </div>
        </div>
        <div class="flex flex-column gap-2 mt-3">
            <div class="flex align-items-center">
                <Checkbox v-model="model.authentication_required" binary id="authentication_required"></Checkbox>
                <label for="authentication_required" class="ml-2"> Authentication Required?</label>
            </div>
        </div>

        <div class="flex flex-column gap-2 mt-3">
            <ToastUIEditor v-model="finding.recommendation" label="Recommendation" v-if="finding.recommendation !== null"></ToastUIEditor>
        </div>
        <div class="flex flex-column gap-2 mt-3">
            <label for="date_retested">Date Retested</label>
            <Calendar v-model="finding.date_retested" id="date_retested"></Calendar>
        </div>

        <div class="flex flex-column gap-2 mt-3">
            <ToastUIEditor v-model="finding.retest_results" label="Retest Results" v-if="finding.retest_results !== null"></ToastUIEditor>
        </div>


        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="patch" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>