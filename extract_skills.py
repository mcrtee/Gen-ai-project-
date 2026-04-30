import pdfplumber
import json
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills(text):
    skills = []
    # Look for sections like "Hard Skills", "Soft Skills", "Skills"
    patterns = [
        r'(?:Hard\s+Skills?|Soft\s+Skills?|Skills?)\s*[:\-]?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
        r'(?:Hard\s+Skills?|Soft\s+Skills?|Skills?)\s*\n(.*?)(?=\n\n|\n[A-Z]|$)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            # Split by commas, newlines, etc.
            items = re.split(r'[,\n;•\-]', match)
            for item in items:
                item = item.strip()
                if item and len(item) > 1:  # Avoid single chars
                    skills.append(item)
    # Also look for bullet points or lists
    bullet_patterns = r'(?:•|\-|\*)\s*(.+?)(?=\n|$)'
    bullets = re.findall(bullet_patterns, text, re.MULTILINE)
    for bullet in bullets:
        bullet = bullet.strip()
        if bullet and len(bullet) > 1:
            skills.append(bullet)
    return list(set(skills))  # Unique

# Read PDFs
cv_text = extract_text_from_pdf('Meerim_CV.pdf')
transcript_text = extract_text_from_pdf('Transcript .pdf')

all_text = cv_text + "\n" + transcript_text

skills = extract_skills(all_text)

# Save to JSON
with open('data/skills.json', 'w') as f:
    json.dump({"skills": skills}, f, indent=4)

print("Skills extracted and saved to data/skills.json")