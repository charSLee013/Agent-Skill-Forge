# Proxy Contract

Read this for every Wayfern start or restart request.

The user supplies the protocol, host, and port. SOCKS5 is preferred. HTTP
CONNECT is supported only when the user accepts that it transports TCP and does
not provide SOCKS-level DNS or UDP behavior. Do not include credentials in a
profile, command, log, or skill document.

Before opening Wayfern, check that the supplied endpoint accepts a connection.
When the user asks to prove egress, use only their supplied check URL or their
stated expected exit. A shell check proves the endpoint path, not that the
browser used it; after launch, confirm Wayfern's process arguments and perform
the requested browser-level verification.

For SOCKS5, follow Wayfern's proxy behavior by using a PAC directive equivalent
to `SOCKS5 host:port`. For HTTP CONNECT, use the equivalent `PROXY host:port`
directive. Compose these only from the user-supplied endpoint. Never replace a
fixed endpoint with a latency-selected group, an inferred local port, or a
historical proxy address.

If the endpoint needs credentials or is unavailable, stop and request a local
listener or a user-approved proxy setup. This skill neither builds one nor
stores its secrets.
