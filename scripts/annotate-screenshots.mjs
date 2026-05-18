#!/usr/bin/env node
/**
 * Re-visits a curated set of admin pages with Playwright, captures the
 * bounding boxes of the key interactive elements (primary buttons, the
 * first 5–8 form fields, the grid's row-action menu), and writes both:
 *
 *   - static/screens/annotated/<slug>.png    (raw screenshot, viewport-cropped)
 *   - static/data/callouts/<slug>.json       (list of {n, x, y, w, h, label})
 *
 * The Python companion (scripts/annotate-screenshots.py) then renders
 * numbered circles onto the PNG using Pillow.
 *
 * Idempotent — re-running overwrites both outputs.
 *
 * Usage:
 *   node scripts/annotate-screenshots.mjs                # default top-20 set
 *   SD_USER=demo SD_PASS=123456 BASE=http://localhost:8080 \
 *     node scripts/annotate-screenshots.mjs
 */

import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const BASE = process.env.BASE || 'http://localhost:8080';
const USER = process.env.SD_USER || 'demo';
const PASS = process.env.SD_PASS || '123456';

const REPO = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const SHOTS = path.join(REPO, 'static', 'screens', 'annotated');
const DATA  = path.join(REPO, 'static', 'data', 'callouts');

// Top-20 "tutorial-worthy" pages — workflow entry points the user docs revolve around.
const TARGETS = [
  { slug: 'orders_list',                  url: '/orders/list',                   title: 'Orders list' },
  { slug: 'orders_view_createOrder',      url: '/orders/view/createOrder',       title: 'Create order (web)' },
  { slug: 'orders_addOrder',              url: '/orders/addOrder',               title: 'Add order' },
  { slug: 'orders_recovery',              url: '/orders/recovery',               title: 'Order recovery' },
  { slug: 'clients_client',               url: '/clients/client',                title: 'Clients list' },
  { slug: 'staff_view_agent',             url: '/staff/view/agent',              title: 'Agents list' },
  { slug: 'staff_view_supervisor',        url: '/staff/view/supervisor',         title: 'Supervisors list' },
  { slug: 'staff_view_expeditor',         url: '/staff/view/expeditor',          title: 'Expeditors list' },
  { slug: 'stock_report',                 url: '/stock/report',                  title: 'Stock report' },
  { slug: 'stock_excretion',              url: '/stock/excretion',               title: 'Write-off / excretion' },
  { slug: 'warehouse_list',               url: '/warehouse/list',                title: 'Warehouse list' },
  { slug: 'warehouse_view_listPurchase',  url: '/warehouse/view/listPurchase',   title: 'Purchases' },
  { slug: 'planning_monthly2',            url: '/planning/monthly2',             title: 'Monthly plan' },
  { slug: 'planning_outlet',              url: '/planning/outlet',               title: 'Outlet plan' },
  { slug: 'dashboard_supervayzer',        url: '/dashboard/supervayzer',         title: 'Supervisor dashboard' },
  { slug: 'dashboard_kpi',                url: '/dashboard/kpi',                 title: 'KPI dashboard' },
  { slug: 'sms_view_list',                url: '/sms/view/list',                 title: 'SMS messages' },
  { slug: 'audit_photoReport',            url: '/audit/photoReport',             title: 'Photo report' },
  { slug: 'markirovka_view_incomingInvoices', url: '/markirovka/view/incomingInvoices', title: 'Markirovka — incoming' },
  { slug: 'onlineOrder_order',            url: '/onlineOrder/order',             title: 'Online orders' },
];

await fs.mkdir(SHOTS, { recursive: true });
await fs.mkdir(DATA,  { recursive: true });

async function login(page) {
  await page.goto(`${BASE}/site/login`, { waitUntil: 'domcontentloaded' });
  await page.fill('#LoginForm_username', USER);
  await page.fill('#LoginForm_password', PASS);
  await Promise.all([
    page.waitForLoadState('domcontentloaded'),
    page.click('#login-form button[type=submit], #login-form input[type=submit]')
      .catch(() => page.press('#LoginForm_password', 'Enter')),
  ]);
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
}

async function pickCallouts(page) {
  // Returns an ordered list of "important" callouts: top action buttons,
  // first form fields, grid header (one box for the whole header).
  return await page.evaluate(() => {
    const out = [];
    const rect = (el) => {
      const r = el.getBoundingClientRect();
      return { x: Math.round(r.left), y: Math.round(r.top),
               w: Math.round(r.width), h: Math.round(r.height) };
    };
    const visible = (el) => {
      const s = getComputedStyle(el);
      if (s.display === 'none' || s.visibility === 'hidden') return false;
      const r = el.getBoundingClientRect();
      return r.width > 30 && r.height > 14 && r.top >= 0 && r.left >= 0 &&
             r.top < window.innerHeight && r.left < window.innerWidth;
    };
    const txt = (el) => (el.innerText || el.value || el.placeholder || '').trim()
                          .replace(/\s+/g, ' ').slice(0, 60);

    // 1. Up to 3 prominent action buttons in the top header/toolbar
    const buttons = Array.from(document.querySelectorAll(
      '.toolbar .btn, .panel-heading .btn, header .btn, .page-header .btn, .sd-panel-head .btn, .btn-primary'
    )).filter(visible).slice(0, 3);
    buttons.forEach(b => out.push({ ...rect(b), label: txt(b), kind: 'action' }));

    // 2. First 5 labeled inputs (top of the form)
    const labels = Array.from(document.querySelectorAll('label[for]'))
      .filter(visible).slice(0, 5);
    labels.forEach(lab => {
      const id = lab.getAttribute('for');
      const ctl = id ? document.getElementById(id) : null;
      if (!ctl || !visible(ctl)) return;
      const r = ctl.getBoundingClientRect();
      const lr = lab.getBoundingClientRect();
      out.push({
        x: Math.round(Math.min(r.left, lr.left)),
        y: Math.round(Math.min(r.top, lr.top)),
        w: Math.round(Math.max(r.right, lr.right) - Math.min(r.left, lr.left)),
        h: Math.round(Math.max(r.bottom, lr.bottom) - Math.min(r.top, lr.top)),
        label: txt(lab),
        kind: 'field',
      });
    });

    // 3. Grid header (single box around the first table's thead)
    const thead = document.querySelector('.grid-view table thead, table.items thead, table.dataTable thead, table thead');
    if (thead && visible(thead)) {
      const r = thead.getBoundingClientRect();
      out.push({
        x: Math.round(r.left), y: Math.round(r.top),
        w: Math.round(r.width), h: Math.round(r.height),
        label: 'Data grid',
        kind: 'grid',
      });
    }

    // Sort top-down, left-right
    out.sort((a, b) => (a.y - b.y) || (a.x - b.x));
    return out.slice(0, 8);
  });
}

async function main() {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();

  console.error(`[annotate] login as ${USER}`);
  await login(page);

  for (const t of TARGETS) {
    try {
      const url = `${BASE}${t.url}`;
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await page.waitForLoadState('networkidle', { timeout: 6000 }).catch(() => {});
      // Viewport-cropped PNG (not fullPage — annotations need fixed coords)
      const shotPath = path.join(SHOTS, `${t.slug}.png`);
      await page.screenshot({ path: shotPath, fullPage: false });
      const callouts = await pickCallouts(page);
      await fs.writeFile(
        path.join(DATA, `${t.slug}.json`),
        JSON.stringify({ slug: t.slug, url: t.url, title: t.title, callouts }, null, 2) + '\n'
      );
      console.error(`[annotate] ${t.slug.padEnd(40)} ${callouts.length} callouts`);
    } catch (e) {
      console.error(`[annotate] !! ${t.slug}: ${e.message}`);
    }
  }

  await browser.close();
}

main().catch(e => { console.error(e); process.exit(1); });
