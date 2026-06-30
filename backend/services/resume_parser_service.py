"""
ResumeParserService — Phase 2 Implementation

Parses PDF (via PyMuPDF) and DOCX (via python-docx) resume files into
structured ResumeData objects. Uses heuristics + regex for section detection.
"""

import re
import io
import logging
from typing import Optional
from fastapi import UploadFile

import fitz  # PyMuPDF
import docx  # python-docx

from models.resume import ResumeData, Experience, Education, Project

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Section heading keywords (case-insensitive)
# ---------------------------------------------------------------------------
SECTION_KEYWORDS = {
    "summary": [
        "summary", "professional summary", "profile", "about me",
        "objective", "career objective", "professional profile",
        "executive summary",
    ],
    "experience": [
        "experience", "work experience", "employment history",
        "professional experience", "work history", "career history",
        "employment", "positions held",
    ],
    "education": [
        "education", "academic background", "academic history",
        "educational background", "qualifications", "academic qualifications",
    ],
    "skills": [
        "skills", "technical skills", "core skills", "key skills",
        "competencies", "technologies", "tools", "expertise",
        "proficiencies", "skill set",
    ],
    "achievements": [
        "achievements", "accomplishments", "awards", "honors",
        "certifications", "certificates", "recognitions",
    ],
    "projects": [
        "projects", "key projects", "personal projects", "notable projects",
        "side projects", "open source",
    ],
}

# Regex patterns
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", re.IGNORECASE)
PHONE_RE = re.compile(
    r"(\+?\d{1,3}[\s.\-]?)?(\(?\d{2,4}\)?[\s.\-]?)?\d{3,4}[\s.\-]?\d{4}"
)
URL_RE = re.compile(
    r"(https?://[^\s]+|(?:www|linkedin\.com|github\.com)[^\s·•]+)",
    re.IGNORECASE,
)
# Date ranges like "Jan 2020 – Present", "2019-2021", "Jan 2024 · Present"
DATE_RANGE_RE = re.compile(
    r"((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)?\s*,?\s*\d{4})"
    r"\s*(?:–|-|to|—|·|·|)\s*"
    r"((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)?\s*,?\s*\d{4}|Present|Current|Now)",
    re.IGNORECASE,
)

# Month Year patterns like "Jan 2020", "January 2020", "2020"
MONTH_YEAR_RE = re.compile(
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)?\s*,?\s*\d{4}",
    re.IGNORECASE,
)
# Graduation date patterns like "May 2020", "May, 2020", "05/2020", "2020"
GRAD_DATE_RE = re.compile(
    r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)?\s*,?\s*\d{4}|\d{1,2}/\d{4}|\d{4})"
)
GPA_RE = re.compile(r"GPA\s*:?\s*(\d\.\d{1,2})", re.IGNORECASE)
# GRAD_YEAR_RE replaced by MONTH_YEAR_RE for more complete date extraction
DEGREE_KEYWORDS = [
    "bachelor", "master", "phd", "doctorate", "b.s.", "m.s.", "b.e.", "m.e.",
    "b.tech", "m.tech", "b.sc", "m.sc", "mba", "b.a.", "m.a.", "associate",
    "diploma", "certificate", "b.com", "m.com", "vocational",
]
# Skill category label pattern e.g. "Languages & Frameworks: "
SKILL_CATEGORY_RE = re.compile(r"^[A-Za-z ,&/]+:\s*", re.IGNORECASE)

# Bullet characters used in PDFs (unicode + standard)
BULLET_CHARS = "•●▪–—*·◦·•▪●"
# Additional bullet-like characters that may appear due to PDF extraction issues
EXTRA_BULLETS = "�"  # replacement char
ALL_BULLETS = BULLET_CHARS + EXTRA_BULLETS


# ===========================================================================
# Public API
# ===========================================================================

class ResumeParserService:
    """
    Parses uploaded resume files (PDF or DOCX) into structured ResumeData.

    Usage:
        resume_data = await ResumeParserService.parse_resume(upload_file)
    """

    @staticmethod
    async def parse_resume(file: UploadFile) -> ResumeData:
        """
        Entry point. Detects file type and dispatches to the right parser.

        Args:
            file: FastAPI UploadFile (PDF or DOCX)

        Returns:
            ResumeData: Structured resume data

        Raises:
            ValueError: If file type is unsupported or parsing fails
        """
        content = await file.read()
        filename = (file.filename or "").lower()

        logger.info("Parsing resume: %s (%d bytes)", filename, len(content))

        if filename.endswith(".pdf"):
            return _parse_pdf(content)
        elif filename.endswith(".docx"):
            return _parse_docx(content)
        else:
            raise ValueError(
                f"Unsupported file type: '{file.filename}'. "
                "Only PDF and DOCX files are accepted."
            )


# ===========================================================================
# Internal — PDF parsing
# ===========================================================================

def _parse_pdf(content: bytes) -> ResumeData:
    """Extract text from PDF and parse into ResumeData."""
    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as exc:
        raise ValueError(f"Failed to open PDF: {exc}") from exc

    full_text_lines: list[str] = []
    for page in doc:
        text = page.get_text("text")  # type: ignore[attr-defined]
        full_text_lines.extend(text.splitlines())

    doc.close()

    lines = [ln.strip() for ln in full_text_lines]
    return _parse_lines(lines)


# ===========================================================================
# Internal — DOCX parsing
# ===========================================================================

def _parse_docx(content: bytes) -> ResumeData:
    """Extract text from DOCX and parse into ResumeData."""
    try:
        document = docx.Document(io.BytesIO(content))
    except Exception as exc:
        raise ValueError(f"Failed to open DOCX: {exc}") from exc

    lines: list[str] = []
    for para in document.paragraphs:
        text = para.text.strip()
        if text:
            lines.append(text)

    return _parse_lines(lines)


# ===========================================================================
# Internal — Section-based parsing (shared for PDF + DOCX)
# ===========================================================================

def _parse_lines(lines: list[str]) -> ResumeData:
    """
    Main parsing logic. Splits the list of text lines into labelled sections
    and extracts structured data from each section.
    """
    # Step 1: Detect name + contact from the very top
    name = _extract_name(lines)
    contact_info = _extract_contact_info(lines[:10], name)

    # Step 2: Identify and split sections
    sections = _split_into_sections(lines)

    # Step 3: Parse each section
    summary = _extract_summary(sections.get("summary", []))
    experience = _extract_experience(sections.get("experience", []))
    education = _extract_education(sections.get("education", []))
    skill_lines = sections.get("skills", [])
    skills = _extract_skills(skill_lines)
    skill_categories = _extract_skill_categories(skill_lines)
    achievements = _extract_achievements(sections.get("achievements", []))
    projects = _extract_projects(sections.get("projects", []))

    return ResumeData(
        contact_info=contact_info,
        summary=summary,
        experience=experience,
        education=education,
        skills=skills,
        skill_categories=skill_categories if skill_categories else None,
        achievements=achievements if achievements else None,
        projects=projects if projects else None,
    )


def _is_section_heading(line: str) -> Optional[str]:
    """
    Returns the section key if `line` matches a known section heading, else None.
    """
    lower = line.lower().strip().rstrip(":")
    if len(lower) > 60:
        return None
    for section_key, keywords in SECTION_KEYWORDS.items():
        for kw in keywords:
            if lower == kw:
                return section_key
    return None


def _split_into_sections(lines: list[str]) -> dict[str, list[str]]:
    """
    Walk through lines and group them under detected section headings.
    """
    sections: dict[str, list[str]] = {}
    current_section = "header"
    sections[current_section] = []

    for line in lines:
        if not line:
            continue
        section_key = _is_section_heading(line)
        if section_key:
            current_section = section_key
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(line)

    return sections


# ---------------------------------------------------------------------------
# Contact info
# ---------------------------------------------------------------------------

def _extract_name(lines: list[str]) -> str:
    """
    Heuristic: the name is the first meaningful line that is NOT an email,
    phone, URL, or section heading, and has 1–5 words starting with uppercase.
    """
    for line in lines[:8]:
        stripped = line.strip()
        if not stripped:
            continue
        if EMAIL_RE.search(stripped):
            continue
        if PHONE_RE.search(stripped):
            continue
        if URL_RE.search(stripped):
            continue
        if _is_section_heading(stripped):
            continue
        words = stripped.split()
        if 1 <= len(words) <= 5 and stripped[0].isupper():
            return stripped
    return ""


def _extract_contact_info(lines: list[str], name: str) -> dict:
    """Extract email, phone, LinkedIn, GitHub, name from the header region."""
    # Join all header lines into one text blob for regex matching
    header_text = " ".join(lines)
    contact: dict = {}

    if name:
        contact["name"] = name

    email_match = EMAIL_RE.search(header_text)
    if email_match:
        contact["email"] = email_match.group()

    # Phone: find after stripping emails and URLs so they don't false-match
    clean_for_phone = EMAIL_RE.sub("", URL_RE.sub("", header_text))
    phone_match = PHONE_RE.search(clean_for_phone)
    if phone_match:
        contact["phone"] = phone_match.group().strip()

    for line in lines:
        # Find all URLs in the line
        for url_match in URL_RE.finditer(line):
            url = url_match.group().strip().rstrip(".,;)")
            url_lower = url.lower()
            if "linkedin" in url_lower and "linkedin" not in contact:
                contact["linkedin"] = url
            elif "github" in url_lower and "github" not in contact:
                contact["github"] = url
            elif not any(k in url_lower for k in ("linkedin", "github", "mailto", "@")):
                if "website" not in contact:
                    contact["website"] = url

    return contact


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def _extract_summary(lines: list[str]) -> Optional[str]:
    """Join summary section lines into a paragraph."""
    clean = [ln for ln in lines if ln.strip()]
    return " ".join(clean) if clean else None


# ---------------------------------------------------------------------------
# Experience
# ---------------------------------------------------------------------------

def _is_location_line(line: str) -> bool:
    """Detect lines that look like 'City, Country' or 'Remote' location markers."""
    line = line.strip()
    # Matches patterns like "Location, India", "New York, USA", "Remote"
    location_re = re.compile(
        r"^(Remote|Hybrid|On-site|[A-Z][a-z]+(?:\s[A-Z][a-z]+)?,\s*[A-Z][a-zA-Z\s]+)$"
    )
    return bool(location_re.match(line))


def _extract_experience(lines: list[str]) -> list[Experience]:
    """
    Parse experience section lines into a list of Experience objects.

    PDF Resume structure observed:
        Company Name
        Location, Country         ← optional location line (skip)
        Job Title
        StartDate · EndDate       ← date range line
        • bullet point            ← description bullets
        ...
    """
    experiences: list[Experience] = []
    if not lines:
        return experiences

    # Merge continuation lines (lines that start with lowercase and follow a bullet line)
    merged = _merge_continuation_lines(lines)

    # Parse into blocks: each block is anchored by a date-range line
    blocks: list[dict] = []
    current_block: Optional[dict] = None
    pending_header: list[str] = []

    for line in merged:
        date_match = DATE_RANGE_RE.search(line)
        if date_match:
            # Save previous block
            if current_block is not None:
                blocks.append(current_block)
            # Strip date from the line to see if anything else is on it
            remaining = DATE_RANGE_RE.sub("", line).strip().strip(BULLET_CHARS + "|,")
            header_lines = [
                h for h in pending_header
                if not _is_location_line(h)  # strip location lines
            ]
            if remaining:
                header_lines.append(remaining)
            current_block = {
                "header_lines": header_lines,
                "start_date": date_match.group(1).strip(),
                "end_date": date_match.group(2).strip(),
                "desc_lines": [],
            }
            pending_header = []
        elif current_block is None:
            if line.strip():
                pending_header.append(line.strip())
        else:
            # Description bullet
            bullet = line.lstrip(BULLET_CHARS).strip()
            if bullet:
                current_block["desc_lines"].append(bullet)

    if current_block is not None:
        blocks.append(current_block)

    for block in blocks:
        title, company = _split_title_company(block["header_lines"])
        experiences.append(
            Experience(
                title=title,
                company=company,
                start_date=block["start_date"],
                end_date=block["end_date"] if block["end_date"] else None,
                description=block["desc_lines"] or ["(no description available)"],
            )
        )

    return experiences


def _merge_continuation_lines(lines: list[str]) -> list[str]:
    """
    Merge lines that are continuations of the previous line
    (lines that start with lowercase and previous line doesn't end with period).
    This handles PDF line-wrapping of bullet points.
    """
    if not lines:
        return lines
    merged: list[str] = []
    for line in lines:
        if (
            merged
            and line
            and line[0].islower()
            and merged[-1]
            and not merged[-1].rstrip().endswith(".")
            and not merged[-1].rstrip().endswith(":")
            and not DATE_RANGE_RE.search(merged[-1])
        ):
            merged[-1] = merged[-1].rstrip() + " " + line.strip()
        else:
            merged.append(line)
    return merged


def _split_title_company(header_lines: list[str]) -> tuple[str, str]:
    """
    Given the header lines for an experience block, split into (job title, company).

    Typical PDF structure (after location lines removed):
        ["Skyllect Private Limited", "Full Stack Developer"]
        → company = header_lines[0], title = header_lines[-1]

    If only one line, check if it contains a separator.
    """
    if not header_lines:
        return ("Unknown Position", "Unknown Company")

    # Filter out anything that looks like just a date
    header_lines = [
        h for h in header_lines
        if not re.match(r"^\d{4}$", h.strip())
    ]

    if not header_lines:
        return ("Unknown Position", "Unknown Company")

    if len(header_lines) == 1:
        combined = header_lines[0]
        for sep in ["|", " @ ", " at ", "—", "–"]:
            if sep in combined:
                parts = combined.split(sep, 1)
                return (parts[0].strip(), parts[1].strip())
        return (combined.strip(), "Unknown Company")

    # Multiple lines: first = company, last = job title (common PDF resume pattern)
    return (header_lines[-1].strip(), header_lines[0].strip())


# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------

def _extract_education(lines: list[str]) -> list[Education]:
    """
    Parse education section lines into a list of Education objects.

    PDF education structure observed:
        Institution Name
        Location
        Degree Name
        Month YYYY
    """
    educations: list[Education] = []
    if not lines:
        return educations

    # Group lines into blocks; each block starts with an institution name
    # Strategy: a degree line contains a degree keyword; institution is before it
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        lower = line.lower()
        has_degree = any(kw in lower for kw in DEGREE_KEYWORDS)
        # A new education entry starts if we see a degree keyword
        if has_degree:
            if current:
                # Attach this line to existing block
                current.append(line)
                blocks.append(current)
                current = []
            else:
                current.append(line)
                blocks.append(current)
                current = []
        else:
            current.append(line)

    if current:
        # Remaining lines — might be part of the last education entry
        if blocks:
            blocks[-1].extend(current)
        else:
            brackets.append(current)

    for block in blocks:
        degree_line = ""
        institution_line = ""
        grad_year = ""
        gpa: Optional[float] = None

        for bl in block:
            lower = bl.lower()
            # Extract degree line
            if any(kw in lower for kw in DEGREE_KEYWORDS) and not degree_line:
                degree_line = bl.strip()
            # Extract GPA
            gpa_match = GPA_RE.search(bl)
            if gpa_match and gpa is None:
                try:
                    gpa = float(gpa_match.group(1))
                except ValueError:
                    pass
            # Extract graduation date (month and year if available)
            if not grad_year:
                date_match = MONTH_YEAR_RE.search(bl)
                if date_match:
                    grad_year = date_match.group()

        # Institution: first non-degree, non-location, non-date line
        for bl in block:
            stripped = bl.strip()
            if stripped == degree_line:
                continue
            if _is_location_line(stripped):
                continue
            # Skip lines that are just dates (month/year format)
            if MONTH_YEAR_RE.search(stripped) and len(stripped) <= 12:
                continue  # skip pure date lines
            if stripped:
                institution_line = stripped
                break

        educations.append(
            Education(
                degree=degree_line or "Unknown Degree",
                institution=institution_line or "Unknown Institution",
                graduation_year=grad_year or "Unknown",
                gpa=gpa,
            )
        )

    return [edu for edu in educations if edu.degree != "Unknown Degree"]


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

def _extract_skills(lines: list[str]) -> list[str]:
    """
    Parse skills section. Handles:
    - "Category: skill1, skill2, skill3" – strips category label, splits on comma
    - Bullet-separated lists
    - Plain comma/newline-separated lists
    """
    all_skills: list[str] = []

    for line in lines:
        # Strip category label (e.g., "Languages & Frameworks: ")
        line_without_category = SKILL_CATEGORY_RE.sub("", line).strip()

        # Split on comma or bullet chars
        raw_skills = re.split(r"[,|•●▪\t·‣·•·‧]+", line_without_category)
        for sk in raw_skills:
            sk = sk.strip().strip(BULLET_CHARS + " ")
            # Filter: must be non-empty, reasonable length, not just a number
            if sk and 2 <= len(sk) <= 60 and not re.match(r"^\d+$", sk):
                all_skills.append(sk)

    # De-duplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for sk in all_skills:
        key = sk.lower()
        if key not in seen:
            seen.add(key)
            unique.append(sk)

    return unique


def _extract_skill_categories(lines: list[str]) -> dict[str, list[str]]:
    """
    Parse skills section preserving category labels.
    Returns {category_name: [skills]} if the section uses "Category: s1, s2" format,
    or an empty dict if no categories are detected.
    """
    categories: dict[str, list[str]] = {}

    for line in lines:
        cat_match = SKILL_CATEGORY_RE.match(line)
        if not cat_match:
            continue
        # Category label without trailing colon/space
        cat_name = cat_match.group(0).strip().rstrip(":").strip()
        skills_part = line[cat_match.end():].strip()
        raw_skills = re.split(r"[,|•●▪\t·‣·•·‧]+", skills_part)
        skills = [s.strip().strip(BULLET_CHARS + " ") for s in raw_skills]
        skills = [s for s in skills if s and 2 <= len(s) <= 60 and not re.match(r"^\d+$", s)]
        if cat_name and skills:
            categories[cat_name] = skills

    return categories


# ---------------------------------------------------------------------------
# Achievements
# ---------------------------------------------------------------------------

def _extract_achievements(lines: list[str]) -> list[str]:
    """Parse achievements/certifications section into a list of strings."""
    achievements: list[str] = []
    for line in lines:
        bullet = line.lstrip(BULLET_CHARS).strip()
        if bullet:
            achievements.append(bullet)
    return achievements


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

def _extract_projects(lines: list[str]) -> list[Project]:
    """
    Parse projects section lines into a list of Project objects.

    Expected format:
        Project Title (may include technologies separated by | or -)
        • bullet point
        • bullet point
        ...

    Handles blank‑line separation between projects.
    """
    projects: list[Project] = []
    if not lines:
        return projects

    # Helper to strip leading bullet-like characters
    def strip_bullet(s: str) -> str:
        # Remove leading bullet characters (including whitespace)
        i = 0
        while i < len(s) and s[i] in ALL_BULLETS:
            i += 1
        # Also strip any whitespace that may follow the bullet
        while i < len(s) and s[i].isspace():
            i += 1
        return s[i:]

    # Group lines into blocks separated by empty lines
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)

    for block in blocks:
        if not block:
            continue
        # First non-empty line is the project title
        title_line = block[0].strip()
        # Remaining lines are description lines
        desc_lines_raw = block[1:] if len(block) > 1 else []
        desc_lines: list[str] = []
        for raw in desc_lines_raw:
            stripped = strip_bullet(raw)
            if stripped:
                desc_lines.append(stripped)
        if not desc_lines:
            desc_lines = ["(no description available)"]
        projects.append(Project(name=title_line, description=desc_lines))

    return projects