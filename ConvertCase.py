import re

import sublime_plugin


def subl_convert_case(view, edit, region, content, case_converter):
    new_content = case_converter(content)

    view.replace(edit, region, new_content)


def parse_casing(content):
    space_parts = content.split(' ')
    dash_parts = content.split('-')
    underscore_parts = content.split('_')

    camel_case_parts = []
    match = re.match('^[^A-Z]+', content)
    if match:
        camel_case_parts.append(match.group(0))
    for match in re.finditer('([A-Z]*)([A-Z])([^A-Z]*)', content):
        if len(match.group(1)) > 1 and len(match.group(3)) > 1:
            # Handle cases with runs of uppercase letters like: "loadHTMLTag".
            # E.g. conversion to snake_case: "loadHTMLTag" -> "load_html_tag"
            camel_case_parts.append(match.group(1))
            camel_case_parts.append(match.group(2) + match.group(3))
        else:
            camel_case_parts.append(match.group(0))

    if content.upper() == content:
        # In the case of SCREAMING_SNAKE_CASE there'll be more camel_case_parts
        # than snake_case_parts, even though it should really be regarded as
        # snake_case. In that case we disregard camel_case_parts.
        patterns = [space_parts, dash_parts, underscore_parts]
    else:
        patterns = [space_parts, dash_parts, underscore_parts, camel_case_parts]

    best_match = max(
        patterns,
        key=lambda l: len(l),
    )

    return best_match


def convert_to_camel_case(self, content):
    parts = parse_casing(content)
    return (
        parts[0][0].lower()
        + parts[0][1:].lower()
        + ''.join(part[0].upper() + part[1:] for part in parts[1:])
    )


def convert_to_pascal_case(self, content):
    parts = parse_casing(content)
    return ''.join(part[0].upper() + part[1:].lower() for part in parts)


def convert_to_snake_case(self, content):
    parts = parse_casing(content)
    return '_'.join(part.lower() for part in parts)


def convert_to_screaming_snake_case(self, content):
    parts = parse_casing(content)
    return '_'.join(part.upper() for part in parts)


def convert_to_kebab_case(self, content):
    parts = parse_casing(content)
    return '-'.join(part.lower() for part in parts)


class BaseCommand:
    def run(self, edit):
        if self.view.sel()[0].empty() and len(self.view.sel()) == 1:
            # No selection
            return

        for region in self.view.sel():
            if region.empty():
                # Empty region
                continue
            else:
                subl_convert_case(
                    self.view,
                    edit,
                    region,
                    self.view.substr(region),
                    self.converter_func,
                )


class ConvertToCamelCase(BaseCommand, sublime_plugin.TextCommand):
    converter_func = convert_to_camel_case


class ConvertToPascalCase(BaseCommand, sublime_plugin.TextCommand):
    converter_func = convert_to_pascal_case


class ConvertToSnakeCase(BaseCommand, sublime_plugin.TextCommand):
    converter_func = convert_to_snake_case


class ConvertToScreamingSnakeCase(BaseCommand, sublime_plugin.TextCommand):
    converter_func = convert_to_screaming_snake_case


class ConvertToKebabCase(BaseCommand, sublime_plugin.TextCommand):
    converter_func = convert_to_kebab_case
