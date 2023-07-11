<script>
import AdvisoryService from '../../../service/AdvisoryService';
import MarkdownEditor from '@/components/elements/forms/MarkdownEditor.vue';

export default {
    name: 'ProofCreate',
    data() {
        return {
            breadcrumbs: [
                {
                    label: 'Advisories',
                    to: this.$router.resolve({
                        name: 'AdvisoryList'
                    })
                },
                {
                    label: 'Advisory Detail',
                    to: this.$router.resolve({
                        name: 'AdvisoryDetail',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Proofs',
                    to: this.$router.resolve({
                        name: 'AdvisoryProofList',
                        params: {
                            advisoryId: this.$route.params.advisoryId
                        }
                    })
                },
                {
                    label: 'Create',
                    disabled: true
                }
            ],
            service: new AdvisoryService(),
            advisoryId: this.$route.params.advisoryId,
            model: {
                title: null,
                image: null,
                image_caption: null,
                text: ''
            }
        };
    },
    methods: {
        getFileObject(event) {
            this.model.image = event.files[0];
        },
        createProof() {
            let data = {};
            if (this.model.image) {
                data = new FormData();
                data.append('image', this.model.image);
                data.append('image_caption', this.model.image_caption);
                data.append('text', this.model.text);
                data.append('order', 1);
                data.append('title', this.model.title);
            } else {
                data = {
                    title: this.model.title,
                    order: 1,
                    text: this.model.text
                };
            }
            this.service.createProof(this.$api, this.advisoryId, data).then(() => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Created',
                    detail: 'Proof was created successfully!',
                    life: 3000
                });
                this.$router.push({ name: 'AdvisoryProofList', params: { advisoryId: this.advisoryId } });
            });
        }
    },
    components: { MarkdownEditor }
};
</script>
<template>
    <div class="grid mt-3">
        <div class="col-12">
            <Breadcrumb :model="breadcrumbs"></Breadcrumb>
        </div>
    </div>

    <div class="grid">
        <div class="col-12">
            <div class="card">
                <div class="formgrid grid p-fluid">
                    <div class="field col-12">
                        <label for="title">Title</label>
                        <InputText id="title" v-model="model.title"></InputText>
                    </div>

                    <div class="field col-12">
                        <label>Text</label>
                        <MarkdownEditor v-model="model.text"></MarkdownEditor>
                    </div>

                    <div class="field col-12">
                        <label for="image">Image</label>
                        <FileUpload accept="image/*" mode="basic" id="image" @select="this.getFileObject"></FileUpload>
                    </div>
                    <div class="field col-12">
                        <label for="caption">Image Caption</label>
                        <InputText id="caption" v-model="model.image_caption"></InputText>
                    </div>
                </div>
                <div class="flex justify-content-end mt-3">
                    <Button @click="createProof" label="Save"></Button>
                </div>
            </div>
        </div>
    </div>
</template>