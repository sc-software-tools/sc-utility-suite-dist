# SC Utility Suite - Distribution & Releases

This repository is the official binary distribution hub and showcase website for **SC Utility Suite**, a collection of 7 high-performance, privacy-focused desktop utilities for Windows 10 and Windows 11.

---

## Applications

| Application | Description | Microsoft Store | Standalone (.exe) | Portable (.zip) |
| :--- | :--- | :--- | :--- | :--- |
| **Archive Unpacker** | Multi-format archive extraction & inspection | [Store Listing](https://apps.microsoft.com/detail/9NXS3LDTBRX8) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/ArchiveUnpacker_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/ArchiveUnpacker_v1.0.1_Portable.zip) |
| **Dup Scrub** | High-speed duplicate file cleaner | [Store Listing](https://apps.microsoft.com/detail/9NL51TH9QR3M) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/DupScrub_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/DupScrub_v1.0.1_Portable.zip) |
| **HEIC Studio** | High-speed Apple image converter | [Store Listing](https://apps.microsoft.com/detail/9N4F9K6G90HK) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/HeicStudio_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/HeicStudio_v1.0.1_Portable.zip) |
| **Media Trim** | Video trimming, conversion and audio extraction | [Store Listing](https://apps.microsoft.com/detail/9PC1HVN60QBP) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/MediaTrim_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/MediaTrim_v1.0.1_Portable.zip) |
| **PDF Knife** | Fast PDF splitter and merger | [Store Listing](https://apps.microsoft.com/detail/9NQLSS021G6T) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/PdfKnife_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/PdfKnife_v1.0.1_Portable.zip) |
| **Screen Lens** | Screen and GIF recorder | [Store Listing](https://apps.microsoft.com/detail/9N7V2FVFL4BN) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/ScreenLens_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/ScreenLens_v1.0.1_Portable.zip) |
| **USB Flasher** | Bootable drive writer & raw imaging | [Store Listing](https://apps.microsoft.com/detail/9P9NBFS7PMJB) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/UsbFlasher_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/UsbFlasher_v1.0.1_Portable.zip) |
| **Master Suite** | Complete 7-app all-in-one package | N/A | [Master Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/SC_Utility_Suite_AllInOne_Setup_v1.0.1.exe) | [Master Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/SC_Utility_Suite_AllInOne_v1.0.1_Portable.zip) |

---

## Cryptographic Verification

The 16 v1.0.1 installer and portable files have SHA256 checksums in `checksums_distribution.sha256`. Current standalone installers are unsigned. A matching hash establishes download integrity, not a trusted publisher signature.

## System Requirements
- Windows 10 (version 19041+) or Windows 11
- 64-bit architecture (x64)
- Self-contained .NET 8 runtimes included

## Channel status and licensing

Standalone v1.0.1 downloads are published. Media Trim is awaiting its Microsoft Store release. The other six apps are listed as available; availability may vary by market. Live Store purchase restoration has not been tested. Eight Winget pull requests (seven apps plus the complete bundle) have passing validation labels but remain unmerged at the last check on 11 November 2026. Do not assume the catalog commands are available yet.

PRO uses Microsoft Store purchases in the Store edition and Gumroad keys in standalone editions. File processing stays local; activation contacts the purchase provider. Free editions display a local upgrade strip; PRO hides it. The published Media Trim v1.0.1 edits one file at a time in both editions. The v1.0.2 preview restores PRO batch conversion; it has not replaced the existing downloads. No multipass feature is offered.

Development fixes are being tested as a separate 1.0.2 candidate. Existing v1.0.1 release files, submitted MSIX packages and Winget download URLs are preserved. The unchanged 1.0.1 downloads still use the earlier FFmpeg build. The 1.0.2 Media Trim package uses a replacement engine with verified public source/build records; standalone publisher signing remains outstanding.

### Known v1.0.1 ZIP-creation issue

In the free edition, selecting several separate inputs for ZIP creation can include only the first input. To include several files in v1.0.1, place them in one folder and add that folder. The 1.0.2 candidate fixes separate multi-input creation and has passed byte-content regression checks; it has not replaced the existing downloads or Store submissions.

## Media Trim 1.0.2 preview

PRO batch conversion has been restored in development: add files or folders, select the files to process, and convert whole files using one shared preset and output folder. The independent single-file editor keeps its preview and trim markers; all five single-file presets remain free, without a paid duration limit. PRO also removes the upgrade strip.

This preview is not yet a public application release. New MSIX, installer and portable packages have passed source/payload checks and Windows installation, upgrade and removal tests. The MSIX is prepared for the existing Store product; no submission has been made by this development session. Standalone files remain unsigned and are held in a draft release while trusted publisher signing is arranged. Existing v1.0.1 assets, Store IDs and Winget URLs are unchanged. See [release status](release-notes.md#media-trim-102-preview) and [matching engine sources/build records](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/tag/ffmpeg-9.0.2-sc1-sources).
