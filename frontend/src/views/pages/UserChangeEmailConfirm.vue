<script>
export default {
    name: 'UserChangeEmailConfirm',

    methods: {
        change_email_confirm() {
            let data = {
                uid: this.$route.params.uid,
                token: this.$route.params.token
            };
            this.$api
                .post('/users/change_email_confirm/', data)
                .then(() => {})
                .finally(() => {
                    this.$router.push({
                        name: 'UserProfileSettings'
                    });
                });
        }
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12 md:col-6 md:col-offset-3">
            <Card>
                <template #title>Confirm Email</template>
                <template #content>
                    <Button @click="change_email_confirm" outlined>Submit</Button>
                </template>
            </Card>
        </div>
    </div>
</template>