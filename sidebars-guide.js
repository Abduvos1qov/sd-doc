// @ts-check

/**
 * Customer onboarding guide — separate from /docs (developer docs).
 * Audience: dealer admins and team leads setting up SalesDoctor for the
 * first time. No technical internals, schemas, configs, or credentials.
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  guideSidebar: [
    'welcome',
    'pages-catalog',
    {
      type: 'category',
      label: '🚀 Getting started',
      collapsed: false,
      items: [
        'getting-started/first-login',
        'getting-started/dashboard-tour',
        'getting-started/navigating-the-app',
      ],
    },
    {
      type: 'category',
      label: '👥 Build your team',
      collapsed: false,
      items: [
        'getting-started/add-agents',
        'getting-started/add-supervisors',
        'getting-started/add-expeditors',
      ],
    },
    {
      type: 'category',
      label: '🏬 Set up your business',
      collapsed: false,
      items: [
        'getting-started/add-clients',
        'getting-started/set-up-warehouses',
        'getting-started/configure-discounts-bonuses',
        'getting-started/stock-and-purchases',
        'getting-started/stock-write-off',
      ],
    },
    {
      type: 'category',
      label: '📦 Daily operations',
      collapsed: false,
      items: [
        'daily-use/first-order',
        'daily-use/plan-visits',
        'daily-use/track-orders',
        'daily-use/approve-clients',
      ],
    },
    {
      type: 'category',
      label: '📱 Field & mobile',
      collapsed: false,
      items: [
        'mobile/agent-app',
        'mobile/visit-and-audit',
        'mobile/expeditor-delivery',
      ],
    },
    {
      type: 'category',
      label: '📈 Reports & online',
      collapsed: false,
      items: [
        'reports/dashboard-kpi',
        'reports/sales-and-debts',
        'reports/online-orders',
      ],
    },
    {
      type: 'category',
      label: '🆘 Help & next steps',
      collapsed: false,
      items: [
        'support/faq',
        'support/glossary',
        'support/contact',
      ],
    },
  ],
};

module.exports = sidebars;
