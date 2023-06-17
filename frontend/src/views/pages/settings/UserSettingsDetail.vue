<script>
export default {
    name: 'UserSettingsDetail',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Settings',
                    disabled: true
                }
            ],
            model: {}
        }
    },
    methods: {
        getItem(){
            let url = "/users/user-settings/"
            this.$api.get(url).then((response) => {
                this.model = response.data
            })
        },
        patch(){
            let url = "/users/user-settings/"
            this.$api.patch(url, this.model).then((response) => {
                this.model = response.data
                this.$toast.add({
                    severity: 'success',
                    summary: 'Updated',
                    detail: 'Settings were updated successfully!',
                    life: 3000
                })
            })
        }
    },
    mounted(){
        this.getItem()
    }
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
                <div class="flex flex-column gap-2">
                    <div class="flex align-items-center">
                        <Checkbox v-model="model.show_real_name_in_report"
                            id="show_real_name_in_report" binary
                           />
                        <label for="show_real_name_in_report" class="ml-2"> Show real name in report? </label>
                    </div>
                </div>
                <div class="flex justify-content-end mt-3">
                    <Button @click="patch" label="Save"></Button>
                </div>
            </div>
        </div>
    </div>
</template>