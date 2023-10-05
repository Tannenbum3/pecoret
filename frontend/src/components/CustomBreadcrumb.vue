<script>
export default {
    name: "CustomBreadcrumb",
    props: {
        modelValue: {
            required: true
        }
    }
};
</script>

<template>
    <Breadcrumb :model="modelValue">
        <template #item="{ label, item, props }">
            <router-link v-if="item.route" :to="item.route" v-bind="props.action">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                <span v-if="item.icon" v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
            </a>
        </template>
    </Breadcrumb>
</template>

<style scoped>

</style>