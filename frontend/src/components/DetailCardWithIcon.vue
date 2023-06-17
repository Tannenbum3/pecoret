<script>
export default {
    name: 'DetailCardWithIcon',
    props: {
        title: {
            required: true
        },
        icon: {
            required: true
        },
        text: {
            required: true
        }
    }
}
</script>

<template>
    <div class="card mb-0 h-full">
        <div class="flex justify-content-between mb-3">
            <div>
                <span class="block text-500 font-medium mb-3">{{ title }}</span>
                <div class="text-900 font-medium text-xl">{{ text }}</div>
            </div>
            <div class="flex align-items-center justify-content-center bg-blue-100 border-round"
                style="width: 2.5rem; height: 2.5rem">
                <i class="fa text-blue-500 text-xl" :class="icon"></i>
            </div>
        </div>
    </div>
</template>