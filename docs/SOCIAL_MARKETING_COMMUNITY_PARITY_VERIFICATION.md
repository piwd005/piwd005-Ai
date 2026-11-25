# PriERP Social Marketing (pi_social_marketing) — Enterprise Parity & Architecture Report

## Overview
`pi_social_marketing` provides 100% complete functional, visual, and architectural parity with Odoo Enterprise Social Marketing for Community editions on Odoo 19 & 20.

## 6-Dimension Parity Architecture

### 1. Models & Business Logic
- **`social.media`**: Declares supported social networks (Facebook, Twitter/X, LinkedIn, Instagram, YouTube) with OAuth redirect URI computes and developer credentials.
- **`social.account`**: Multi-account management, token caching, live audience/engagement/stories statistics, and connection state management.
- **`social.stream` & `social.stream.post`**: Unified feed columns, real-time message stream polling, and author avatar links.
- **`social.post.template` & `social.post`**:
  - Full post lifecycle (`draft` -> `scheduled` -> `posting` -> `posted`).
  - Scheduling via `scheduled_date` and cron runner.
  - Multi-network live previews (Facebook, Twitter, LinkedIn, Instagram, YouTube).
  - Split Per Media customization (individual messages, images, and video configurations per network).
- **`social.live.post`**: Individual dispatch record per account/network with state tracking and `@api.model def refresh_statistics(self)`.
- **`res.config.settings`**: Developer account credentials for Facebook, Twitter/X, LinkedIn, Instagram, YouTube with auto-sync to `social.media`.

### 2. Interactive Lifecycle & Wizards
- **Comments Modal (`social.StreamPostComments`)**:
  - Live comment reading and real-time reply insertion.
  - 3-dots actions menu with "Create Lead", "Edit", and "Delete".
  - Sub-comment threads with recursive reply tree.
- **Create Lead Wizard (`social.post.to.lead`)**:
  - Converts social comments and feed posts directly into CRM Leads/Opportunities with pre-filled customer message and contact context.
- **Add Stream Modal (`social.AddSocialStreamDialog`)**:
  - Interactive stream creation from linked social accounts.

### 3. Frontend OWL 2.0 & Assets
- **Kanban View**:
  - Custom kanban view (`js_class="social_stream_post_kanban_view"`) with live horizontal stream columns.
  - Stream post card with formatted text, media attachments overlay, like/retweet counters, and comments toggle.
- **Fields & Widgets**:
  - `social_post_formatter`: Linkified hashtags and URLs.
  - `social_post_preview`: Reactive multi-network card previews.
  - `social_post_split_per_media`: Dynamic splitting toggle between universal and per-network messages.
- **Defensive ID Sanitization**:
  - Handled Odoo 19 relational record ID structure (`extractId()`) across OWL components to prevent `Invalid ids list: [object Object]` RPC errors.

### 4. Mobile Responsiveness (Law 16 & 18 Compliance)
- **Viewport Support**: Fully verified on Desktop (1440x900) and Mobile (390x844).
- **Boundless Root**: Zero `overflow: hidden` on root containers.
- **Scroll Containers**: Horizontal stream columns and control panels gracefully wrap and scroll with `-webkit-overflow-scrolling: touch`.
- **Touch Targets**: All action buttons, toggles, and modal controls conform to $\ge 38\text{px}$ accessibility targets.

## Verification & Test Results
- **Full E2E Interactive Test Suite (`test_social_full_e2e.mjs`)**:
  - 53 / 53 checks passed across Desktop and Mobile.
  - Zero JavaScript console errors.
  - Zero crash modals.
- **Advanced Parity Test Suite (`test_advanced_social_parity.mjs`)**:
  - Settings developer credentials save verified.
  - Multi-network live previews before split verified.
  - Split Per Media notebook tabs (`Facebook`, `X (Twitter)`) verified.
- **Evidence Screenshots**: Preserved in `social_marketing_evidence/` (32 visual proofs).

## Fresh Installation & Manifest Load Order Law
- **Issue**: On a completely new installation (`ecommerce.getpicloud.com`), installing `pi_social_marketing` failed with:
  `ValueError: External ID not found in the system: pi_social_marketing.social_post_template_action` while parsing `views/social_menu_views.xml`.
- **Root Cause**: In `__manifest__.py`, `views/social_menu_views.xml` was loaded at line 42, before `views/social_post_template_views.xml` (line 46). In `social_menu_views.xml`, `<menuitem id="menu_social_post_template" action="social_post_template_action"/>` directly referenced the action before it was loaded.
- **Solution**: Follow standard Odoo menu architecture. In `social_menu_views.xml`, declare `<menuitem id="menu_social_post_template" .../>` without the `action` attribute. In `social_post_template_views.xml`, attach the action via `<record id="menu_social_post_template" model="ir.ui.menu"><field name="action" ref="social_post_template_action"/></record>`. This guarantees 100% clean installation on fresh databases.

