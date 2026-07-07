# -*- coding: utf-8 -*-
import re

file_path = r"c:\Coding\WorkSpace\자기소개서\3_applications\2026-07-DB_Inc\cover_letter.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Split by 문항
sections = content.split("## ")

q1_text = ""
q2_text = ""
q3_text = ""
q4_text = ""

for sec in sections:
    if sec.startswith("1."):
        parts = sec.split("📊 글자 수:")
        q1_text = parts[0]
    elif sec.startswith("2."):
        parts = sec.split("📊 글자 수:")
        q2_text = parts[0]
    elif sec.startswith("3."):
        parts = sec.split("📊 글자 수:")
        q3_text = parts[0]
    elif sec.startswith("4."):
        parts = sec.split("📊 글자 수:")
        q4_text = parts[0]

def get_body(text):
    lines = text.split("\n")
    body_lines = []
    started = False
    for line in lines:
        if line.strip().startswith("*") or line.strip().startswith("_") or "최대 " in line:
            continue
        if line.strip().startswith("##"):
            continue
        if line.strip() == "" and not started:
            continue
        started = True
        body_lines.append(line)
    
    while body_lines and body_lines[-1].strip() == "":
        body_lines.pop()
    
    return "\n".join(body_lines).strip()

q1_body = get_body(q1_text)
q2_body = get_body(q2_text)
q3_body = get_body(q3_text)
q4_body = get_body(q4_text)

def count_chars(text):
    normalized = text.replace("\r\n", "\n")
    space_included = len(normalized)
    space_excluded = len(re.sub(r'\s', '', normalized))
    return space_included, space_excluded

q1_inc, q1_exc = count_chars(q1_body)
q2_inc, q2_exc = count_chars(q2_body)
q3_inc, q3_exc = count_chars(q3_body)
q4_inc, q4_exc = count_chars(q4_body)

print(f"Q1: {q1_inc} chars (with space), {q1_exc} chars (without space)")
print(f"Q2: {q2_inc} chars (with space), {q2_exc} chars (without space)")
print(f"Q3: {q3_inc} chars (with space), {q3_exc} chars (without space)")
print(f"Q4: {q4_inc} chars (with space), {q4_exc} chars (without space)")
