from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from django.db import models
from .bloks import TextBlock, StructuralBlock, GalleryBlock


class FlexPage(Page):
    template = 'project/base.html'
    author = models.CharField(max_length=255, default='')
    content = StreamField(
        [
            ('rich_text', TextBlock()),
            ('image', ImageChooserBlock()),
            ('gallery', GalleryBlock()),
            ('structural', StructuralBlock()),

        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("author"),
        StreamFieldPanel("content"),
    ]
