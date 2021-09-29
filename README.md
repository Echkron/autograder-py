# autograder-py
a python based autograder for grading text submissions.

Grades files in a directory by checking for if a specific string or set of strings is present in them.
Can grade grade pdf and text/image (experimental) by converting them into a text string.

built and tested in wsl using python3.
python3 autograde.py --help

dependicies:

  pdf2text

  cv2 (autograde-cv)

  pytesseract (autograde-cv)


TODO:

  rewrite code to be mantainable

  combine pdf-only (autograde.py) and multiformat (autograde-cv.py) into a single script

  rewrite input parser, add flags for --verbose --quiet,  
  
  improve output dlalog (when running and --help menu)
  
  remove the need to write to a tempoary folder
  
  rewirte README to be more useful
