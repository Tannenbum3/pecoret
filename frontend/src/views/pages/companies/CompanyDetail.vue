<script>
import markdown from "@/utils/markdown"
import CompanyService from '@/service/CompanyService'
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue'
import CompanyInformationCreateDialog from "@/components/dialogs/CompanyInformationCreateDialog.vue"
import CompanyUpdateDialog from "@/components/dialogs/CompanyUpdateDialog.vue"
import CompanyTabMenu from "../../../components/pages/CompanyTabMenu.vue"


export default {
    name: 'CompanyDetail',
    data() {
        return {
            companyService: new CompanyService(),
            companyId: this.$route.params.companyId,
            breadcrumbs: [
                { label: 'Companies', to: this.$router.resolve({ name: 'CompanyList' }) },
                { label: 'Company Detail', disabled: true }
            ],
            company: {},
            companyInformation: [],
            reportTemplate: {}
        }
    },
    methods: {
        getCompany() {
            this.companyService.getCompany(this.companyId).then((response) => {
                this.company = response.data
                this.getReportTemplate()
            })
        },
        getReportTemplate() {
            let url = "/report-templates/" + this.company.report_template + "/"
            this.$api.get(url).then((response) => {
                this.reportTemplate = response.data
            })
        },
        getCompanyInformation() {
            this.companyService.getCompanyInformations(this.companyId).then((response) => {
                this.companyInformation = response.data.results
            })
        },
        displayMarkdown(text) {
            if (text !== null) {
                return markdown.renderMarkdown(text)
            }
            return text
        },
    },
    mounted() {
        this.getCompany()
        this.getCompanyInformation()
    },
    components: { DetailCardWithIcon, CompanyInformationCreateDialog, CompanyUpdateDialog, CompanyTabMenu }

}
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-6">
            <div class="flex justify-content-start">
                <strong class="text-lg">{{ company.name }}</strong>
            </div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <CompanyUpdateDialog :company="company" @object-updated="getCompany"></CompanyUpdateDialog>
                <CompanyInformationCreateDialog @object-created="getCompanyInformation" :company-id="company.pk"></CompanyInformationCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <CompanyTabMenu class="surface-card"></CompanyTabMenu>
            <Card>
                <template #content>
                    <div class="grid">
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="Street" icon="fa-road" class="surface-ground" :text="company.street">
                            </DetailCardWithIcon>
                        </div>
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="City" icon="fa-city" class="surface-ground" :text="company.city">
                            </DetailCardWithIcon>
                        </div>
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="Country" icon="fa-earth" class="surface-ground"
                                :text="company.country"></DetailCardWithIcon>
                        </div>
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="Report Template" icon="fa-file" class="surface-ground"
                                :text="reportTemplate.name"></DetailCardWithIcon>
                        </div>
                    </div>
                    <div class="grid">
                        <div class="col-12">
                            <p class="text-xl">Company Information</p>
                            <DataView :value="companyInformation" class="w-full">
                                <template #list="slotProps">
                                    <div class="col-12">
                                        <div v-html="displayMarkdown(slotProps.data.text)"></div>
                                    </div>
                                </template>
                            </DataView>
                        </div>
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>