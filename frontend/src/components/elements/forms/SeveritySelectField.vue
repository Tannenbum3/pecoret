<script>
export default {
    name: "SeveritySelectField",
    props: ["modelValue"],
    emits: ["update:modelValue"],
    methods: {
        change() {
            this.$emit("update:modelValue", this.model)
        }
    },
    data() {
        return {
            model: this.modelValue,
            choices: [
                { name: "Critical", value: "Critical" },
                { name: "High", value: "High" },
                { name: "Medium", value: "Medium" },
                { name: "Low", value: "Low" },
                { name: "Informational", value: "Informational" }
            ],
        }
    }
}
</script>

<template>
    <label for="severity">Severity</label>
    <Dropdown @change="change" v-model="this.model" :options="choices" optionLabel="name" optionValue="value"
        class="w-full"></Dropdown>
</template>
  