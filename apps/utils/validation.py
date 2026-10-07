from django.core.exceptions import ValidationError


def validate_asset_category(asset, expected_variant):
    errors = {}
    if not asset.category_id:
        return
    category = asset.category
    if category.parent_id is None:
        errors["category"] = "Assets must belong to a child category."
    elif not category.variant_id or not category.variant.is_active or category.variant.code != expected_variant:
        errors["category"] = f"This asset requires an active {expected_variant} category variant."

    for field in ("status", "frame_type", "effect_type", "slide_type", "key"):
        lookup = getattr(asset, field, None)
        if lookup is not None and not lookup.is_active:
            errors[field] = "Inactive lookup values cannot be used."

    if errors:
        raise ValidationError(errors)