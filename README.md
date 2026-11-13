# SC Utility Suite - Distribution & Releases

This repository is the official binary distribution hub and showcase website for **SC Utility Suite**, a collection of 7 high-performance, privacy-focused desktop utilities for Windows 10 and Windows 11.

---

## Applications

| Application | Description | Microsoft Store | Standalone (.exe) | Portable (.zip) |
| :--- | :--- | :--- | :--- | :--- |
| **Archive Unpacker** | Multi-format archive extraction & inspection | [Store Listing](https://apps.microsoft.com/detail/9NXS3LDTBRX8) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/ArchiveUnpacker_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/ArchiveUnpacker_v1.0.1_Portable.zip) |
| **Dup Scrub** | High-speed duplicate file cleaner | [Store Listing](https://apps.microsoft.com/detail/9NL51TH9QR3M) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/DupScrub_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/DupScrub_v1.0.1_Portable.zip) |
| **HEIC Studio** | High-speed Apple image converter | [Store Listing](https://apps.microsoft.com/detail/9N4F9K6G90HK) | [Setup](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/HeicStudio_Setup_v1.0.1.exe) | [Portable](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/v1.0.1/HeicStudio_v1.0.1_Portable.zip) |
| **Media Trim** | Video trimming, conversion and audio extraction | [Store Listing](https://apps.microsoft.com/detail/9PC1HVN60QBP) | [Setup (v1.0.2)](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/media-trim-v1.0.2/MediaTrim_Setup_v1.0.2.exe) | [Portable (v1.0.2)](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/download/media-trim-v1.0.2/MediaTrim_v1.0.2_Portable.zip) |
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

Standalone v1.0.1 downloads and Media Trim v1.0.2 downloads are published. Six apps are live in the Microsoft Store (Archive Unpacker, Dup Scrub, HEIC Studio, Media Trim, PDF Knife, Screen Lens); USB Flasher is in final publishing. Eight Winget pull requests have passing validation labels and are awaiting volunteer moderator approval.

PRO uses Microsoft Store purchases in the Store edition and Gumroad keys in standalone editions. File processing stays local; activation contacts the purchase provider. Free editions display a local upgrade strip; PRO hides it.

## Media Trim 1.0.2

Media Trim 1.0.2 is released:
- Restores the PRO whole-file batch queue: add files or folders, select the files to process, and convert using a shared preset and output folder.
- Dedicated single-file trimmer keeps its preview, waveform, and precision trim markers.
- All five single-file presets (MP3 320k, WAV, MP4 H.264, 720p, lossless cut) remain free with no duration cap.
- Bundles embedded FFmpeg 9.0.2-sc1 engine with verified source/build records publicly delivered at [FFmpeg 9.0.2-sc1 sources](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/tag/ffmpeg-9.0.2-sc1-sources).
- Available via [Media Trim v1.0.2 Release](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/tag/media-trim-v1.0.2) and Microsoft Store. Standalone checksums are available in the release assets.
