<script>
import AdvisoryService from '@/service/AdvisoryService'
import AdvisoryTabMenu from '../../../components/pages/AdvisoryTabMenu.vue'


export default {
    name: "ProofList",
    data() {
        return {
            service: new AdvisoryService(),
            loading: false,
            breadcrumbs: [
                {
                    label: "Advisories",
                    to: this.$router.resolve({
                        name: "AdvisoryList"
                    })
                },
                {
                    label: "Advisory Detail",
                    to: this.$router.resolve({
                        name: "AdvisoryDetail",
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: "Proofs",
                    disabled: true
                }
            ],
            advisoryId: this.$route.params.advisoryId,
            items: [],
            pagination: { limit: 50, page: 1 },
            editButtonDisabled: true,
            editProofPk: null
        };
    },
    methods: {
        getItems() {
            this.loading = true;
            let data = {
                limit: this.pagination.limit,
                page: this.pagination.page
            };
            this.service.getProofs(this.$api, this.advisoryId, data).then((response) => {
                this.items = response.data.results;
            }).finally(() => { this.loading = false; });
        },
        reorderProofs(event){
            event.value.forEach((item, index) => {
                let data = {order: index + 1}
                this.service.patchProof(this.$api, this.advisoryId, item.pk, data)
            })
        },
        onProofSelect(event){
            if (event.length === 1){
                this.editButtonDisabled = false
                this.editProofPk = event[0].pk
            } else {
                this.editButtonDisabled = true
            }
        },
        onEditButtonClick(){
            this.$router.push({
                name: 'AdvisoryProofUpdate',
                params: {
                    advisoryId: this.advisoryId,
                    proofId: this.editProofPk
                }
            })
        }
    },
    mounted(){
        this.getItems()
    },
    components: { AdvisoryTabMenu}
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
            <div class="flex justify-content-start"></div>
        </div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <Button :disabled="editButtonDisabled" label="Edit" icon="fa fa-pen-to-square" outlined @click="onEditButtonClick"></Button>
                <Button @click="this.$router.push({name: 'AdvisoryProofCreate', params: {advisoryId: this.advisoryId}})" label="Proof" icon="fa fa-plus"></Button>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12">
            <AdvisoryTabMenu class="surface-card"></AdvisoryTabMenu>
            <div class="card">
                <OrderList v-model="items" listStyle="height:auto" dataKey="pk" @reorder="reorderProofs" @update:selection="onProofSelect">
                    <template #header>Proofs</template>
                    <template #item="slotProps">
                        {{ slotProps.item.title }}
                    </template>
                </OrderList>
            </div>
        </div>
    </div>
</template>