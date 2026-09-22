---
name: antidetect-browser-lab
description: Bootstrap a user-owned Donut/Wayfern browser on macOS arm64 with an isolated profile, explicit proxy, and loopback CDP.
disable-model-invocation: true
argument-hint: "Requested operation and its required release, profile, proxy, or CDP details"
---

# Donut / Wayfern Bootstrap

Use this skill only for a browser and profile owned by the user. Its job is to
install a specified Donut release, launch Wayfern with an isolated profile and
an explicit proxy, and make CDP available on loopback. It does not select a
release, proxy, node, region, account, or target site for the user.

## Boundaries

- A requested install authorizes downloading and installing that exact release,
  not replacing an existing installation unless the user also names the target
  and authorizes replacement.
- Keep CDP on `127.0.0.1`. Do not expose it on a network interface.
- Use only a proxy endpoint supplied by the user. Do not create or edit proxy
  subscriptions, sing-box, Clash, TUN, relay, or account settings.
- Do not automate login, registration, page interaction, fingerprint refresh,
  or cleanup unless the user specifically requests that operation.
- Do not treat a paid API or CDP automation rejection as authorization to work
  around it. Read [Local API boundaries](references/local-api-boundaries.md)
  when a request reports 401, 403, or 402.

## Required Inputs

Collect only the inputs needed for the requested branch. Do not invent missing
values.

| Branch | Required user input |
|---|---|
| Install or update | Exact Donut release version and durable installation directory |
| Start or restart | Profile directory, proxy protocol/address/port, and CDP port |
| Browser egress check | A check URL or expected exit supplied by the user |

The supported proxy forms are SOCKS5 and HTTP CONNECT. SOCKS5 is preferred.
The endpoint must not embed credentials; when authentication is required, the
user must provide a suitable local listener or explicitly direct a separate
authentication setup.

## Routes

### Install or Update

Read [install and release verification](references/install-and-release-verification.md).
The user-specified release is sufficient even when Donut is not installed yet:
discover its actual assets and checksum file from the official release, verify
before extraction, and install only to the user-specified durable path.

Completion: the verified app bundle is at the requested path, launches, and
the Wayfern engine is available after Donut has downloaded it.

### Start or Restart

Read [CDP and profile launch](references/cdp-and-profile-launch.md) and
[proxy contract](references/proxy-contract.md). Verify the supplied proxy
before launch, use the supplied profile and CDP port, and launch the macOS app
through LaunchServices so it remains open after the execution session ends.

Completion: the intended Wayfern process still owns the requested profile after
ten seconds, `/json/version` responds on the requested loopback CDP port, and
the process was started with the supplied proxy endpoint.

### Diagnose a Browser Network Problem

Read [diagnostic lessons](references/diagnostic-lessons.md) only when the user
reports a matching symptom: proxy connection failure, DNS leakage, exit changes,
ShadowTLS failure, fake-IP failure, clock suspicion, browser exit, or a
timezone/language mismatch. Diagnose the existing configuration first; do not
turn a browser request into proxy-stack reconfiguration.

### Optional Work

- For a user-requested leak check, read [leak-test guidance](references/leak-test-guidance.md).
- For a user-requested browser comparison, read [browser selection](references/browser-selection.md).
- For an internal-behavior claim after an upgrade, first identify the running
  release and read that exact source tag. Never infer it from `main`.

## Finish

Report the exact release, install path, profile path, proxy endpoint, CDP
endpoint, and evidence collected for the requested operation. Leave browser,
profile, proxy, tokens, license files, and temporary files in place unless the
user separately asks to remove named targets.
