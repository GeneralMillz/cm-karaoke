"""Build ../tags.json (artist -> "G|dec,dec") from artist-tags.txt and report coverage.
Run from anywhere: python3 tools/build_tags.py"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
songs = json.load(open(os.path.join(here, '..', 'songs.json')))
tags = {}
for line in open(os.path.join(here, 'artist-tags.txt'), encoding='utf-8'):
    line = line.rstrip('\n')
    if not line or line.startswith('#'): continue
    name, g, dec = line.split('|')
    tags[name] = g + '|' + dec
artists = {a for _, vs in songs for a, _ in vs}
for a in artists:   # whole-category artists in the catalog
    if a.startswith('Showtunes:') and a not in tags: tags[a] = 'M|'
missing = [t for t in tags if t not in artists]
out = {a: v for a, v in tags.items() if a in artists}
json.dump(out, open(os.path.join(here, '..', 'tags.json'), 'w'), ensure_ascii=False, separators=(',', ':'), sort_keys=True)
tot = sum(len(vs) for _, vs in songs)
tagged = sum(1 for _, vs in songs for a, _ in vs if a in out)
print(f'{len(out)} artists tagged; {tagged}/{tot} versions ({tagged/tot:.0%}) covered')
print('names not found in songs.json:', missing)
