# ContextualExamGen (CEG): A Framework for Personalized Assessment Generation Using LLMs

**ContextualExamGen (CEG)** is an open-source, research-driven framework for generating *individualized programming assessment questions* for large-scale introductory computer science courses. The system programmatically analyzes student submissions, generates both contextually grounded and abstracted questions using large language models (LLMs), and constructs customized test documents. CEG integrates seamlessly with educational tools such as **Gradescope** and leverages **OpenAI’s GPT-4 batch API** for scalable and cost-efficient generation.

---

## System Capabilities

### 1. Submission Collection via Gradescope

Using secure session tokens or instructor credentials, CEG:

* Authenticates into Gradescope
* Retrieves student submissions for a given assignment
* Parses and stores relevant code artifacts per student

Pulling data from GitHub for non Gradescope courses (COMING SOON)

### 2. Dual-Mode Question Generation (via LLMs)

#### **A. Context-Based Questions**

Questions are derived from each student’s unique code submission and address specific implementation steps using snippits from students own code.

> *Examples:*
>
> * “Why does this loop in `your_file` not terminate as expected?”
```python
i = 0
while i > 0:
print("Hello")
  i++
```
> * “What is missing in this function implementation of `my_cool_function` in `your_file`?”
```pthon
def my_cool_fucntion(n: int):
  for i in range(n):
    ______

```

#### **B. Abstracted Conceptual Questions**

These are based on the student's engagement with course topics but do not reference their specific code directly.

> *Examples:*
>
> * “What does your `merge_sort()` function aim to accomplish?”
> * “You used recusion in `your_file` why did you use that verus itteration name 2 reasons why.”

### 3. Scalable Batch Processing

CEG can use OpenAI's GPT **batch inference API** to:

* Process thousands of questions asynchronously
* Log inputs/outputs for reproducibility
* Support automatic retry logic for incomplete generations

### 4. Exam Assembly & Document Modification

CEG accepts a **template test document** (PDF, LaTeX, or structured TXT) and generates customized versions for each student by:

* Inserting personalized questions into designated page slots (e.g., page 0)
* Aligning question placement and formatting
* Reconstructing final test PDFs suitable for printing or digital upload

### Languages Currently Suported 
* Python
* Java (COMING SOON)
* C (COMING SOON)

---

## Research Applications

CEG supports experimental and pedagogical research in:

* **Personalized learning** and its impact on student engagement and retention
* **Automation of formative feedback** at scale
* **Ethical considerations** in automated grading and question generation
* **Comparative effectiveness** of context-grounded vs. abstract question framing

---

## Example Use Case

A CS instructor managing 300 students can execute the full pipeline with three commands:

```bash
python run_pipeline.py \
  --assignment "PA3" \
  --gradescope_email you@school.edu \
  --gradescope_password mypass \
  --output_dir ./student_tests \
  --test_template ./base_exam.pdf \
  --insert_page 0
```

This command will:

1. Download all submissions for *PA3* from Gradescope
2. Generate individualized comprehension questions
3. Assemble final personalized exams for each student

---

## Output Per Student

Each student receives:

* `context_questions.txt` — Personalized, code-linked questions
* `abstracted_questions.txt` — Higher-level conceptual prompts
* `personalized_exam.pdf` — Final exam file with embedded questions

---

## Project Goals and Contributions

* Demonstrate a viable system for **scalable, personalized assessment generation**
* Provide a reproducible pipeline suitable for CS education research
* Offer instructors a practical tool for **customized test construction**
* Serve as a benchmark for evaluating LLM-driven educational tooling

---

## Roadmap & Planned Extensions

* Auto-generated answer keys using LLM evaluation
* Bloom's Taxonomy tagging of questions (e.g., Apply, Analyze, Evaluate)
* Similarity-based clustering for scalable question reuse
* Export to LMS-compatible formats (Canvas, Moodle)
* Instructor-facing user interface for drag-and-drop test assembly

---

## Citation

If you use ContextualExamGen in your work, please cite the forthcoming paper or reference this repository as:

> Jones, C. (2025). *ContextualExamGen: An Open-Source Framework for Individualized Assessment Using Large Language Models*. UNC Chapel Hill.

---

## Contributing

We welcome contributions, feature requests, and feedback from both educators and developers. Please submit an issue or pull request via [GitHub Issues](https://github.com/ConorJones05/ContextualExamGen).
