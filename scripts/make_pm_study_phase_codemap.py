import pandas as pd
from make_zenodo_files import MDE_HOME

# Study phase
PM_STUDY_CODEMAP_F = MDE_HOME / "mkpy/pm_study_codemap.tsv"

# read the item information table
pm_items = pd.read_csv(
    MDE_HOME / "mkpy/pm_item_id_by_scn.tsv", delim_whitespace=True
).query("scn in ['studyp1', 'testp1']")


def make_study_phase_codemap():

    print(pm_items.head())
    print(pm_items.tail())

    # code map
    pm_study_codemap_cols = [
        "regexp",
        "study_bin_id",
        "animacy",
        "study_response",
    ] + list(pm_items.columns)

    # stimulus-response tag template as a Python dictionary
    # The key:val pair says "this code sequence gets these tags"
    # The ITEM_ID string will be replaced by the actual 3-digit item number

    study_code_tags = {
        "(#[12]) 8 (ITEM_ID) 1040": (2000, "like"),
        "(#[12]) 8 1040 (ITEM_ID)": (2001, "like"),
        "(#[12]) 1040 8 (ITEM_ID)": (2002, "like"),
        "(#[12]) 8 (ITEM_ID) 2064": (2100, "dislike"),
        "(#[12]) 8 2064 (ITEM_ID)": (2101, "dislike"),
        "(#[12]) 2064 8 (ITEM_ID)": (2102, "dislike"),
        "(#[12]) 8 (ITEM_ID) (?!(1040|2064))": (2003, "no_response"),
    }

    # the new 4-digit "study_bin_id" tag re-codes the match event 1 or 2 with more information
    #
    #  phase animacy response response_timing
    #    phase: study=2
    #    animacy: 1=animate, 2=inanimate
    #    response(0=like, 1=dislike)
    #    response timing: 0=prompted,1,2 anticipation, 3=no response)
    #
    study_code_tags = {
        # animate
        "(#[1]) 8 (ITEM_ID) 1040": (2100, "animate", "like"),
        "(#[1]) 8 1040 (ITEM_ID)": (2101, "animate", "like"),
        "(#[1]) 1040 8 (ITEM_ID)": (2102, "animate", "like"),
        "(#[1]) 8 (ITEM_ID) 2064": (2110, "animate", "dislike"),
        "(#[1]) 8 2064 (ITEM_ID)": (2111, "animate", "dislike"),
        "(#[1]) 2064 8 (ITEM_ID)": (2112, "animate", "dislike"),
        "(#[1]) 8 (ITEM_ID) (?!(1040|2064))": (2103, "animate", "no_response"),
        # inanimate
        "(#[2]) 8 (ITEM_ID) 1040": (2200, "inanimate", "like"),
        "(#[2]) 8 1040 (ITEM_ID)": (2201, "inanimate", "like"),
        "(#[2]) 1040 8 (ITEM_ID)": (2202, "inanimate", "like"),
        "(#[2]) 8 (ITEM_ID) 2064": (2210, "inanimate", "dislike"),
        "(#[2]) 8 2064 (ITEM_ID)": (2211, "inanimate", "dislike"),
        "(#[2]) 2064 8 (ITEM_ID)": (2212, "inanimate", "dislike"),
        "(#[2]) 8 (ITEM_ID) (?!(1040|2064))": (2203, "inanimate", "no_response"),
    }

    #
    # Build a list of codemap lines.

    # The first line says *any* code matching 1 or 2 gets the tags 200, "_any", 2, ... etc.
    # This tags all matching stimulus events, it is not contingent the response.
    # It is not necessary but it is useful here, we will see why shortly.
    study_code_map = [
        ("(#[1234])", 0, "cal", "cal", 0, "study", 0, -1, "cal", "cal"),
        ("(#[12])", 200, "_any", "_any", 2, "study", 2, -1, "_any", "_any"),
    ]

    # plug each row of the pictmem item info into the template and append the
    # result to the list of codemap lines
    for idx, row in pm_items.query("phase == 'study'").iterrows():
        for pattern, tags in study_code_tags.items():
            code_tags = (
                pattern.replace(
                    "ITEM_ID", str(row.item_id)
                ),  # current item number goes in the template
                *(str(t) for t in tags),
                *(str(c) for c in row),  # this adds the rest of the item to the tags
            )
            study_code_map.append(code_tags)

    # convert the list of lines to a pandas.DataFrame and save as a tab separated text file
    pm_study_codemap = pd.DataFrame(study_code_map, columns=pm_study_codemap_cols)
    pm_study_codemap.to_csv(PM_STUDY_CODEMAP_F, sep="\t", index=False)

    print(pm_study_codemap.shape)
    print(pm_study_codemap)