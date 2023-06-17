<script>
import AdvisoryService from '@/service/AdvisoryService'


export default {
    name: "AdvisoryMembershipCreateDialog",
    emits: ["object-created"],
    data() {
        return {
            visible: false,
            advisoryId: this.$route.params.advisoryId,
            model: {
                email: null,
                role: null,
                active_until: null
            },
            roleChoices: [
                { label: "Read Only", value: "Read Only" },
                { label: "Creator", value: "Creator" },
                { label: "Vendor", value: "Vendor" }
            ],
            service: new AdvisoryService()
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
                email: this.model.email,
                role: this.model.role.value,
                active_until: this.model.active_until
            }
            this.service.createMembership(this.$api, this.advisoryId, data).then((response) => {
                this.$toast.add({
                    severity: "success",
                    summary: "Member added!",
                    life: 3000,
                    detail: "New member was addedd to advisory!"
                });
                this.$emit("object-created", response.data);
                this.visible = false;
            });
        }
    },
}
</script>

<template>
    <Button icon="fa fa-plus" label="Membership" outlined @click="open"></Button>

    <Dialog header="Create Membership" v-model:visible="visible" modal :style="{ width: '70vw' }">
        <div class="flex flex-column gap-2">
            <label for="email">E-Mail</label>
            <InputText id="email" type="email" v-model="model.email"></InputText>
        </div>
        <div class="flex flex-column gap-2">
            <label for="role">Role</label>
            <Dropdown id="role" v-model="model.role" :options="roleChoices" optionLabel="label" class="w-full"></Dropdown>
        </div>
        <div class="flex flex-column gap-2">
            <label for="active_until">Active Until</label>
            <Calendar showTime timeFormat="24" v-model="model.active_until"></Calendar>
        </div>

        <template #footer>
            <Button label="Cancel" @click="close" class="p-button-outlined"></Button>
            <Button label="Save" @click="create" icon="pi pi-check" class="p-button-outlined"></Button>
        </template>
    </Dialog>
</template>