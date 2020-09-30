import numpy as np
from itertools import product
import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.logic import POSform

# Montar expressão a partir de tabela
def expessionFromTable(table):
    symbols = table[0][:-1]
    if (len(symbols) > 10):
        return "Entrada muito grande :/ máximo são 10 colunas."

    s = sympy.symbols(symbols)

    minterms = []
    dontcares = []
    for i in range(1, len(table)):
        line = [int (n) for n in table[i]]
        if (line[-1] == 1):
            minterms.append(line[:-1])
        elif (line[-1] == -1):
            dontcares.append(line[:-1])

    expression = POSform(s, minterms, dontcares)
    return expression


# Tabela a partir de expressão
def tableFromExpression(op):
    reserved = ['&', '|', '^', '~', '(', ')', ' ', '>', '<', '.', '!']
    
    # Substituindo alguns caracteres de entrada para ajudar o Sympy
    if ('>' in op and '>>' not in op):
        op = op.replace('>', '>>')
    if ('<' in op and '<<' not in op):
        op = op.replace('<', '<<')
    if ('!' in op):
        op = op.replace('!', '~')
    if ('.' in op):
        op = op.replace('.', '&')

    elements = []
    for element in op:
        if (element not in reserved and element not in elements):
            elements.append(element)

    if (len(elements) > 10):
        return "Muito grande :/ a expressão pode ter no máximo 10 elementos diferentes."    
        
    s = sympy.symbols(elements)
    parsed_op = parse_expr(op)
    
    n = len(elements)
    states = [p for p in product([1, 0], repeat=n)]
    
    result_str = ''
    result_str +=  f"{' '.join(elements)} || {parsed_op} \n"
    values = {}
    for state in reversed(states):
        for i in range(len(elements)):
            values[s[i]] = state[i]
            
        result = parsed_op.subs(values)
        result_str += f"{' '.join([str(n) for n in state])}  ||  {int(result==True)}\n"
    
    return result_str