import re
import pandas as pd
from make_zenodo_files import MDE_HOME

# test phase codemap name
pm_test_codemap_f = MDE_HOME / "mkpy/pm_codemap.tsv"

# read the item information table
pm_items = pd.read_csv(
    MDE_HOME / "mkpy/pm_item_id_by_scn.tsv", delim_whitespace=True
).query("scn in ['studyp1', 'testp1']")

print(pm_items.head())
print(pm_items.tail())

# test phase codemap column names
pm_test_codemap_cols = [
    "regexp",
    "test_bin_id",
    "animacy",
    "stimulus",
    "test_response",
    "accuracy",
] + list(pm_items.columns)


# test phase template: stimulus, old/new response (include pre-prompt anticipations)
test_code_tags = {
    # new stim animate
    "(#1) 8 (ITEM_ID) 2064": (1100, "animate", "distractor", "new", "cr"),
    "(#1) 8 2064 (ITEM_ID)": (1101, "animate", "distractor", "new", "cr"),
    "(#1) 2064 8 (ITEM_ID)": (1102, "animate", "distractor", "new", "cr"),
    "(#1) 8 (ITEM_ID) 1040": (1110, "animate", "distractor", "old", "fa"),
    "(#1) 8 1040 (ITEM_ID)": (1111, "animate", "distractor", "old", "fa"),
    "(#1) 1040 8 (ITEM_ID)": (1112, "animate", "distractor", "old", "fa"),
    "(#1) 8 (ITEM_ID) (?!(2064|1040))": (1103, "animate", "distractor", "none", "nr"),
    # new stim inanimate
    "(#2) 8 (ITEM_ID) 2064": (1200, "inanimate", "distractor", "new", "cr"),
    "(#2) 8 2064 (ITEM_ID)": (1201, "inanimate", "distractor", "new", "cr"),
    "(#2) 2064 8 (ITEM_ID)": (1202, "inanimate", "distractor", "new", "cr"),
    "(#2) 8 (ITEM_ID) 1040": (1210, "inanimate", "distractor", "old", "fa"),
    "(#2) 8 1040 (ITEM_ID)": (1211, "inanimate", "distractor", "old", "fa"),
    "(#2) 1040 8 (ITEM_ID)": (1212, "inanimate", "distractor", "old", "fa"),
    "(#2) 8 (ITEM_ID) (?!(2064|1040))": (1203, "inanimate", "distractor", "none", "nr"),
    # old stim animate
    "(#3) 8 (ITEM_ID) 1040": (1300, "animate", "studied", "old", "hit"),
    "(#3) 8 1040 (ITEM_ID)": (1301, "animate", "studied", "old", "hit"),
    "(#3) 1040 8 (ITEM_ID)": (1302, "animate", "studied", "old", "hit"),
    "(#3) 8 (ITEM_ID) 2064": (1310, "animate", "studied", "new", "miss"),
    "(#3) 8 2064 (ITEM_ID)": (1311, "animate", "studied", "new", "miss"),
    "(#3) 2064 8 (ITEM_ID)": (1312, "animate", "studied", "new", "miss"),
    "(#3) 8 (ITEM_ID) (?!(2064|1040))": (1303, "animate", "studied", "none", "nr"),
    # old stim inanimate
    "(#4) 8 (ITEM_ID) 1040": (1400, "inanimate", "studied", "old", "hit"),
    "(#4) 8 1040 (ITEM_ID)": (1401, "inanimate", "studied", "old", "hit"),
    "(#4) 1040 8 (ITEM_ID)": (1402, "inanimate", "studied", "old", "hit"),
    "(#4) 8 (ITEM_ID) 2064": (1410, "inanimate", "studied", "new", "miss"),
    "(#4) 8 2064 (ITEM_ID)": (1411, "inanimate", "studied", "new", "miss"),
    "(#4) 2064 8 (ITEM_ID)": (1412, "inanimate", "studied", "new", "miss"),
    "(#4) 8 (ITEM_ID) (?!(2064|1040))": (1403, "inanimate", "studied", "none", "nr"),
}

# initialize the code map to tag stimulus codes, not response contingent
test_code_map = [
    ("(#[1234])", 0, "cal", "cal", "cal", "cal", 0, "test", "cal", "-1", "cal", "cal"),
    (
        "(#[1234])",
        10,
        "_any",
        "_any",
        "_any",
        "_any",
        1,
        "test",
        "_any",
        "-1",
        "_any",
        "_any",
    ),
    (
        "(#[1])",
        11,
        "animate",
        "distractor",
        "_any",
        "_any",
        1,
        "test",
        1,
        "-1",
        "_any",
        "_any",
    ),
    (
        "(#[2])",
        12,
        "inanimate",
        "distractor",
        "_any",
        "_any",
        1,
        "test",
        2,
        "-1",
        "_any",
        "_any",
    ),
    (
        "(#[3])",
        13,
        "animate",
        "studied",
        "_any",
        "_any",
        1,
        "test",
        3,
        "-1",
        "_any",
        "_any",
    ),
    (
        "(#[4])",
        14,
        "inanimate",
        "studied",
        "_any",
        "_any",
        1,
        "test",
        4,
        "-1",
        "_any",
        "_any",
    ),
]

# iterate through the item info and plug the item number into the template lines
for idx, row in pm_items.query("phase == 'test'").iterrows():
    for pattern, tags in test_code_tags.items():
        # condition_id is 1, 2, 3, or 4 only plug into the relevant template lines.
        if re.match(r"^\(#" + str(row.condition_id), pattern):
            code_tags = (
                pattern.replace("ITEM_ID", str(row.item_id)),
                tags[0],
                *(str(t) for t in tags[1:]),
                *(str(c) for c in row),
            )
            test_code_map.append(code_tags)

pm_test_codemap = pd.DataFrame(test_code_map, columns=pm_test_codemap_cols)

# write test demo phase codemap
pm_test_codemap.to_csv(pm_test_codemap_f, sep="\t", index=False)

print(pm_test_codemap.shape)
print(pm_test_codemap)