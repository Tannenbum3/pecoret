<script>
import ProjectVulnerabilityAutocompleteField from '@/components/elements/forms/ProjectVulnerabilityAutocompleteField.vue';
import UserAccountService from '@/service/UserAccountService'
import SeveritySelectField from '@/components/elements/forms/SeveritySelectField.vue'
import AssetSelectField from '@/components/elements/forms/AssetSelectField.vue'
import FindingService from '@/service/FindingService'


export default {
    name: "FindingCreate",
    methods: {
        onUserAccountFocus() {
            if (this.userAccountChoices.length) {
                return
            }
            this.accountService.getAccounts(this.$api, this.projectId).then((response) => {
                this.userAccountChoices = response.data.results
            })
        },
        createFinding() {
            let data = {
                asset: this.model.asset,
                severity: this.model.severity.value,
                name: this.model.name,
                status: "Open",
                vulnerability_id: this.model.vulnerability,
                authenticated_test: this.model.authentication_required,
            }
            if (this.model.user_account) {
                data["user_account"] = this.model.user_account.pk
            }
            this.service.createFinding(this.$api, this.projectId, data).then((response) => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Finding created!',
                    life: 3000,
                    detail: 'Finding was created successfully!'
                })
                this.$router.push({
                    name: 'FindingDetail',
                    params: {
                        projectId: this.projectId,
                        findingId: response.data.pk
                    }
                })
            })
        }
    },
    data() {
        return {
            breadcrumbs: [
                {
                    label: "Findings",
                    to: this.$router.resolve({
                        name: "FindingList",
                        params: {
                            projectId: this.$route.params.projectId,
                        }
                    })
                },
                {
                    label: "Create",
                    disabled: true
                },
            ],
            model: {
                vulnerability: null,
                severity: null,
                asset: null,
                authentication_required: false,
                user_account: null
            },
            userAccountChoices: [],
            accountService: new UserAccountService(),
            service: new FindingService(),
            projectId: this.$route.params.projectId
        };
    },
    components: { ProjectVulnerabilityAutocompleteField, SeveritySelectField, AssetSelectField }
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
            <Card>
                <template #content>
                    <div class="p-fluid grid formgrid">
                        <div class="field col-12">
                            <ProjectVulnerabilityAutocompleteField v-model="model.vulnerability">
                            </ProjectVulnerabilityAutocompleteField>
                        </div>
                        <div class="field col-12">
                            <label for="name">Name</label>
                            <InputText id="name" type="text" v-model="model.name" label="Name"></InputText>
                        </div>
                        <div class="field col-12">
                            <SeveritySelectField v-model="model.severity"></SeveritySelectField>
                        </div>
                        <AssetSelectField v-model="model.asset"></AssetSelectField>

                        <div class="field col-12">
                            <InputSwitch v-model="model.authentication_required" id="auth_required"></InputSwitch>
                            <label for="auth_required" class="ml-3">Authentication Required?</label>
                        </div>
                        <div class="field col-12" v-if="model.authentication_required">
                            <label for="account">Account</label>
                            <Dropdown :options="userAccountChoices" @focus="onUserAccountFocus" optionLabel="username"
                                v-model="model.user_account"></Dropdown>
                        </div>

                    </div>
                    <div class="flex flex-column gap-2 mt-3">
                        <div class="flex justify-content-end">
                            <Button label="Save" @click="createFinding"></Button>
                        </div>
                    </div>
                </template>
            </Card>

        </div>
    </div>
</template>