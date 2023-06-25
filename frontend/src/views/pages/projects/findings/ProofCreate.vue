<script>
import FindingService from '@/service/FindingService'
import ToastUIEditor from '@/components/elements/forms/ToastUIEditor.vue'


export default {
  name: 'ProofCreate',
  data() {
    return {
      breadcrumbs: [
        {
          label: "Findings",
          to: this.$router.resolve({
            name: "FindingList",
            params: {
              projectId: this.$route.params.projectId
            }
          })
        },
        {
          label: "Finding Detail",
          to: this.$router.resolve({
            name: "FindingDetail",
            params: {
              projectId: this.$route.params.projectId
            }
          })
        },
        {
          label: "Create",
          disabled: true
        }
      ],
      service: new FindingService(),
      projectId: this.$route.params.projectId,
      findingId: this.$route.params.findingId,
      model: {
        title: null,
        image: null,
        image_caption: null,
        text: "",
      }
    }
  },
  methods: {
    getFileObject(event) {
      this.model.image = event.files[0]
    },
    createProof() {
      let data = {}
      if (this.model.image) {
        data = new FormData()
        data.append("image", this.model.image)
        data.append("image_caption", this.model.image_caption)
        data.append("text", this.model.text)
        data.append("order", 1)
        data.append("title", this.model.title)
      } else {
        data = {
          title: this.model.title,
          order: 1,
          text: this.model.text
        }
      }
      this.service.createProof(this.$api, this.projectId, this.findingId, data).then(() => {
        this.$toast.add({
          severity: 'success',
          summary: 'Created',
          detail: 'Proof was created successfully!',
          life: 3000
        })
        this.$router.push({name: 'FindingDetail', params: {projectId: this.projectId, findingId: this.findingId}})
      })
    }
  },
  components: {ToastUIEditor}
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
      <div class="card">
        <div class="grid formgrid p-fluid">
          <div class="col-12 field">
            <label for="title">Title</label>
            <InputText id="title" v-model="model.title"></InputText>
          </div>
          <div class="col-12 field">
            <ToastUIEditor v-model="model.text" label="Text"></ToastUIEditor>
          </div>
          <div class="col-12 field md:col-6">
            <label for="image">Image</label>
            <FileUpload accept="image/*" mode="basic" id="image" @select="this.getFileObject"></FileUpload>
          </div>
          <div class="col-12 field md:col-6">
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