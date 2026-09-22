# CDP And Profile Launch

Read this for a start, restart, CDP, or profile-isolation request.

## Discover Before Launch

Find the Wayfern application below the user's installed Donut data directory.
Do not assume its version, Chromium version, or bundle path from an older run.
Use the engine belonging to the installed Donut release.

Use a distinct user-data directory for each requested profile. Never point two
Wayfern instances at the same profile directory. If a process already owns the
requested directory, report that fact and follow the user's direction rather
than starting a second instance or killing it.

## Launch Contract

Launch the `Wayfern.app` bundle with macOS `open -n ... --args`, not as a child
of a short-lived terminal command. Pass the user-specified profile directory,
proxy configuration, remote-debugging port, and
`--remote-debugging-address=127.0.0.1`. Preserve the GUI-compatible launch
flags only when they have been checked against the actual running release.

Wait for `http://127.0.0.1:<user CDP port>/json/version`. Confirm it responds,
then wait ten seconds and confirm both the endpoint and the Wayfern process
still exist. A momentarily live CDP endpoint is not a successful launch.

## CDP Limits

The free Wayfern path permits local CDP transport and page navigation, but some
automation commands, including `Runtime.evaluate`, are paid-plan operations.
Treat the resulting error as a product boundary.

When a user explicitly asks for a CDP WebSocket operation, connect with origin
suppression because modern Chromium rejects unauthorized Origin headers. Do not
perform `Wayfern.refreshFingerprint` by default. If the user explicitly asks
for identity refresh after changing a proxy, run it before the requested page
navigation and report the returned timezone, language, and geolocation.

## Completion Evidence

Report the exact engine path, profile path, PID, loopback CDP URL, and the two
successful CDP checks. For a user-requested page navigation, also report the
observed page URL; do not infer success from a navigation timeout alone.
