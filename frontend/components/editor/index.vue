<template>
  <div class="form-group">
    <!-- Title -->
    <div class="m-b-10">
      <label
        v-if="label"
        class="editor-label no-margin"
        :for="id"
        v-html="label"
      />

      <p class="no-margin small hint-text font-arial">
        {{ description }}
      </p>
    </div>

    <!-- Toolbar -->
    <template v-if="editor && !disabled">
      <CompactToolbar v-if="compact" :editor="editor" :set-link="setLink" />
      <RegularToolbar v-else :editor="editor" :set-link="setLink" />
    </template>

    <!-- Content -->
    <EditorContent
      class="tip-tap-editor"
      :editor="editor"
      :class="{ disabled: disabled }"
    />
  </div>
</template>

<script>
import StarterKit from '@tiptap/starter-kit';
import { Editor, EditorContent } from '@tiptap/vue-3';

// tiptap-extensions
import Underline from '@tiptap/extension-underline';
import TextAlign from '@tiptap/extension-text-align';
import Link from '@tiptap/extension-link';
import TextStyle from '@tiptap/extension-text-style';
import Image from '@tiptap/extension-image';
import FontSize from '@/utils/tiptap-fontsize';
import { Color } from '@tiptap/extension-color';

// components
import CompactToolbar from '@/components/editor/CompactToolbar.vue';
import RegularToolbar from '@/components/editor/RegularToolbar.vue';

export default {
  name: 'PgEditor',
  components: {
    EditorContent,
    CompactToolbar,
    RegularToolbar,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
    modelValue: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: '',
    },
    name: {
      type: String,
      default: '',
    },
    required: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    description: {
      type: String,
      default: '',
    },
    maxUploadSize: {
      type: Number,
      default: 5 * 1024 * 1024,
    },
    uploadImage: {
      type: Function,
      required: true,
    },
    deleteImage: {
      type: Function,
      required: true,
    },
    compact: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      editor: null,
      fontsize: '16px',
      fontSizeOptions: [
        '14px',
        '16px',
        '18px',
        '20px',
        '24px',
        '28px',
        '32px',
        '36px',
        '48px',
      ],
      editorOptions: {
        modules: {
          clipboard: {
            matchVisual: false,
          },
          toolbar: {
            container: '#toolbar',
            handlers: {
              custom: this.toggleDropdown,
            },
          },
        },
      },
    };
  },
  watch: {
    disabled(val) {
      this.editor.setOptions({ editable: !val });
    },
    modelValue(value) {
      // HTML
      const isSame = this.editor.getHTML() === value;

      if (isSame) {
        return;
      }

      this.editor.commands.setContent(value, false);
    },
  },
  mounted() {
    this.editor = new Editor({
      content: this.modelValue,
      onUpdate: () => {
        this.$emit('update:modelValue', this.editor.getHTML());
      },
      extensions: [
        StarterKit,
        Underline,
        TextAlign.configure({
          types: ['heading', 'paragraph'],
        }),
        Link.configure({
          autolink: false,
          openOnClick: false,
        }),
        TextStyle,
        Color,
        Image,
        FontSize,
      ],
      editable: !this.disabled,
    });

    this.editor.commands.setColor('575757ff');
  },

  beforeUnmount() {
    this.editor.destroy();
  },
  methods: {
    setLink() {
      const previousUrl = this.editor.getAttributes('link').href;
      const url = window.prompt('URL', previousUrl);

      // cancelled
      if (url === null) {
        return;
      }

      // empty
      if (url === '') {
        this.editor.chain().focus().extendMarkRange('link').unsetLink().run();

        return;
      }

      // update link
      this.editor
        .chain()
        .focus()
        .extendMarkRange('link')
        .setLink({ href: url })
        .run();
    },
  },
};
</script>

<style>
.toolbar {
  border: 1px solid rgba(0, 0, 0, 0.07) !important;
  flex-wrap: wrap;
  background-color: white;
  align-items: center;
}

.toolbar > span {
  width: auto !important;
  margin-left: 8px !important;
  padding: 6px 3px;
  font-weight: 700;
  cursor: pointer;
  user-select: none;
}

.image-uploader__hidden {
  display: none;
}

.font-size__selector {
  border: none;
  cursor: pointer;
  background: transparent;
  font-size: 14px;
  color: #575757;
}

.ProseMirror {
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.07) !important;
  min-height: 28vh !important;
  margin-bottom: 1vh !important;
  padding: 12px 8px !important;
}

.ProseMirror:focus {
  outline: none;
}

.disabled {
  background-color: #f3f3f3;
}

.disabled span {
  background-color: #f3f3f3;
}

.disabled .ProseMirror {
  background-color: #f3f3f3;
}

.variable-dropdown {
  position: absolute;
  top: 250px;
  min-width: 100px;
  max-height: 200px;
  overflow: auto;
  border: 1px solid rgba(0, 0, 0, 0.07);
  border-radius: 2px;
  display: flex;
  flex-direction: column;
  background-color: white;
  z-index: 1;
  width: max-content;
  max-width: 300px;
}

.ProseMirror a {
  color: blue;
  text-decoration: underline;
  font-style: italic;
}

.ProseMirror p,
.ProseMirror p span {
  line-height: 150% !important;
}

.icon-variable {
  display: flex;
  width: max-content;
  gap: 4px;
  align-items: center;
}

.icon-variable svg {
  width: 28px;
  height: 28px;
}

span.ql-custom {
  position: relative;
  top: -4px;
}

.option:hover {
  background-color: rgba(0, 0, 0, 0.07);
}

span.option {
  width: 100%;
  cursor: pointer;
  height: max-content;
  padding: 8px;
}

.toolbar {
  display: flex;
  padding: 4px 4px;
}

.toolbar h6 {
  font-weight: 500;
  opacity: 0.9;
  font-size: 14px;
  margin-top: 2px;
}

.editor-tiptap label {
  font-weight: 700;
  font-family: 'Montserrat';
  font-size: 11px;
  letter-spacing: 0.06em;
  margin-bottom: 1vh !important;
  text-transform: uppercase;
}
.editor-tiptap label::after {
  color: #f55753;
  content: '*';
  font-family: arial;
  font-size: 1px;
}
.is-active {
  color: blue;
}
.header-tools {
  font-size: 14px;
}
.form-group label:not(.error) {
  font-weight: 700;
}

.form-group.required-label::after {
  color: #f55753;
  content: '*';
  font-family: arial;
  font-size: 15px;
}

.editor-label {
  text-transform: capitalize;
}
.hide-color-picker {
  opacity: 0;
  width: 0;
  margin: -8px;
  pointer-events: none;
}

.ProseMirror img {
  display: block;
  margin: 0 auto;
  max-width: 100%;
  width: fit-content;
  object-fit: cover;
}

.tip-tap-editor {
  max-height: 400px;
  overflow-y: auto;
}

.editor-options-divider {
  background: #575757;
  opacity: 0.4;
  width: 1px;
  height: 22px;
  margin-left: 10px;
  user-select: none;
}

.editor-group-toggle {
  position: relative;
}

.editor-group {
  display: block;
  position: absolute;
  background: #ffffff;
  font-size: 14px;
  box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.08),
    0px 12px 24px 0px rgba(0, 0, 0, 0.04);
  border-radius: 4px;
  top: 30px;
  left: 55%;
  transform: translate(-45%, 0);
  color: #575757;
  z-index: 5;
  max-height: 200px;
  overflow-y: auto;
  min-width: max-content;
}

.editor-group-item {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  user-select: none;
  font-size: 12px;
}

.dropdown-toggle-icons {
  gap: 5px;
  align-items: center;
}

/* This CSS is being used for spacing issue for Firefox browser */
.ProseMirror * {
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
}
</style>
