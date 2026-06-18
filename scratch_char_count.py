# -*- coding: utf-8 -*-
import re

with open("d:/Coding/자기소개서/3_applications/2026-06-롯데홈쇼핑/cover_letter.md", "r", encoding="utf-8") as f:
    content = f.read()

# Split by 문항
sections = content.split("## ")

q1_text = ""
q2_text = ""
q3_text = ""

for sec in sections:
    if sec.startswith("1."):
        # Get content between first line and the word count note
        parts = sec.split("📊 글자 수:")
        q1_text = parts[0]
    elif sec.startswith("2."):
        parts = sec.split("📊 글자 수:")
        q2_text = parts[0]
    elif sec.startswith("3."):
        parts = sec.split("📊 글자 수:")
        q3_text = parts[0]

# Clean up Q1, Q2, Q3 (remove title, description lines)
def get_body(text):
    lines = text.split("\n")
    # Skip lines until we find bold title or body text
    body_lines = []
    started = False
    for line in lines:
        if line.strip().startswith("*") or line.strip().startswith("_") or "작성방법" in line:
            continue
        if line.strip().startswith("##"):
            continue
        if line.strip() == "" and not started:
            continue
        started = True
        body_lines.append(line)
    
    # Remove empty lines at the end
    while body_lines and body_lines[-1].strip() == "":
        body_lines.pop()
    
    return "\n".join(body_lines).strip()

q1_body = get_body(q1_text)
q2_body = get_body(q2_text)
q3_body = get_body(q3_text)

print("Q1 body len:", len(q1_body))
print("Q1 body non-space len:", len(q1_body.replace(" ", "").replace("\n", "").replace("\r", "")))
print("----------------")
print("Q2 body len:", len(q2_body))
print("Q2 body non-space len:", len(q2_body.replace(" ", "").replace("\n", "").replace("\r", "")))
print("----------------")
print("Q3 body len:", len(q3_body))
print("Q3 body non-space len:", len(q3_body.replace(" ", "").replace("\n", "").replace("\r", "")))
