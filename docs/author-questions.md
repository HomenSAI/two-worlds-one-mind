# Questions for the author

One list of everything the editor could not settle without the author. Each item says which
statement needs it, which document would settle it, and what the book says in the meantime
(a neutral version that is already in the text). Answer in any order; nothing here blocks the
build.

| # | Question | Statement that depends on it | What would settle it | Neutral wording used meanwhile |
|---|----------|------------------------------|----------------------|--------------------------------|
| 1 | **CAD dates.** The first contact with 3D modelling is given as 2002. In which company or project did you first model equipment in 3D, and were you the one modelling? When did EKVIPTEH switch fully (2010–2011)? | Chapter 1 table, Chapter 3 (P-03), Chapter 6 ("When 3D came in") | Old project files with dates; the CV | "From 2002, as I date it"; "whole company about 2010–2011"; no claim about 2002 being mass use |
| 2 | **Peak turnover.** Was the figure of about $0.9M per year reached in each of 2012 and 2013, or in one of them? Is it turnover (revenue) in USD, and from which records? | Chapter 6 "Numbers behind the story" | Accounting statements, bank statements or tax returns for 2012–13 | "about $0.9M in each of the two best years (2012 and 2013); other years roughly half; turnover, not profit; not audited" |
| 3 | **"CIS leader" for UViS Technologii (2002–2005).** On what basis: market share, number of lines sold, an industry ranking, a customer survey? | Chapter 6 | A source: ranking, a trade press article, sales statistics | "how the company described its position … the author's account"; no independent ranking cited |
| 4 | **Robotics case.** Is there a finished project in which you integrated a robot (not only automated machines)? | Chapter 7 "Join in", Chapter 6 | A project description, photos, a reference | "the direction I am moving into … not yet a project I can show" |
| 5 | **EXP-001 data.** The measurements and the set-up (see the table in [EXP-001](../experiments/EXP-001.md)): GPU variant and VRAM, CPU, RAM, OS and driver, model file and hash, quantization, back end and version, KV cache, launch command, test prompt, parallel clients, memory, time to first token, tokens/s, the exact 262k error. | Chapter 5 table | The actual machine; the server's launch scripts and logs; or a new run on a test machine by the procedure in the protocol | "author-reported; reproducibility details pending" |
| 6 | **Team size and role at UViS Technologii.** The site says 26 for EKVIPTEH, a CV says 25. Confirm "up to about 26". Confirm your wording for UViS Technologii (member of the founding team, employed; your CVs give the title "deputy production director"). Confirm the UViS Technologii start year (2002 here; some sources say 2001). | Chapter 6 table, Chapter 6 numbers | CVs, employment record, company documents | "up to about 26"; "member of the founding team, employed"; 2002 |
| 7 | **The mark inside the robot illustration.** Do you allow the illustration `line-of-development.svg` to be reproduced under CC BY 4.0 *including* the gear-and-circuit mark on the robot's chest, as long as the mark is not separated from the picture? | [LICENSING.md](../LICENSING.md) | Your decision (a proposed wording is in LICENSING.md) | "reproduce the illustration unchanged with attribution; do not separate the mark" |
| 8 | **GitHub "Cite this repository".** Do you want a `CITATION.cff` with a `preferred-citation` of type book, accepting that the file's top level would call the repository "software" or "dataset"? | [docs/citation.md](citation.md) | Your decision | No CFF; `CITATION.bib` and README |
| 9 | **License of the build scripts and example code.** MIT (proposed) or another licence, or none? | [LICENSING.md](../LICENSING.md) | Your decision | Not licensed yet |
| 10 | **German edition review.** Should a native speaker or you review the German text before release? | [docs/translation-status.md](translation-status.md) | Your review (say whether you prefer an external proofreader) | "machine-assisted translation by the editor, not independently reviewed" |
| 11 | **Book archive.** Do you want the whole book archived separately on Zenodo (new record and DOI)? | [archive kit](archive/zenodo-archive-kit.md) | Your decision and Zenodo account access | Nothing claimed |
| 12 | **Git author for future commits.** Is `info@homensai.com` added and verified in your GitHub account? If not, use the GitHub-provided noreply address shown at Settings → Emails. | [docs/github-settings.md](github-settings.md) | Settings → Emails | Commits are made with the name Serhii Khomenko and `info@homensai.com` |
| 13 | **Preferred reading page.** One main path for reading outside GitHub: a page on homensai.com, or GitHub Pages? | README "Read and download" | Your decision | PDF/HTML from the build; no site change made |

## Answers received (5 October 2026)

| # | Answer | Applied |
|---|--------|---------|
| 1 | 2D AutoCAD introduced by the author from 2004 (not as the designer); 3D SolidWorks in 2010, later Inventor | Chapters 1, 3, 6 (EN, DE) |
| 2 | Confirmed in the softer form: "up to about $0.9M", best years 2012–2013; this is EKVIPTEH | Chapter 6 |
| 3 | Subjective: no comparable website in the CIS with such detailed material and video, supplies around the world; stated as the author's judgement | Chapter 6 |
| 4 | No finished robot-integration project; text unchanged | none |
| 5 | Keep `PENDING` in 1.1; data to follow | none |
| 6 | EKVIPTEH peak 25 (not 26), UViS Technologii about 35; one of the three who started UViS Technologii, de facto founder, oral arrangement without documents, salary only, no influence on finances; start year 2002 kept | Chapter 6 |
| 7 | Yes, as proposed | LICENSING.md |
| 8 | No `CITATION.cff` | none |
| 9 | MIT for code | LICENSE-CODE, LICENSING.md, README |
| 10 | Release 1.1 with the "not proof-read" note; proof-reading later | none |
| 11 | Yes, archive the book on Zenodo after the release of 1.1 | open |
| 12 | `info@homensai.com`, verified in GitHub Settings | done |
| 13 | A page on homensai.com | open (site not changed yet) |
