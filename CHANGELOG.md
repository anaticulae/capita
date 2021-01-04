# changelog

Every noteable change is logged here.

## v0.13.7

### Fix

* shrink chapter selector for better results (777a01c1843e)

## v0.13.6

## v0.13.5

## v0.13.4

## v0.13.3

## v0.13.2

## v0.13.1

## v0.13.0

### Feature

* cut non required `precision` (def3a31f0de6)
* introduce threshold to avoid surprising results (04aa24bb219b)
* use content navigator to improve performance (d07938d2fb76)

### Fix

* skip very small headlines (82e8d5fa09a4)

## v0.12.2

### Feature

* extend special word list (2fdfab60d16d)

### Fix

* fix broken import (2becc5c609fe)

## v0.12.1

## v0.12.0

### Feature

* extend keywords to detect bib section (b702f4cd82c0)

## v0.11.0

### Feature

* use authors to improve bib section detection (8e0d84514f5f)
* add authors to extract list of authors (1c1f0504d704)
* use parse level for toc line detection (aee74d45a72d)
* make bib detector more robust against level (de9b7c12cce4)

### Fix

* add min value of marker to use feature (aaa5d0e941ce)
* improve single char feature (279e0c51814f)
* fix hugest font size determiner for correct title page extraction (673bb33043f4)

## v0.10.0

### Feature

* add white list to improve headline detection (0d6dcb2b9669)
* add headline as hundred percent marker (152114a16026)

### Fix

* disable check for (short) document without toc (bc87038042cc)
* skip pages with more than two column (8e64164ab26f)

## v0.9.7

## v0.9.6

## v0.9.5

## v0.9.4

## v0.9.3

## v0.9.2

### Fix

* add missing package (54e9f310f895)

## v0.9.1

### Fix

* add missing package (1343968e2853)

## v0.9.0

### Feature

* add double column bib detector (c1d99317cb58)
* add double column parser (786bb6e06aa9)
* introduce strategy infrastructure (7e3d12af23dc)
* support more appendix start headlines (8f5e8ee5e155)

### Fix

* add missing default values (76bb51dac5e2)

### Documentation

* add module information (41291b73681f)
* extend interface documentation (2c6d8517f540)
* extend interface documentation (3bc29f1ae811)

## v0.8.3

## v0.8.2

## v0.8.1

## v0.8.0

### Feature

* extend table headline detector (f1d4df159f44)

### Fix

* fix wrong detected bib section detection (215e4048dfb6)

## v0.7.1

### Fix

* adjust test to correct page ranges (98c78534467a)

## v0.7.0

### Feature

* add symbol section detection step (f8ce1ba7cdc7)
* extend chapter headline detector (6f1c09b4bf50)

### Fix

* clarify source of error message (03f2b84755e8)

### Documentation

* fix interface documentation (d5ae25577c69)

## v0.6.0

### Feature

* add first draft of appendix detector (a75419b2c438)
* add abstract step detection step (2c741ec74623)
* add figuretable and tabletable section detection step (affd2043478f)
* use new toc likelihood detector (e1254f89c517)
* add method to determine potential headline out of text style (12530995b1ee)

### Fix

* use mean bib value to avoid holes in group while merging with (817f6f697aec)

## v0.5.1

## v0.5.0

### Feature

* add dynamic next class selector (141806e27f9f)
* make chapter start detector more robust (1d466e72be67)

### Fix

* do not parse newlines in headline pattern (a97ac4bc366a)
* do not detect appendix with a lot of points as toc page (81b047fcb1f7)

### Documentation

* extend interface documentation (cc1524c4560c)

## v0.4.10

## v0.4.9

## v0.4.8

## v0.4.7

## v0.4.6

## v0.4.5

## v0.4.4

## v0.4.3

## v0.4.2

## v0.4.1

## v0.4.0

### Feature

* select hugest single potential bib group (089a5e3e464d)
* open interface to use result directly (2bebb735bd8a)

## v0.3.1

### Fix

* fix unit test (72bfe86493f4)

## v0.3.0

### Feature

* create huger sections to avoid splitting document area (7c0b5966fe29)
* use python style range pattern (538c6a95e5eb)
* improve chapter detector (2e3c7d860d5f)
* extend legal detection (a07938c2ccbb)

### Fix

* replace with correct copy pattern (b745ca333ab6)
* log missing font access (a398ad474a11)

### Documentation

* fix description (cfb41ae8494f)

## v0.2.34

## v0.2.33

## v0.2.32

## v0.2.31

## v0.2.30

## v0.2.29

## v0.2.28

## v0.2.27

## v0.2.26

## v0.2.25

## v0.2.24

## v0.2.23

## v0.2.22

## v0.2.21

## v0.2.20

## v0.2.19

## v0.2.18

## v0.2.17

## v0.2.16

## v0.2.15

## v0.2.14

## v0.2.13

## v0.2.12

## v0.2.11

## v0.2.10

## v0.2.9

## v0.2.8

## v0.2.7

## v0.2.6

## v0.2.5

## v0.2.4

## v0.2.3

## v0.2.2

## v0.2.1

### Feature

* add first draft of validating 5 examples (f94b1e1692c5)

## v0.2.0

### Feature

* introduce header to define variable replacements (8d6621eb9fe3)
* add method to dump config to string (5320ea50d4f0)
* introduce execution plan link config and cmds (cd69982e533f)
* add method to load configuration files (024dceb76573)
* change format to .pl of generated working plan (2fc6504c7427)
* add workplan step to extract planned extraction (445cdc59a195)
* add method to setup folder structure (b97f3819fb28)
* add runtime parallelize (d69397d643b6)
* add method to split raw execution plan (692cfd153859)
* add method to convert plan to raw plan (d71ba638f392)
* merge section `Chapter` and `Text` (80fda1f5ec4d)
* add workplan runner (9bdd2fe82ccc)
* add workplan creator (e591c1195d48)

### Fix

* fix expected return type (0838d1342881)

### Documentation

* add purpose of sections tool (f0db3ae13dbe)

## v0.1.1

### Fix

* fix linter warnings (ca0d9d6c014e)
* fix linter warning (aee32425d5e7)
* fix linter warnings (ab60d3b418db)
* fix outdated todo (05d786ccff94)

## v0.1.0

### Feature

* move code from, hey project (55e54508c774)

## v0.0.0 Initial release
