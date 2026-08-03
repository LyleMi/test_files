# AriadneBench API Parser v3

Write a general Python parser in `/workspace/solution.py`. During evaluation it
is invoked four times, once for each previously unseen JavaScript artifact
case:

```bash
python /workspace/solution.py --artifacts <case-directory> --output <evaluator-owned-output>
```

The evaluated artifacts are not available while you write the parser. Submit
one reusable analysis program; the evaluator runs it unchanged on every
unknown case. The task is not to inspect a known private case and manually
report its APIs, and solutions must not depend on teaching-example names,
values, paths, or layouts.

Each case has a 30-second execution budget and the evaluator rejects output
larger than 16 MiB. Bound source-map expansion instead of repeatedly rescanning
embedded sources. Manifests and normalized source paths may be used to
prioritize application-owned sources and defer separable vendor sources; do
not assume that every source in a production map is relevant to API recovery.

The case directory contains `artifacts.json` conforming to the published
`artifacts-v2.schema.json`, plus captured response bodies. Verify relative body
paths, byte counts and SHA-256 values before analysis.
Honor body `content-encoding`, MIME and charset metadata; real inputs can
include minified chunks, source maps, manifests, runtime configuration,
workers, a UTF-8 BOM, GBK and misleading MIME types. Do not assume evaluator
mount paths or case names. Use only the Python standard library in the final
solution.

Write exactly submission schema v3 to `--output`. Each API has `url`, `method`,
`parameters`, and `evidence`. Submission v2 and any API containing `state` are
invalid. Dynamic path segments use `{name}`.
Use the stable name present in source for each dynamic path segment. Query
values are request instances, not API identity; report every query name,
including names whose values are fixed literals.

Parameter locations follow these rules:

- `header`: application-level names, lowercased. Keep `authorization` and
  custom headers. Exclude fixed protocol headers: `content-type`,
  `content-length`, every `accept*` name, `host`, `origin`, `referer`,
  `user-agent`, `connection`, `cache-control`, and `pragma`.
- `body`: only top-level fields of a JSON/object body. Do not invent a name
  for an anonymous or scalar body.
- `form`: fields from `URLSearchParams`, `FormData`, and HTML forms.
- `cookie`: cookie names. Deduplicate all parameters by `(name, location)`.

The target is the application's business API. URLs used to retrieve scripts,
workers, source maps, manifests, runtime configuration, or route configuration
are support resources, not APIs. They may be evidence. Exclude
disabled, rollback, historical, example-only and dead-code candidates.
Duplicate path/method reports do not earn extra credit.

Treat browser request sinks according to their HTTP semantics. In particular,
`navigator.sendBeacon(url, data)` is a `POST` request even though it
does not use `fetch`.

Evidence `source` identifies the artifact URL that supports the API.

The included `solution.py` writes an empty valid result and `validator.py`
checks the output contract. Ten `examples/teaching-*` cases publish truth for
basic calls, parameter semantics, simple configuration, local data flow,
current-versus-rollback selection with feature filtering, and
wire/source-map/worker handling. A small real Vite production build demonstrates
how multiple authored modules, shared request contexts, minified output and its
source map fit together. Independent production examples also cover ES-module
object resources, application-versus-vendor map triage, and an explicit lazy
deployment closure. The composed cases demonstrate that URL expressions,
request wrappers, separately assembled options, and evidence provenance must be
resolved together rather than by independent text matches.
The larger `examples/development-case` intentionally
has no truth. Example structures and values do not occur in evaluated cases.
