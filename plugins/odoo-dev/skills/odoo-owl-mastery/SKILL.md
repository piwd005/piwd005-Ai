---
name: odoo-owl-mastery
description: >-
  Advanced OWL 2.0 Web Component Engineering and Hoot Testing for Odoo 19 & 20.
  Covers custom field widgets with standardFieldProps, interactive client actions,
  kanban & list controller extensions, systray items, patch() patterns, reactive state management,
  and automated frontend unit testing with @odoo/hoot.
  Use when building or debugging modern frontend features in Odoo 19 and 20.
---

# Odoo OWL 2.0 & Hoot Testing Mastery (Odoo 19 & 20)

Architectural handbook for building scalable, high-performance web components in Odoo 19 and Odoo 20 using the modern OWL 2.0 framework and Hoot test runner.

---

## 1. Custom Field Widget Architecture

Field widgets in Odoo 19/20 are OWL components registered in the `fields` registry category.

### A. JavaScript Component (`static/src/components/color_picker_field.js`)
```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { registry } from "@web/core/registry";

export class ColorPickerField extends Component {
    static template = "my_addon.ColorPickerField";
    static props = {
        ...standardFieldProps,
        colors: { type: Array, optional: true },
    };
    static defaultProps = {
        colors: ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#9933FF"],
    };

    setup() {
        this.state = useState({
            isDropdownOpen: false,
        });
    }

    get currentColor() {
        return this.props.record.data[this.props.name] || "#CCCCCC";
    }

    async selectColor(color) {
        this.state.isDropdownOpen = false;
        await this.props.record.update({ [this.props.name]: color });
    }

    toggleDropdown() {
        if (!this.props.readonly) {
            this.state.isDropdownOpen = !this.state.isDropdownOpen;
        }
    }
}

export const colorPickerField = {
    component: ColorPickerField,
    displayName: "Color Picker",
    supportedTypes: ["char"],
    extractProps: ({ attrs }) => ({
        colors: attrs.options?.colors,
    }),
};

registry.category("fields").add("color_picker", colorPickerField);
```

### B. Companion XML Template (`static/src/components/color_picker_field.xml`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="my_addon.ColorPickerField">
        <div class="o_color_picker d-inline-block position-relative">
            <div class="border rounded-circle shadow-sm cursor-pointer"
                 t-attf-style="width: 24px; height: 24px; background-color: #{currentColor};"
                 t-on-click="toggleDropdown"
                 t-att-class="{ 'opacity-50': props.readonly }"/>

            <t t-if="state.isDropdownOpen">
                <div class="position-absolute bg-white p-2 border rounded shadow mt-1 d-flex gap-1"
                     style="z-index: 1050;">
                    <t t-foreach="props.colors" t-as="col" t-key="col">
                        <span class="rounded-circle cursor-pointer border"
                              t-attf-style="width: 20px; height: 20px; background-color: #{col};"
                              t-on-click="() => this.selectColor(col)"/>
                    </t>
                </div>
            </t>
        </div>
    </t>
</templates>
```

---

## 2. Interactive Client Action Dashboard

### A. JavaScript Component (`static/src/components/dashboard_action.js`)
```javascript
/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class OperationsDashboard extends Component {
    static template = "my_addon.OperationsDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");

        this.state = useState({
            loading: true,
            kpis: {
                totalOrders: 0,
                pendingRevenue: 0,
                topPartners: [],
            },
        });

        onWillStart(async () => {
            await this.loadMetrics();
        });
    }

    async loadMetrics() {
        try {
            this.state.loading = true;
            const res = await this.orm.call(
                "my.operations",
                "get_dashboard_kpis",
                [],
                {}
            );
            this.state.kpis = res;
        } catch (error) {
            this.notification.add(error.message || "Could not load KPIs", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    async openOrders(domain = []) {
        await this.action.doAction({
            type: "ir.actions.act_window",
            name: "Orders Overview",
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            domain: domain,
            target: "current",
        });
    }
}

registry.category("actions").add("my_addon.operations_dashboard", OperationsDashboard);
```

---

## 3. Extending Views with `patch`

When extending core controllers in Odoo 19/20:
```javascript
/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        // Custom controller extension
    },

    async onCustomBatchAction() {
        const selectedResIds = await this.getSelectedResIds();
        if (!selectedResIds.length) {
            return;
        }
        await this.model.orm.call(
            this.props.resModel,
            "action_batch_process",
            [selectedResIds]
        );
        await this.model.load();
    },
});
```

---

## 4. Frontend Unit Testing with Hoot (`@odoo/hoot`)

Write unit tests for custom widgets under `static/tests/`:

```javascript
/** @odoo-module **/

import { describe, expect, test } from "@odoo/hoot";
import { mountWithCleanup, makeMockEnv } from "@web/../tests/web_test_helpers";
import { ColorPickerField } from "@my_addon/components/color_picker_field";

describe("ColorPickerField Component", () => {
    test("renders current color and opens palette on click", async () => {
        const mockRecord = {
            data: { custom_color: "#FF5733" },
            update: async (vals) => {
                mockRecord.data = { ...mockRecord.data, ...vals };
            },
        };

        const fixture = await mountWithCleanup(ColorPickerField, {
            props: {
                name: "custom_color",
                record: mockRecord,
                readonly: false,
            },
        });

        const colorDot = fixture.querySelector(".o_color_picker div");
        expect(colorDot).not.toBeNull();
        expect(colorDot.style.backgroundColor).toBe("rgb(255, 87, 51)");

        // Click to open dropdown
        colorDot.click();
        await fixture.tick();

        const options = fixture.querySelectorAll(".position-absolute span");
        expect(options.length).toBeGreaterThan(0);
    });
});
```
