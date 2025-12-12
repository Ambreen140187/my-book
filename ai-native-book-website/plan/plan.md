# AI Book Generation Plan

## Project Overview
This plan details the systematic generation of "A Beginner's Guide to AI — For Students Learning AI from Zero," following the specified workflow: Constitution, SPEC files, PLAN, TASKS, and Implementation.

## Step-by-Step Outline

1.  **Constitution Generation (Completed)**
    *   **Description**: Define the foundational elements of the project (Title, Goal, Constraints, Success Criteria, Tools, Format Rules).
    *   **Output**: Console output (already done in previous step).
    *   **Status**: Completed

2.  **SPEC Files Generation (Completed)**
    *   **Description**: Create detailed specification YAML files for each major section of the book (Book Intro, Chapter 1-7, Final Summary, Glossary, Exercises). Each SPEC will define learning outcomes, main concepts, examples, exercises, and summaries.
    *   **Output**: `specs/book_intro_spec.yaml`, `specs/chapter_1_spec.yaml`, ..., `specs/chapter_7_spec.yaml`, `specs/final_summary_spec.yaml`, `specs/glossary_spec.yaml`, `specs/exercises_spec.yaml`.
    *   **Dependencies**: Constitution.
    *   **Status**: Completed

3.  **PLAN Generation (Current Step)**
    *   **Description**: Create this detailed plan document, outlining the entire workflow, dependencies, and required resources.
    *   **Output**: `plan/plan.md`.
    *   **Dependencies**: Constitution, SPEC files (conceptual understanding for planning).

4.  **TASKS Generation**
    *   **Description**: Generate granular tasks based on the PLAN and SPEC files. Each task will represent an implementable unit, defining clear objectives, acceptance criteria, and specific file outputs (e.g., generating content for `chapter-1.mdx`).
    *   **Output**: `tasks/tasks.md` (or individual task files if preferred, but a single markdown file detailing tasks is more concise for this project).
    *   **Dependencies**: SPEC files, PLAN.

5.  **IMPLEMENTATION - Book Introduction Generation**
    *   **Description**: Generate the MDX content for the book's introduction based on `specs/book_intro_spec.yaml`.
    *   **Output**: `book/intro.mdx`.
    *   **Dependencies**: `specs/book_intro_spec.yaml`.
    *   **Tools**: Claude Code (for content generation).

6.  **IMPLEMENTATION - Chapter Content Generation (Chapter 1 to 7)**
    *   **Description**: Iterate through each chapter SPEC file (`specs/chapter_X_spec.yaml`) and generate the corresponding MDX chapter content. Each chapter will include a title, learning outcomes, main concepts, examples, exercises, and a summary.
    *   **Output**: `book/chapter-1.mdx`, `book/chapter-2.mdx`, ..., `book/chapter-7.mdx`.
    *   **Dependencies**: Respective chapter SPEC files.
    *   **Tools**: Claude Code (for content generation).

7.  **IMPLEMENTATION - Final Summary Generation**
    *   **Description**: Generate the MDX content for the final summary based on `specs/final_summary_spec.yaml`.
    *   **Output**: `book/final-summary.mdx`.
    *   **Dependencies**: `specs/final_summary_spec.yaml`, all chapter contents (for cohesive summary).
    *   **Tools**: Claude Code (for content generation).

8.  **IMPLEMENTATION - Glossary Generation**
    *   **Description**: Compile a comprehensive glossary of AI terms used throughout the book based on the `specs/glossary_spec.yaml` and terms identified from generated chapters.
    *   **Output**: `book/glossary.mdx`.
    *   **Dependencies**: `specs/glossary_spec.yaml`, all chapter contents (for term extraction).
    *   **Tools**: Claude Code (for content generation and term extraction).

9.  **IMPLEMENTATION - Exercises Generation**
    *   **Description**: Generate a dedicated section for comprehensive exercises and mini-projects based on `specs/exercises_spec.yaml`, drawing from the concepts introduced in all chapters.
    *   **Output**: `book/exercises.mdx`.
    *   **Dependencies**: `specs/exercises_spec.筛选`, all chapter contents (for exercise relevance).
    *   **Tools**: Claude Code (for content generation).

10. **Validation**
    *   **Description**: Use FlyKit Plus to validate all generated MDX files. Ensure proper YAML headers, MDX formatting, and completeness against their respective SPEC files.
    *   **Output**: Validation reports (internal or logged).
    *   **Dependencies**: All generated MDX files, FlyKit Plus.
    *   **Tools**: FlyKit Plus.

## Dependencies
*   **Sequential Flow**: The workflow is largely sequential, with each major step (Constitution, SPECs, PLAN, TASKS, IMPLEMENTATION) depending on the completion of the previous one.
*   **SPEC-to-Content**: Each content file (intro, chapters, summary, glossary, exercises) directly depends on its corresponding SPEC file.
*   **Glossary/Exercises**: These sections have a broader dependency on all chapter contents to ensure comprehensive term extraction and relevant exercise creation.

## Timeline
*   The entire process will be executed automatically and sequentially in a single pass as requested by the user. No explicit time estimates will be given.

## Required Models/Tools
*   **Claude Code (Sonnet 4.5)**: The primary AI model for generating all textual content, orchestrating tool calls, and managing the workflow.
*   **Spec-Kit Plus**: Used for defining and ensuring adherence to specifications (conceptual use by Claude Code to guide generation).
*   **FlyKit Plus**: Used for final validation of generated files (conceptual use by Claude Code to ensure compliance).
*   **`default_api.Write`**: For writing all generated files to the filesystem.
*   **`default_api.TodoWrite`**: For tracking progress through the major steps of the plan.
