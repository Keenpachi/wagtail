from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail.core import blocks
import re


class TextBlock(blocks.RichTextBlock):
    class Meta:
        template = "project/rich_text_block.html"
        label = "Rich Text"


class StructuralBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add title")
    text = blocks.RichTextBlock(required=True, help_text='Past text', features=['bold', 'ol', 'hr'])
    local_page = blocks.PageChooserBlock(required=False)
    external_url = blocks.URLBlock(required=False)

    class Meta:
        template = "project/structural_block.html"
        label = "Structural"
        icon = "form"

    def clean(self, value):
        errors = {}

        if 'the' in value.get('title'):
            errors['title'] = ErrorList(["Title cannot contain word 'the'"])

        title_words = [x.lower() for x in value.get('title').split(' ')]
        text_words = [x.lower() for x in re.sub(r'<.*?>', '', str(value.get('text'))).split(' ')]
        if any(x in title_words for x in text_words):
            errors['text'] = ErrorList(["The text cannot contain any words from the title field"])

        if errors:
            raise ValidationError('Validation error in StructBlock', params=errors)

        return super().clean(value)


class GalleryBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True)
    images = blocks.ListBlock(blocks.StructBlock([("raw_image", ImageChooserBlock(required=True)), ], icon='image'))

    class Meta:
        template = "project/images_gallery.html"
        label = 'Gallery'
        icon = 'image'
