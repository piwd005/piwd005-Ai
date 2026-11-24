# Upstream candidates reviewed

The kit vendors no upstream code. Public release candidates previously reviewed were REA
6.9.0 (d74549e495c58eb4a560279fd9f05508401ea0a0), Odoo Skills
634b2db69c0ffb9766a5d16cff09a81ff1df54f4, Odoo MCP Pro 4.1.2
(6af7f74470444ddd85a98e403fe1652770aa3859) and Reverse Skill 1.0.1
(9c28c6ca1062a1a076e28baf40f241dbb4cf5dc2). None is installed by this kit.

REA needs a supported Node runtime and restricted local stdio exposure. Odoo Skills has
client-specific installers and requires file-level licensing review. Odoo MCP Pro exposes
write tools by default and has mixed Elastic 2.0/MPL licensing. Reverse Skill contains
broad toolchain bootstraps beyond ordinary reference analysis. Treat all as candidates,
review exact files and dependencies before admission, and preserve applicable notices.

Internal environment inspection and codebase maps are excluded from public distribution.
