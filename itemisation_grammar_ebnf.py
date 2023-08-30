INITIAL_GRAMMAR = f"""
EndOfLineComment ::= ';;;' [^#xA]* #xA
BracketedComment ::= '/*' ( [^/] | ( '/' [^*] ) | BracketedComment )* '/'? '*/'

Item ::= Word | String | CharacterConstant | DecimalNumber | RadixNumber

Word ::= InitialWordPart WordPart* | SeparatorChar

InitialWordPart ::= AlphaChar AlnumChar* | SignChar+ | '_'

WordPart ::= '_' (AlnumChar* | SignChar*)

String ::= QuoteChar SingleChar* QuoteChar

CharacterConstant ::= BacktickChar SingleChar BacktickChar?

SingleChar ::= [^#x20#xA] | ('\' #xA ) | EscapedChar

/* SIMPLIFICATION, IGNORING VED ATTRIBUTES */
EscapedChar ::= '\\' ( [btnres@a-zA-Z^_?\\\\\\[] | ']' | '(' '0'* N255 ')' )

/* Numbers from 0 to 255 - SIMPLIFICATION, RADIXES NOT LIMITED */
N255 ::= Decimal255 | RadixIntegerCore
Decimal255 ::= ([1]? [0-9])? [0-9] | [2][0-4][0-9] | [2][5][0-5]

AlphaChar ::= [A-Za-z]
NumChar ::= [0-9]
AlnumChar ::= AlphaChar | NumChar

/*******************************************************************************
| Decimal Numbers
\******************************************************************************/


DecimalNumber ::= DecimalInteger | DecimalRatio | DecimalFloatingPoint

/* Note this may produce a ratio e.g. 23e-2   = 23 * (10 ** -2)  = 23_/100 */
DecimalInteger ::= '-' ? UnsignedDecimalInteger
UnsignedDecimalInteger ::= NumChar+ ([esd] '-'? NumChar+)?

DecimalRatio ::= '_'? UnsignedDecimalRatio
UnsignedDecimalRatio ::= UnsignedDecimalInteger '_' '/' UnsignedDecimalInteger

DecimalFloatingPoint ::= '-'? UnsignedDecimalFloatingPoint 
UnsignedDecimalFloatingPoint ::= UnsignedDecimalInteger '.' NumChar+ ( [esd] '-'? NumChar+ )

DecimalComplexNumber ::= '_'? UnsignedDecimalReal ('_+:'|'_-:') UnsignedDecimalReal
UnsignedDecimalReal ::= UnsignedDecimalInteger | UnsignedDecimalRatio | UnsignedDecimalFloatingPoint

/*******************************************************************************
| Other Radix Numbers
\******************************************************************************/


RadixNumber ::= { ' | '.join( f"Radix{i}Number" for i in range(2, 36+1) ) }
RadixIntegerCore ::= { ' | '.join( f"Radix{i}IntegerCore" for i in range(2, 36+1) ) }

"""


RADIX_TEMPLATE = """
/*******************************************************************************
| Radix{0}Numbers
\******************************************************************************/


Radix{0}Number ::= Radix{0}Integer | Radix{0}Ratio | Radix{0}FloatingPoint | Radix{0}ComplexNumber

Radix{0}Integer ::= '-'? Radix{0} ':' Radix{0}IntegerCore | Radix{0} ':' '-' Radix{0}IntegerCore
Radix{0}IntegerCore ::= Radix{0}AppropriateChar+ ( [esd] '-'? NumChar+ )

Radix{0}Ratio ::= '-'? Radix{0} ':' Radix{0}IntegerCore '_/' Radix{0}IntegerCore

Radix{0}FloatingPoint ::= '-'? Radix{0} ':' Radix{0}FloatingPointCore | Radix{0} ':' '-' Radix{0}FloatingPointCore
Radix{0}FloatingPointCore ::= Radix{0}AppropriateChar+ '.' Radix{0}AppropriateChar+ ( [esd] '-'? NumChar+ )

Radix{0}ComplexNumber ::= '-'? Radix{0} ':' Radix{0}RealCore ('_+:'|'_-:') Radix{0}RealCore

Radix{0}RealCore ::= Radix{0}IntegerCore | Radix{0}RatioCore | Radix{0}FloatingPointCore
"""

APPENDIX = """
Radix2 ::= '0'* '2'
Radix3 ::= '0'* '3'
Radix4 ::= '0'* '4'
Radix5 ::= '0'* '5'
Radix6 ::= '0'* '6'
Radix7 ::= '0'* '7'
Radix8 ::= '0'* '8'
Radix9 ::= '0'* '9'
Radix10 ::= '0'* '1' '0'
Radix11 ::= '0'* '1' '1'
Radix12 ::= '0'* '1' '2'
Radix13 ::= '0'* '1' '3'
Radix14 ::= '0'* '1' '4'
Radix15 ::= '0'* '1' '5'
Radix16 ::= '0'* '1' '6'
Radix17 ::= '0'* '1' '7'
Radix18 ::= '0'* '1' '8'
Radix19 ::= '0'* '1' '9'
Radix20 ::= '0'* '2' '0'
Radix21 ::= '0'* '2' '1'
Radix22 ::= '0'* '2' '2'
Radix23 ::= '0'* '2' '3'
Radix24 ::= '0'* '2' '4'
Radix25 ::= '0'* '2' '5'
Radix26 ::= '0'* '2' '6'
Radix27 ::= '0'* '2' '7'
Radix28 ::= '0'* '2' '8'
Radix29 ::= '0'* '2' '9'
Radix30 ::= '0'* '3' '0'
Radix31 ::= '0'* '3' '1'
Radix32 ::= '0'* '3' '2'
Radix33 ::= '0'* '3' '3'
Radix34 ::= '0'* '3' '4'
Radix35 ::= '0'* '3' '5'
Radix36 ::= '0'* '3' '6'


Radix2AppropriateChar ::= [0-1]
Radix3AppropriateChar ::= [0-2]
Radix4AppropriateChar ::= [0-3]
Radix5AppropriateChar ::= [0-4]
Radix6AppropriateChar ::= [0-5]
Radix7AppropriateChar ::= [0-6]
Radix8AppropriateChar ::= [0-7]
Radix9AppropriateChar ::= [0-8]
Radix10AppropriateChar ::= [0-9]
Radix11AppropriateChar ::= [0-9A]
Radix12AppropriateChar ::= [0-9A-B]
Radix13AppropriateChar ::= [0-9A-C]
Radix14AppropriateChar ::= [0-9A-D]
Radix15AppropriateChar ::= [0-9A-E]
Radix16AppropriateChar ::= [0-9A-F]
Radix17AppropriateChar ::= [0-9A-G]
Radix18AppropriateChar ::= [0-9A-H]
Radix19AppropriateChar ::= [0-9A-I]
Radix20AppropriateChar ::= [0-9A-J]
Radix21AppropriateChar ::= [0-9A-K]
Radix22AppropriateChar ::= [0-9A-L]
Radix23AppropriateChar ::= [0-9A-M]
Radix24AppropriateChar ::= [0-9A-N]
Radix25AppropriateChar ::= [0-9A-O]
Radix26AppropriateChar ::= [0-9A-P]
Radix27AppropriateChar ::= [0-9A-Q]
Radix28AppropriateChar ::= [0-9A-R]
Radix29AppropriateChar ::= [0-9A-S]
Radix30AppropriateChar ::= [0-9A-T]
Radix31AppropriateChar ::= [0-9A-U]
Radix32AppropriateChar ::= [0-9A-V]
Radix33AppropriateChar ::= [0-9A-W]
Radix34AppropriateChar ::= [0-9A-X]
Radix35AppropriateChar ::= [0-9A-Y]
Radix36AppropriateChar ::= [0-9A-Z]
"""

if __name__ == "__main__":
    print( INITIAL_GRAMMAR )
    for i in range( 2, 36 + 1 ):
        print( RADIX_TEMPLATE.format( i ) )
    print( APPENDIX )
