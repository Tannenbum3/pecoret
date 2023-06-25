<script>
import FindingService from '@/service/FindingService'


export default {
  name: "FindingCopyDialog",
  emits: ["object-created"],
  props: {
    finding: {
      required: true
    }
  },
  data() {
    return {
      visible: false,
      projectId: this.$route.params.projectId,
      model: {
        name: null,
      },
      service: new FindingService()
    };
  },
  methods: {
    close() {
      this.visible = false;
    },
    open() {
      this.visible = true;
    },
    create() {
      let data = {
        name: this.model.name,
      }
      this.service.copyFinding(this.$api, this.projectId, this.finding, data).then((response) => {
        this.$toast.add({
          severity: "success",
          summary: "Finding copied!",
          life: 3000,
          detail: "Finding copied successfully!"
        });
        this.$emit("object-created", response.data);
        this.visible = false;
      });
    }
  },
}
</script>

<template>
  <Button icon="fa fa-copy" outlined @click="open"></Button>

  <Dialog header="Copy Finding" v-model:visible="visible" modal :style="{ width: '70vw' }">
    <div class="grid formgrid p-fluid">
      <div class="col-12 field">
        <label for="name">Name</label>
        <InputText id="name" v-model="model.name"></InputText>
      </div>
    </div>

    <template #footer>
      <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
      <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
    </template>
  </Dialog>
</template>