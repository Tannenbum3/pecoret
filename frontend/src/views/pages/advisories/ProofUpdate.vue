<script>
import AdvisoryService from '../../../service/AdvisoryService'
import MarkdownEditor from "@/components/elements/forms/MarkdownEditor.vue";


export default {
  name: 'ProofCreate',
  data() {
    return {
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
          to: this.$router.resolve({
            name: "AdvisoryProofList",
            params: {
              advisoryId: this.$route.params.advisoryId
            }
          })
        },
        {
          label: "Update",
          disabled: true
        }
      ],
      service: new AdvisoryService(),
      advisoryId: this.$route.params.advisoryId,
      proofId: this.$route.params.proofId,
      model: {
        title: null,
        image: null,
        image_caption: null,
        text: "",
      }
    }
  },
  mounted() {
    this.getProof()
  },
  methods: {

    getProof() {
      this.service.getProof(this.$api, this.advisoryId, this.proofId).then((response) => {
        this.model.title = response.data.title
        this.model.image_caption = response.data.image_caption
        this.model.text = response.data.text
      })
    },
    getFileObject(event) {
      this.model.image = event.files[0]
    },
    confirmDialogDelete(id) {
      this.$confirm.require({
        message: 'Do you want to remove this proof?',
        header: 'Delete confirmation',
        icon: "fa fa-trash",
        acceptClass: 'p-button-danger',
        accept: () => {
          this.service.deleteProof(this.$api, this.advisoryId, this.proofId).then(() => {
            this.$toast.add({
              severity: 'success',
              summary: 'Deleted',
              detail: 'Proof was deleted successfully!',
              life: 3000
            })
          })
          this.$router.push({
            name: 'AdvisoryProofList',
            params: {
              advisoryId: this.advisoryId,
            }
          })
        }
      })
    },
    createProof() {
      let data = {}
      if (this.model.image) {
        data = new FormData()
        data.append("image", this.model.image)
        data.append("image_caption", this.model.image_caption);
        data.append("text", this.model.text);
        data.append("title", this.model.title);
      } else {
        data = {
          title: this.model.title,
          text: this.model.text
        }
      }
      this.service.patchProof(this.$api, this.advisoryId, this.proofId, data).then(() => {
        this.$toast.add({
          severity: 'success',
          summary: 'Updated',
          detail: 'Proof was updated successfully!',
          life: 3000
        })
        this.$router.push({name: 'AdvisoryProofList', params: {advisoryId: this.advisoryId}})
      })
    }
  },
  components: {MarkdownEditor}
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
        <Button label="Delete" icon="fa fa-trash" outlined severity="danger" @click="confirmDialogDelete"></Button>
      </div>
    </div>
  </div>

  <div class="grid">
    <div class="col-12">
      <div class="card">
        <div class="p-fluid formgrid grid">
          <div class="field col-12">
            <label for="title">Title</label>
            <InputText id="title" v-model="model.title"></InputText>
          </div>
          <div class="field col-12">
            <label>Text</label>
            <MarkdownEditor v-model="model.text"></MarkdownEditor>
          </div>
          <div class="field col-12">
            <label for="image">Image</label>
            <FileUpload accept="image/*" mode="basic" id="image" @select="this.getFileObject"></FileUpload>
          </div>
          <div class="field col-12">
            <label for="caption">Image Caption</label>
            <InputText id="caption" v-model="model.image_caption"></InputText>
          </div>
        </div>
        <div class="flex justify-content-end mt-3">
          <Button @click="createProof" label="Save"></Button>
        </div>
      </div>
    </div>
  </div>
</template>