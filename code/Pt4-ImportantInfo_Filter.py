import re, gzip
from pathlib import Path

# three-letter → one-letter
AA3 = {"Ala":"A","Arg":"R","Asn":"N","Asp":"D","Cys":"C","Gln":"Q","Glu":"E","Gly":"G",
       "His":"H","Ile":"I","Leu":"L","Lys":"K","Met":"M","Phe":"F","Pro":"P","Ser":"S",
       "Thr":"T","Trp":"W","Tyr":"Y","Val":"V","Ter":"*","Stop":"*","X":"*"}

R3 = re.compile(r'^(?:p\.)?([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$')  # p.Arg29Trp / Arg29Trp
R1 = re.compile(r'^(?:p\.)?([A-Z])(\d+)([A-Z])$')                   # p.R29W / R29W
NP_PAT = re.compile(r'\bNP_\d+\.\d+\b')                              # RefSeq protein accession

def parse_hgvsp(token):
    """Return (pos:int, refAA:str, altAA:str) or None."""
    token = token.split(':')[-1]  # allow "NP_xxx:p.Arg29Trp"
    m = R3.match(token) or R1.match(token)
    if not m: return None
    ref, pos, alt = m.groups()
    if len(ref) > 1:
        ref = AA3.get(ref, '?'); alt = AA3.get(alt, '?')
    return int(pos), ref, alt

def open_text(path: Path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "rt", encoding="utf-8", errors="replace")

def get_info_field(line: str) -> str:
    # If it's a VCF, INFO is col 8 (index 7). If not, treat whole line as INFO.
    parts = line.rstrip("\n").split("\t")
    return parts[7] if len(parts) >= 8 else line.strip()

def extract_records(info: str):
    """Yield (AC:int, accession:str, pos:int, ref:str, alt:str) for each NP_* found."""
    # AC (take first if multiallelic)
    ac = 0
    m = re.search(r'(?:^|;)AC=([^;]+)', info)
    if m:
        try:
            ac = int(m.group(1).split(',')[0])
        except ValueError:
            ac = 0

    # Find VEP/CSQ blob
    m = re.search(r'(?:^|;)(?:vep|CSQ)=([^;]+)', info)
    if not m: 
        return
    blob = m.group(1)

    # Each record is pipe-delimited; records are comma-separated
    for rec in blob.split(','):
        fields = rec.split('|')
        # HGVSp field: "p.Arg29Trp" or "... NP_XXXX:p.Arg29Trp ..."
        hgvsp = next((f for f in fields if f.startswith('p.') or ':p.' in f), None)
        if not hgvsp:
            continue

        # Accession: prefer the one directly before ':p.' if present, else any NP_ in the record
        acc = None
        m2 = re.search(r'(\bNP_\d+\.\d+\b):p\.', hgvsp)
        if m2:
            acc = m2.group(1)
        else:
            # look across fields for NP_* token
            for f in fields:
                m3 = NP_PAT.search(f)
                if m3:
                    acc = m3.group(0)
                    break
        if not acc:
            continue

        parsed = parse_hgvsp(hgvsp)
        if not parsed:
            continue
        pos, refAA, altAA = parsed
        yield ac, acc, pos, refAA, altAA

def main():
    in_path = Path(input("Input file path: ").strip().strip('"').strip("'"))
    out_path = Path(input("Output file path ").strip().strip('"').strip("'"))

    if not in_path.exists():
        print(f"[error] Input not found: {in_path}")
        return

    lines_out = 0
    try:
        with open_text(in_path) as fin, open(out_path, "w", encoding="utf-8", errors="replace") as fout:
            for line in fin:
                if not line or line.startswith('#'):
                    continue
                info = get_info_field(line)
                for ac, acc, pos, refAA, altAA in extract_records(info):
                    fout.write(f"{acc}, AC={ac}, {pos}, {refAA}, {altAA}\n")
                    lines_out += 1
    except Exception as e:
        print(f"[error] {e}")
        return

    if lines_out == 0:
        print(f"[info] No NP_* protein changes found. Wrote empty file: {out_path}")
    else:
        print(f"[done] Wrote {lines_out} line(s) to: {out_path}")

if __name__ == "__main__":
    main()
