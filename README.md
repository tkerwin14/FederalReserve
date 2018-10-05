# FederalReserve
Pulls all FOMC Meeting transcripts and identifies speaker's gender


pull_pdf.py - Pulls the transcripts from 1990 - 2012 for the Federal Open Market Committee (FOMC) meeting. Since there are 8 meetings in total for 22 years, it downloads 176 PDF files.

fed_pdf.py - Reads in the FOMC transcripts, pulls all text from the PDFs, and then breaks out each speaker's section and their identified gender.
