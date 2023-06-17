<script>
import ProjectService from '@/service/ProjectService';
import FindingService from '@/service/FindingService'
import DetailCardWithIcon from '@/components/DetailCardWithIcon.vue';
import InfoCardWithForm from '@/components/InfoCardWithForm.vue';
import ProjectUpdateDialog from '@/components/dialogs/ProjectUpdateDialog.vue';


const projectService = new ProjectService();
const findingService = new FindingService()


export default {
    name: "ProjectDetail",
    data() {
        return {
            projectId: this.$route.params.projectId,
            project: {},
            latestFindings: [],
            role: {},
            severityChartData: {
                labels: ['Critical', 'High', 'Medium', 'Low', 'Informational'],
                datasets: [
                    {
                        data: [],
                        backgroundColor: ["#8f0d2d", "#e21538", "#f0801d", "#fab725", "#86cbce"]
                    }
                ]
            },
            severityChartOptions: {
                cutout: '60%'
            },
            breadcrumbs: [
                { label: "Projects", to: this.$router.resolve({ name: "ProjectList" }) },
                { label: "Project Detail", disabled: true }
            ],
            statusChoices: [
                { label: 'Open', value: 'Open' },
                { label: 'Closed', value: 'Closed' }
            ]
        };
    },
    mounted() {
        this.getProject();
        this.getMembership()
        this.getLatestFindings()
        this.getSeverityChartData()
    },
    methods: {
        getProject() {
            projectService.getProject(this.projectId).then((response) => {
                this.project = response.data;
            });
        },
        getMembership() {
            projectService.getProjectMembershipMe(this.projectId).then((response) => {
                this.role = response.data
            })
        },
        getLatestFindings() {
            let params = {
                limit: 5,
                page: 1,
                ordering: '-date_created'
            }
            findingService.getFindings(this.$api, this.projectId, params).then((response) => {
                    this.latestFindings = response.data.results
                })
        },
        getSeverityChartData() {
            let url = "/projects/" + this.projectId + "/stats_finding_dashboard/";
            this.$api.get(url).then((response) => {
                this.severityChartData.datasets[0].data = [
                    response.data.Critical, response.data.High,
                    response.data.Medium, response.data.Low, response.data.Information
                ]
            })
        },
        getPentestTypeDisplay() {
            if (!this.project.pentest_types) {
                return ""
            }
            let pentestTypeNames = []
            this.project.pentest_types.forEach(element => {
                pentestTypeNames.push(element.name)
            })
            return pentestTypeNames.join(", ")
        },
        patchProject(data) {
            projectService.patchProject(this.$api, this.projectId, data).then((response) => {
                this.project = response.data
            })
        }
    },
    computed: {
        projectDateDisplay() {
            return this.project.start_date + " - " + this.project.end_date;
        }
    },
    components: { DetailCardWithIcon, ProjectUpdateDialog, InfoCardWithForm }
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
            <div class="flex justify-content-end">
                <ProjectUpdateDialog :project="project" @object-updated="getProject"></ProjectUpdateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Dates" :text="projectDateDisplay" icon="fa-calendar"></DetailCardWithIcon>
        </div>
        <div class="col-12 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Role" icon="fa-crown" :text="role.role">
            </DetailCardWithIcon>
        </div>
        <div class="col-12 lg:col-6 xl:col-3">
            <!--
            <DetailCardWithIcon title="Status" icon="fa-clock" :text="project.status"></DetailCardWithIcon>-->
            <InfoCardWithForm title="Status" icon="fa-bookmark">
                <Dropdown v-model="project.status" :options="statusChoices" optionValue="value"
                    @change="patchProject({ status: project.status })" optionLabel="label" class="w-full">
                </Dropdown>
            </InfoCardWithForm>
        </div>
        <div class="col-12 lg:col-6 xl:col-3">
            <DetailCardWithIcon title="Pin Project" icon="fa-pin" :text="project.pinned"></DetailCardWithIcon>
        </div>
    </div>

    <div class="grid mt-3">
        <div class="col-12 lg:col-6 xl:col-4">
            <Card class="h-full">
                <template #title>Lastest Findings</template>
                <template #content>
                    <DataView :value="latestFindings">
                        <template #list="slotProps">
                            <div class="col-12">
                                <div class="flex p-4 gap-4">
                                    <div class="flex justify-content-start w-full">
                                        {{ slotProps.data.vulnerability.name }} / {{ slotProps.data.name }}
                                    </div>

                                    <div class="flex align-items-center justify-content-end">
                                        <span class="severity-badge"
                                            :class="'severity-' + slotProps.data.severity.toLowerCase()">{{
                                                slotProps.data.severity }}</span>

                                    </div>
                                </div>
                            </div>
                        </template>
                    </DataView>

                </template>
            </Card>
        </div>
        <div class="col-12 lg:col-6 xl:col-4">
            <Card class="h-full">
                <template #title>Severities</template>
                <template #content>
                    <Chart type="doughnut" :data="severityChartData" :options="severityChartOptions"></Chart>
                </template>
            </Card>
        </div>
        <div class="col-12 lg:col-6 xl:col-4">
            <Card class="h-full">
                <template #title>Information</template>
                <template #content>
                    <div class="grid">
                        <div class="col-6">Test Method</div>
                        <div class="col-6">{{ project.test_method }}</div>
                    </div>
                    <div class="grid">
                        <div class="col-6">Company</div>
                        <div class="col-6">{{ project.company_name }}</div>
                    </div>
                    <div class="grid">
                        <div class="col-6">Pentest Types</div>
                        <div class="col-6">{{ getPentestTypeDisplay() }}</div>
                    </div>
                    <div class="grid">
                        <div class="col-6">Language</div>
                        <div class="col-6">{{ project.language }}</div>
                    </div>
                </template>
            </Card>
        </div>
    </div>
</template>