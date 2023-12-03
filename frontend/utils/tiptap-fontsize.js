import { Extension } from '@tiptap/core';
import '@tiptap/extension-text-style';

export default Extension.create({
  addGlobalAttributes() {
    return [
      {
        types: ['textStyle'],
        attributes: {
          fontSize: {
            default: null,
            parseHTML: (element) =>
              element.style.fontSize.replace(/['"]+/g, ''),
            renderHTML: (attributes) => {
              if (!attributes.fontSize) {
                return {};
              }

              const numericFontSize = parseInt(attributes.fontSize, 10);
              return {
                style: `font-size: ${numericFontSize}px;`,
              };
            },
          },
        },
      },
    ];
  },
  addCommands() {
    return {
      setFontSize:
        (fontSize) =>
        ({ chain }) => {
          const numericFontSize = parseInt(fontSize, 10);
          return chain()
            .setMark('textStyle', { fontSize: numericFontSize })
            .run();
        },
      unsetFontSize:
        () =>
        ({ chain }) => {
          return chain()
            .setMark('textStyle', { fontSize: null })
            .removeEmptyTextStyle()
            .run();
        },
    };
  },
});
