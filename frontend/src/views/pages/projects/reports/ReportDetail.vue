<script>
import ReportService from '@/service/ReportService'
import ProjectService from '@/service/ProjectService'
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue'
import ReportTabMenu from '@/components/pages/ReportTabMenu.vue'


export default {
    name: 'ReportDetail',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Reports',
                    to: this.$router.resolve({
                        name: 'ReportList',
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: 'Report Detail',
                    disabled: true
                }
            ],
            report: { author: {} },
            project: {},
            reportTemplate: {},
            projectId: this.$route.params.projectId,
            reportId: this.$route.params.reportId,
            reportService: new ReportService(),
            projectService: new ProjectService(),
            authorChoices: []
        }
    },
    mounted() {
        this.getItem()
        this.projectService.getProject(this.projectId).then((response) => {
            this.project = response.data
        })
    },
    methods: {
        getItem() {
            this.reportService.getReport(this.$api, this.projectId, this.reportId).then((response) => {
                this.report = response.data
                this.authorChoices.push(this.report.author)
                this.getReportTemplate()
            })
        },
        getReportTemplate() {
            this.reportService.getReportTemplate(this.$api, this.report.template).then((response) => {
                this.reportTemplate = response.data
            })
        },
        updateReport() {
            let data = {
                author: this.report.author.pk,
                title: this.report.title,
                name: this.report.name
            }
            this.reportService.updateReport(this.$api, this.projectId, this.reportId, data).then((response) => {
                this.getItem()
            })
        },
        getAuthorChoices() {
            let url = "/projects/" + this.projectId + "/memberships/";
            this.$api.get(url).then((response) => {
                let authors = []
                response.data.results.forEach(function (item) {
                    authors.push(item.user)
                });
                this.authorChoices = authors;
            });
        }
    },
    components: { DetailCardWithIcon, ReportTabMenu }
}
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <ReportTabMenu class="surface-card"></ReportTabMenu>
            <Card>
                <template #content>
                    <div class="grid">
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="Language" icon="fa fa-flag" class="surface-ground"
                                :text="project.language"></DetailCardWithIcon>
                        </div>
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="Author" icon="fa fa-feather" class="surface-ground"
                                :text="report.author.username"></DetailCardWithIcon>
                        </div>
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="Template" icon="fa fa-wand-magic-sparkles" class="surface-ground"
                                :text="reportTemplate.name"></DetailCardWithIcon>
                        </div>
                        <div class="col-12 md:col-3">
                            <DetailCardWithIcon title="Variant" icon="fa fa-file-invoice" class="surface-ground"
                                :text="report.variant"></DetailCardWithIcon>
                        </div>
                    </div>

                    <div class="grid mt-3">
                        <div class="col-12">
                            <div class="flex flex-column gap-2">
                                <label for="name">Name</label>
                                <InputText id="name" v-model="report.name"></InputText>
                            </div>
                            <div class="flex flex-column gap-2">
                                <label for="title">Title</label>
                                <InputText id="title" v-model="report.title"></InputText>
                            </div>
                            <div class="flex flex-column gap-2">
                                <label for="author">Author</label>
                                <Dropdown id="author" optionLabel="username" :options="authorChoices"
                                    v-model="report.author" @focus="getAuthorChoices"></Dropdown>
                            </div>

                            <div class="flex justify-content-end mt-3">
                                <Button label="Save" @click="updateReport"></Button>
                            </div>
                        </div>

                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>