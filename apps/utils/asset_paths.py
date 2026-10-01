def tag_icon_upload_path(instance, filename):
    return f"tags/{instance.tag_type}/{instance.pk}/{filename}"


def category_cover_upload_path(instance, filename):
    return f"{instance.app.slug}/home/categories/{instance.pk}/cover/{filename}"


def frame_asset_upload_path(instance, filename):
    app_slug = instance.frame.category.app.slug
    category_id = instance.frame.category_id
    return (
        f"{app_slug}/home/frames/{category_id}/{instance.frame_id}/assets/"
        f"{instance.pk}/{filename}"
    )


def sticker_upload_path(instance, filename):
    app_slug = instance.category.app.slug
    return f"{app_slug}/stickers/{instance.category_id}/{instance.pk}/{filename}"


def effect_cover_upload_path(instance, filename):
    app_slug = instance.category.app.slug
    return f"{app_slug}/effects/{instance.category_id}/{instance.pk}/cover/{filename}"


def effect_file_upload_path(instance, filename):
    app_slug = instance.category.app.slug
    return f"{app_slug}/effects/{instance.category_id}/{instance.pk}/file/{filename}"


def slide_cover_upload_path(instance, filename):
    return f"slides/{instance.pk}/{filename}"


def font_upload_path(instance, filename):
    app_slug = instance.category.app.slug
    return f"{app_slug}/fonts/{instance.category_id}/{instance.pk}/{filename}"