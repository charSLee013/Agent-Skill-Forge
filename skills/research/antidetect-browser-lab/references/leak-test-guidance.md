# Leak Test Guidance

Read only when the user explicitly requests a leak check. A real IP without a
proxy is normal; a leak means a proxy-configured browser exposes a conflicting
IP, resolver, WebRTC candidate, timezone, or language.

Start with signals under the user's control: the browser's reported timezone,
language, proxy exit, and WebRTC candidates. Compare them with the user-supplied
expected proxy behavior rather than assuming a country determines every field.

If the user asks to use an external test site, use only the site they name or
ask them to choose one. Do not create a webhook collector or a hosted probe
page by default. A webhook response can carry a restrictive script CSP, so it
is not a reliable place to host a JavaScript probe page.

Classify a DNS result by resolver ownership. Mixed resolvers can come from the
proxy client's DNS strategy rather than the browser itself. Report the raw
evidence and the scope of the conclusion.
