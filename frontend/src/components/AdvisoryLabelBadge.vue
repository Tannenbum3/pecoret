<template>
  <span class="severity-badge" :style="'background-color:' + this.color">{{ this.name }}</span>
</template>

<script>
export default {
  name: "SeverityBadge",
  props: {
    name: {
      required: true
    },
    color: {
      required: true
    }
  },
  computed: {
    getClasses() {
      return "severity-badge"
    }
  }
}
</script>
