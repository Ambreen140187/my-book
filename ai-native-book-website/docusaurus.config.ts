import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AI-Native Driven Development',
  tagline: 'Premium Book Website',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // ✅ GitHub Pages CONFIG (ONLY ONCE)
  url: 'https://ambreen140187.github.io',
  baseUrl: '/my-book/',
  organizationName: 'Ambreen140187',
  projectName: 'my-book',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          path: 'docs',
          routeBasePath: 'docs',
        },
        blog: {
          showReadingTime: true,
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'book',
        path: './book',
        routeBasePath: '/book',
        sidebarPath: require.resolve('./sidebarsBook.ts'),
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'sp-plans',
        path: './content/chapters/sp.plans',
        routeBasePath: '/sp.plans',
        sidebarPath: false,
      },
    ],
    [
      '@docusaurus/plugin-client-redirects',
      {
        fromExtensions: ['html'],
        toExtensions: ['html'],
      },
    ],
    async function myPlugin() {
      return {
        name: 'chatbot-wrapper',
        getClientModules() {
          return [require.resolve('./src/components/RootWrapper')];
        },
      };
    },
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',

    colorMode: {
      respectPrefersColorScheme: true,
    },

    navbar: {
      title: 'My Site',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },
      items: [
        {to: '/', label: 'Home', position: 'left'},
        {to: '/book', label: 'AI Book', position: 'left'},
        {to: '/waitlist', label: 'Waitlist', position: 'left'},
        {to: '/about', label: 'About', position: 'left'},
        {to: '/contact', label: 'Contact', position: 'left'},
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'AI Book',
          items: [
            {label: 'Introduction', to: '/book/intro'},
            {label: 'Chapters', to: '/book/chapter_1'},
            {label: 'Exercises', to: '/book/exercises'},
          ],
        },
        {
          title: 'Resources',
          items: [
            {label: 'Glossary', to: '/book/glossary'},
            {label: 'Waitlist', to: '/waitlist'},
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/Ambreen140187/my-book',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Project.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
