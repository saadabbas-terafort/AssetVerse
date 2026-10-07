import json
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Idempotently upsert app and lookup rows from JSON files under seeds/."

    @transaction.atomic
    def handle(self, *args, **options):
        seed_dir = Path(settings.BASE_DIR) / "seeds"
        files = sorted(seed_dir.glob("*.json")) if seed_dir.exists() else []
        if not files:
            raise CommandError(f"No seed JSON files found under {seed_dir}.")

        count = 0
        for seed_file in files:
            try:
                payload = json.loads(seed_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise CommandError(f"Could not read {seed_file.name}: {exc}") from exc

            app_label = payload.get("app_label")
            models_data = payload.get("models")
            if not app_label or not isinstance(models_data, dict):
                raise CommandError(f"{seed_file.name} must define app_label and a models object.")

            for model_name, rows in models_data.items():
                if "." in model_name:
                    model_app, model_class = model_name.split(".", 1)
                else:
                    model_app, model_class = app_label, model_name
                model = apps.get_model(model_app, model_class)
                if not isinstance(rows, list):
                    raise CommandError(f"{model_name} in {seed_file.name} must be a list.")

                field_names = {field.name for field in model._meta.fields}
                for row in rows:
                    if not isinstance(row, dict):
                        raise CommandError(f"Rows for {model_name} must be JSON objects.")
                    values = dict(row)
                    if "is_active" in field_names:
                        values.setdefault("is_active", True)
                    key_field = "code" if "code" in field_names else "slug" if "slug" in field_names else None
                    if key_field is None or key_field not in values:
                        raise CommandError(f"Each {model_name} row needs a code or slug upsert key.")
                    lookup = {key_field: values.pop(key_field)}
                    defaults = {key: value for key, value in values.items() if key in field_names}
                    model.objects.update_or_create(defaults=defaults, **lookup)
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded or updated {count} rows from {len(files)} file(s)."))
