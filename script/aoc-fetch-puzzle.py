#!/usr/bin/env python3

# Downloads Advent of Code Puzzle for the given year and day.
# Author: Ben Bornstein


import argparse
import os
import re
import sys
import textwrap
import urllib.request


Session = os.environ.get('AOC_SESSION', None)
NotSet  = """
error: An Advent of Code Session ID is required.
Please export AOC_SESSION="...";

To find your Advent of Code Session ID, once logged-in to Advent of
Code, use your web inspector to find a request cookie that starts with
"session=..." and copy-and-paste the value into the AOC_SESSION
environment variable.  Sessions values are comprised of digits ([0-9])
and letters ([a-f]) and are nearly 100 characters long, e.g.
'536...be3'.
"""

HTML_a       = re.compile('<a href="(.*?)"[^>]*>(.*?)</a>', re.DOTALL)
HTML_article = re.compile('<article[^>]*>(.*?)</article>' , re.DOTALL)
HTML_code    = re.compile('<code>(.*?)</code>'            , re.DOTALL)
HTML_em      = re.compile('<em>(.*?)</em>'                , re.DOTALL)
HTML_h2      = re.compile('<h2[^>]*>(.*?)</h2>'           , re.DOTALL)
HTML_li      = re.compile('<li>(.*?)</li>'                , re.DOTALL)
HTML_p       = re.compile('(?:<p>|<p\s+[^>]*>)(.*?)</p>'  , re.DOTALL)
HTML_pre     = re.compile('<pre><code>(.*?)</code></pre>' , re.DOTALL)
HTML_span    = re.compile('<span[^>]*>(.*?)</span>'       , re.DOTALL)
HTML_ul      = re.compile('<ul>(.*?)</ul>'                , re.DOTALL)


def fetch (url):
    """Fetches and returns the contents of the given `url` as a UTF-8
    string."""
    headers = { 'Cookie': f'session={Session}' }
    request = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(request) as stream:
        return stream.read()


def replaceAll (text, pattern, transform):
    """Replace all occurences in `text` of the regular expression `pattern`
    with `transform(match)`.  Returns a copy of `text` with all
    replacements made.
    """
    while match := pattern.search(text):
        text = replaceMatch(text, match, transform(match))

    return text


def replaceMatch (text, match, s):
    """Returns `text` with the regular expression `match` replaced by `s`."""
    return text[:match.start(0)] + s + text[match.end(0):]


def replace_a (html):
    """Replaces all HTML anchor elements (`<a href="...">`) in `html` with
    their Markdown equivalent.
    """
    return replaceAll(html, HTML_a, lambda match: f'[{match[2]}]({match[1]})')


def replace_code (html):
    """Replaces all `<code>` elements in `html` with their Markdown
    equivalent.
    """
    return replaceAll(html, HTML_code, lambda match: f'`{match[1]}`')


def replace_em (html):
    """Replaces all `<em>` elements in `html` with their Markdown
    equivalent.
    """
    return replaceAll(html, HTML_em, lambda match: f'**{match[1]}**')


def replace_inline (html):
    """Replaces all HTML inline elements (`<a>`, `<code>`, `<em>`, `<span>`)
    in `html` with their Markdown equivalent.
    """
    return replace_a( replace_code( replace_em( replace_span(html) ) ) )


def replace_span (html):
    """Replaces all `<span>` elements in `html` with their Markdown
    equivalent.
    """
    return stripAll(html, HTML_span)


def savePuzzle (url, filename):
    """Fetches and saves the Advent of Code puzzle description at `url` to
    `filename`, after converting it from HTML to Markdown.
    """
    with open(filename, 'wt') as output:
        html = fetch(url).decode('utf-8')
        pos  = 0

        for pattern in HTML_article, HTML_p, HTML_article, HTML_p, HTML_p:
            if match := pattern.search(html, pos):
                if match[0].startswith('<article'):
                    writeMarkdown_article(match[1], output)
                elif match[0].startswith('<p'):
                    writeMarkdown_p(match[1], output)
                pos = match.end()

    print(f'Wrote {filename}.')


def savePuzzleData (url, filename):
    """Fetches and saves the Advent of Code puzzle data (input) at `url` to
    `filename`.
    """
    with open(filename, 'wb') as output:
        output.write( fetch(url) )

    print(f'Wrote {filename}.')


def stripAll (html, pattern):
    """Replaces all occurences in `text` of the regular expression `pattern`
    with `match[1]`.  For the `HTML_*` patterns defined in this file,
    this has the effect of strippig the HTML tag, but leaving the inner
    text.
    """
    return replaceAll(html, pattern, lambda match: match[1])


def writeMarkdown_article (html, output):
    """Writes the `html` `<article>` to `output` stream as Markdown text."""
    matches = [ ]

    for pattern in HTML_h2, HTML_pre, HTML_p, HTML_ul:
        matches.extend( list( pattern.finditer(html) ) )

    matches.sort(key=lambda match: match.start())

    for match in matches:
        if match[0].startswith('<h2'):
            writeMarkdown_h2(match[1], output)
        elif match[0].startswith('<ul>'):
            writeMarkdown_ul(match[1], output)
        elif match[0].startswith('<p>'):
            writeMarkdown_p(match[1], output)
        elif match[0].startswith('<pre>'):
            writeMarkdown_pre(match[1], output)


def writeMarkdown_h2 (html, output):
    """Writes the `html` `<h2>` to `output` stream as Markdown text."""
    output.write(f'### {html.replace("---", "").strip() }\n\n')


def writeMarkdown_li (html, output):
    """Writes the `html` `<li>` to `output` stream as Markdown text."""
    lines = textwrap.wrap( replace_inline(html) )
    output.write('  - ' + '\n    '.join(lines) + '\n\n')


def writeMarkdown_p (html, output):
    """Writes the `html` `<p>` to `output` stream as Markdown text."""
    output.write(f'{textwrap.fill( replace_inline(html) )}\n\n')


def writeMarkdown_pre (html, output):
    """Writes the `html` `<pre>` to `output` stream as Markdown text."""
    lines = stripAll(html.strip(), HTML_em).split('\n')
    text  = '\n    '.join(lines)
    output.write(f'    {text}' + '\n\n')


def writeMarkdown_ul (html, output):
    """Writes the `html` `<ul>` to `output` stream as Markdown text."""
    for match in HTML_li.finditer(html):
        writeMarkdown_li(match[1], output)


def main ():
    """Downloads Advent of Code Puzzle for the given year and day."""
    p = argparse.ArgumentParser(description=main.__doc__)
    p.add_argument('day'   , type=int)
    p.add_argument('--year', type=int, default='2023')
    p.add_argument('-p', '--puzzle', type=str, metavar='filename', default='README.md')
    p.add_argument('-d', '--puzzle-data', type=str, metavar='filename')

    args = p.parse_args()
    url  = f'https://adventofcode.com/{args.year}/day/{args.day}'

    if Session is None:
        print(NotSet)
        return 2

    if os.path.exists(args.puzzle):
        print(f'Skipping puzzle fetch ("{args.puzzle}" already exists).')
    else:
        savePuzzle(url, args.puzzle)

    if args.puzzle_data:
        filename = args.puzzle_data
    else:
        filename = f'aoc-{args.year}-d{args.day:02d}.txt'

    if os.path.exists(filename):
        print(f'Skipping puzzle data fetch ("{filename}" already exists).')
    else:
        savePuzzleData(f'{url}/input', filename)

    print('done.')


if __name__ == '__main__':
    sys.exit( main() )
