from pyparsing import Literal, quotedString, Suppress, removeQuotes, restOfLine


dependency_keyword = Literal('.dependency')
dependency_name = quotedString.addParseAction(lambda n: n[0].split('/', maxsplit=1)[0])
dependency_definition = dependency_keyword + dependency_name + Suppress(restOfLine())
grammar = dependency_definition


class PodspecParser:
  def parse(self, content):
      return (match[1] for match in grammar.searchString(content))
