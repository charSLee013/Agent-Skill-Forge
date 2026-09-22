# Browser Selection

Read this only when the user asks which browser to use. It is not a startup
requirement.

For a manually used Chromium profile with GUI profile management, Donut is the
practical default. Its application is open source, while its Wayfern Chromium
engine is not; do not present it as a fully open browser engine. Keep high-value
assets such as cryptocurrency wallets out of any fingerprint browser.

`fingerprint-chromium` is the fallback for a user who specifically requires an
open Chromium-derived engine and accepts command-line profile management.
`Camoufox` is a Firefox- and automation-oriented tool, so it is generally not
the right choice for a manual Chromium login workflow.

Do not make a recommendation from stale popularity metrics. Check each
candidate's current release, license, supported operating system, and requested
workflow before recommending it. Treat a free client as distinct from an
open-source engine.
