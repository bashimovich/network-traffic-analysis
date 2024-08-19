from django.shortcuts import render, redirect
def main(request):
    return render(request, "CyberChef_v9.32.3.html")
def get_main(request):
    return render(request, 'main.html')
from django.shortcuts import render
import itertools
# -------------- Arguments & Usage -------------- #
def unique(l):
    unique_list = []
    for i in l:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list
# ----------------( Base Settings )---------------- #
mutations_cage = []
basic_mutations = []
trans_keys = []
transformations = [
    {'a': '@'},
    {'b': '8'},
    {'e': '3'},
    {'g': ['9', '6']},
    {'i': ['1', '!']},
    {'o': '0'},
    {'s': ['$', '5']},
    {'t': '7'}
]
for t in transformations:
    for key in t.keys():
        trans_keys.append(key)
def all_var(custom_paddings_only, append_padding, common_paddings_before, common_paddings_after):
    common_paddings = []
    # Paddings
    if "False" in custom_paddings_only or custom_paddings_only == False:
        custom_paddings_only = False
    if (common_paddings_before or common_paddings_after) and not custom_paddings_only:
        common_paddings = [
            '!', '@', '#', '$', '%', '^', '&', '*', ',', '.', '?', '-'
            '123', '234', '345', '456', '567', '678', '789', '890',
            '!@', '@#', '#$', '$%', '%^', '^&', '&*', '*(', '()',
            '!@#', '@#$', '#$%', '$%^', '%^&', '^&*', '&*(', '*()', ')_+',
            '1!1', '2@2', '3#3', '4$4', '5%5', '6^6', '7&7', '8*8', '9(9', '0)0',
            '@2@', '#3#', '$4$', '%5%', '^6^', '&7&', '*8*', '(9(',
            '!@!', '@#@', '!@#$%', '1234', '12345', '123456', '123!@#',
            '!!!', '@@@', '###', '$$$', '%%%', '^^^', '&&&', '***', '(((', ')))', '---', '+++'
        ]
    elif custom_paddings_only:
        for val in custom_paddings_only.split(','):
            if val.strip() != '' and val not in common_paddings:
                common_paddings.append(val)
    if not custom_paddings_only:
        if append_padding:
            for val in append_padding.split(','):
                if val.strip() != '' and val not in common_paddings:
                    common_paddings.append(val)
    common_paddings = unique(common_paddings)
    return custom_paddings_only, append_padding, common_paddings_before, common_paddings_after, common_paddings
# ----------------( Functions )---------------- #
def evalTransformations(w):
    trans_chars = []
    total = 1
    c = 0
    w = list(w)
    for char in w:
        for t in transformations:
            if char in t.keys():
                trans_chars.append(c)
                if isinstance(t[char], list):
                    total *= 3
                else:
                    total *= 2
        c += 1
    return [trans_chars, total]
def mutate(tc, word):
    global trans_keys, mutations_cage, basic_mutations
    i = trans_keys.index(word[tc].lower())
    trans = transformations[i][word[tc].lower()]
    limit = len(trans) * len(mutations_cage)
    c = 0
    for m in mutations_cage:
        w = list(m)
        if isinstance(trans, list):
            for tt in trans:
                w[tc] = tt
                transformed = ''.join(w)
                mutations_cage.append(transformed)
                c += 1
        else:
            w[tc] = trans
            transformed = ''.join(w)
            mutations_cage.append(transformed)
            c += 1

        if limit == c:
            break

    return mutations_cage
def mutations_handler(kword, trans_chars, total, outfile):
    global mutations_cage, basic_mutations
    container = []
    for word in basic_mutations:
        mutations_cage = [word.strip()]
        for tc in trans_chars:
            results = mutate(tc, kword)
        container.append(results)
    for m_set in container:
        for m in m_set:
            basic_mutations.append(m)
    basic_mutations = unique(basic_mutations)
    with open(f'{outfile}', 'a') as wordlist:
        for m in basic_mutations:
            wordlist.write(m + '\n')
def mutateCase(word):
    trans = list(map(''.join, itertools.product(
        *zip(word.upper(), word.lower()))))
    return trans
def caseMutationsHandler(word, mutability, outfile):
    global basic_mutations
    case_mutations = mutateCase(word)
    for m in case_mutations:
        basic_mutations.append(m)
    if not mutability:
        basic_mutations = unique(basic_mutations)
        with open(f'{outfile}', 'a') as wordlist:
            for m in basic_mutations:
                wordlist.write(m + '\n')
def append_numbering_func(append_numbering,_max, outfile):

    first_cycle = True
    previous_list = []
    lvl = append_numbering

    with open(f'{outfile}', 'a') as wordlist:
        for word in basic_mutations:
            for i in range(1, lvl+1):
                for k in range(1, _max):
                    if first_cycle:
                        wordlist.write(f'{word}{str(k).zfill(i)}\n')
                        wordlist.write(f'{word}_{str(k).zfill(i)}\n')
                        previous_list.append(f'{word}{str(k).zfill(i)}')

                    else:
                        if previous_list[k - 1] != f'{word}{str(k).zfill(i)}':
                            wordlist.write(f'{word}{str(k).zfill(i)}\n')
                            wordlist.write(f'{word}_{str(k).zfill(i)}\n')
                            previous_list[k - 1] = f'{word}{str(k).zfill(i)}'

                first_cycle = False
    del previous_list
def mutate_years(years_arr,outfile):
    current_mutations = basic_mutations.copy()
    with open(f'{outfile}', 'a') as wordlist:
        for word in current_mutations:
            for y in years_arr:
                wordlist.write(f'{word}{y}\n')
                wordlist.write(f'{word}_{y}\n')
                wordlist.write(f'{word}{y[2:]}\n')
                basic_mutations.append(f'{word}{y}')
                basic_mutations.append(f'{word}_{y}')
                basic_mutations.append(f'{word}{y[2:]}')

    del current_mutations
def check_underscore(word, pos):
    if word[pos] == '_':
        return True
    else:
        return False
def append_paddings_before_func(common_padding_before,common_paddings, outfile):
    current_mutations = basic_mutations.copy()
    with open(f'{outfile}', 'a') as wordlist:
        for word in current_mutations:
            for val in common_paddings:
                wordlist.write(f'{val}{word}\n')
                if not check_underscore(val, -1):
                    wordlist.write(f'{val}_{word}\n')
    del current_mutations
def append_paddings_after_func(common_paddings_after,common_paddings, outfile):

    current_mutations = basic_mutations.copy()

    with open(f'{outfile}', 'a') as wordlist:
        for word in current_mutations:
            for val in common_paddings:
                wordlist.write(f'{word}{val}\n')
                if not check_underscore(val, 0):
                    wordlist.write(f'{word}_{val}\n')

    del current_mutations
def calculate_output(keyw, years, common_paddings_after, common_paddings_before, append_numbering, years_arr, common_paddings, _max):
    global trans_keys
    c = 0
    total = 1
    basic_total = 1
    basic_size = 0
    size = 0
    numbering_count = 0
    numbering_size = 0

    # Basic mutations calc
    for char in keyw:
        if char in trans_keys:
            i = trans_keys.index(keyw[c].lower())
            trans = transformations[i][keyw[c].lower()]
            basic_total *= (len(trans) + 2)
        else:
            basic_total = basic_total * 2 if char.isalpha() else basic_total

        c += 1

    total = basic_total
    basic_size = total * (len(keyw) + 1)
    size = basic_size

    # Words numbering mutations calc
    if append_numbering:
        word_len = len(keyw) + 1
        first_cycle = True
        previous_list = []
        lvl = int(append_numbering)

        for w in range(0, total):
            for i in range(1, lvl+1):
                for k in range(1, _max):
                    n = str(k).zfill(i)
                    if first_cycle:
                        numbering_count += 2
                        numbering_size += (word_len * 2) + (len(n) * 2) + 1
                        previous_list.append(f'{w}{n}')

                    else:
                        if previous_list[k - 1] != f'{w}{n}':
                            numbering_size += (word_len * 2) + (len(n) * 2) + 1
                            numbering_count += 2
                            previous_list[k - 1] = f'{w}{n}'

                first_cycle = False

        del previous_list

    # Adding years mutations calc
    if years:
        patterns = 3
        year_chars = 4
        _year = 5
        year_short = 2
        yrs = len(years_arr)
        size += (basic_size * patterns * yrs) + (basic_total * year_chars *
                                                 yrs) + (basic_total * _year * yrs) + (basic_total * year_short * yrs)
        total += total * len(years_arr) * 3
        basic_total = total
        basic_size = size

    # Common paddings mutations calc
    patterns = 2

    if common_paddings_after or common_paddings_before:
        paddings_len = len(common_paddings)
        pads_wlen_sum = sum([basic_total*len(w) for w in common_paddings])
        _pads_wlen_sum = sum([basic_total*(len(w)+1) for w in common_paddings])

        if common_paddings_after and common_paddings_before:
            size += ((basic_size * patterns * paddings_len) +
                     pads_wlen_sum + _pads_wlen_sum) * 2
            total += (total * len(common_paddings) * 2) * 2

        elif common_paddings_after or common_paddings_before:
            size += (basic_size * patterns * paddings_len) + \
                pads_wlen_sum + _pads_wlen_sum
            total += total * len(common_paddings) * 2

    return [total + numbering_count, size + numbering_size]
def check_mutability(word):
    global trans_keys
    m = 0
    for char in word:
        if char in trans_keys:
            m += 1
    return m
def chill():
    pass
# Create your views here.
def generate_password(words, append_numbering, numbering_limit, years, append_padding_post, common_paddings_before_post, common_paddings_after_post, custom_paddings_only_post, outfile):
    custom_paddings_only, append_padding, common_paddings_before, common_paddings_after, common_paddings =  all_var(custom_paddings_only_post, append_padding_post, common_paddings_before_post, common_paddings_after_post)
    outfile = outfile + ".txt"
    _max = numbering_limit + \
        1 if numbering_limit and isinstance(numbering_limit, int) else 51
    # Create years list
            
    if years:
        years_arr = []
        if years.count(',') == 0 and years.count('-') == 0 and years.isdecimal() and int(years) >= 1000 and int(years) <= 3200:
            years_arr.append(str(years))
        elif years.count(',') > 0:
            for year in years.split(','):
                if year.strip() != '' and year.isdecimal() and int(year) >= 1000 and int(year) <= 3200:
                    years_arr.append(year)
                else:
                    print('Illegal year(s) input. Acceptable years range: 1000 - 3200.')
        elif years.count('-') == 1:
            years_range = years.split('-')
            start_year = years_range[0]
            end_year = years_range[1]

            if (start_year.isdecimal() and int(start_year) < int(end_year) and int(start_year) >= 1000) and (end_year.isdecimal() and int(end_year) <= 3200):
                for y in range(int(years_range[0]), int(years_range[1])+1):
                    years_arr.append(str(y))
            else:
                print('Illegal year(s) input. Acceptable years range: 1000 - 3200.')
        else:
            print('Illegal year(s) input. Acceptable years range: 1000 - 3200.')

    global basic_mutations, mutations_cage
    keywords = []
    for w in words.split(','):
        if w.strip().isdecimal():
            print('Unable to mutate digit-only keywords.')
        elif w.strip() not in [None, '']:
            keywords.append(w.strip())

    # Calculate total words and size of output
    open(f'{outfile}', "w").close()
    for word in keywords:
        mutability = check_mutability(word.lower())
        # Produce case mutations
        caseMutationsHandler(word.lower(), mutability, outfile)
        # Append numbering
        if append_numbering:
            append_numbering_func(append_numbering,_max, outfile)
        # Handle years
        if years:
            mutate_years(years_arr,outfile)
        # Append common paddings
        if common_paddings_after or custom_paddings_only:
            append_paddings_after_func(common_paddings_after,common_paddings, outfile)
        if common_paddings_before:
            append_paddings_before_func(common_paddings_before,common_paddings, outfile)
        basic_mutations = []
        mutations_cage = []

