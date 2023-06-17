<script>
import ReportTabMenu from '../../../../components/pages/ReportTabMenu.vue';
import ToastUIEditor from '../../../../components/elements/forms/ToastUIEditor.vue';
import ReportService from '@/service/ReportService'


export default {
    name: "ExecutiveSummary",
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
                    to: this.$router.resolve({
                        name: 'ReportDetail',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Executive Summary',
                    disabled: true
                }
            ],
            model: {
                evaluation: "",
                recommendation: ""
            },
            reportService: new ReportService(),
            reportId: this.$route.params.reportId,
            projectId: this.$route.params.projectId
        };
    },
    methods: {
        patchEvaluation() {
            let data = {
                evaluation: this.model.evaluation
            }
            this.reportService.updateReport(this.$api, this.projectId, this.reportId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Evaluation updated!',
                    life: 3000,
                    detail: 'Evaluation was updated successfully!'
                })
            })
        },
        patchRecommendation(){
            let data = {
                recommendation: this.model.recommendation
            }
            this.reportService.updateReport(this.$api, this.projectId, this.reportId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Recommendation updated!',
                    life: 3000,
                    detail: 'Recommendation was updated successfully!'
                })
            })
        }
    },
    components: { ReportTabMenu, ToastUIEditor }
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
                        <div class="col-12">
                            <div class="flex flex-column gap-2">
                                <ToastUIEditor label="Evaluation"
                                    v-model="model.evaluation"
                                    @editor-blur="patchEvaluation"
                                    ></ToastUIEditor>
                            </div>
                            <div class="flex flex-column gap-2">
                                <ToastUIEditor label="Recommendation"
                                    v-model="model.recommendation"
                                    @editor-blur="patchRecommendation"
                                    ></ToastUIEditor>
                            </div>
                        </div>
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>