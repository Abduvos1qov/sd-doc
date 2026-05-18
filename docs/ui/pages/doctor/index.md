---
title: "Doctor UI pages"
audience: All sd-main developers, QA
summary: Index of UI page reference docs for the doctor (KPI planning) module
topics: [doctor, ui, page-index]
---

# Doctor UI pages

The `doctor` module is the KPI planning subsystem — Active Client Base (АКБ / AKB), Coverage, SKU plans, Strike Rate, Volume targets, Forecast, Outlet plans, Personal/Agent assignments, and SMS broadcast. It sits between the salesdoctor's planning team and the agents/supervisors who execute the plans. Most pages share the same shape: filters → big table of agent × KPI rows with "share to agents" action that pushes the plan downstream.

## Pages

| Page | Route | Audience |
|---|---|---|
| [АКБ — Active Client Base](./doctor_akb_index.md) | `/doctor/akb` | admin / supervisor |
| [Coverage planning](./doctor_coverage_index.md) | `/doctor/coverage` | admin / supervisor |
| [SKU plan](./doctor_sku_index.md) | `/doctor/sku` | admin / supervisor |
| [Strike rate plan](./doctor_strike_index.md) | `/doctor/strike` | admin / supervisor |
| [SMS broadcast](./doctor_sms_index.md) | `/doctor/sms` | admin |
| [Forecast](./doctor_forecast_index.md) | `/doctor/forecast` | admin / supervisor |

> Doctor2 (`/doctor/doctor2/dashboard`, `/doctor/doctor2/index`, etc.) is a refactor of the same surface with a richer dashboard and is reached from the legacy `Doctor` links — it's not a separate UX, so it isn't listed here.

## Other endpoints

| Endpoint | Status |
|---|---|
| `/doctor/default/index` | Stub landing page (renders empty `index` view). |
| `/doctor/doctor/index`, `/doctor/doctor/akb`, `/doctor/doctor/sku`, `/doctor/doctor/strikerate` | Legacy combined KPI screens kept for backwards-compat; same data as the standalone pages above. |
| `/doctor/outletPlan/...` | Per-outlet plan write/import — admin-only data-entry. |
| `/doctor/personal/index` | Agent-level personal plan view. |
| `/doctor/targetVolume/index`, `/doctor/volume/view` | Target volume plans (parallel to SKU/Strike). |

## See also

- Module reference: [/modules/doctor](/docs/modules/doctor)
- Page-to-module map: [/quality/page-to-module-map](/docs/quality/page-to-module-map)
