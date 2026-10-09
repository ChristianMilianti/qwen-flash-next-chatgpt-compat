# Public release check

The v1.0.0 release source files and ZIP metadata were inspected before packaging.

- No personal names, email addresses, account identifiers, credentials, personal filesystem paths, device identifiers, chat IDs, conversations, or diagnostic logs were found in the selected files.
- General test hardware, software versions, model identifiers, and performance results are included.
- Public upstream repository links, model checksums, official action commit hashes, relative filenames, and local API endpoint paths are intentional technical information.
- Model weights, runtimes, cache files, environment files, Git history, and operating-system metadata are excluded.
- ZIP timestamps are normalized; creator identity and file ownership metadata are absent.
- SHA256SUMS records the release files. The separate ZIP checksum verifies the complete archive.
- Five fixture tests passed locally. Hosted workflow results are available in the repository's Actions tab after publication.

This check applies to this prepared archive. Future files and commit metadata need their own review before publication.
