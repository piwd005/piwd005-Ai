---
name: odoo-owl
description: >-
  Develop, debug, and architect modern Odoo OWL (Odoo Web Library) components,
  custom field widgets, client actions, view extensions, systray items, and
  reactive UI elements for Odoo 17, 18, 19, and 20. Use when creating or
  modifying JavaScript, XML Owl templates, or SCSS under static/src/.
---

# Odoo OWL 2.0 Web Component Development

Guide for developing reactive, high-performance UI components using Odoo's OWL 2.0 framework (Odoo 17, 18, 19, and 20).

## 1. Core OWL Component Structure

```javascript
/** @odoo-module **/

import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class MyCustomWidget extends Component {
    static template = "my_addon.MyCustomWidget";
    static props = {
        title: { type: String, optional: true },
        recordId: { type: Number, optional: true },
    };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");

        this.state = useState({
            loading: true,
            data: [],
            counter: 0,
        });

        onWillStart(async () => {
            await this.loadData();
        });

        onMounted(() => {
            // DOM-ready operations
        });
    }

    async loadData() {
        try {
            this.state.loading = true;
            const records = await this.orm.searchRead(
                "res.partner",
                [["is_company", "=", true]],
                ["name", "email", "phone"],
                { limit: 10 }
            );
            this.state.data = records;
        } catch (error) {
            this.notification.add(error.message || "Failed to load data", {
                type: "danger",
            });
        } finally {
            this.state.loading = false;
        }
    }

    onIncrement() {
        this.state.counter++;
    }

    async openRecord(id) {
        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.partner",
            res_id: id,
            views: [[false, "form"]],
            target: "current",
        });
    }
}
```

## 2. Companion XML Template (`static/src/xml/my_custom_widget.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="my_addon.MyCustomWidget">
        <div class="my-custom-widget p-3 border rounded bg-white shadow-sm">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="m-0 text-primary">
                    <t t-esc="props.title || 'Overview'"/>
                </h4>
                <button class="btn btn-sm btn-outline-primary" t-on-click="onIncrement">
                    Count: <span class="badge bg-primary" t-esc="state.counter"/>
                </button>
            </div>

            <t t-if="state.loading">
                <div class="text-center py-4 text-muted">
                    <i class="fa fa-circle-o-notch fa-spin fa-2x"/>
                    <p class="mt-2 mb-0">Loading data...</p>
                </div>
            </t>
            <t t-else="">
                <div class="table-responsive">
                    <table class="table table-hover table-sm">
                        <thead class="table-light">
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr t-foreach="state.data" t-as="item" t-key="item.id">
                                <td><t t-esc="item.name"/></td>
                                <td><t t-esc="item.email || '-'"/></td>
                                <td>
                                    <button class="btn btn-xs btn-link" t-on-click="() => this.openRecord(item.id)">
                                        View
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </t>
        </div>
    </t>
</templates>
```

## 3. Registering Different Types of Components

### A. Client Action
```javascript
registry.category("actions").add("my_addon.dashboard_action", MyCustomWidget);
```

### B. Custom Field Widget
```javascript
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class MyFieldWidget extends Component {
    static template = "my_addon.MyFieldWidget";
    static props = {
        ...standardFieldProps,
    };

    get formattedValue() {
        return this.props.record.data[this.props.name] || "";
    }
}

export const myFieldWidget = {
    component: MyFieldWidget,
    displayName: "My Field Widget",
    supportedTypes: ["char", "text"],
};

registry.category("fields").add("my_custom_field", myFieldWidget);
```

### C. Systray Item (Top Navbar)
```javascript
export class MySystrayItem extends Component {
    static template = "my_addon.MySystrayItem";
    setup() {
        this.action = useService("action");
    }
    onClick() {
        // open panel or action
    }
}

export const systrayItem = {
    Component: MySystrayItem,
};

registry.category("systray").add("my_addon.systray_item", systrayItem, { sequence: 50 });
```

## 4. Declaring Assets in `__manifest__.py`

```python
'assets': {
    'web.assets_backend': [
        'my_addon/static/src/scss/my_custom_widget.scss',
        'my_addon/static/src/js/my_custom_widget.js',
        'my_addon/static/src/xml/my_custom_widget.xml',
    ],
},
```
