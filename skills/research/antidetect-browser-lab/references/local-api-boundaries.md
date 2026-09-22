# Local API Boundaries

Read this only when the user explicitly asks about Donut's Local API or reports
an API status code. The bootstrap workflow does not require the API or a token.

| Result | Meaning | Action |
|---|---|---|
| 401 | Missing or mismatched Local API token | Ask whether the user wants to use the official GUI token flow; inspect logs before changing anything. |
| 403 | Wayfern terms have not been accepted | Direct the user to the official application flow; do not modify license state as a side effect of browser startup. |
| 402 | Paid API launch or automation capability | Stop this path and use the manual GUI/Wayfern launch path if that satisfies the request. |

Do not reseal, create, copy, delete, or disclose `api_token.dat` from this
skill. A browser start request does not authorize Local API recovery.
