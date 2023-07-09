<script>
import FindingService from "@/service/FindingService";
import FindingTabMenu from "@/components/pages/FindingTabMenu.vue";
import DetailCardWithIcon from "@/components/DetailCardWithIcon.vue";
import InfoCardWithForm from "@/components/InfoCardWithForm.vue";
import FindingAsAdvisoryDialog from "@/components/dialogs/FindingAsAdvisoryDialog.vue";

export default {
  name: "FindingDetail",
  mounted() {
    this.getFinding();
    this.getProofs();
  },
  data() {
    return {
      findingService: new FindingService(),
      projectId: this.$route.params.projectId,
      findingId: this.$route.params.findingId,
      proofs: [],
      finding: { user_account: {}, component: {} },
      breadcrumbs: [
        {
          label: "Findings",
          to: this.$router.resolve({
            name: "FindingList",
            params: { projectId: this.$route.params.projectId }
          }).path
        },
        {
          label: "Finding Detail",
          disabled: true
        }
      ],
      severityOptions: [
        { label: "Critical", value: "Critical" },
        { label: "High", value: "High" },
        { label: "Medium", value: "Medium" },
        { label: "Low", value: "Low" },
        { label: "Informational", value: "Informational" }
      ],
      statusChoices: [
        { title: "Open", value: "Open" },
        { title: "Fixed", value: "Fixed" },
        { title: "Won't Fix", value: "Wont Fix" }
      ],
      editButtonDisabled: true,
      editProofPk: null,
      downloadPending: false
    };
  },
  methods: {
    getFinding() {
      this.findingService.getFinding(this.projectId, this.findingId).then((response) => {
        this.finding = response.data;
        if (response.data.user_account === null) {
          this.finding.user_account = {};
        }
      });
    },
    getProofs() {
      this.findingService.getProofs(this.projectId, this.findingId).then((response) => {
        this.proofs = response.data.results;
      });
    },
    deleteFinding() {
      this.findingService.deleteFinding(this.projectId, this.findingId).then(() => {
        this.$toast.add({ severity: "info", summary: "Confirmed", detail: "Finding deleted!", life: 3000 });
        this.$router.push({ name: "FindingList", params: { projectId: this.projectId } });

      });
    },
    patchFindingData(data) {
      this.findingService.patchFinding(this.$api, this.projectId, this.findingId, data).then((response) => {
        this.finding = response.data;
        if (response.data.user_account === null) {
          this.finding.user_account = {};
        }
      });
    },
    confirmDialogDelete() {
      this.$confirm.require({
        message: "Do you want to delete this finding?",
        header: "Delete Confirmation",
        icon: "fa fa-trash",
        acceptClass: "p-button-danger",
        accept: () => {
          this.deleteFinding();
        }
      });
    },
    onProofSelect(event) {
      if (event.length === 1) {
        this.editButtonDisabled = false;
        this.editProofPk = event[0].pk;
      } else {
        this.editButtonDisabled = true;
      }
    },
    onEditButtonClick() {
      this.$router.push({
        name: "FindingProofUpdate",
        params: {
          projectId: this.projectId,
          findingId: this.findingId,
          proofId: this.editProofPk
        }
      });
    },
    forceFileDownload(response, title) {
      let blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", title);
      link.click();
      this.downloadPending = false;
    },
    downloadAsPDF() {
      this.downloadPending = true;
      this.findingService.downloadAsPDF(this.$api, this.projectId, this.findingId).then((response) => {
        const filename = "finding_" + this.finding.internal_id + ".pdf";
        this.forceFileDownload(response, filename);
      }).finally(() => {
        this.downloadPending = false;
      });
    },
    reorderProofs(event) {
      event.value.forEach((item, index) => {
        let data = { order: index + 1 };
        this.findingService.patchProof(this.$api, this.projectId, this.findingId, item.pk, data);
      });
    }
  },
  components: { FindingTabMenu, DetailCardWithIcon, InfoCardWithForm, FindingAsAdvisoryDialog }
};
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
        <strong class="text-lg" v-if="finding.vulnerability">{{ finding.vulnerability.name }} / {{ finding.name
          }}</strong>
      </div>
    </div>
    <div class="col-6 h-full">
      <div class="flex justify-content-end">
        <Button label="Download" outlined icon="fa fa-download" :loading="downloadPending" :disabled="downloadPending"
                @click="downloadAsPDF"></Button>
        <FindingAsAdvisoryDialog></FindingAsAdvisoryDialog>
        <Button outlined icon="fa fa-pen-to-square" label="Edit"
                @click="this.$router.push({name: 'FindingUpdate', params: {projectId: this.projectId, findingId: this.findingId}})"
        ></Button>
        <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
      </div>
    </div>
  </div>

  <div class="grid">
    <div class="col-12">
      <FindingTabMenu class="surface-card"></FindingTabMenu>
      <Card>
        <template #content>
          <div class="grid">
            <div class="col-12 md:col-4">
              <DetailCardWithIcon title="Asset" icon="fa-crosshairs" class="surface-ground"
                                  :text="finding.component.name">
              </DetailCardWithIcon>
            </div>
            <div class="col-12 md:col-4">
              <DetailCardWithIcon title="User Account" icon="fa-user" class="surface-ground"
                                  :text="finding.user_account.username || '-'"></DetailCardWithIcon>
            </div>
            <div class="col-12 md:col-4">
              <DetailCardWithIcon title="Status" icon="fa-bookmark" class="surface-ground"
                                  :text="finding.status"></DetailCardWithIcon>
            </div>
          </div>
          <div class="grid">
            <div class="col-12 md:col-3">
              <InfoCardWithForm class="surface-ground w-full" title="Status" icon="fa-bookmark">
                <Dropdown v-model="finding.status" :options="statusChoices" optionValue="value"
                          @change="patchFindingData({ status: finding.status })" optionLabel="title"
                          class="w-full">
                </Dropdown>
              </InfoCardWithForm>
            </div>
            <div class="col-12 md:col-3">
              <InfoCardWithForm class="surface-ground" title="Finding Date" icon="fa-calendar">
                <Calendar v-model="finding.finding_date"
                          @change="patchFindingData({ finding_date: finding.finding_date })"></Calendar>
              </InfoCardWithForm>
            </div>
            <div class="col-12 md:col-3">
              <InfoCardWithForm class="surface-ground" title="Severity" icon="fa-attention">
                <Dropdown v-model="finding.severity" :options="severityOptions" optionLabel="label"
                          @change="patchFindingData({ severity: finding.severity })" optionValue="value">
                </Dropdown>
              </InfoCardWithForm>
            </div>
            <div class="col-12 md:col-3">
              <InfoCardWithForm class="surface-ground" title="Needs review?" icon="fa-user-tag">
                <InputSwitch v-model="finding.needs_review"
                             @change="patchFindingData({ needs_review: finding.needs_review })"></InputSwitch>
              </InfoCardWithForm>
            </div>
          </div>
          <div class="grid mt-3">
            <div class="col-6">
              <div class="justify-content-start flex"></div>
            </div>
            <div class="col-6">
              <div class="justify-content-end flex">
                <Button :disabled="editButtonDisabled" label="Edit Proof" icon="fa fa-pen-to-square"
                        outlined @click="onEditButtonClick"></Button>
                <Button label="Proof" icon="fa fa-plus" outlined
                        @click="this.$router.push({ name: 'FindingProofCreate', params: { projectId: this.projectId, findingId: this.findingId } })"></Button>
              </div>
            </div>
          </div>
          <div class="grid">
            <div class="col-12">
              <OrderList v-model="proofs" listStyle="height:auto" dataKey="pk" @reorder="reorderProofs"
                         @update:selection="onProofSelect">
                <template #header>Proofs</template>
                <template #item="slotProps">
                  {{ slotProps.item.title }}
                </template>
              </OrderList>
            </div>

          </div>
        </template>
      </Card>
    </div>
  </div>
</template>