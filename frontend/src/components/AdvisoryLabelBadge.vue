<template>
  <span class="severity-badge" :style="getStyle">{{ this.label.name }}</span>
</template>

<script>
export default {
  name: "SeverityBadge",
  props: {
    label: {
      required: true
    }
  },
  computed: {
    getClasses() {
      return "severity-badge";
    },
    getStyle() {
      let r = "--label-r: " + this.label.color_rgb[0] + ";";
      let g = "--label-g: " + this.label.color_rgb[1] + ";";
      let b = "--label-b: " + this.label.color_rgb[2] + ";";
      let h = "--label-h: " + this.label.color_hsl[0] + ";";
      let s = "--label-s: " + this.label.color_hsl[1] + ";";
      let l = "--label-l: " + this.label.color_hsl[2] + ";";
      return r + g + b + h + s + l;
    }
  }
}
</script>
