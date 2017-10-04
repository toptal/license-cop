from pyparsing import Keyword, quotedString, Suppress, removeQuotes, restOfLine


pod_keyword = Keyword('pod')
pod_name = quotedString.addParseAction(removeQuotes, lambda n: n[0].split('/', maxsplit=1)[0])
pod_definition = pod_keyword + pod_name + Suppress(restOfLine())
grammar = pod_definition


class PodfileParser:
  def get_pod_names(self, content):
      return (match[1] for match in grammar.searchString(content))
