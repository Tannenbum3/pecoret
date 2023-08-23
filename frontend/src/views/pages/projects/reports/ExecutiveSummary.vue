<script>
import ReportTabMenu from "../../../../components/pages/ReportTabMenu.vue";
import MarkdownEditor from "@/components/elements/forms/MarkdownEditor.vue";
import ReportService from "@/service/ReportService";


export default {
    name: "ExecutiveSummary",
    data() {
        return {
            breadcrumbs: [
                {
                    label: "Reports",
                    to: this.$router.resolve({
                        name: "ReportList",
                        params: {
                            projectId: this.$route.params.projectId
                        }
                    })
                },
                {
                    label: "Report Detail",
                    to: this.$router.resolve({
                        name: "ReportDetail",
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: "Executive Summary",
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
    mounted() {
        this.getItem();
    },
    methods: {
        patchEvaluation() {
            let data = {
                evaluation: this.model.evaluation
            };
            this.reportService.updateReport(this.$api, this.projectId, this.reportId, data).then(() => {
                this.$toast.add({
                    severity: "success",
                    summary: "Evaluation updated!",
                    life: 3000,
                    detail: "Evaluation was updated successfully!"
                });
            });
        },
        getItem() {
            this.reportService.getReport(this.$api, this.projectId, this.reportId).then((response) => {
                this.model = response.data;
            });
        },
        patchRecommendation() {
            let data = {
                recommendation: this.model.recommendation
            };
            this.reportService.updateReport(this.$api, this.projectId, this.reportId, data).then(() => {
                this.$toast.add({
                    severity: "success",
                    summary: "Recommendation updated!",
                    life: 3000,
                    detail: "Recommendation was updated successfully!"
                });
            });
        }
    },
    components: { ReportTabMenu, MarkdownEditor }
};
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
                    <div class="grid formgrid p-fluid">
                        <div class="field col-12">
                            <label for="evaluation">Evaluation</label>
                            <MarkdownEditor v-model="model.evaluation" @blur="patchEvaluation"></MarkdownEditor>
                        </div>
                        <div class="field col-12">
                            <label for="recommendation">Recommendation</label>
                            <MarkdownEditor v-model="model.recommendation" @blur="patchRecommendation"></MarkdownEditor>
                        </div>
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>