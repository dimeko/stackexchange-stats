# Welcome to Stackexchange stats

This is a simple CLI tool that calculates StackOverflow answers and comments statictics,
for a given time period.
The stats are below and are caculated with simple logic.

- **total_accepted_answers**: Loop through all answers and keeps only the accepted ones
- **accepted_answers_average_score**: Divides the accepted answers with the total amount of scores
- **average_answers_per_question**: Total questions divided by the total answers
- **top_ten_answers_comment_count**: Array of ten key/value elements with key -> answer_id and value -> comment_count

## Project layout

    docs/
        index.md        # The documentation homepage.
        core.md         # Core functionality documentation.
        cmd.md          # Command line interface documentation
    stats/
        cmd/
            cmd.py
            __init__.py
        core/
            __init__.py
            core.py
            utils.py
        __init__.py
        
    setup.py
    stats.py       # For running the application locally, without install.
    test_stats.py  # Unit test
    mkdocs.yml          # The configuration file.