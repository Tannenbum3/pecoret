<template>
    <div class="mb-4">
      <label v-if="label">{{ label }}</label>
      <div ref="editor" @load="onEditorLoad"></div>
    </div>
  </template>
  
  <script>
  import Editor from '@toast-ui/editor';
  import '@toast-ui/editor/dist/toastui-editor.css';
  import '@toast-ui/editor/dist/theme/toastui-editor-dark.css'
  
  export default {
    name: "ToastUIEditor",
    props: {
      modelValue: {
        type: String,
        required: false,
        default: ''
      },
      editorSize: {
        type: String,
        required: false,
        default: '500px'
      },
      label: {
        type: String,
        required: false
      }
  
    },
    data() {
      return {
        toastuiEditor: null,
      }
    },
    emits: ["update:modelValue", "editorBlur"],
    methods: {
      onEditorLoad() {
        //editor.setMarkdown('test', true)
      },
      onChange(){
        this.$emit('update:modelValue', this.toastuiEditor.getMarkdown())
      },
    },
    mounted() {
      this.toastuiEditor = new Editor({
        el: this.$refs.editor,
        height: this.editorSize,
        initialEditType: 'markdown',
        initialValue: this.modelValue,
        useStatistics: false,
        hideModeSwitch: true,
        autofocus: false,
        theme: 'dark',
        previewStyle: 'tab',
        toolbarItems: [
          ['heading', 'bold', 'italic', 'strike'],
          ['hr', 'quote'],
          ['ul', 'ol', 'task', 'indent', 'outdent'],
          ['table', 'image', 'link'],
          ['code', 'codeblock'],
        ],
        events: {
          change: () => this.$emit('update:modelValue', this.toastuiEditor.getMarkdown()),
          blur: () => this.$emit("editorBlur", this.toastuiEditor.getMarkdown())
        }
      })
    }
  }
  </script>
  
  <style>
  .toastui-editor-main {
    color: var(--text-color);
  }
  
  .toastui-editor-md-container {
    background: var(--surface-b) !important;

  }

  .toastui-editor-dark.toastui-editor-defaultUI {
    border-color: var(--surface-border);
  }

  
  .toastui-editor-defaultUI-toolbar {
    background-color: rgba(var(--surface-ground)) !important;
  }
  
  .toastui-editor-md-tab-container {
      background-color: rgba(var(--surface-ground)) !important;
  }

  .toastui-editor-md-tab-container .tab-item {
    background-color: var(--surface-ground) !important;
  }

  .toastui-editor-md-tab-container .tab-item.active {
    background-color: var(--surface-card) !important;
  }
</style>
  