# Chilean RUN processing.


def runtup(r):
    '''Splits run and validating digit into (run_string, validating_digit_string).

    Comma and decimal point chars are removed.
    First, try to split using the hyphen char '-',
    if fail, use the  last char as validating digit.
    Always remove hyphen.'''
    fixed = r
    fixed = fixed.replace('.','').replace(',','').replace(' ','')
    if len(fixed.split('-')) == 2:
        fixed, vd = fixed.split('-')
    else:
        fixed = fixed.replace('-','')
        fixed, vd = fixed[:-1], fixed[-1]
    return fixed, vd

def validating_digit(run):
    '''Calculate the run validating digit or K.'''

    # Cast input to string then cast individual chars to int.
    factors = zip(str(run).zfill(8), '32765432')
    suma = sum([ int(a)*int(b)  for a,b in factors])
    val = (-suma) % 11
    return {10: 'K', 11: '0'}.get(val, str(val))

def run_is_valid(s):
    '''Test if is a valid chilean RUN string using its validating digit.'''

    is_valid = False
    if s:
        n_str, d_str = runtup(s)
        try:
            n = int(n_str)
        except ValueError:
            pass
        else:
            if 5*10**5 < n < 47*10**6:
                is_valid = d_str.upper() == validating_digit(n)
    return is_valid

def run_clean(s):
    '''To lowercase, use hyphen, remove comma and decimal point.'''

    n, d = runtup(s)
    return '-'.join([n, d.lower()])
