### LinkedIn Applier

A selenium bot for automating the application process for "Easy Apply" job
postings.

### Usage

    main.py [-h] --username USERNAME --password PASSWORD --keyword KEYWORD --location LOCATION [--amount AMOUNT]

    Automate LinkedIn Job Applications.

    options:
      -h, --help           show this help message and exit
      --username USERNAME  LinkedIn username (email).
      --password PASSWORD  LinkedIn password.
      --keyword KEYWORD    Job title to search for (e.g., "Software Developer").
      --location LOCATION  Location to filter job search (e.g., "Ottawa, ON").
      --amount AMOUNT      Number of jobs to apply to.
