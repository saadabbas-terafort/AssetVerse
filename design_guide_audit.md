# AssetVerse Backend Design Guide Audit

Audit date: 2026-10-06  
Reference: `design_guide_extracted.txt` and the complete 18-page PDF text supplied in the conversation.  
Scope: current Django source, registered routes, model/migration metadata, and the configured PostgreSQL schema.

## Executive result

The database is substantially aligned with the guide. The live database has all 19 expected domain tables; every concrete model column matches its live table; the expected migration files are applied; and `makemigrations --check --dry-run` reports no model/migration drift.

The backend is **not yet compliant overall**. Important API routes and authentication flows are absent, multiple public querysets violate app/status scope, serializers do not implement the documented code-based contract, model validation is not consistently invoked, the lookup bundle is incomplete and incorrectly protected, and seed/deploy/storage requirements are absent. One direct schema mismatch exists in the many-to-many join tables.

## Verified database fields and relationships

### Account and app tables

| Relationship/table | Current implementation | Result |
| --- | --- | --- |
| `users_user` | UUID PK, unique email, Django staff fields, no username; separate from device users | Matches |
| `users_publicuser` | UUID PK; `(device_id, app_name)` unique; `(app_name, is_active)` index | Matches |
| `users_publicusertoken.user` | One-to-one to PublicUser, `CASCADE`; key is varchar(40) PK | Matches |
| `app_settings_appsetting` | UUID PK; unique slug; label/is_active/sort_order/timestamps | Matches |

### Lookup tables

All eight documented lookup tables exist: orientation, record status, asset variant, frame key, frame type, effect type, slide type, and tag. The shared UUID/code/label/order/active/timestamp fields are present. Tag has all six documented types and the `(tag_type, is_active, sort_order)` index.

### Catalog and assets relationship matrix

| From | To | Current `on_delete` / nullability | Result |
| --- | --- | --- | --- |
| Category.app | AppSetting | `PROTECT`, required | Matches |
| Category.parent | Category | `CASCADE`, nullable | Matches |
| Category.orientation/status/variant | Corresponding lookup | `PROTECT`, required | Matches |
| Category.tag | Tag | `PROTECT`, required | Matches relationship; tag-type validation is incomplete for writes |
| Category.section | Tag | `PROTECT`, nullable | Matches relationship; tag-type validation is incomplete for writes |
| Frame/Sticker/Effect/Slide/Font.category | Category | `CASCADE`, required | Matches |
| Frame.frame_type/status | Lookup | `PROTECT`, required | Matches |
| FrameConstraint.frame | Frame | `CASCADE`, required | Matches |
| FrameAsset.frame | Frame | `CASCADE`, required | Matches |
| FrameAsset.key/status | Lookup | `PROTECT`, required | Matches |
| Effect.effect_type/status | Lookup | `PROTECT`, required | Matches |
| Slide.slide_type/status | Lookup | `PROTECT`, required | Matches |
| Sticker/Font.status | Lookup | `PROTECT`, required | Matches |
| Frame/Sticker/Effect/Font.tags | Tag | M2M, join rows cascade | Relationship matches; join-table columns do not (see below) |

The required UUID domain IDs, documented table names, category/asset fields, and the documented model index field combinations are represented by the models and migrations. `makemigrations --check --dry-run` found no drift.

### Confirmed physical schema mismatch

The guide says each tag join table contains only its two foreign keys. The live auto-generated Django join tables contain an extra surrogate `id` column:

- `home_assets_frame_tags`: `id`, `frame_id`, `tag_id`
- `stickers_sticker_tags`: `id`, `sticker_id`, `tag_id`
- `effects_effect_tags`: `id`, `effect_id`, `tag_id`
- `fonts_font_tags`: `id`, `font_id`, `tag_id`

This is the one concrete table-column mismatch found in the live schema audit.

## API and behavior cross-check

### Present, but incomplete or incorrect

- `GET /health/` returns the required `{status, data, message}` success envelope. Its view does not access the database.
- `POST /api/users/auth/` exists, validates an active app slug, upserts by device/app, and rotates a 32-character UUID-hex token.
- Public list/detail paths exist for categories, frames, stickers, effects, slides, and fonts.
- Public views mostly use the expected trailing-slash plural paths.
- `success_response` and `error_response` use the correct envelope keys when explicitly called.
- File upload path functions match the guide’s documented path patterns, including the global `slides/{id}/` prefix.

### Verified API gaps and incorrect behavior

1. **Category public list leaks rows across apps and statuses.** `CategoryView.get()` runs `Category.objects.all()`. It does not filter to the header app or active status and ignores `section`, `variant`, `parent_id`, and `parent`. It also prints the queryset, producing unwanted console output and an extra evaluation. The category detail view scopes by app but does not restrict status to active.
2. **Effect public list is unscoped.** `EffectView.get()` uses `Effect.objects.all()` and does not filter by app, active status, `category`, or `effect_type`. This can return records belonging to other apps and inactive effects.
3. **Lookup bundle has incorrect access and incomplete contents.** `/api/lookups/` is unauthenticated (`authentication_classes = []`, `permission_classes = []`) and currently requires the public API key plus app header. The guide requires an authenticated staff/session/device-token caller, without the catalog API-key/app-header contract. The response includes only orientations, all tags, and statuses. It omits sections, screen tags, variant tags, hashtags, locales, variants, frame keys, frame types, effect types, and slide types. The `tags` key should contain availability tags only, not every tag type.
4. **Tag endpoints use the wrong access contract.** `/api/lookups/tags/` and its detail endpoint call the helper that also requires `X-App-Name` and an active app. The guide specifies API-key access for these endpoints, without requiring the app header.
5. **Public detail endpoints do not consistently require an active record.** Category, frame, sticker, effect, slide, and font detail querysets do not uniformly filter their own status to active. Frame detail specifically returns inactive frames, although public frame reads must be active.
6. **Frame read payload is incomplete.** The current frame serializer does not nest `constraints`, `assets`, or tag codes in the required structure. The layer list must include inactive layers when the frame itself is active. No frame-asset API route exists.
7. **Category output contract is incomplete.** The serializer emits related objects as read-only strings, not nested app/lookups with codes. It does not return the required `app_name`, absolute cover URL, `child_count`, `is_parent`, or `is_child` fields.
8. **Serializers cannot perform documented writes.** Related fields on category and asset serializers are `StringRelatedField(read_only=True)`. Clients therefore cannot submit lookup codes or UUID category/parent IDs through these serializers. No write serializers implement active-lookup lookup-by-code, variant validation, tag-code handling, or multipart behavior.
9. **Serializer file URLs are not guaranteed absolute.** The views instantiate serializers without a request context, so DRF file fields do not have the request required to build absolute URLs. The S3/local storage backend described by the guide is also absent.
10. **Admin JSON API is absent.** There are no `/admin/` API routes for categories, frames, frame assets, stickers, effects, slides, or fonts. Django browser admin registration exists, but does not substitute for the specified staff CRUD API.
11. **Lookup writes and inactive lookup rejection are absent.** There are no JSON admin lookup writes accepting codes or consistently rejecting missing/inactive lookup rows.
12. **Device auth messages and token authentication are incomplete.** Login always returns `User registered successfully`; the guide says the message changes for later logins. There is no `Authorization: PublicToken <key>` authentication class, no app-match check when authenticating that token, and no authenticated lookup-bundle use of the token.
13. **The JSON envelope is not global.** No DRF exception handler is configured. Framework-generated validation errors, 404s, 405s, and other errors will not consistently use `{status, data: {}, message}`. Public write methods will be 405, but not necessarily with the documented envelope.
14. **Staff API authentication/default permissions are not configured.** `rest_framework.authtoken` is installed, but DRF defaults, staff-only permission classes, and the guide’s authentication ordering are not configured. All current API views explicitly disable authentication and permissions.
15. **Category validation has edge cases.** `Category.clean()` rejects direct self-parenting, grandchildren through an existing parent, cross-app parent assignment, and wrong tag types. It does not reject moving a category that already has children underneath another root (which creates depth three), nor changing a parent’s app while its children remain in the old app. Lookup activity is not checked. `Model.clean()` is not automatically called by `.save()`, and there is no API write serializer to invoke equivalent validation.
16. **Asset validation is model-only and incomplete.** `validate_asset_category()` checks child-category placement and matching variant code, but does not reject inactive lookup records or validate tag M2M membership. There is no write serializer layer to repeat model checks as the guide requires.

## Configuration, seed, admin, storage, and deployment

- `SECRET_KEY`, `DEBUG`, and `PUBLIC_API_KEY` are read from the environment, but the secret has an insecure fallback, `DEBUG` defaults to true, and `ALLOWED_HOSTS` defaults to `*`.
- Database username variable is `DB_USER`; the guide specifies `DB_USERNAME`. `.env.example` also uses `DB_USER`.
- `CSRF_TRUSTED_ORIGINS` and CORS configuration for `X-App-Name` and `X-Api-Key` are absent. `django-cors-headers` is not in requirements or middleware.
- The guide specifies Unfold admin; the project uses Django’s standard admin. `django-unfold` is not a dependency.
- WhiteNoise middleware/dependency and production static configuration (`STATIC_ROOT`/collectstatic startup) are absent.
- S3 storage selection, public unsigned URLs, custom domain handling, and one-day cache settings are absent. `django-storages`/`boto3` are not in requirements.
- No `seed_data` or `ensure_superuser` management commands exist, and no `seeds/` JSON data is present.
- `main/settings.py` imports `dotenv`, but `python-dotenv` is not listed in `requirements.txt`; a clean dependency install is not reproducible from that file alone.
- No Dockerfile, compose configuration, Gunicorn startup script, or GitHub Actions deploy workflow is present in the workspace listing. Gunicorn is not in requirements.
- Seed code rows and the five documented variant constants are not implemented in the repository.

## Verification performed

- `manage.py check`: passed with no system-check issues.
- `manage.py makemigrations --check --dry-run`: `No changes detected`.
- `manage.py showmigrations --plan`: all listed project and Django migrations are applied in the configured database.
- Live PostgreSQL introspection: all 19 expected domain tables exist; all model concrete columns match the corresponding live table columns; FK and unique constraints are present. The tag join tables have the extra `id` discrepancy listed above.
- `manage.py test`: discovered **0 tests**, so this command did not validate behavior.
- Explicit `manage.py test apps.users.tests apps.utils.tests`: 6 tests passed. These tests do not cover the app-leak, inactive-row, route/auth, serializer-write, relation-validation, or deploy/storage requirements. The test output also showed the `CategoryView` queryset debug print.
- Pylance workspace diagnostics returned warnings for unused variables/imports only; no error-severity diagnostics were returned.

## Final missing-items checklist

- [ ] Correct category list app/status scoping and implement all category query filters; remove the debug print.
- [ ] Correct effect list app/status scoping and implement its documented filters.
- [ ] Apply active-status scoping to all public detail reads.
- [ ] Implement the exact lookup-bundle authentication contract and all documented grouped keys.
- [ ] Remove the app-header requirement from API-key-only tag endpoints.
- [ ] Implement `PublicToken` authentication and enforce active-user and app-name matching; distinguish registration and login response messages.
- [ ] Configure staff/session/token authentication and staff-only JSON admin permissions.
- [ ] Add admin CRUD routes for categories, frames, frame assets, stickers, effects, slides, and fonts.
- [ ] Build code-based writable serializers; include model and serializer validation for active lookup codes, category depth/app, asset child/variant, tag codes, and TTF extension.
- [ ] Implement documented nested category and frame response payloads, absolute file URLs, constraints replacement-on-present semantics, and frame-assets filtering.
- [ ] Configure the global JSON exception handler, including validation, not-found, and method-not-allowed responses.
- [ ] Remove the unexpected `id` column from the four tag join tables if strict physical schema parity is required, then create/apply migrations.
- [ ] Add CORS/CSRF settings, correct the DB username variable, and harden environment defaults.
- [ ] Add Unfold, WhiteNoise, S3/local storage configuration, dependencies, and startup/deploy files.
- [ ] Add idempotent JSON `seed_data` and environment-driven `ensure_superuser` commands with all guide seed rows.
- [ ] Fix test discovery and add behavior tests for every checklist requirement against a clean database.

## Boundary of this audit

The current configured PostgreSQL database was read-only inspected. Its migrations and declared columns/constraints are present, but no destructive database reset was performed. The guide’s clean-database seeding check could not pass because the seed command and seed files are absent.
