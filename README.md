ConvertCase
===========
**ConvertCase** allows converting to and from the following "cases" inside
Sublime Text:

- PascalCase
- camelCase
- kebab-case
- snake_case
- SCREAMING_SNAKE_CASE

by adding commands to the Command Palette.


Note that Sublime Text as of some recent version provides these case-conversions
by default:

- lowerCamelCase
- UpperCamelCase
- lowercase
- UPPERCASE
- Title case

How does it work?
-----------------
Put simply, **ConvertCase** detects the current case by counting the number of

- dashes
- underscores
- uppercase letters
- spaces

and the casing is then assumed to be the one with the most occurences.
More precisely we're actually splitting the string and counting the number of
resulting parts.
For uppercase letters there are some caveats, namely that if the string begins
with an uppercase letter we don't split there, and runs of uppercase letters
like in "loadHTMLTag" aren't counted individually -- only the full run is
counted.


Similar projects
----------------
- https://github.com/jdavisclark/CaseConversion
