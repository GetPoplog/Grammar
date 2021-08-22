from railroad import Diagram, Choice, Comment, NonTerminal, Sequence, Terminal, Skip, Optional, ZeroOrMore, OneOrMore
import sys
import pymustache
import io

ALLOWED_NAMES = {
    "Comment": Comment,
    "Diagram": Diagram, 
    "Choice": Choice, 
    "Comment": Comment, 
    "NonTerminal": NonTerminal, 
    "Sequence": Sequence, 
    "Terminal": Terminal,
    "Skip": Skip,
    "Optional": Optional,
    "ZeroOrMore": ZeroOrMore,
    "OneOrMore": OneOrMore,
    "undefined": 'undefined'
}

def eval_expression(input_string, allowed_names = {}):
    code = compile(input_string, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"Use of {name} not allowed")
    return eval(code, {"__builtins__": {}}, allowed_names)

def parse_tabatkins_file():
    dump = []
    current = []
    with open( 'pop11_grammar_tabatkins.txt', 'r' ) as file:
        for line in file:
            if line.startswith('//'):
                if current:
                    dump.append( current )
                    current = []
            else:
                current.append( line )
        if current:
            dump.append( current )
    return map( lambda L: ''.join(L), dump )

def diagram2string( diag ):
    with io.StringIO() as buffer:
        diag.writeSvg(buffer.write)   
        return buffer.getvalue()

def svg_list():
    return [ 
        { 'svg': diagram2string( eval_expression(diag_text, ALLOWED_NAMES) ) }
        for diag_text in parse_tabatkins_file() 
    ]

mustache_template = """
<!DOCTYPE html>
<html>
<head>
<title>Pop-11 Grammar</title>
<style type="text/css">
svg.railroad-diagram {
    background-color: hsl(30,20%,95%);
}
svg.railroad-diagram path {
    stroke-width: 3;
    stroke: black;
    fill: rgba(0,0,0,0);
}
svg.railroad-diagram text {
    font: bold 14px monospace;
    text-anchor: middle;
    white-space: pre;
}
svg.railroad-diagram text.diagram-text {
    font-size: 12px;
}
svg.railroad-diagram text.diagram-arrow {
    font-size: 16px;
}
svg.railroad-diagram text.label {
    text-anchor: start;
}
svg.railroad-diagram text.comment {
    font: italic 12px monospace;
}
svg.railroad-diagram g.non-terminal text {
    /*font-style: italic;*/
}
svg.railroad-diagram rect {
    stroke-width: 3;
    stroke: black;
    fill: hsl(120,100%,90%);
}
svg.railroad-diagram rect.group-box {
    stroke: gray;
    stroke-dasharray: 10 5;
    fill: none;
}
svg.railroad-diagram path.diagram-text {
    stroke-width: 3;
    stroke: black;
    fill: white;
    cursor: help;
}
svg.railroad-diagram g.diagram-text:hover path.diagram-text {
    fill: #eee;
}
</style>
</head>

<body>
<h1>Pop-11 Grammar</h1>

{{#DIAGRAMS}}
<div>{{{svg}}}</div>
{{/DIAGRAMS}}

</body>
</html>
"""

def print_tabatkins_grammar_as_html():
    print( pymustache.render( mustache_template, { 'DIAGRAMS': svg_list() } ) )

if __name__ == "__main__":
    print_tabatkins_grammar_as_html()
