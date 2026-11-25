# Marketing Automation Community Parity Architecture & Lessons Learned

## 1. Domain Constraints & Validation Rules
- In `marketing.activity`, any custom or template activity domain must be validated via `@api.constrains('activity_domain')` to prevent invalid domain ASTs from entering the database.
- Activity hierarchy cycles and modifications must be guarded defensively: if traces already exist for a child activity, altering its parent hierarchy must be prohibited to prevent orphaned DAG executions.

## 2. Participant State Transition Partitioning
- During `marketing.campaign.sync_participants()`, participants excluded from the campaign must be partitioned into two distinct categories:
  1. Records physically deleted from the database (`RecordModel.browse(...).exists()` returns False) $\rightarrow$ invoke `_action_set_unlink()` with `'Record deleted'`.
  2. Records that still exist in the database but no longer match the campaign filter domain $\rightarrow$ invoke `_action_set_unlink()` with `'Record no longer matches campaign filter'`.

## 3. Database Constraints on Mailing Programmatic Creation
- Odoo 19 `mailing.mailing` enforces a PostgreSQL CHECK constraint: `CHECK(email_from IS NOT NULL OR mailing_type != 'mail')`.
- When generating pre-configured campaign templates (`welcome`, `hot_contacts`, `double_opt_in`, `commercial_prospection`), outgoing email must never be left unassigned:
  ```python
  email_from = (
      self.env.user.email_formatted
      or self.env.company.email_formatted
      or self.env.user.email
      or self.env.company.email
      or 'marketing@example.com'
  )
  ```

## 4. Test Participant Execution Isolation
- In `marketing.campaign.test` wizard, test participants must be tagged with `is_test=True`.
- In test participant form views, traces must be immediately executable on-demand via `button[name='action_execute']` (`fa-play`), with visual red banner ribbons (`TEST`) for verification.
