from django.conf import settings
from django.template import (Template, Parser, TemplateEncodingError,
                             StringOrigin, tag_re, Token, BLOCK_TAG_START,
                             VARIABLE_TAG_START, TOKEN_VAR, TOKEN_BLOCK,
                             COMMENT_TAG_START, TRANSLATOR_COMMENT_MARK,
                             TOKEN_COMMENT, TOKEN_TEXT)
from django.utils.functional import Promise
from django.utils.encoding import is_protected_type, DjangoUnicodeDecodeError

# extracted code from django 1.5

def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first, saves 30-40% when s is an instance of
    # text_type. This function gets called often in that setting.
    if isinstance(s, unicode):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                try:
                    s = unicode(bytes(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    s = ' '.join([force_text(arg, encoding, strings_only,
                            errors) for arg in s])
        else:
            # Note: We use .decode() here, instead of text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise DjangoUnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join([force_text(arg, encoding, strings_only,
                    errors) for arg in s])
    return s

def smart_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a text object representing 's' -- unicode on Python 2 and str on
    Python 3. Treats bytestrings using the 'encoding' codec.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, Promise):
        # The input is the result of a gettext_lazy() call.
        return s
    return force_text(s, encoding, strings_only, errors)

class Template1_5(Template):
    def __init__(self, template_string, origin=None,
                 name='<Unknown Template>'):
        try:
            template_string = smart_text(template_string)
        except UnicodeDecodeError:
            raise TemplateEncodingError("Templates can only be constructed "
                                        "from unicode or UTF-8 strings.")
        if settings.TEMPLATE_DEBUG and origin is None:
            origin = StringOrigin(template_string)
        self.nodelist = compile_string(template_string, origin)
        self.name = name

def compile_string(template_string, origin):
    "Compiles template_string into NodeList ready for rendering"
    #if settings.TEMPLATE_DEBUG:
        #from django.template.debug import DebugLexer, DebugParser
        #lexer_class, parser_class = DebugLexer, DebugParser
    #else:
    lexer_class, parser_class = Lexer, Parser
    lexer = lexer_class(template_string, origin)
    parser = parser_class(lexer.tokenize())
    return parser.parse()

class Lexer(object):
    def __init__(self, template_string, origin):
        self.template_string = template_string
        self.origin = origin
        self.lineno = 1
        self.verbatim = False

    def tokenize(self):
        """
        Return a list of tokens from a given template_string.
        """
        in_tag = False
        result = []
        for bit in tag_re.split(self.template_string):
            if bit:
                result.append(self.create_token(bit, in_tag))
            in_tag = not in_tag
        return result

    def create_token(self, token_string, in_tag):
        """
        Convert the given token string into a new Token object and return it.
        If in_tag is True, we are processing something that matched a tag,
        otherwise it should be treated as a literal string.
        """
        if in_tag and token_string.startswith(BLOCK_TAG_START):
            # The [2:-2] ranges below strip off *_TAG_START and *_TAG_END.
            # We could do len(BLOCK_TAG_START) to be more "correct", but we've
            # hard-coded the 2s here for performance. And it's not like
            # the TAG_START values are going to change anytime, anyway.
            block_content = token_string[2:-2].strip()
            if self.verbatim and block_content == self.verbatim:
                self.verbatim = False
        if in_tag and not self.verbatim:
            if token_string.startswith(VARIABLE_TAG_START):
                token = Token(TOKEN_VAR, token_string[2:-2].strip())
            elif token_string.startswith(BLOCK_TAG_START):
                if block_content[:9] in ('verbatim', 'verbatim '):
                    self.verbatim = 'end%s' % block_content
                token = Token(TOKEN_BLOCK, block_content)
            elif token_string.startswith(COMMENT_TAG_START):
                content = ''
                if token_string.find(TRANSLATOR_COMMENT_MARK):
                    content = token_string[2:-2].strip()
                token = Token(TOKEN_COMMENT, content)
        else:
            token = Token(TOKEN_TEXT, token_string)
        token.lineno = self.lineno
        self.lineno += token_string.count('\n')
        return token

# end extract

