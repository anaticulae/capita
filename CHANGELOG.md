# changelog

Every noteable change is logged here.

## v1.12.2

### Feature

* move headlines from elements (367ac63e8174)
* add literature headline (129cc6113c35)

## v1.12.1

### Fix

* remove magic value (ab51fc17cd5c)
* adjust number rate computation (9a76ae706a79)

## v1.12.0

### Feature

* add modifiable holy values (69555779a2c9)
* introduce configo holy values (8cb6c5e077b4)

### Fix

* adjust bug in feature detection (a542e1da1701)

## v1.11.1

### Feature

* change to appendix if glossary is detected (bd1879436fcb)

### Fix

* make headline skip size dependent (e7c700688e97)

## v1.11.0

### Feature

* add list of headlines (401ef4e91258)
* improve starts with check (ee1cc025cc6e)
* extend bib headlines (f3692565d4e0)

## v1.10.0

### Feature

* connect glossary step (1c3f7360b99b)
* add glossary detector step (888d5dece9fd)
* add more invalid bib chapter headlines (0e3209dd7332)

### Fix

* skip page with very low matching (8c7b2046b1c6)
* its a single file not a pattern (ca3cb7ea0477)

### Documentation

* clarify code (90bbb53a4ca0)

## v1.9.0

### Feature

* add docinfo step (657bb865dc41)

## v1.8.0

### Feature

* add white space rate (8607fab04d67)
* introduce max level to shrink headline extraction (fd1f2e2ba7ab)
* adjust valid chapter area (f021db535edf)

### Fix

* skip white spaced abbr page (272f0b1732e0)
* use maxlevel to reduce false positive extraction (e28f01c9c93e)

## v1.7.0

### Feature

* improve section merger (081ed17049e0)
* extend valid headlines list (3d8d395b0f0d)

### Documentation

* fix logic error (45ebed986391)

## v1.6.1

### Fix

* convert path newlines (a1afc6176cae)
* skip empty outline element (6df348c266f9)

## v1.6.0

### Feature

* skip potential headlines with very low char rate (5d8b38377710)
* extend valid chapter headlines (d0c98dea2552)
* add more valid headlines (237c55054750)
* use hyperlink as another marker (f4c20e225dbf)
* add acknowledge section detection step (a80690ae5fc7)

### Fix

* copy is not required here (5c16b7bf5bac)
* do not create multiple section on CitePart (afbe13d5ee32)

### Documentation

* extend interface documentation (6a3c90ea2e47)

## v1.5.0

### Feature

* disable top search restriction to detect more tables (e29141a5dfc9)
* add valid table to tabletable detector (1b36b61aa937)
* add option to disable top search (e44804f14ee0)
* extend no headline list (8014fe277c64)
* improve symbol headline detector (927e69b0199a)
* add English list of figures pattern (495d091ca2e6)
* add more valid headlines (8b18287396cb)
* use more modern approach (54644019d430)
* extend list of valid headlines (75d075e721b0)
* extend list of valid headlines (a37c62df8f9c)
* add another headline marker (6c22367ec943)
* replace with content navigator (23fff92ae9ca)

### Fix

* strip first outline if necessary (bac329dd8f97)
* increase headline word count (499981beda7c)
* skip references as chapter (8948dbd50014)

## v1.4.0

### Feature

* add tolerance in bib grouper (fee6190ce9d1)
* improve main merger (fc257175cbfd)
* introduce layout min height to avoid (0482b76cff18)
* add option to write images to a common folder (360b53832a82)
* introduce CiteContent (5c2b3b231604)
* ensure that section is not sorted alphabetically (86e661d5ac68)
* link paper result to default extractor (3ed045ec2e4f)
* add paper step (af4cffd136f8)
* improve code style (cb6317bee156)
* ensure to have a more proper group start (7527ff4d0a7a)
* user grouper to determine valid range of pages (9d699ded5041)
* do not run double column on rotated page (9faeb1940a93)
* reduce execution time (72ee670f958a)
* adjust layout extractor (a94d3fe0c861)
* add option to analyze selected pages (79c6f4b24ae6)
* add double layout detector (b61e335f2125)
* skip small rectangles (770564d2009a)
* add pdf to image converter (d88c1d1e631e)
* add page font detection (11f67c30a77f)
* add paper detection package (660e9ae4a8c3)

### Fix

* reset bonus after failure group (04f98a72ceb4)
* make pattern parser more robust (92bd8235bd84)
* add missing pages flag (fd1c50834023)
* ensure correct return value (5813f151697b)
* reduce verbosity (49130d15fe84)
* fix normal skipper (95619b50e7d4)
* skip empty pages (67dce7c73048)
* run clustering more than once (5022aeadbf56)

### Documentation

* extend code docs (3e800f7dc219)

## v1.3.2

### Feature

* ensure that left and right column are balanced (d349b401988f)
* ease testing ability (97deb2082ba9)

## v1.3.1

### Fix

* ensure that part of headline is long enough (c27b1ff7f7b8)

## v1.3.0

### Feature

* extend pattern (389c687b52ac)
* remove roman number from flat toc (a88ff8b3c957)
* skip not matching chapter headlines (a9d7c6eed58a)
* skip rotated pages (e4382e4332ae)
* extend chapter noheadline pattern (20aa5f4eb652)
* use improved chapter headline detector (c8bce5d4954b)
* add another headline to bib section detector (0811f3bbb1af)

### Fix

* do not detect single character as headline (9a49029ec218)
* make start comparison more robust against white spaces (c954e438e097)
* do not handle anhang as separate chapter (3483e984c56b)
* adjust method name (eff5e1a8df6c)
* make approach more stable against caps (86b6e1325eb9)

## v1.2.0

### Feature

* skip too hight chapter cause of false positive (bd4f5efc50c1)
* extend appendix pattern (eaacc4d87805)
* use content navigator to exclude header (8e27921b9885)
* lower min headline match (2589e256f935)
* use figures for blank/empty page check (bf5a11026556)
* load figures and images if exists (7d4a2b9275cd)

## v1.1.0

### Feature

* add method to skip regular content pages (1bc3b43610fd)
* use improved headline comparer (a83e47634317)
* add short left column check (bc682e41912f)
* skip potential toc page as title page (3f8205466eb7)
* add min toc value to identify as table of content (d2844d7dde41)

### Fix

* skip numbered column as abbreviation table (50ea7a268f0c)
* ensure to support double headline detection (9ccb42d641c4)

## v1.0.1

## v1.0.0

### Feature

* remove workplan (95eeda297026)
* increase strictness of column check (29a96bf2016a)
* use merge to merge following non headlined pages (dd79bd146b12)
* use better headline selector strategy (c082c4772fb7)
* improve code style and use better data structure (2cdb26c95969)

### Documentation

* Happy New Year! (dc9688b42eda)

## v0.15.1

### Fix

* pass minimal value to method checker (5d7dfbf5c042)

## v0.15.0

### Feature

* use pattern to extend figuretable detector (dfc90182f950)
* add option to define own valid line strategy (8bae99681b91)

## v0.14.2

### Feature

* extend table detection strategy (6e5299ba2ec4)
* unite strategy with detected pages without headline (c2f828337aac)
* add appendix line checker (c3cbe681d637)

## v0.14.1

## v0.14.0

### Feature

* extend toc page detection (edd73cc03c7a)
* improve chapter start detector (3c91c267a034)

## v0.13.8

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
