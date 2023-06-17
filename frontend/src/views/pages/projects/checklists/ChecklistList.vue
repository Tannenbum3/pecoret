<script>
import ChecklistService from '@/service/ChecklistService';
import markdown from '@/utils/markdown'
import AssetSelectField from '@/components/elements/forms/AssetSelectField.vue';
import AssetChecklistCreateDialog from '@/components/dialogs/AssetChecklistCreateDialog.vue';


export default {
    name: "ChecklistList",
    data() {
        return {
            projectId: this.$route.params.projectId,
            categories: [],
            selectedKey: null,
            checklistChoices: [],
            checklist: null,
            expandedItem: null,
            service: new ChecklistService(),
            asset: null,
            model: null,
            breadcrumbs: [
                {
                    label: "Checklists",
                    disabled: true
                }
            ]
        };
    },
    methods: {
        getChecklists() {
            this.service.getChecklists(this.$api).then((response) => {
                this.checklistChoices = response.data.results;
            });
        },
        renderMarkdown(text) {
            return markdown.renderMarkdown(text)
        },
        onAssetChange() {
            this.loadAssetChecklists()
        },
        onChecklistChange() {
            this.loadAssetCategories()
        },
        loadAssetCategories() {
            let params = {
                "checklist": this.checklist
            }
            this.service.getAssetCategories(this.$api, this.projectId, params).then((response) => {
                this.categories = response.data.results
                this.categories.forEach((category) => {
                    category.children = category.items
                    category.key = category.pk.toString()
                    category.children.forEach((item) => {
                        item.checked = false
                        if (item.status == "Closed") {
                            item.checked = true
                        }
                    })
                })
            })
        },
        loadAssetChecklists() {
            let params = {}
            params[this.asset.type] = this.asset.pk
            this.service.getAssetChecklists(this.$api, this.projectId, params).then((response) => {
                this.checklistChoices = response.data.results
            })
        },
        onCheckboxChange(event, item) {
            let status = "Open"
            if (item.checked === true) {
                status = "Closed"
            }
            let data = {
                status: status
            }
            return this.service.patchAssetItem(this.$api, this.projectId, item.pk, data).then(() => {
            })
        },
        onDeleteDialogChecklist() {
            this.$confirm.require({
                message: 'Do you want to delete this checklist for the asset?',
                header: 'Delete confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteAssetChecklist(this.$api, this.projectId, this.checklist).then((response) => {
                        this.$router.push({
                            name: 'ProjectChecklistList',
                            params: {
                                projectId: this.projectId
                            }
                        })
                    })
                }
            })
        }
    },
    mounted() {
    },
    components: { AssetSelectField, AssetChecklistCreateDialog }
}
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs" />
        </div>
    </div>
    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <AssetChecklistCreateDialog @object-created="getChecklists"></AssetChecklistCreateDialog>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="p-fluid formgrid grid">
                    <AssetSelectField v-model="asset" :displayInline="true" @update:model-value="onAssetChange">
                    </AssetSelectField>
                    <div class="field col-10">
                        <Dropdown :options="checklistChoices" placeholder="Checklist" v-model="checklist"
                            @change="onChecklistChange" :disabled="checklistChoices.length < 1" optionLabel="name"
                            optionValue="pk"></Dropdown>
                    </div>
                    <div class="field col-2">
                        <Button label="Checklist" size="small" severity="danger" :disabled="this.checklist === null"
                            icon="fa fa-trash" outlined @click="onDeleteDialogChecklist"></Button>

                    </div>
                </div>
                <div class="grid">
                    <Accordion class="mt-3 w-full col">
                        <AccordionTab v-for="category in categories" :key="category.pk">
                            <template #header>
                                {{ category.name }}
                            </template>
                            <div class="grid">
                                <div class="col-12">
                                    <div class="flex flex-column xl:flex-row xl:align-items-start p-2 gap-2"
                                        v-for="item in category.items">
                                        <div class="flex align-items-center">
                                            <Checkbox @change="onCheckboxChange($event, item)" :binary="true"
                                                v-model="item.checked"></Checkbox>
                                            <label class="ml-3">

                                                <Button @click="this.expandedItem = item" text class="text-color">{{
                                                    item.name
                                                }}</Button>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </AccordionTab>
                    </Accordion>
                    <div class="col md:col-6 mt-3 h-full" v-if="expandedItem">
                        <div class="card surface-ground">
                            <div v-html="renderMarkdown(expandedItem.description)" class="checklist-description"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
