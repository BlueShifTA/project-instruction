# Template Maintainer

Use the root `just` commands first:
- `just install`
- `just lint`
- `just test`
- `just typecheck`
- `just run-ci`

Start with:
1. `CLAUDE.md`
2. `ProjectMap.md`
3. `justfile`

Template lifecycle:
- Customize with `just bootstrap`
- After first successful build, run `just template-clean`
- Remove template-only example code and update docs
