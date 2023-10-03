import re
import markdown
import nh3
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from markdown.extensions.codehilite import CodeHiliteExtension
from django.utils.safestring import mark_safe


class HighlightCodeBlockProcessor(Postprocessor):
    line = re.compile(r"(<span.*>.*)§§(.*)§§(.*</span>)*", re.MULTILINE)

    @staticmethod
    def match_bold(code):
        if code.group(3) is not None:
            replaced_code = f"{code.group(1)}<b>{code.group(2)}</b>{code.group(3)}"
            return replaced_code
        return f"{code.group(1)}<b>{code.group(2)}</b>"

    def run(self, text):
        return self.line.sub(self.match_bold, text)


class HighlightCodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(
            HighlightCodeBlockProcessor(md), "custom-highlighter", 30
        )


def bleach_md(markdown_content, allow_images=False):
    allowed_tags = [
        "p",
        "a",
        "code",
        "pre",
        "blockquote",
        "strong",
        "em",
        "br",
        "b",
        "i",
        "ul",
        "li",
        "div",
        "span",
        "h1", "h2", "h3", "h4", "h5", "h6"
        "sup",
        "ol",
        "hr",
    ]
    allowed_attributes = {
        "code": {"class"},
        "a": {"href"},
        "div": {"class"},
        "span": {"class"},
        "sup": {"id"},
    }
    protocols = set()
    if not markdown_content:
        return ""
    if allow_images:
        allowed_tags.append("img")
        allowed_attributes["img"] = {"alt", "src"}
        protocols.add("data")
    cleaned = nh3.clean(
        markdown.markdown(
            markdown_content,
            extensions=[
                "fenced_code",
                "footnotes",
                CodeHiliteExtension(
                    guess_lang=False,
                    linenums=True,
                    linenos="inline",
                    linespans="line",
                    startinline=True,
                ),
                HighlightCodeBlockExtension(),
            ],
        ),
        tags=set(allowed_tags),
        attributes=allowed_attributes,
        url_schemes=protocols,
    )
    return cleaned


def md_to_clean_html(content):
    return mark_safe(bleach_md(content))
