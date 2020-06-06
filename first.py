from copy import deepcopy


def get_first(formulas):
    firsts = {x.name : set() for x in formulas}
    f_copy = deepcopy(firsts)
    while True:
        for f in formulas:
            first_expr(firsts, f.name, f.expression)
        if f_copy == firsts: return firsts
        f_copy = deepcopy(firsts)


def first_atom(firsts, name, atom):
    if atom.type == 'expression':
        first_expr(firsts, name, atom.expr)
    elif atom.type == 'term':
        firsts[name].add(atom.val)
    elif atom.type == 'noterm':
        firsts[name].update(firsts[atom.val])


def first_expr(firsts, name, expr):
    for t in expr:
        need_eps = True
        for a in t:
            first_atom(firsts, name, a)
            if not a.eps:
                need_eps = False 
                break
        if need_eps: firsts[name].add('eps')
        
