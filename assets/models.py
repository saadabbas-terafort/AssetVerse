from django.db import models

# Create your models here.

class BaseLookup(models.Model):
    lable = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    sortorder = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.lable


class Orientation(BaseLookup):
    ...
    
class AssetVariant(BaseLookup):
    ...

class RecordStatus(BaseLookup):
    ...
class FrameKey(BaseLookup):
    ...

class FrameType(BaseLookup):
    ...

class EffectType(BaseLookup):
    ...

class SlideType(BaseLookup):
    ...

class App(models.Model):
    lable = models.CharField(max_length=255)
    slug = models.CharField(max_length=255 )
    status = models.ForeignKey(RecordStatus , on_delete = models.SET_NULL , null=True , blank=True , related_name="apps")
    sortorder = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lable
    
class Tag(models.Model):
    class TagType(models.TextChoices):
        SCREEN = "screen", "Screen"
        LISTING = "listing", "Listing"
        AVAILABILITY = "availability", "Availability"
        VARIANT = "variant", "Variant"
        HASHTAG = "hashtag", "Hashtag"
        LOCALE = "locale", "Locale"
    icon = models.CharField(max_length=500)
    label = models.CharField(max_length=255)
    update_at = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=100)
    tag_type = models.CharField(
        max_length=20,
        choices=TagType.choices
    )
    sortorder = models.IntegerField()
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label


    
class Category(models.Model):
    cover = models.ImageField(max_length=500)
    title = models.CharField(max_length=255)
    actionbar =models.BooleanField(default=True)
    app = models.ForeignKey(App , on_delete =models.CASCADE, related_name ="categories")
    parent = models.ForeignKey("self", on_delete = models.SET_NULL , null = True , blank=True , related_name = "children")
    variant = models.ForeignKey(AssetVariant , on_delete = models.SET_NULL , null = True ,  blank=True , related_name="assetvariant")
    api_option = models.CharField(max_length=255 , blank=True)
    sortorder = models.IntegerField()
    status = models.ForeignKey(RecordStatus , on_delete = models.SET_NULL , null=True , blank=True , related_name="categories")
    tags = models.ManyToManyField(Tag , blank=True , related_name="categories")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(Orientation , on_delete = models.CASCADE , related_name ="orientation")
    
    def __str__(self):
        return self.title
    
class Frame(models.Model):
    cover = models.ImageField(max_length=500)
    title = models.CharField(max_length=355)
    category = models.ForeignKey(Category , on_delete = models.CASCADE , related_name ="frames")
    frame_type = models.ForeignKey(FrameType ,on_delete = models.SET_NULL , null = True , blank=True , related_name ="frames")
    status = models.ForeignKey(RecordStatus , on_delete = models.SET_NULL , null=True , blank=True , related_name="frames")
    sortorder = models.IntegerField()
    editor = models.CharField(max_length = 255 , blank=True)
    ratio_height = models.CharField(null = True  , blank = True)
    ratio_width = models.CharField(null = True  , blank = True)
    frame_key = models.ForeignKey(FrameKey , on_delete = models.SET_NULL , null = True , blank = True , related_name = "frames")
    tags = models.ManyToManyField(Tag , blank=True , related_name="frames" )
    image_picker = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    
    def __str__(self):
        return self.title


class Sticker(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="stickers")
    image = models.ImageField(max_length=500)
    tags = models.ManyToManyField(Tag,blank=True,related_name="stickers")
    status = models.ForeignKey(RecordStatus,on_delete=models.SET_NULL,null=True,blank=True,related_name="stickers" )
    sort_order = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Font(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="fonts"
    )
    file = models.FileField(max_length=500)
    status = models.ForeignKey(
        RecordStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fonts"
    )
    sort_order = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="fonts"
    )
    def __str__(self):
        return self.title
    
class Slide(models.Model):
    title = models.CharField(max_length=255)
    cover = models.ImageField(max_length=500)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="slides"
    )
    slide_type = models.ForeignKey(
        SlideType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="slides"
    )
    status = models.ForeignKey(
        RecordStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="slides"
    )
    sort_order = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title



class Effect(models.Model):
    cover = models.ImageField(max_length=500)
    title = models.CharField(max_length=255)
    effect = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="effects"
    )
    effect_type = models.ForeignKey(
        EffectType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="effects"
    )
    status = models.ForeignKey(
        RecordStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="effects"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    sortorder = models.IntegerField()
    file = models.FileField(max_length=500)

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="effects"
    )

    def __str__(self):
        return self.title