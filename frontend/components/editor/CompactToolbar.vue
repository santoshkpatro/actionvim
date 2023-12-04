<template>
  <div v-click-away="out" class="toolbar">
    <!-- Bold -->
    <span
      :class="{ 'is-active': editor.isActive('bold') }"
      @click="editor.chain().focus().toggleBold().run()"
    >
      <i class="fa fa-bold" />
    </span>

    <!-- Italic -->
    <span
      :class="{ 'is-active': editor.isActive('italic') }"
      @click="editor.chain().focus().toggleItalic().run()"
    >
      <i class="fa fa-italic" />
    </span>

    <!-- MORE STYLES -->
    <span
      :class="{ 'is-active': isTextStyleMenuActive }"
      class="editor-group-toggle"
      @click="toggleMenu('isTextStyleMenuExpanded')"
    >
      <i class="fa fa-ellipsis" />
      <div v-show="isTextStyleMenuExpanded" class="editor-group">
        <!-- Underline -->
        <div
          class="editor-group-item"
          @click="editor.chain().focus().toggleUnderline().run()"
        >
          <span class="group-item-name">Underline</span>
          <span :class="{ 'is-active': editor.isActive('underline') }">
            <i class="fa fa-underline" />
          </span>
        </div>

        <!-- Strikethrough -->
        <div
          class="editor-group-item"
          @click="editor.chain().focus().toggleStrike().run()"
        >
          <span class="group-item-name">Strikethrough</span>
          <span :class="{ 'is-active': editor.isActive('strike') }">
            <i class="fa fa-strikethrough" />
          </span>
        </div>
      </div>
    </span>

    <div class="editor-options-divider" />

    <!-- LIST STYLE -->
    <span
      :class="{ 'is-active': isListTypeMenuActive }"
      class="editor-group-toggle"
      @click="toggleMenu('isListTypeMenuExpanded')"
    >
      <div class="d-flex dropdown-toggle-icons">
        <i class="fa fa-list" />
        <i class="fa fa-caret-down" />
      </div>

      <div v-show="isListTypeMenuExpanded" class="editor-group">
        <!-- Unordered List -->
        <div
          class="editor-group-item"
          @click="editor.chain().focus().toggleBulletList().run()"
        >
          <span class="group-item-name">Bullet List</span>
          <span :class="{ 'is-active': editor.isActive('bulletList') }">
            <i class="fa fa-list" />
          </span>
        </div>

        <!-- Ordered List -->
        <div
          class="editor-group-item"
          @click="editor.chain().focus().toggleOrderedList().run()"
        >
          <span class="group-item-name">Ordered List</span>
          <span :class="{ 'is-active': editor.isActive('orderedList') }">
            <i class="fa fa-list-ol" />
          </span>
        </div>
      </div>
    </span>

    <!-- TEXT ALIGNMENT -->
    <span
      :class="{ 'is-active': isTextAlignmentMenuActive }"
      class="editor-group-toggle"
      @click="toggleMenu('isTextAlignmentMenuExpanded')"
    >
      <div class="d-flex dropdown-toggle-icons">
        <i class="fa fa-align-left" />
        <i class="fa fa-caret-down" />
      </div>

      <div v-show="isTextAlignmentMenuExpanded" class="editor-group">
        <!-- Text Align Left -->
        <div
          class="editor-group-item"
          @click="editor.chain().focus().setTextAlign('left').run()"
        >
          <span class="group-item-name">Align Left</span>
          <span
            :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }"
          >
            <i class="fa fa-align-left" />
          </span>
        </div>

        <!-- Text Align Center -->
        <div
          class="editor-group-item"
          @click="editor.chain().focus().setTextAlign('center').run()"
        >
          <span class="group-item-name">Align Center</span>
          <span
            :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }"
          >
            <i class="fa fa-align-center" />
          </span>
        </div>

        <!-- Text Align Right -->
        <div
          class="editor-group-item"
          @click="editor.chain().focus().setTextAlign('right').run()"
        >
          <span class="group-item-name">Align Right</span>
          <span
            :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }"
          >
            <i class="fa fa-align-right" />
          </span>
        </div>
      </div>
    </span>

    <!-- Font Size -->
    <span
      class="editor-group-toggle"
      @click="toggleMenu('isFontSizeMenuExpanded')"
    >
      <div class="d-flex dropdown-toggle-icons">
        <span>{{ fontsize }}</span>
        <i class="fa fa-caret-down" />
      </div>

      <div v-show="isFontSizeMenuExpanded" class="editor-group">
        <div
          v-for="fontSizeOption in fontSizeOptions"
          :key="fontSizeOption"
          class="editor-group-item"
          @click="
            () => {
              fontsize = fontSizeOption;
              editor.chain().focus().setFontSize(fontSizeOption).run();
            }
          "
        >
          <span
            :class="{ 'is-active': fontSizeOption === fontsize }"
            class="group-item-name"
          >
            {{ fontSizeOption }}
          </span>
        </div>
      </div>
    </span>

    <div class="editor-options-divider" />

    <!-- MORE OPTIONS -->
    <span
      :class="{ 'is-active': isMoreOptionsMenuActive }"
      class="editor-group-toggle"
      @click="toggleMenu('isMoreOptionsMenuExpanded')"
    >
      <i class="fa fa-plus" />

      <div v-show="isMoreOptionsMenuExpanded" class="editor-group">
        <!-- URL -->
        <div
          :class="{ 'is-active': editor.isActive('link') }"
          class="editor-group-item"
          @click="setLink"
        >
          <span class="group-item-name">URL</span>
          <span>
            <i class="fa fa-link" />
          </span>
        </div>

        <!-- Color -->
        <div class="editor-group-item" @click="$refs.colorPicker.click()">
          <span class="group-item-name">Color</span>
          <span>
            <i class="fa fa-tint" />
          </span>
        </div>
      </div>
    </span>

    <input
      ref="colorPicker"
      type="color"
      class="hide-color-picker"
      @input="editor.chain().focus().setColor($event.target.value).run()"
    />
  </div>
</template>

<script>
import { directive } from 'vue3-click-away';
import set from 'lodash/set';
import get from 'lodash/get';

export default {
  directives: {
    ClickAway: directive,
  },
  props: {
    editor: {
      type: Object,
      default: () => ({}),
    },
    setLink: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
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
      isTextStyleMenuExpanded: false,
      isTextAlignmentMenuExpanded: false,
      isListTypeMenuExpanded: false,
      isFontSizeMenuExpanded: false,
      isMoreOptionsMenuExpanded: false,
    };
  },
  computed: {
    isTextStyleMenuActive() {
      return (
        this.isTextStyleMenuExpanded ||
        this.editor.isActive('underline') ||
        this.editor.isActive('strike')
      );
    },
    isListTypeMenuActive() {
      return (
        this.isListTypeMenuExpanded ||
        this.editor.isActive('bulletList') ||
        this.editor.isActive('orderedList')
      );
    },
    isTextAlignmentMenuActive() {
      return (
        this.isTextAlignmentMenuExpanded ||
        this.editor.isActive({ textAlign: 'left' }) ||
        this.editor.isActive({ textAlign: 'center' }) ||
        this.editor.isActive({ textAlign: 'right' })
      );
    },
    isMoreOptionsMenuActive() {
      return this.isMoreOptionsMenuExpanded || this.editor.isActive('link');
    },
  },
  methods: {
    out() {
      this.isTextStyleMenuExpanded = false;
      this.isListTypeMenuExpanded = false;
      this.isTextAlignmentMenuExpanded = false;
      this.isFontSizeMenuExpanded = false;
      this.isMoreOptionsMenuExpanded = false;
    },
    toggleMenu(menu) {
      if (!get(this, menu)) {
        this.out();
      }
      set(this, menu, !get(this, menu));
    },
  },
};
</script>
