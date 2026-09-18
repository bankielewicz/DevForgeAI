# QA-owned setup failure

Rust compile E0425: windows-sys 0.61.2 does not expose JOB_OBJECT_TERMINATE in the imported namespace. No test executed. This is a PREREQUISITE_OR_HARNESS_GAP, not a product defect, integrity failure, behavioral Red, or passing case.

Preserved input-snapshot contains every original harness input. Existing receipt binds their bytes. The installed Windows SDK header `C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/um/winnt.h` lines 12740-12741 defines JOB_OBJECT_QUERY=0x0004 and JOB_OBJECT_TERMINATE=0x0008 (two other installed SDK headers agree). Correction adds the locally documented constant to the QA function. No production bytes or oracle change. Reinspection confirms the helper still uses a real reduced-access duplicate, restores ownership, and resumes panic. Authorized next attempt is a fresh compile/list only, then initial behavior execution if compilation and identity checks succeed.
