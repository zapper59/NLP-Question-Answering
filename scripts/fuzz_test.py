from fuzzywuzzy import fuzz
from fuzzywuzzy import process

print(fuzz.ratio("ACME Factory", "ACME Factory Inc."))
print(fuzz.partial_ratio("ACME Factory", "ACME Factory Inc."))

a="Ned Stark"
b="Arya Stark"
b2="King of the andals first of his name"
c="Ned's oldest wife*****************************"

print(process.extract(c, [a,b], scorer=fuzz.ratio))
print(process.extract(c, [a,b,b2], scorer=fuzz.partial_ratio))
print(process.extract(c, [a,b], scorer=fuzz.token_set_ratio))
print(process.extract(c, [a,b], scorer=fuzz.token_sort_ratio))
print(fuzz.partial_ratio(a,c))
print(fuzz.partial_ratio(c,a))
