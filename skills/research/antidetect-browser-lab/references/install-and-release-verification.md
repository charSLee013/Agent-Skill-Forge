# Install And Release Verification

Read this for a user-requested install or update. Donut does not need to be
preinstalled.

## Official Sources

- Release index: <https://github.com/zhom/donutbrowser/releases>
- Exact release page: `https://github.com/zhom/donutbrowser/releases/tag/v<VERSION>`
- Exact release metadata: `https://api.github.com/repos/zhom/donutbrowser/releases/tags/v<VERSION>`

`VERSION` is the exact value supplied by the user. Do not replace it with a
latest release, a cached version, or a version observed on another machine.

## Install Procedure

1. Request the exact release metadata and list its assets. If GitHub's
   unauthenticated API is rate-limited or rejected, use the exact official
   release page instead; do not switch to a different version or infer an asset
   name from an older release.
2. Detect the local architecture. For this skill, proceed only on macOS arm64.
   Select the one application archive actually listed for that architecture. If
   there is not exactly one match, show the asset list and stop.
3. From the same release, obtain the published checksum file. Match the chosen
   archive by its complete filename and require exactly one checksum entry.
4. Download both files to a newly created staging directory. Run `shasum -a
   256` against the published value before extracting anything.
5. On a checksum match, extract the archive into staging and verify that it
   contains exactly one application bundle. Install that bundle to the durable
   directory supplied by the user.
6. If that destination already exists, stop unless the user explicitly asked to
   replace it. Do not replace a bundle merely because its version differs.
7. Launch the installed Donut application. Wayfern is downloaded by Donut when
   needed; wait for the engine bundle to appear before attempting a Wayfern
   start.

## Stop Conditions

Stop on a missing release, unsupported architecture, ambiguous asset,
missing/ambiguous checksum, checksum mismatch, malformed archive, existing
destination without replacement authorization, or unavailable engine download.

The checksum belongs to the selected release asset, not to this document. Never
copy a checksum, asset filename, or version into this skill.
