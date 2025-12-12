import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  bookSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Chapters',
      items: [
        'chapter_1',
        'chapter_2',
        'chapter_3',
        'chapter_4',
        'chapter_5',
        'chapter_6',
        'chapter_7',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Conclusion',
      items: ['final_summary'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Resources',
      items: ['glossary', 'exercises'],
      collapsed: false,
    },
  ],
};

export default sidebars;
