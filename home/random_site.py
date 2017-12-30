import random
import string
OUTPUT_FILE = '/home/mic/zero/random.txt'
country_tuple = ('Denmark', 'Finland', 'Ireland', 'Luxembourgh', 'United Kingdom', 'Poland', 'All Country', 'Sweden', 'Norway',)
category_tuple = ('All Category', 'CategoryA', 'CategoryB', 'CategoryC', 'CategoryD', 'CategoryE', 'CategoryF', 'CategoryG', 'Other', )
solution_tuple = ('All Solution', 'SolutionA', 'SolutionB', 'SolutionC', 'SolutionD', 'Other', '-N/A-', )


def random_entry():
    #name~site~country~solution~testdirect~testindirect~systdirect~systindirect~proddirect~prodindirect
    r_string = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    name = 'Site {}'.format(r_string)
    testurl_direct = 'https://www.google.co.in?search=testd{}'.format(r_string)
    testurl_indirect = 'https://www.google.co.in?search=testi{}'.format(r_string)
    systurl_direct = 'https://www.google.co.in?search=systd{}'.format(r_string)
    systurl_indirect = 'https://www.google.co.in?search=systi{}'.format(r_string)
    produrl_direct = 'https://www.google.co.in?search=prodd{}'.format(r_string)
    produrl_indirect = 'https://www.google.co.in?search=prodi{}'.format(r_string)
    category = random.choice(category_tuple)
    country = random.choice(country_tuple)
    solution = random.choice(solution_tuple)
    r_entry = [ name, category, country,  solution, testurl_direct, testurl_indirect, systurl_direct, systurl_indirect, produrl_direct, produrl_indirect ] 
    r_entry = '~'.join(r_entry)
    print (r_entry)
    return r_entry
    
with open(OUTPUT_FILE, 'w') as outfile:
    for _ in range(200):
        outfile.write(random_entry() + "\n")
    