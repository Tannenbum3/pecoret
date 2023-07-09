<script>
import { defineComponent } from "vue";
import FindingService from "@/service/FindingService";
import DetailCardWithIcon from "@/components/DetailCardWithIcon.vue";

export default defineComponent({
  name: "DashboardFindingsCount",
  components: { DetailCardWithIcon },
  data() {
    return {
      service: new FindingService(),
      model: {},
      projectId: this.$route.params.projectId
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
      this.service.getFindings(this.$api, this.projectId).then((response) => {
        this.model.count = response.data.count;
      });
    }
  }
});
</script>

<template>
  <DetailCardWithIcon title="Findings" :text="model.count" icon="fa fa-bugs" styleClass="">
  </DetailCardWithIcon>
</template>

<style scoped>

</style>