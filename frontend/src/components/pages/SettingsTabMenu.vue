<script>
export default {
    name: "SettingsTabMenu",
    data() {
        return {
            items: [
                {
                    label: "General & Notifications",
                    to: this.$router.resolve({
                        name: "UserSettingsDetail"
                    })
                },
                {
                    label: "Profile",
                    to: this.$router.resolve({
                        name: "UserProfileSettings"
                    })
                },
            ]
        };
    }
};
</script>

<template>
    <TabMenu :model="items"></TabMenu>
</template>