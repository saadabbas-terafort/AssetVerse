from django.core.exceptions import ValidationError


def validate_asset_category(asset, expected_variant):
    if not asset.category_id:
        return
    category = asset.category
    if category.parent_id is None:
        raise ValidationError({"category": "Assets must belong to a child category."})
    if not category.variant_id or category.variant.code != expected_variant:
        raise ValidationError(
            {"category": f"This asset requires the {expected_variant} category variant."}
        )