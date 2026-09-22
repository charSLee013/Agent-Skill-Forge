# Diagnostic Lessons

Read only for the named symptom. These are investigation rules, not default
startup steps and not authorization to alter the user's proxy stack.

## Browser Exits Immediately

First distinguish a Wayfern crash from a process that was reclaimed with the
terminal session. Inspect the Wayfern log and macOS diagnostic reports. For a
GUI browser launched by an agent, use LaunchServices (`open -n`) and verify CDP
again after ten seconds.

## Proxy Connects But Requests Fail

Identify the proxy topology before editing anything. If the user maintains a
Shadowsocks 2022 endpoint with a ShadowTLS plugin, the Shadowsocks outbound must
detour through a matching ShadowTLS outbound. A bare Shadowsocks configuration
can establish TCP and then fail silently after the application handshake.

If a TUN client returns fake IP addresses for subscription hostnames, an
outbound bound to a physical interface cannot use those addresses. Resolve the
hostname through a real bootstrap resolver selected by the user's proxy
configuration; do not pin a historical node IP.

When all SS2022 nodes fail at once, clock skew is plausible but an HTTP `Date`
header through a cache is not proof. Compare direct NTP with more than one time
source before changing the system clock.

## DNS Leakage

Separate browser behavior from the proxy resolver. A browser using an explicit
proxy usually delegates resolution to that proxy path, so a proxy client that
performs split or concurrent DNS can leak independently of the browser. Do not
claim a browser flag fixed DNS until a post-change resolver test proves it.

SOCKS5 through Wayfern's PAC path uses the `SOCKS5 host:port` directive, which
routes DNS and UDP through SOCKS. HTTP CONNECT is TCP-only. DoH strict mode
requires AsyncDns to remain enabled; disabling AsyncDns can silently force a
fallback resolver.

## Exit Changes Or Geographic Mismatch

An automatic latency group can move an established browser session when it
retakes measurements. A user who needs a stable session must supply a fixed
proxy listener instead of an automatic group.

Wayfern can generate a synthetic startup identity and can refresh location
fields from the current proxy exit. Treat its reported timezone and language as
observations to verify after a user-requested refresh, not as values to assume
from a country name. A country-level identity can still disagree with a
city-level IP database.

## Release-Specific Claims

If diagnosis requires implementation details, discover the installed release
first and inspect that release tag. `main` may use a different vault, launch,
or fingerprint implementation.
