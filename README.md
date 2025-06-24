## 🧠 LLM\_Question\_Gen: Individualized Question Generation & Test Assembly for Intro CS Students

**LLM\_Question\_Gen** is a research-oriented and production-capable tool that automatically generates *customized programming questions* for introductory CS students by analyzing their code submissions. The system integrates with **Gradescope**, leverages **OpenAI GPT-4 batch jobs** for scalable question creation, and can even **modify and organize full test documents**, making it a one-stop pipeline for individualized assessment generation.

---

### 🔧 What It Does

#### ✅ Scrape student code from Gradescope

Using login credentials or a session token, LLM\_Question\_Gen:

* Logs into Gradescope
* Retrieves all student submissions for a specified assignment
* Extracts and organizes each student’s Python code

#### ✅ Generate two types of LLM-based questions

1. **Context-Based Questions**

   * Refer directly to student-submitted code
   * Examples:

     * “What is missing in this function?”
     * “Why does this loop not terminate as expected?”

2. **Abstracted Questions**

   * Conceptual, based on student activity, without direct code excerpts
   * Examples:

     * “What does your `merge_sort()` function aim to solve?”
     * “Could you rewrite your algorithm using iteration instead of recursion?”

#### ✅ Batch LLM Jobs (OpenAI API)

* Uses GPT-4 batch API for **cost-efficient**, **asynchronous** large-scale generation
* Supports batch retries and logging for auditing results

#### ✅ Test Page Modification and Assembly

* Accepts a **finished test template** as input (e.g., PDF or structured LaTeX/TXT format)
* Automatically **inserts generated questions** into designated page slots (starting at 0)
* Reconstructs tests per student for distribution or printing
* Ensures alignment of:

  * Page numbers
  * Question placement
  * Student-specific variants

---

### 🧪 Example Use Case

You’re a CS instructor teaching 300 students. You want to:

1. Download all code for "PA3 – Recursion and Sorting" from Gradescope.
2. Generate custom comprehension questions for each student.
3. Integrate those questions into versioned exam documents for final review.

**One command handles all of this**:

```bash
python run_pipeline.py \
  --assignment "PA3" \
  --gradescope_email you@school.edu \
  --gradescope_password mypass \
  --output_dir ./student_tests \
  --test_template ./base_exam.pdf \
  --insert_page 0
```

---

### 🧠 Research Focus

This project supports a paper exploring:

* Whether personalized assessments improve engagement and retention
* How LLMs can fill gaps in TA feedback during scale
* Ethical boundaries of automated code analysis and feedback
* Evaluation of **contextualization vs. abstraction** in question generation

---

### 📁 Outputs Per Student

Each student gets:

* `student_code.py` – their original code
* `context_questions.txt` – questions with embedded code
* `abstracted_questions.txt` – concept-based questions
* `personalized_exam.pdf` – test file with embedded questions at the right page

---

### 🧱 Planned Features

* [ ] Auto-grading answer keys via LLM
* [ ] Bloom taxonomy tagging (e.g., Apply, Analyze)
* [ ] Student similarity detection (for question reuse)
* [ ] LMS (Canvas/Moodle) export format
* [ ] Plug-and-play UI for instructors

---
