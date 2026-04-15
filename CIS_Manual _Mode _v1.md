# **CIS Manual Mode v0.1**

## _**What you are building first**

You are **not** building the whole app first.

You are building the first usable version of CIS as:

* a project folder  
* a source intake process  
* a manifest  
* a preprocessing step  
* a draft knowledge record  
* a human review step  
* an approved knowledge record you can reuse later

That is enough to make CIS real.

At the end of this manual, you should be able to take **one PDF or image-heavy document**, process it, and end up with:

* a structured source container  
* a draft knowledge record  
* an approved knowledge record  
* a simple index of what you processed  
* a repeatable habit you or your coworker can follow

That matches the execution-centered system you’ve been defining, where workflow must be enforceable, raw files are not knowledge, and the workbench exists to move material toward structured knowledge.

---

# 

# 

# 

# **1\. What to keep in your head while doing this**

These are the rules for this first build:

1. **Project first.** Everything belongs to a project.  
2. **Raw files are not knowledge.** A file only becomes knowledge when it becomes a structured `knowledge_record`.  
3. **The system proposes. You decide.** AI does not define truth; approved outputs do.  
4. **Discovery comes before perfection.** Structure is discovered through interaction with real material.  
5. **Every step must leave a visible result.** If you cannot see what changed, the step was not useful.  
6. **Do not overbuild.** One real source processed correctly is worth more than ten vague plans.

---

# **2\. What you need before starting**

You already appear to have a working Ubuntu VM, `/mnt/projects`, OCR, and a local visual model environment in some form, plus a stable creative environment.

For this manual, you need only:

* your Ubuntu terminal  
* a text editor  
* one source file to process  
* access to ChatGPT or another frontier model for the merge/review step if needed  
* patience to do one source end-to-end

Use a **single test source** first. Good choices:

* one PDF tutorial  
* one comic PDF  
* one art book PDF  
* one image-heavy guide

Do **not** start with a whole folder.

---

# **3\. What the finished folder should look like**

For every source you ingest, create one **source container**. This matches your source-container and manifest logic.

The finished structure should look like this:

/mnt/projects/cis/  
 projects/  
   \<project\_slug\>/  
     01\_WORD/  
     02\_IMAGE/  
     03\_ACTION/  
     04\_SOUND/  
     05\_WEB/  
     06\_EXPORTS/  
     sources/  
       \<source\_container\>/  
         source/  
         working/  
         text/  
         pages/  
         intelligence/  
         metadata/  
         logs/  
         records/

This reflects the project-centered system, WIAS storage alignment, and source-container model.

---

# **4\. Step 1 — Create the CIS root folder**

Open terminal.

Run:

mkdir \-p /mnt/projects/cis  
mkdir \-p /mnt/projects/cis/projects  
mkdir \-p /mnt/projects/cis/logs  
mkdir \-p /mnt/projects/cis/templates

Then check it exists:

ls \-la /mnt/projects/cis

You should see at least:

* `projects`  
* `logs`  
* `templates`

---

# **5\. Step 2 — Create one project**

Pick a simple project name.

Example:

`blender_animation_test`

Run:

PROJECT=blender\_animation\_test  
mkdir \-p /mnt/projects/cis/projects/$PROJECT/{01\_WORD,02\_IMAGE,03\_ACTION,04\_SOUND,05\_WEB,06\_EXPORTS,sources}

Check it:

find /mnt/projects/cis/projects/$PROJECT \-maxdepth 1 \-type d | sort

You should see the WIAS folders plus `sources`. This aligns with your workflow-to-structure rule and project-centered architecture.

---

# **6\. Step 3 — Pick one source and create a source container**

Let’s say your test file is:

/home/eric/Downloads/my\_tutorial.pdf

Create a clean source slug. Keep it simple and lowercase.

Example:

`my_tutorial`

Now run:

PROJECT=blender\_animation\_test  
SOURCE\_SLUG=my\_tutorial  
SOURCE\_TYPE=pdf  
SEQ=001  
CONTAINER=${SOURCE\_TYPE}\_\_${SOURCE\_SLUG}\_\_${SEQ}

mkdir \-p /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/{source,working,text,pages,intelligence,metadata,logs,records}  
cp "/home/eric/Downloads/my\_tutorial.pdf" "/mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/source/"

Check it:

find /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER \-maxdepth 1 \-type d | sort

This follows your naming and storage convention idea: one processed source gets one contained record family.

---

# **7\. Step 4 — Create the source manifest**

Now create the intake control object. This is the file that says what entered the system and how it should be processed.

Run:

PROJECT=blender\_animation\_test  
SOURCE\_SLUG=my\_tutorial  
SOURCE\_TYPE=pdf  
SEQ=001  
CONTAINER=${SOURCE\_TYPE}\_\_${SOURCE\_SLUG}\_\_${SEQ}

cat \> /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/metadata/manifest.json \<\<'EOF'  
{  
 "project\_id": "blender\_animation\_test",  
 "project\_title": "Blender Animation Test",  
 "source\_container": "pdf\_\_my\_tutorial\_\_001",  
 "source\_type": "pdf",  
 "source\_name": "my\_tutorial.pdf",  
 "source\_path": "/mnt/projects/cis/projects/blender\_animation\_test/sources/pdf\_\_my\_tutorial\_\_001/source/my\_tutorial.pdf",  
 "processing\_profile": "document\_multimodal",  
 "processing\_plan": "ocr\_plus\_visual\_plus\_merge",  
 "status": "arrived",  
 "created\_by": "manual\_operator",  
 "notes": "First CIS manual-mode test source"  
}  
EOF

Open it and check it:

cat /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/metadata/manifest.json

If the file looks wrong, stop and fix it now.

---

# **8\. Step 5 — Preprocess the PDF into text and pages**

This is the point where the raw source becomes model-ready input. Preprocessing prepares material; it does not interpret it.

Run:

PROJECT=blender\_animation\_test  
CONTAINER=pdf\_\_my\_tutorial\_\_001  
PDF="/mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/source/my\_tutorial.pdf"

pdftotext \-layout "$PDF" "/mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/text/raw\_text.txt"  
pdftoppm \-png "$PDF" "/mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/pages/page"

Check the outputs:

ls \-la /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/text  
ls \-la /mnt/projects/cis/projects/$CONTAINER/pages 2\>/dev/null  
ls \-la /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/pages | head

You should now have:

* `raw_text.txt`  
* multiple PNG page images

If `pdftotext` or `pdftoppm` are missing, install them:

sudo apt update  
sudo apt install \-y poppler-utils

Then rerun the preprocessing commands.

---

# **9\. Step 6 — OCR the page images**

If the PDF text is weak, OCR gives you another signal. In CIS terms, OCR is one pass, not the whole answer.

Install Tesseract if needed:

sudo apt update  
sudo apt install \-y tesseract-ocr

Run OCR over all pages:

PROJECT=blender\_animation\_test  
CONTAINER=pdf\_\_my\_tutorial\_\_001  
PAGES\_DIR="/mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/pages"  
TEXT\_DIR="/mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/text"

mkdir \-p "$TEXT\_DIR/ocr"

for img in "$PAGES\_DIR"/\*.png; do  
 base=$(basename "$img" .png)  
 tesseract "$img" "$TEXT\_DIR/ocr/$base" \>/dev/null 2\>&1  
done

Check it:

ls \-la /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/text/ocr | head

Now combine the OCR into one file:

cat /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/text/ocr/\*.txt \> /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/text/ocr\_combined.txt

Check that file exists:

wc \-l /mnt/projects/cis/projects/$PROJECT/sources/$CONTAINER/text/ocr\_combined.txt  
---

# 

# **10\. Step 7 — Create a visual extraction file**

This step depends on what local visual pipeline you already have. Your docs say you have local visual analysis in some form, but they do not lock one exact command in the files you gave me.

So for **immediate usability**, do this in the simplest way:

Take 3–5 representative page images from the `pages/` folder and upload them to ChatGPT with this prompt.

## **Prompt: visual extraction**

You are performing strict multimodal extraction for CIS.

Describe only what is visible and directly supportable.

Return:  
1\. visible\_text  
2\. scene\_description  
3\. layout\_description  
4\. style\_mood\_tags  
5\. functional\_tags  
6\. uncertainty\_notes

Rules:  
\- do not invent names  
\- do not infer unsupported meaning  
\- if unsure, state uncertainty clearly  
\- keep tags concrete and reusable

Save the result into:

nano /mnt/projects/cis/projects/blender\_animation\_test/sources/pdf\_\_my\_tutorial\_\_001/intelligence/visual\_extraction.md

Paste the model output and save.

Why this is acceptable: your system already allows frontier/manual refinement where it improves quality and is human-in-the-loop.

---

# **11\. Step 8 — Merge OCR \+ visual into one draft knowledge record**

This is the most important step. In your docs, the merge layer is required because OCR and visual alone are incomplete.

Create the JSON file:

nano /mnt/projects/cis/projects/blender\_animation\_test/sources/pdf\_\_my\_tutorial\_\_001/records/knowledge\_record\_\_learning\_\_my\_tutorial\_\_document\_\_v1.json

Paste this template:

{  
 "record\_id": "KNOWLEDGE\_\_PDF\_\_MY\_TUTORIAL\_\_DOCUMENT\_\_001",  
 "record\_type": "knowledge\_record",  
 "title": "My Tutorial",  
 "working\_title": "My Tutorial",  
 "source\_type": "pdf",  
 "source\_name": "my\_tutorial.pdf",  
 "source\_path": "/mnt/projects/cis/projects/blender\_animation\_test/sources/pdf\_\_my\_tutorial\_\_001/source/my\_tutorial.pdf",  
 "source\_unit": "document",  
 "project\_id": "blender\_animation\_test",  
 "project\_title": "Blender Animation Test",  
 "concept": "Learning material for Blender animation work",  
 "intended\_output\_type": "animation",  
 "project\_scope": "minor",  
 "active\_stages": \["word", "image", "action"\],  
 "knowledge\_category": "learning",  
 "subject": "blender\_animation",

 "tags": \[\],  
 "summary": "",  
 "retrieval\_text": "",  
 "visible\_text": "",  
 "scene\_description": "",  
 "layout\_description": "",  
 "style\_mood\_tags": \[\],  
 "functional\_tags": \[\],  
 "example\_uses": \[\],  
 "required\_skills": \[\],  
 "inferred\_constraints": \[\],  
 "risk\_flags": \[\],  
 "confidence\_notes": "",  
 "source\_origin": "frontier\_manual",  
 "model\_used": "ChatGPT\_manual\_merge",  
 "created\_at": "",  
 "updated\_at": "",  
 "status": "draft",  
 "version": "v1",  
 "is\_current": true  
}

Now fill it using:

* `raw_text.txt`  
* `ocr_combined.txt`  
* `visual_extraction.md`  
* your own judgment

Do not aim for perfect. Aim for:

* clear  
* useful  
* honest  
* source-linked

---

# 

# 

# **12\. Step 9 — Create the human-readable markdown mirror**

Create the markdown version:

nano /mnt/projects/cis/projects/blender\_animation\_test/sources/pdf\_\_my\_tutorial\_\_001/records/knowledge\_record\_\_learning\_\_my\_tutorial\_\_document\_\_v1.md

Paste this template:

\# My Tutorial

\#\# Record ID  
KNOWLEDGE\_\_PDF\_\_MY\_TUTORIAL\_\_DOCUMENT\_\_001

\#\# Project  
Blender Animation Test

\#\# Knowledge Category  
learning

\#\# Subject  
blender\_animation

\#\# Summary

\#\# Visible Text

\#\# Scene Description

\#\# Layout Description

\#\# Style / Mood Tags

\#\# Functional Tags

\#\# Example Uses

\#\# Required Skills

\#\# Inferred Constraints

\#\# Risk Flags

\#\# Confidence Notes

\#\# Status  
draft

This markdown is for human reading. The JSON is the source of truth. That rule comes directly from your architecture and knowledge docs.

---

# **13\. Step 10 — Review the draft**

This is where the system stops being a model toy and becomes your system.

Open:

* the original source  
* the OCR text  
* the visual extraction  
* the draft JSON  
* the markdown mirror

Now ask six questions:

1. Did the system invent anything unsupported?  
2. Is the category wrong?  
3. Are the tags too vague?  
4. Is uncertainty clearly stated where needed?  
5. Is the record useful for future retrieval?  
6. Could a future Teacher or Librarian use this?

This matches your reinforcement model: accepted outputs define truth, not model output.

If the draft is usable, change:

* `status` from `draft` → `checked`

If you trust it enough for reuse, change:

* `status` from `checked` → `approved`

Do **not** use `locked` yet.

---

# **14\. Step 11 — Create a tiny index so you can find what you made**

Make a CSV index:

nano /mnt/projects/cis/projects/blender\_animation\_test/01\_WORD/knowledge\_index.csv

Paste:

record\_id,title,knowledge\_category,subject,status,source\_container,record\_path  
KNOWLEDGE\_\_PDF\_\_MY\_TUTORIAL\_\_DOCUMENT\_\_001,My Tutorial,learning,blender\_animation,approved,pdf\_\_my\_tutorial\_\_001,/mnt/projects/cis/projects/blender\_animation\_test/sources/pdf\_\_my\_tutorial\_\_001/records/knowledge\_record\_\_learning\_\_my\_tutorial\_\_document\_\_v1.json

This is your first searchable registry. It is primitive, but real.

---

# 

# **15\. Step 12 — Use the approved record in an actual task**

Now use the record.

Open ChatGPT and paste the approved markdown file or the relevant JSON fields with this prompt:

## **Prompt: teacher mode**

You are acting as the CIS Teacher.

Use only the approved knowledge below.

Task:  
Help me apply this tutorial to my current Blender animation goal.

Return:  
1\. what this source is useful for  
2\. the first 3 actions I should take in Blender  
3\. what I should avoid  
4\. what skill gaps I still have  
5\. which parts are uncertain

This is how you prove the loop:

**source → knowledge → guidance → production**

That is exactly what your system is for.

---

# 

# 

# 

# **16\. Step 13 — Log what happened**

Create or append to your system log:

nano /mnt/projects/cis/logs/system\_log.md

Append something like:

\#\# 2026-04-13 — First manual CIS ingestion test

Project: Blender Animation Test  
Source: pdf\_\_my\_tutorial\_\_001  
Actions:  
\- created source container  
\- created manifest  
\- ran preprocessing  
\- ran OCR  
\- performed visual extraction manually  
\- merged into knowledge\_record  
\- reviewed and approved

Outcome:  
\- first approved knowledge record created  
\- teacher-mode reuse now possible

Problems noticed:  
\- merge step still manual  
\- tagging still rough  
\- retrieval index still primitive

This matches your control and runtime logging rules.

---

# 

# 

# 

# **17\. What counts as success for this first build**

You are successful if all of these are true:

* one project exists  
* one source container exists  
* one manifest exists  
* one source was preprocessed  
* one draft knowledge record was created  
* one record was reviewed  
* one record was approved  
* one approved record was used in a real creative task

If you do that once, CIS is no longer theory.

---

# **18\. What you should NOT do yet**

Do not do these yet:

* do not process the whole archive  
* do not build the full app  
* do not build a real database  
* do not build agents as software  
* do not chase perfect schema  
* do not rewrite all docs again

Your only job right now is:

**prove one source can become one approved knowledge record and then help you make something**

---

# 

# **19\. The next three practical expansions after this works once**

Once you complete one source successfully, do these in order.

## **Expansion 1**

Process **three** sources from the same project.

Goal:

* discover repeated tags  
* discover repeated fields  
* discover merge problems

## **Expansion 2**

Create a reusable prompt set:

* visual extraction prompt  
* merge prompt  
* teacher prompt  
* librarian prompt

## **Expansion 3**

Replace one manual step with one repeatable helper command.

Good first target:

* a shell script that creates the source container and manifest automatically

---

# 

# **20\. Your first-day version of the system, explained simply**

You are building this:

1. Put a file into a project.  
2. Give the file a manifest.  
3. Preprocess it.  
4. Extract text and visual signals.  
5. Merge them into a draft record.  
6. Review the record.  
7. Approve it.  
8. Use it in a real task.

That is CIS in first usable form.

---

# **21\. What to do right now, in order**

Do exactly this next:

1. Open terminal.  
2. Create `/mnt/projects/cis`.  
3. Create one project folder.  
4. Copy one PDF into a source container.  
5. Create `manifest.json`.  
6. Run `pdftotext`.  
7. Run `pdftoppm`.  
8. Run Tesseract OCR.  
9. Use ChatGPT to create visual extraction.  
10. Fill the draft JSON.  
11. Fill the markdown mirror.  
12. Review and mark it `checked` or `approved`.  
13. Add one line to `knowledge_index.csv`.  
14. Use the approved record in Teacher mode.

Do not skip ahead.

---

# 

# **22\. The one sentence that should guide you**

**Do not try to build CIS all at once. Build one honest, reusable knowledge record from one real source inside one real project.**

If you want, the next step can be a **literal copy-paste template pack** for:

* `manifest.json`  
* `knowledge_record.json`  
* `knowledge_record.md`  
* `knowledge_index.csv`  
* `system_log.md`  
* the exact prompts for visual extraction, merge, teacher, and librarian modes

