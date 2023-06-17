<script>
export default {
    name: 'ReportTemplateSelectField',
    props: ['modelValue'],
    emits: ['update:modelValue'],
    mounted() {
        this.loadData()
    },
    methods: {
        change(){
            this.$emit('update:modelValue', this.model)
        },
        loadData(){
            let url = "/report-templates/"
            this.$api.get(url).then((response) => {
                this.choices = response.data.results
            })
        }
    },
    data() {
        return {
            model: this.modelValue,
            choices: []
        }
    }
}
</script>
<template>
    <label for="report_template">Report Template</label>
    <Dropdown v-model="model" :options="choices" optionLabel="name"
        @change="change"
        optionValue="pk" id="report_template"></Dropdown>
</template>