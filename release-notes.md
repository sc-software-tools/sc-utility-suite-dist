## SC Utility Suite v1.0.3 - Archive Selection and Reliability

The suite bundle contains **Media Trim 1.0.4** and **version 1.0.3 of the other six applications**.

- Archive Unpacker correctly extracts selected files and folders when archive paths begin with ./ or use backslashes.
- Large archive inspections run in the background, with cancellation and protection against stale results when clearing or changing the source.
- Cleared archive items no longer send updates to the current workspace.
- Filename validation rejects additional Windows-reserved device names before opening output files.
- Settings reads each application's own version metadata.
- Previous PRO dialog fixes, Explorer menu icons, suite branding and bundled FFmpeg source delivery are retained.

All installers and portable ZIPs contain the same app payloads as the all-in-one bundle. Matching Microsoft Store packages are prepared for publisher upload; their availability follows submission and certification. Previous releases and submissions have not been overwritten. Existing licences, prices, PRO features and Store identities are unchanged. Standalone installers remain unsigned; a matching SHA256 verifies integrity, not publisher trust.

## SC Utility Suite v1.0.2 - Standalone Upgrade Dialog Fixes

The new bundle contains Media Trim 1.0.3 and Archive Unpacker, HEIC Studio, PDF Knife, Dup Scrub, Screen Lens and USB Flasher 1.0.2.

- Fixed the shared standalone PRO window crashing because of missing button/text styles. Both the header and upgrade-strip buttons open the real activation dialog.
- Fixed missing resources in Archive Unpacker's password prompt, including the prompt used by Explorer extraction.
- Added clear feedback for unavailable or incomplete Microsoft Store upgrades, with a visible opening state and duplicate-click protection.
- The all-in-one installer and its uninstall entry now use the suite website's emerald diamond branding. Individual app icons remain unchanged.
- Media Trim and Screen Lens bundle the source-verified FFmpeg 9.0.2-sc1 engine and its corresponding-source delivery information. No separate FFmpeg installation is needed.

These are new standalone packages; old 1.0.1 files and Media Trim1.0.2 remain unchanged. Updated MSIX packages have also been submitted and are in certification for all seven Store applications: Media Trim 1.0.3.0 and 1.0.2.0 of the other six. They include the shared Store upgrade feedback improvements; Archive Unpacker also includes its native Explorer integration. The updates are set to publish after certification approval; live Store listings may still deliver earlier versions. Standalone installers remain unsigned and may show browser/Windows reputation warnings; hashes verify integrity, not publisher trust. Existing PRO licences, prices and features remain unchanged.

## Archive Unpacker v1.0.2 - Explorer Integration

- The new Microsoft Store package includes native Explorer commands with embedded application icons for **Extract to folder**, **Extract Here**, and **Compress to ZIP**. Extraction applies to ZIP, 7Z, RAR, TAR, GZ, TGZ and BZ2; ZIP creation applies to a selected file or folder.
- Store menu commands support one selected item at a time. Standalone installs retain the **Show more options** menu on Windows11 and per-user registration on Windows10.
- PRO upgrade attempts now show progress and an explanation when checkout is unavailable or not completed, including Store error details when supplied. Entitlement queries are bounded; no purchase or licence bypass was added.
- Existing free and PRO features, Store identity and add-on IDs remain unchanged.

The1.0.2 standalone installer and portable ZIP are available in the [Archive Unpacker release](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/tag/suite-v1.0.2). The new MSIX has been submitted and is in certification; its Store rollout follows approval. Current standalone files remain unsigned. The old 1.0.1 releases remain available unchanged; a separate updated all-in-one bundle is included in the new release.

## Media Trim v1.0.2 - Production Release

Media Trim 1.0.2 is released:
- **PRO Batch Queue**: Process whole queues of video and audio files using a shared preset and output directory. Errors on one file do not interrupt processing of remaining queue items.
- **Dedicated Single-File Editor**: Responsive preview player, waveform visualizer, and precision trim markers remain free and dedicated for quick edits.
- **Five Free Presets**: MP3 320k, WAV, MP4 H.264, 720p compression, and lossless stream cut have no paid duration limits.
- **Embedded FFmpeg 9.0.2-sc1**: Self-contained engine with full open source archives and build scripts published at [FFmpeg 9.0.2-sc1 sources](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/tag/ffmpeg-9.0.2-sc1-sources).
- **Downloads**: Available on [GitHub Releases](https://github.com/sc-software-tools/sc-utility-suite-dist/releases/tag/media-trim-v1.0.2) and the Microsoft Store.

### Media Trim v1.0.2 SHA256 Checksums

| File | Type | SHA256 Hash |
| :--- | :--- | :--- |
| MediaTrim_Setup_v1.0.2.exe | Setup Wizard | `383507c06fb3c3700e527c6ad7d0819a837cc17d60b257c94b2f7aca9aa69f09` |
| MediaTrim_v1.0.2_Portable.zip | Portable ZIP | `35ccf63b8ca6f36e49cfe2afe207ec0e6d39c13df341031a0d107678c1b172bb` |
| MediaTrim_1.0.2.0_x64.msix | Store Package | `5745b5037cf43ef1225a66982c1cfeea8a5feb1f5b0c3c92d24f4d86cb54f310` |

---

## SC Utility Suite v1.0.1 - Production Release

Standalone v1.0.1 release. Existing Microsoft Store packages use package identity 1.0.1.0 and predate the latest standalone binaries. Media Trim is awaiting its Microsoft Store release. The other six apps are listed as available; availability may vary by market.

### Included Applications
- **Archive Unpacker**: Fast multi-format archive extraction (.zip, .7z, .tar, .gz, .bz2, .rar) and inspection
- **Dup Scrub**: Multi-phase duplicate file scanner (file size -> sampled XxHash64 -> full XxHash64; byte comparison before recycling) with Recycle Bin safety
- **HEIC Studio**: Batch convert Apple HEIC/HEIF photos, WebP, and AVIF to JPG, PNG, and PDF offline
- **Media Trim**: Video trimming, keyframe-dependent lossless video cuts and MP3/WAV audio extraction powered by embedded static FFmpeg
- **PDF Knife**: Local PDF page manipulation (split ranges, merge documents, burst pages) with zero cloud dependencies
- **Screen Lens**: Screen recording and optimized GIF creation with region selection and floating pause/resume/stop controls
- **USB Flasher**: Bootable UEFI ISO burning and raw sector disk imaging (.img, .bin) to removable drives

### Verified SHA256 Package Checksums

| File | Type | SHA256 Hash |
| :--- | :--- | :--- |
| SC_Utility_Suite_AllInOne_Setup_v1.0.1.exe | Master Installer | 17b82c13a377469e27918fcbaf65116fcf5ed484a34507884ce26a6aa979b114 |
| SC_Utility_Suite_AllInOne_v1.0.1_Portable.zip | Master Portable | d93a5641659dd86c107e398e6fb4aa23a6bf579f39d7a37db6af9eb4c6f4737e |
| ArchiveUnpacker_Setup_v1.0.1.exe | Setup Wizard | 8336557cf5ce27be8404a0464cc1bca15ffb66bd83ba4add93cce243e1ee5808 |
| ArchiveUnpacker_v1.0.1_Portable.zip | Portable ZIP | 5c6300366928101b9442c7af580a6b59edec6bb8edb899a556be8710556df6b3 |
| DupScrub_Setup_v1.0.1.exe | Setup Wizard | e244e0716dd67eaab4dd9f56931e0da82ac8b2a25aaf9ef01f6889e180b34c2b |
| DupScrub_v1.0.1_Portable.zip | Portable ZIP | 67fac2b1b2a966490e8a8f54eaf43723e7d1b16bef1aa756e4e0f8dc518594de |
| HeicStudio_Setup_v1.0.1.exe | Setup Wizard | a01aae722d65f47c46ffabfafe4861cc53dcad2960955dc7441ea4b50175f29e |
| HeicStudio_v1.0.1_Portable.zip | Portable ZIP | 9649f6ca721ebbb8c643801234cdb3569d2ad413bae7f688a733b68d9f1d2229 |
| MediaTrim_Setup_v1.0.1.exe | Setup Wizard | 5a929b8a0ef4585dfe5b6688c5444c44637b916ed87eba6b765a9804af081601 |
| MediaTrim_v1.0.1_Portable.zip | Portable ZIP | 17f27e9ee71e1fcd4abcd4f59f9f8b401412a8930b7d86dbdabd6eaafbbf95ab |
| PdfKnife_Setup_v1.0.1.exe | Setup Wizard | a4bae8c0d824545e7f1a637b00a1ce2d7224e5fddabf13628b438bf4eef8e617 |
| PdfKnife_v1.0.1_Portable.zip | Portable ZIP | 864a3223295c82231d3e9574696bbac2460a5b6691303debeb979b8d8e80634e |
| ScreenLens_Setup_v1.0.1.exe | Setup Wizard | 41385f5c66c589b04fa985fc30fa3fda055f1632af3b7cf364834fbb76f79a78 |
| ScreenLens_v1.0.1_Portable.zip | Portable ZIP | 1bb025afa444c51405608f99ebea46a16095b90dcab854f4235c8f8acdf44f31 |
| UsbFlasher_Setup_v1.0.1.exe | Setup Wizard | 8874ce4dce67a650e8e1666bee7c6c207858c7979a024ffaa61de8f9ff203191 |
| UsbFlasher_v1.0.1_Portable.zip | Portable ZIP | aebee5988ef96bb8a8ffa02977c80fa5a6ece66d7eb2dc657d085171fe55aa6a |

### System Requirements
- Windows 10 (Build 19041+) or Windows 11
- 64-bit (x64) processor architecture
- Completely self-contained .NET 8 runtime included; no external prerequisites required
### Signing and channel status

Current standalone installers are unsigned. The hashes above establish file integrity, not trusted publisher identity. Media Trim is awaiting its Microsoft Store release. Winget catalog merges remain pending; passing manifest validation does not establish catalog availability. File processing is local; purchase/activation checks contact Microsoft Store or Gumroad.

Media Trim edits one file at a time in both tiers; no batch queue or multipass feature is provided. PRO hides the upgrade strip. Other PRO limits are described on the showcase page. The exact source/build/dependency delivery for the included FFmpeg build remains an unresolved distribution requirement, separate from binary integrity checks.

### Known v1.0.1 ZIP-creation issue

In the free edition, selecting several separate inputs for ZIP creation can include only the first input. To include several files in v1.0.1, place them in one folder and add that folder. The 1.0.2 candidate fixes separate multi-input creation and has passed byte-content regression checks; it has not replaced the existing downloads or Store submissions.



