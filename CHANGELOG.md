# Changelog

Every noteable change is logged here.

## v1.23.1 (2022-12-04)

### Chore

* upgrade requirements.txt (173548832b44)

## v1.23.0 (2022-12-03)

### Feature

* use more modern data (78ac898ee085)
* use improved resource (fdef09b487bf)

### Chore

* run faster tasks first (81a417c55da9)
* use docken to cache generation (215c425e38a8)
* use quick installer (b3b569d18e2b)
* remove sections dependency (b721952a5803)
* update pipeline (cfff22ccc969)
* upgrade pipe library (338c95a0375b)
* reduce feedback time (352fe4684f8b)
* upgrade environment (9a1f2f7a882d)
* add groupme hefopa-merger (3326f6b88cb0)
* upgrade requirements.txt (a23a2c7c91f4)

## v1.22.1 (2022-11-06)

### Fix

* load white page likelihood correctly (80bd15716d33)
* do not fill gaps inside document (f520b632b956)
* adjust data loader (2de61eda3691)

### Chore

* add missing ghost (f7c2769d15ac)
* remove default config (1ea4351855e3)
* upgrade requirements.txt (8a4b2f48e817)
* upgrade baw (1689e6a847c7)
* upgrade requirements.txt (9af25fd3c293)
* upgrade pipe library (23be05d5a1b4)
* convert nightly to all (9ac00abe2548)
* upgrade environment (485fbd0c5769)
* upgrade requirements.txt (865d38657aba)

## v1.22.0 (2022-10-05)

### Chore

* publish generated data if nightly fails (50d3cdec1d03)
* do not run in privileged mode (0816919bbf11)
* run cleanup (efd362a10ad7)
* add cleanup (8ba56efcf1ca)
* upgrade requirements.txt (b3788ea4b34f)
* upgrade baw (9dacb377c208)
* increase number of executor in nightly (425c712a2f55)
* adjust worker on ci (9e974ddd3519)
* run headnote extractor (41b5789ed6ba)
* add headnote (32f8e2ce6e71)

## v1.21.3 (2022-09-28)

### Fix

* extend level outline collector (a0db0740381f)

### Chore

* use more worker if running in CI (d01104127ba2)
* adjust to current generator (172eb81f536f)
* add missing dev requirement (a5b6e5cb3834)
* add separate generation step (92c9fe5bb484)
* add Jenkinsfile (1add9a26b475)
* upgrade requirements.txt (2acc79466c67)
* upgrade requirements.txt (30aa5aa79460)
* upgrade requirements.txt (186552514625)

## v1.21.2

### Feature

* return failure earlier (6cff81450114)

### Fix

* adjust abbrev column detector (1da955a0b1ce)

## v1.21.1

### Feature

* add pattern to overwrite special pattern (2bd14e6e8a17)
* skip pages with too many footnotes (8e795e09ba13)
* use footnote to improve bib extraction (b5f468be9736)

## v1.21.0

### Feature

* do not change Appendix on MultipleSection (eaf7547ad409)

### Fix

* change from unknown to appendix if required (39eab97ace8c)
* do not intro on multiple section (abac448e226e)

## v1.20.0

### Feature

* add better author detector (9fb500d3b304)
* remove headline end char to improve detection (8c08a8d77e30)

## v1.19.2

### Fix

* skip empty page (acfd7092bd2f)

## v1.19.1

### Feature

* do not detect paper inside documents for just a few pages (abd889e52991)

### Fix

* adjust chapter detector (1f7ba188646e)
* ensure that first match does not reduce value (bce955ebba7b)
* make pattern case insensitive (0b56c58cf5e1)
* we already use ptcn (3d1d5daef664)

## v1.19.0

### Feature

* indent to increase readability (0a06d724e662)
* add huge number chapter start detector (9ab7a3528059)
* add debugging information (666e88349dbd)
* increase legal feature points (94d242e1454f)

### Fix

* do not detect huge number with short toc as dotted list (a310b2ea7c9f)
* adjust logger message (4037d7e08ca4)
* match single chars with toc correctly (1df121c91183)

### Documentation

* extend interface information (766aba3b5893)

## v1.18.1

### Fix

* adjust text on page converter (e28547257cf2)

## v1.18.0

### Feature

* disable glossary if rate is too low (21d7570ca579)
* pass page count if required (e1b7e259c82f)
* limit glossary rate without headlines (28b017a87ca1)
* make glossary detector line length dependent (0e1c1a8bd3da)
* make glossary rate page number dependent (447ef3bc0e86)
* skip page with too many lines as glossary (1f340a9b9b48)
* increase special words (4d0bcdf5c730)
* increase logging (a946aa93bc48)

### Fix

* reduce verbosity (b94a432704dc)

## v1.17.0

### Feature

* reduce amount of required patterns (9902d57b0cfb)
* increase debugging information (f3ab4a78fd5d)
* extend pattern list (0febca416f05)
* add method to determine range of section (b364e1a5272d)

### Fix

* ensure that pdfinfo is optional (3bd83de00009)
* do not detect MainPart before toc (1fc6a75c70b0)
* the headline is not enough (4b6a43df8328)

### Documentation

* adjust modules path (e96692b38966)

## v1.16.0

### Feature

* do not detect low dens double column as paper (d9ffe2c4b73a)
* add global page numbers (606b91bd3a46)
* add page generator (387693e85743)

### Fix

* do not always detect bib if bib headline is on page (85c1e94c4132)

## v1.15.0

### Feature

* use shortcut as error title (639d4bda950b)
* use table strategy to detect index page (af731ff2dac4)

### Fix

* adjust debug message (e529bf713691)
* ensure that empty page is skipped correctly (0929861e218d)

### Documentation

* add module documentation (798a1b98c2cb)

## v1.14.2

### Feature

* add hint that merging does not work (3c0fe46bf641)
* skip very short pages to improve extraction result (096935d25e18)

## v1.14.1

### Feature

* allow abstract at the end of the document (3a5e5b9c90ca)

### Fix

* skip false detected empty tables (0aaf3208ea00)

## v1.14.0

### Feature

* increase debugging information (0b92ede73b2d)
* add volume pattern to detect more pattern (4dd356f8c4e0)
* enable profiling (6e4d989b9d7f)
* determine document language (08c9890b7dc6)
* skip pages with too many content as title pages (473c48629ab7)
* increase number of words inside a headline (e411004864cd)
* shrink pages to given pages (a2a9fea25b8e)

### Fix

* make junk remover less strict (1f27d9d74fda)
* remove duplication to reduce junk detection (254d95d7acc8)
* do not split hyperlink as german sentences (3a17bba46e11)

## v1.13.0

### Feature

* line count based min marker rate (12ab98b178c8)
* skip potential chapter with too few text lines at start (5be931c89755)
* add chapter support for line with a lot spaces (85fc93e7d9b2)
* use headline list as backup strategy (ca2a967932af)
* disable pattern approach on too many page detections (357d9ab6e98b)
* shrink loaded ptn to possible toc ranges (c991eaa642c2)
* add method to shrink pages (d61033a3ed1f)
* add backup strategy to determine headlines (c4006655459c)
* extend toc detector (9ba5f21803b2)

### Fix

* skip multiple sections for abbr and symbol table (eb345d48637e)
* skip abbr headline inside table of content (816f190888e3)

### Documentation

* Happy New Year! (99be6920f93d)

## v1.12.3

### Feature

* extend figure table detector (6a94aa57cb72)

### Fix

* do not skip single char headlines (82d2606c7c17)

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
