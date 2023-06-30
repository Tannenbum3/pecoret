<template>
  <div class="vue-simplemde border-0 border-round">
    <textarea class="vue-simplemde-textarea p-3" :name="name" :value="modelValue"
              @blur="this.$emit('blur')"
              @input="handleInput($event.target.value)"/>
  </div>
</template>

<script>
/*
Original source which only support vue2
https://raw.githubusercontent.com/F-loat/vue-simplemde/master/src/index.vue
*/
import EasyMDE from 'easymde';
import markdown from '@/utils/markdown'

export default {
  name: 'MarkdownEditor',
  props: {
    value: String,
    modelValue: String,
    label: String,
    name: String,
    autoinit: {
      type: Boolean,
      default() {
        return true;
      },
    },
    forceSync: {
      type: Boolean,
      default() {
        return true;
      },
    },
    highlight: {
      type: Boolean,
      default() {
        return true;
      },
    },
    sanitize: {
      type: Boolean,
      default() {
        return true;
      },
    },
    configs: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  emits: ['blur', "update:modelValue", "input"],
  data() {
    return {
      isValueUpdateFromInner: false,
    };
  },
  mounted() {
    if (this.autoinit) this.initialize();
  },
  deactivated() {
    const editor = this.simplemde;
    if (!editor) return;
    const isFullScreen = editor.codemirror.getOption('fullScreen');
    if (isFullScreen) editor.toggleFullScreen();
  },
  methods: {
    initialize() {
      const configs = Object.assign({
        element: this.$el.firstElementChild,
        initialValue: this.modelValue || this.value,
        previewRender: (plaintext) => {
          // use markdown-it and sanatize values to prevent XSS
          // the default copy&pasted code from the docs rendered `<img src=/X onerror=alert(document.domain)>`
          return markdown.renderMarkdown(plaintext)
        },
        renderingConfig: {},
        promptURLs: false,
        uploadImage: false,
        hideIcons: ["guide", "image", "fullscreen", "side-by-side"],
        imagesPreviewHandler: (src) => {
          console.log(src)
        },
        imageUploadFunction: (file, onSuccess, onError) => {
          const reader = new FileReader();
          reader.onload = () => onSuccess(reader.result);
          reader.onerror = () => onError(`Error loading ${file.name}`);
          reader.readAsDataURL(file);
        },
      }, this.configs);

      if (configs.initialValue) {
        this.$emit('update:modelValue', configs.initialValue);
      }

      if (this.highlight) {
        configs.renderingConfig.codeSyntaxHighlighting = true;
      }

      this.simplemde = new EasyMDE(configs);

      const className = this.previewClass || '';

      this.bindingEvents();

      this.$nextTick(() => {
        this.$emit('initialized', this.simplemde);
      });
    },
    bindingEvents() {
      this.simplemde.codemirror.on('change', (instance, changeObj) => {
        if (changeObj.origin === 'setValue') {
          return;
        }
        const val = this.simplemde.value();
        this.handleInput(val);
      });

      this.simplemde.codemirror.on('blur', () => {
        const val = this.simplemde.value();
        this.handleBlur(val);
      });
    },
    addPreviewClass(className) {
      const wrapper = this.simplemde.codemirror.getWrapperElement();
      const preview = document.createElement('div');
      wrapper.nextSibling.className += ` ${className}`;
      preview.className = `editor-preview ${className}`;
      wrapper.appendChild(preview);
    },
    handleInput(val) {
      this.isValueUpdateFromInner = true;
      this.$emit('update:modelValue', val);
      this.$emit('input', val);
    },
    handleBlur(val) {
      this.isValueUpdateFromInner = true;
      this.$emit('blur', val);
    },
  },
  unmounted() {
    this.simplemde = null;
  },
  watch: {
    modelValue(val) {
      if (!this.forceSync && this.isValueUpdateFromInner) {
        this.isValueUpdateFromInner = false;
      } else {
        const pos = this.simplemde.codemirror.getCursor();
        this.simplemde.value(val);
        this.simplemde.codemirror.setSelection(pos);
      }
    },
  },
};
</script>

<style>
@import '@/../node_modules/easymde/dist/easymde.min.css';


.CodeMirror {
  background: var(--surface-b) !important;
  color: inherit !important;
  border: 1px solid var(--surface-border) !important;
}

.editor-preview {
  background: var(--surface-b) !important;
  color: inherit !important;

}

.editor-toolbar button:hover {
  background-color: var(--surface-c) !important;

}

.editor-toolbar {
  border-top: 1px solid var(--surface-border);
  border-left: 1px solid var(--surface-border);
  border-right: 1px solid var(--surface-border);
}

.CodeMirror-cursor {
  border-left: 1px solid var(--text-color);
}

.editor-toolbar button.active, .editor-toolbar button:hover {
  background-color: var(--surface-c);
  color: var(--text-color);
}

.CodeMirror .cm-spell-error:not(.cm-url):not(.cm-comment):not(.cm-tag):not(.cm-word) {
  background: inherit !important;
}

.editor-preview pre {
  background: var(--surface-a);
  padding: 1em;
}
</style>
  