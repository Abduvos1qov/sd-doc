// @ts-check

const { themes } = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'SalesDoctor Docs',
  tagline: 'Distribution CRM — Developer Documentation',
  favicon: 'img/favicon.ico',

  url: 'https://docs.salesdoc.io',
  baseUrl: '/',

  organizationName: 'jamshidtulaganov',
  projectName: 'sd-doc',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ru', 'uz'],
    localeConfigs: {
      en: { label: 'English', htmlLang: 'en' },
      ru: { label: 'Русский', htmlLang: 'ru' },
      uz: { label: "O'zbekcha", htmlLang: 'uz' },
    },
  },

  markdown: { mermaid: true },
  themes: [
    '@docusaurus/theme-mermaid',
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      /** @type {import('@easyops-cn/docusaurus-search-local').PluginOptions} */
      ({
        hashed: true,
        // Index all three locales so UZ readers see UZ results
        language: ['en', 'ru'],
        // Index BOTH the developer docs and the client guide
        docsRouteBasePath: ['/docs', '/guide'],
        indexBlog: false,
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        // Trim what gets indexed to reduce payload weight
        // (the index is downloaded fresh each session, so smaller = faster
        // first-search response)
        searchResultLimits: 8,
        searchResultContextMaxLength: 50,
      }),
    ],
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          id: 'default',
          path: 'docs',
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/jamshidtulaganov/sd-doc/edit/main/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'guide',
        path: 'guide',
        routeBasePath: 'guide',
        sidebarPath: require.resolve('./sidebars-guide.js'),
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.png',
      colorMode: { defaultMode: 'light', respectPrefersColorScheme: true },
      navbar: {
        title: 'SalesDoctor',
        logo: {
          alt: 'SalesDoctor',
          src: 'img/logo.svg',
          href: '/',
        },
        items: [
          {
            type: 'doc',
            docId: 'sd-main/overview',
            position: 'left',
            label: 'sd-main',
          },
          {
            type: 'doc',
            docId: 'sd-cs/overview',
            position: 'left',
            label: 'sd-cs',
          },
          {
            type: 'doc',
            docId: 'sd-billing/overview',
            position: 'left',
            label: 'sd-billing',
          },
          {
            type: 'doc',
            docId: 'diagrams/index',
            position: 'left',
            label: 'Diagrams',
          },
          {
            type: 'docSidebar',
            sidebarId: 'qaSidebar',
            position: 'left',
            label: 'QA',
          },
          {
            to: '/guide/welcome',
            label: 'Guide',
            position: 'left',
          },
          {
            href: 'https://www.figma.com/board/y2kWMuxLwrpdaCGhVwYYYI',
            label: 'FigJam',
            position: 'right',
          },
          {
            type: 'localeDropdown',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Projects',
            items: [
              { label: 'sd-main · Dealer CRM', to: '/docs/sd-main' },
              { label: 'sd-cs · HQ Country Sales', to: '/docs/sd-cs/overview' },
              { label: 'sd-billing · Subscriptions', to: '/docs/sd-billing/overview' },
            ],
          },
          {
            title: 'Docs',
            items: [
              { label: 'Introduction', to: '/docs/intro' },
              { label: 'Ecosystem', to: '/docs/ecosystem' },
              { label: 'Diagram gallery', to: '/docs/diagrams' },
              { label: 'API reference', to: '/docs/api/overview' },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'FigJam (master board)',
                href: 'https://www.figma.com/board/y2kWMuxLwrpdaCGhVwYYYI',
              },
              { label: 'Diagram inventory', to: '/docs/diagrams-inventory' },
              { label: 'Changelog', to: '/docs/changelog' },
              { label: 'Troubleshooting', to: '/docs/troubleshooting' },
            ],
          },
        ],
        copyright: `© ${new Date().getFullYear()} Novus Distribution / SalesDoctor.`,
      },
      prism: {
        theme: themes.github,
        darkTheme: themes.dracula,
        additionalLanguages: ['php', 'bash', 'json', 'sql', 'yaml', 'nginx', 'docker'],
      },
      mermaid: {
        theme: { light: 'neutral', dark: 'dark' },
      },
    }),
};

module.exports = config;
