"""Resume Parser — PDF, DOCX, TXT extraction and section segmentation."""
import re
from io import BytesIO


def extract_text(file_bytes: bytes, file_format: str) -> str:
    fmt = file_format.lower().strip(".")
    if fmt == "pdf":
        from pdfminer.high_level import extract_text as pdf_extract
        return pdf_extract(BytesIO(file_bytes))
    elif fmt in ("docx", "doc"):
        from docx import Document
        doc = Document(BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])
    elif fmt == "txt":
        return file_bytes.decode("utf-8", errors="ignore")
    raise ValueError(f"Unsupported format: {file_format}")


def _extract_section(text, keywords):
    lines = text.split("\n")
    all_headers = ["education","experience","skills","projects","certifications","achievements","awards",
        "summary","objective","work history","technical skills","professional experience",
        "contact","references","publications","interests","languages","courses","training"]
    start = -1
    end = len(lines)
    for i, line in enumerate(lines):
        cl = line.strip().lower().strip(":- ")
        if any(k in cl for k in keywords) and len(cl) < 40:
            start = i + 1
            continue
        if start >= 0 and i > start:
            if any(k in cl for k in all_headers if k not in keywords) and len(cl) < 40:
                end = i
                break
    return "\n".join(lines[start:end]).strip() if start >= 0 else ""


def parse_sections(text):
    return {
        "personal_details": _extract_personal(text),
        "education": _extract_education(text),
        "skills": _extract_skills(text),
        "work_experience": _extract_experience(text),
        "projects": _extract_projects(text),
        "certifications": _extract_certs(text),
        "achievements": _extract_achievements(text),
        "raw_text": text
    }


def _extract_personal(text):
    d = {"name":"","email":"","phone":"","linkedin":"","github":""}
    em = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    if em: d["email"] = em[0]
    ph = re.findall(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if ph: d["phone"] = ph[0]
    li = re.findall(r'linkedin\.com/in/([\w-]+)', text, re.I)
    if li: d["linkedin"] = f"linkedin.com/in/{li[0]}"
    gh = re.findall(r'github\.com/([\w-]+)', text, re.I)
    if gh: d["github"] = f"github.com/{gh[0]}"
    for line in text.strip().split("\n")[:5]:
        line = line.strip()
        if line and len(line)<60 and not re.match(r'[\w.+-]+@', line):
            if not any(k in line.lower() for k in ["resume","cv","objective","summary"]):
                d["name"] = line; break
    return d


def _extract_education(text):
    sec = _extract_section(text, ["education","academic","qualification"])
    if not sec: return []
    result = []
    for line in sec.split("\n"):
        line = line.strip()
        if not line: continue
        entry = {"raw": line}
        yrs = re.findall(r'20\d{2}|19\d{2}', line)
        if yrs: entry["year"] = yrs[-1]
        gpa = re.search(r'(?:CGPA|GPA)[\s:]*(\d+\.?\d*)', line, re.I)
        if gpa: entry["cgpa"] = gpa.group(1)
        result.append(entry)
    return result


def _extract_skills(text):
    sec = _extract_section(text, ["skills","technical skills","core competencies","technologies","tech stack"])
    if not sec: return {"technical":[], "soft":[]}
    soft_kw = ["leadership","communication","teamwork","problem solving","time management",
        "critical thinking","adaptability","creativity","collaboration","project management"]
    tech, soft = [], []
    for line in sec.split("\n"):
        for s in re.split(r'[,|•·]', line.strip().strip("-•*")):
            s = s.strip().strip("-•* ")
            if s and 1 < len(s) < 50:
                if any(k in s.lower() for k in soft_kw): soft.append(s)
                else: tech.append(s)
    return {"technical": tech, "soft": soft}


def _extract_experience(text):
    sec = _extract_section(text, ["experience","work experience","professional experience","employment","internship"])
    if not sec: return []
    result = []
    for block in re.split(r'\n{2,}', sec):
        block = block.strip()
        if len(block) < 10: continue
        lines = block.split("\n")
        entry = {"title": lines[0].strip(), "description": "\n".join(lines[1:]).strip()}
        dm = re.search(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}\s*[-–]\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}))', block, re.I)
        if dm: entry["duration"] = dm.group(1)
        result.append(entry)
    return result


def _extract_projects(text):
    sec = _extract_section(text, ["projects","personal projects","academic projects","key projects"])
    if not sec: return []
    result = []
    for block in re.split(r'\n{2,}', sec):
        block = block.strip()
        if len(block) < 10: continue
        lines = block.split("\n")
        p = {"title": lines[0].strip().strip("-•* "), "description": "\n".join(lines[1:]).strip()}
        tm = re.search(r'(?:Tech|Stack|Tools|Built with)[\s:]+(.+)', block, re.I)
        if tm: p["technologies"] = tm.group(1).strip()
        result.append(p)
    return result


def _extract_certs(text):
    sec = _extract_section(text, ["certifications","certificates","courses","training"])
    if not sec: return []
    result = []
    for line in sec.split("\n"):
        line = line.strip().strip("-•* ")
        if line and len(line) > 5:
            c = {"name": line}
            yr = re.search(r'20\d{2}', line)
            if yr: c["year"] = yr.group()
            result.append(c)
    return result


def _extract_achievements(text):
    sec = _extract_section(text, ["achievements","awards","honors","accomplishments"])
    if not sec: return []
    return [l.strip().strip("-•* ") for l in sec.split("\n") if l.strip() and len(l.strip()) > 5]
