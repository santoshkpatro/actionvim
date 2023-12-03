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

    <!-- Underline -->
    <span
      :class="{ 'is-active': editor.isActive('underline') }"
      @click="editor.chain().focus().toggleUnderline().run()"
    >
      <i class="fa fa-underline" />
    </span>

    <!-- Strikethrough -->
    <span
      :class="{ 'is-active': editor.isActive('strike') }"
      @click="editor.chain().focus().toggleStrike().run()"
    >
      <i class="fa fa-strikethrough" />
    </span>

    <div class="editor-options-divider" />

    <!-- LIST STYLE -->

    <!-- Unordered List -->
    <span
      :class="{ 'is-active': editor.isActive('bulletList') }"
      @click="editor.chain().focus().toggleBulletList().run()"
    >
      <i class="fa fa-list" />
    </span>

    <!-- Ordered List -->
    <span
      :class="{ 'is-active': editor.isActive('orderedList') }"
      @click="editor.chain().focus().toggleOrderedList().run()"
    >
      <i class="fa fa-list-ol" />
    </span>

    <!-- TEXT ALIGNMENT -->

    <!-- Text Align Left -->
    <span
      :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }"
      @click="editor.chain().focus().setTextAlign('left').run()"
    >
      <i class="fa fa-align-left" />
    </span>

    <!-- Text Align Center -->
    <span
      :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }"
      @click="editor.chain().focus().setTextAlign('center').run()"
    >
      <i class="fa fa-align-center" />
    </span>

    <!-- Text Align Right -->
    <span
      :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }"
      @click="editor.chain().focus().setTextAlign('right').run()"
    >
      <i class="fa fa-align-right" />
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

    <!-- URL -->
    <span :class="{ 'is-active': editor.isActive('link') }" @click="setLink">
      <i class="fa fa-link" />
    </span>

    <!-- Color -->
    <span @click="$refs.colorPicker.click()">
      <i class="fa fa-tint" />
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
      isFontSizeMenuExpanded: false,
    };
  },
  methods: {
    out() {
      this.isFontSizeMenuExpanded = false;
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
