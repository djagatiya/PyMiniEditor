# https://www.dabeaz.com/ply/ply.html

import ply.lex as lex

tokens = (
    "INCLUDE",
    "NUMBER",
    "COMMENT",
    "SYMBOL",
    "STRING",
    "KEY_WORDS"
)

t_COMMENT = r"//.*"
t_INCLUDE = r"\#include"
t_NUMBER = r"\d+"
t_SYMBOL = r"[\-&*<>()={}.,;]"
t_STRING = r"\".+\""
t_KEY_WORDS = r"(auto|break|case|char|const|continue|default|do|double" \
              r"|else|enum|extern|float|for|goto|if|int|long|register" \
              r"|return|short|signed|sizeof|static|struct|switch|typedef" \
              r"|union|unsigned|void|volatile|while)"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def get_c_lexer():
    return lex.lex()
