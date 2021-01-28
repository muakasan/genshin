from requests_html import HTMLSession
session = HTMLSession()

is_live = False
cont_wrapper_index = 0 if is_live else 1

r = session.get("https://genshin.honeyhunterworld.com/db/char/hutao/")
stat_tables = r.html.find('.data_cont_wrapper')[cont_wrapper_index].find(".add_stat_table")

char_stats = stat_tables[1]
na_stats = stat_tables[2]
skill_stats = stat_tables[3]
burst_stats = stat_tables[4]
talent_mats = stat_tables[5]

d = {}
for tr in skill_stats.find('tr'):
    tds = tr.find('td')
    name = tds[0].text
    if name: # name empty means first row/ lvl 1 lvl2 lvl3 ...
        d[name] = []
        for td in tds[1:]:
            d[name].append(td.text)
print(d)

