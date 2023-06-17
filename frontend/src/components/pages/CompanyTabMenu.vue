<script>
export default {
    name: 'CompanyTabMenu',
    data(){
        return {
            items: [
                {
                    label: 'Details',
                    to: this.$router.resolve({
                        name: 'CompanyDetail',
                        params: {
                            companyId: this.$route.params.companyId
                        }
                    })
                },
                {
                    label: 'Contacts',
                    to: this.$router.resolve({
                        name: 'CompanyContactList',
                        params: {
                            companyId: this.$route.params.companyId
                        }
                    })
                },
            ]
        }
    }
}
</script>

<template>
    <TabMenu :model="items"></TabMenu>
</template>