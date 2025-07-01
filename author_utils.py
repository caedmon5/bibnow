# author_utils.py

def parse_responsible_parties(entry):
    """Returns a list of CSL-compatible name dicts from the BibTeX entry."""
    responsible_fields = ["author", "editor", "institution", "organization", "court"]
    for field in responsible_fields:
        if field in entry:
            names = entry[field].split(" and ")
            result = []
            for name in names:
                if "," in name:
                    family, given = [x.strip() for x in name.split(",", 1)]
                    result.append({"family": family, "given": given})
                else:
                    result.append({"literal": name.strip()})
            return result
    return []
