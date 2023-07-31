<script>
import UserAccountService from "@/service/UserAccountService";
import MarkdownEditor from "@/components/elements/forms/MarkdownEditor.vue";

export default {
  name: "UserAccountCreateDialog",
  emits: ["object-created"],
  data() {
    return {
      visible: false,
      projectId: this.$route.params.projectId,
      model: {
        username: null,
        password: null,
        role: null,
        compromised: false,
        description: ""
      },
      accountService: new UserAccountService()
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
        username: this.model.username,
        password: this.model.password,
        role: this.model.role,
        compromised: this.model.compromised,
        description: this.model.description
      };
      this.accountService.createAccount(this.$api, this.projectId, data).then((response) => {
        this.$toast.add({
          severity: "success",
          summary: "Account added!",
          life: 3000,
          detail: "Account added to project!"
        });
        this.$emit("object-created", response.data);
        this.visible = false;
      });
    }
  },
  components: { MarkdownEditor }
};
</script>

<template>
  <Button icon="fa fa-plus" label="Account" outlined @click="open"></Button>

  <Dialog header="Create Account" v-model:visible="visible" modal :style="{ width: '70vw' }">
    <div class="grid formgrid p-fluid">
      <div class="field col-12">
        <label for="username">Username</label>
        <InputText id="username" v-model="model.username"></InputText>
      </div>
      <div class="field col-12">
        <label for="password">Password</label>
        <Password id="password" v-model="model.password" :feedback="false" toggleMask></Password>
      </div>
      <div class="field col-12">
        <label for="rolel">Role</label>
        <InputText id="role" v-model="model.role"></InputText>
      </div>
      <div class="field col-12">
        <label for="description">Description</label>
        <MarkdownEditor v-model="model.description"></MarkdownEditor>
      </div>
      <div class="field col-12">
        <div class="flex align-items-center">
            <Checkbox v-model="model.compromised" inputId="compromised" :binary="true" />
          <label for="compromised" class="ml-2"> Compromised?</label>
        </div>
      </div>
    </div>

    <template #footer>
      <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
      <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
    </template>
  </Dialog>
</template>