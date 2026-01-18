"""
STORY-242: OS-Specific Installer Generation Module

This module generates installer configuration files for multiple platforms:
- Windows: WiX (.wxs) and NSIS (.nsi)
- Linux: Debian (DEBIAN directory) and RPM (.spec)
- macOS: pkgbuild scripts and distribution.xml

All generated configurations are templates that can be built with platform-specific
tools (WiX Toolset, NSIS, dpkg-deb, rpmbuild, pkgbuild).
"""

import logging
import os
import shutil
import stat
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class InstallerConfig:
    """
    Holds generated installer configuration details.

    Technical Specification fields:
    - platform: Target platform (windows, linux_deb, linux_rpm, macos)
    - format: Installer format (msi, nsis, deb, rpm, pkg)
    - config_path: Path to generated configuration file(s)
    - build_command: Optional shell command to build installer from config
    - tool_required: Tool needed to build installer
    - tool_available: True if required tool is installed on system
    - metadata: Platform-specific metadata (GUIDs, dependencies, etc.)
    """
    platform: str
    format: str
    config_path: str
    build_command: Optional[str] = None
    tool_required: str = ""
    tool_available: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class InstallerGenerator:
    """
    Service for generating OS-specific installer configurations.

    Implements EPIC-037 Feature 2 - Phase 0.4a (OS-Specific Installer Generation).
    Generates installer configuration files for platform-specific installation tools.
    """

    # Platform to format mapping
    PLATFORM_FORMATS = {
        "windows": ["msi", "nsis"],
        "linux_deb": ["deb"],
        "linux_rpm": ["rpm"],
        "macos": ["pkg"],
    }

    # Format to tool mapping
    FORMAT_TOOLS = {
        "msi": "wix",
        "nsis": "nsis",
        "deb": "dpkg-deb",
        "rpm": "rpmbuild",
        "pkg": "pkgbuild",
    }

    # Tool detection command mapping (actual executables to check)
    TOOL_EXECUTABLES = {
        "wix": ["candle", "light", "wix"],
        "nsis": ["makensis"],
        "dpkg-deb": ["dpkg-deb"],
        "rpmbuild": ["rpmbuild"],
        "pkgbuild": ["pkgbuild"],
    }

    # Build command templates
    BUILD_COMMANDS = {
        "msi": "candle {config_path} && light {wixobj_path}",
        "nsis": "makensis {config_path}",
        "deb": "dpkg-deb --build {package_dir}",
        "rpm": "rpmbuild -bb {config_path}",
        "pkg": "pkgbuild --root {root_dir} --identifier {identifier} --version {version} {output_path} && productbuild --distribution {distribution_xml} --package-path . {final_pkg}",
    }

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize InstallerGenerator.

        Args:
            output_dir: Directory for generated installer configs.
                        Defaults to current directory.
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def detect_tool(self, tool_name: str) -> bool:
        """
        Detect if a required build tool is installed.

        Args:
            tool_name: Name of the tool (wix, nsis, dpkg-deb, rpmbuild, pkgbuild)

        Returns:
            True if any of the tool's executables are found in PATH
        """
        executables = self.TOOL_EXECUTABLES.get(tool_name, [tool_name])
        for exe in executables:
            if shutil.which(exe):
                return True
        return False

    def extract_file_list(self, package_path: str) -> List[str]:
        """
        Extract file list from a package archive.

        Args:
            package_path: Path to ZIP, tar.gz, or other archive

        Returns:
            List of file paths within the archive
        """
        file_list = []
        path = Path(package_path)

        if path.suffix == ".zip" or path.suffixes == [".tar", ".gz"]:
            try:
                with zipfile.ZipFile(path, 'r') as zf:
                    file_list = zf.namelist()
            except (zipfile.BadZipFile, FileNotFoundError):
                logger.warning(f"Could not read package archive: {package_path}")

        return file_list

    def generate(
        self,
        platform: str,
        format: str,
        package_info: Dict[str, Any],
        output_subdir: Optional[str] = None,
    ) -> InstallerConfig:
        """
        Generate installer configuration for a specific platform and format.

        Args:
            platform: Target platform (windows, linux_deb, linux_rpm, macos)
            format: Installer format (msi, nsis, deb, rpm, pkg)
            package_info: Package metadata (name, version, description, files, etc.)
            output_subdir: Optional subdirectory within output_dir

        Returns:
            InstallerConfig with generated configuration details
        """
        # Determine output directory
        out_dir = self.output_dir
        if output_subdir:
            out_dir = self.output_dir / output_subdir
            out_dir.mkdir(parents=True, exist_ok=True)

        # Get tool for this format
        tool_required = self.FORMAT_TOOLS.get(format, format)
        tool_available = self.detect_tool(tool_required)

        # Log warning if tool not available (BR-001: still generate config)
        if not tool_available:
            logger.info(f"Tool '{tool_required}' not found. Config will be generated but cannot be built locally.")

        # Generate format-specific configuration
        generator_method = getattr(self, f"_generate_{format}", None)
        if not generator_method:
            raise ValueError(f"Unsupported format: {format}")

        config_path, metadata = generator_method(out_dir, package_info)

        # Build command template
        build_command = self.BUILD_COMMANDS.get(format, "")
        if build_command:
            build_command = build_command.format(
                config_path=config_path,
                wixobj_path=str(Path(config_path).with_suffix(".wixobj")),
                package_dir=str(Path(config_path).parent),
                root_dir=out_dir / "root",
                identifier=package_info.get("identifier", package_info.get("name", "package")),
                version=package_info.get("version", "1.0.0"),
                output_path=out_dir / f"{package_info.get('name', 'package')}.pkg",
                distribution_xml=out_dir / "distribution.xml",
                final_pkg=out_dir / f"{package_info.get('name', 'package')}-final.pkg",
            )

        return InstallerConfig(
            platform=platform,
            format=format,
            config_path=str(config_path),
            build_command=build_command if build_command else None,
            tool_required=tool_required,
            tool_available=tool_available,
            metadata=metadata,
        )

    def generate_all(
        self,
        package_info: Dict[str, Any],
        platforms: Optional[List[str]] = None,
    ) -> List[InstallerConfig]:
        """
        Generate installer configurations for multiple platforms.

        Args:
            package_info: Package metadata
            platforms: List of platforms to generate for.
                       Defaults to all platforms.

        Returns:
            List of InstallerConfig for each platform/format combination
        """
        if platforms is None:
            platforms = list(self.PLATFORM_FORMATS.keys())

        configs = []
        for platform in platforms:
            formats = self.PLATFORM_FORMATS.get(platform, [])
            for fmt in formats:
                try:
                    config = self.generate(
                        platform=platform,
                        format=fmt,
                        package_info=package_info,
                        output_subdir=platform,
                    )
                    configs.append(config)
                except Exception as e:
                    logger.error(f"Failed to generate {fmt} for {platform}: {e}")
                    # Continue with other formats (AC#5 - continue even if one fails)

        return configs

    def _generate_msi(
        self,
        output_dir: Path,
        package_info: Dict[str, Any],
    ) -> tuple[str, Dict[str, Any]]:
        """
        Generate WiX source file (.wxs) for Windows MSI installer.

        AC#1: Windows Installer Configuration (MSI/WiX)
        - Product ID and upgrade code (GUIDs)
        - Component definitions for all files
        - Start menu shortcuts
        - Uninstall support
        """
        name = package_info.get("name", "Package")
        version = package_info.get("version", "1.0.0")
        manufacturer = package_info.get("manufacturer", package_info.get("publisher", "Unknown"))
        description = package_info.get("description", "")
        files = package_info.get("files", [])

        # Generate unique GUIDs (BR-002)
        product_guid = str(uuid.uuid4()).upper()
        upgrade_code = str(uuid.uuid4()).upper()
        component_guid = str(uuid.uuid4()).upper()

        # Build file components
        file_components = ""
        for i, file_path in enumerate(files):
            file_name = Path(file_path).name
            file_components += f'''
            <Component Id="Component{i}" Guid="{str(uuid.uuid4()).upper()}">
                <File Id="File{i}" Source="{file_path}" Name="{file_name}" KeyPath="yes" />
            </Component>'''

        wxs_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="{product_guid}"
             Name="{name}"
             Version="{version}"
             Manufacturer="{manufacturer}"
             Language="1033"
             UpgradeCode="{upgrade_code}">

        <Package Description="{description}"
                 InstallerVersion="200"
                 Compressed="yes"
                 InstallScope="perMachine" />

        <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
        <MediaTemplate EmbedCab="yes" />

        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="{name}">
                    {file_components}
                </Directory>
            </Directory>
            <Directory Id="ProgramMenuFolder">
                <Directory Id="ApplicationProgramsFolder" Name="{name}">
                    <Component Id="ApplicationShortcut" Guid="{component_guid}">
                        <Shortcut Id="ApplicationStartMenuShortcut"
                                  Name="{name}"
                                  Target="[INSTALLFOLDER]{name}.exe"
                                  WorkingDirectory="INSTALLFOLDER" />
                        <RemoveFolder Id="RemoveApplicationProgramsFolder" On="uninstall" />
                        <RegistryValue Root="HKCU" Key="Software\\{manufacturer}\\{name}"
                                       Name="installed" Type="integer" Value="1" KeyPath="yes" />
                    </Component>
                </Directory>
            </Directory>
        </Directory>

        <Feature Id="ProductFeature" Title="{name}" Level="1">
            <ComponentRef Id="ApplicationShortcut" />
        </Feature>

        <!-- Uninstall support -->
        <Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />
        <UIRef Id="WixUI_InstallDir" />
    </Product>
</Wix>
'''

        config_path = output_dir / f"{name}.wxs"
        config_path.write_text(wxs_content, encoding="utf-8")

        metadata = {
            "product_guid": product_guid,
            "upgrade_code": upgrade_code,
            "component_guid": component_guid,
        }

        return str(config_path), metadata

    def _generate_nsis(
        self,
        output_dir: Path,
        package_info: Dict[str, Any],
    ) -> tuple[str, Dict[str, Any]]:
        """
        Generate NSIS script (.nsi) for Windows EXE installer.

        AC#2: Windows Installer Configuration (NSIS)
        - Installer metadata (name, version, publisher)
        - Installation directory selection
        - File installation commands
        - Uninstaller creation
        """
        name = package_info.get("name", "Package")
        version = package_info.get("version", "1.0.0")
        publisher = package_info.get("publisher", package_info.get("manufacturer", "Unknown"))
        description = package_info.get("description", "")
        files = package_info.get("files", [])

        # Build file installation commands
        file_commands = ""
        for file_path in files:
            file_commands += f'    File "{file_path}"\n'

        # Build uninstaller delete commands
        delete_commands = ""
        for file_path in files:
            file_name = Path(file_path).name
            delete_commands += f'    Delete "$INSTDIR\\{file_name}"\n'

        nsi_content = f'''!include "MUI2.nsh"

; Installer metadata
Name "{name}"
OutFile "{name}-{version}-setup.exe"
InstallDir "$PROGRAMFILES\\{name}"
InstallDirRegKey HKLM "Software\\{name}" "Install_Dir"

; Version information
VIProductVersion "{version}.0"
VIAddVersionKey "ProductName" "{name}"
VIAddVersionKey "ProductVersion" "{version}"
VIAddVersionKey "CompanyName" "{publisher}"
VIAddVersionKey "FileDescription" "{description}"
VIAddVersionKey "FileVersion" "{version}"

; Request admin privileges
RequestExecutionLevel admin

; UI settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; Installation section
Section "Install"
    SetOutPath "$INSTDIR"

    ; Install files
{file_commands}

    ; Create uninstaller
    WriteUninstaller "$INSTDIR\\uninstall.exe"

    ; Create Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\\{name}"
    CreateShortCut "$SMPROGRAMS\\{name}\\{name}.lnk" "$INSTDIR\\{name}.exe"
    CreateShortCut "$SMPROGRAMS\\{name}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"

    ; Write registry keys for Add/Remove Programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{name}" "DisplayName" "{name}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{name}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{name}" "DisplayVersion" "{version}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{name}" "Publisher" "{publisher}"
SectionEnd

; Uninstaller section
Section "Uninstall"
    ; Remove files
{delete_commands}
    Delete "$INSTDIR\\uninstall.exe"

    ; Remove shortcuts
    Delete "$SMPROGRAMS\\{name}\\*.*"
    RMDir "$SMPROGRAMS\\{name}"

    ; Remove installation directory
    RMDir "$INSTDIR"

    ; Remove registry keys
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{name}"
    DeleteRegKey HKLM "Software\\{name}"
SectionEnd
'''

        config_path = output_dir / f"{name}.nsi"
        config_path.write_text(nsi_content, encoding="utf-8")

        metadata = {
            "installer_name": f"{name}-{version}-setup.exe",
        }

        return str(config_path), metadata

    def _generate_deb(
        self,
        output_dir: Path,
        package_info: Dict[str, Any],
    ) -> tuple[str, Dict[str, Any]]:
        """
        Generate DEBIAN control directory for Debian/Ubuntu .deb packages.

        AC#3: Linux Installer Configuration (Debian)
        - control file (package metadata)
        - postinst script (post-installation)
        - prerm script (pre-removal)
        """
        name = package_info.get("name", "package").lower().replace(" ", "-")
        version = package_info.get("version", "1.0.0")
        description = package_info.get("description", "No description")
        maintainer = package_info.get("maintainer", package_info.get("publisher", "Unknown <unknown@example.com>"))
        architecture = package_info.get("architecture", "all")
        dependencies = package_info.get("dependencies", [])

        # Create DEBIAN directory
        debian_dir = output_dir / "DEBIAN"
        debian_dir.mkdir(parents=True, exist_ok=True)

        # Build dependencies string (BR-003)
        depends_str = ", ".join(dependencies) if dependencies else ""

        # Generate control file
        control_content = f'''Package: {name}
Version: {version}
Section: misc
Priority: optional
Architecture: {architecture}
Maintainer: {maintainer}
Description: {description}
'''
        if depends_str:
            control_content += f"Depends: {depends_str}\n"

        control_path = debian_dir / "control"
        control_path.write_text(control_content, encoding="utf-8")

        # Generate postinst script (BR-004: use bash)
        postinst_content = f'''#!/bin/bash
# Post-installation script for {name}

set -e

# Configure the package
echo "Configuring {name}..."

# Update ldconfig if installing libraries
if [ -d /usr/lib/{name} ]; then
    ldconfig
fi

# Restart services if needed
# systemctl restart {name} || true

echo "{name} installation complete."

exit 0
'''
        postinst_path = debian_dir / "postinst"
        postinst_path.write_text(postinst_content, encoding="utf-8")
        # Make executable
        postinst_path.chmod(postinst_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        # Generate prerm script (BR-004: use bash)
        prerm_content = f'''#!/bin/bash
# Pre-removal script for {name}

set -e

# Stop services before removal
# systemctl stop {name} || true

echo "Preparing to remove {name}..."

exit 0
'''
        prerm_path = debian_dir / "prerm"
        prerm_path.write_text(prerm_content, encoding="utf-8")
        prerm_path.chmod(prerm_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        metadata = {
            "package_name": name,
            "control_path": str(control_path),
            "postinst_path": str(postinst_path),
            "prerm_path": str(prerm_path),
            "depends": dependencies,  # BR-003: Store dependencies in metadata
        }

        return str(debian_dir), metadata

    def _generate_rpm(
        self,
        output_dir: Path,
        package_info: Dict[str, Any],
    ) -> tuple[str, Dict[str, Any]]:
        """
        Generate RPM spec file for RHEL/CentOS/Fedora packages.

        AC#4: Linux Installer Configuration (RPM)
        - Package metadata (name, version, release)
        - Build instructions
        - File list
        - Pre/post install scripts
        """
        name = package_info.get("name", "package")
        version = package_info.get("version", "1.0.0")
        release = package_info.get("release", "1")
        summary = package_info.get("summary", package_info.get("description", "Package"))[:80]
        description = package_info.get("description", "No description")
        license_type = package_info.get("license", "MIT")
        url = package_info.get("url", "")
        files = package_info.get("files", [])
        dependencies = package_info.get("dependencies", [])

        # Build requires string
        requires_str = "\n".join([f"Requires: {dep}" for dep in dependencies]) if dependencies else ""

        # Build file list
        files_list = "\n".join([f"%{{_bindir}}/{Path(f).name}" for f in files]) if files else "%{_bindir}/*"

        spec_content = f'''Name:           {name}
Version:        {version}
Release:        {release}%{{?dist}}
Summary:        {summary}

License:        {license_type}
URL:            {url}
Source0:        %{{name}}-%{{version}}.tar.gz

{requires_str}

%description
{description}

%prep
%autosetup -n %{{name}}-%{{version}}

%build
# Build commands here
%configure
%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%files
%license LICENSE
%doc README.md
{files_list}

%post
# Post-installation script
echo "Installing %{{name}}..."
/sbin/ldconfig

%preun
# Pre-uninstallation script
if [ $1 -eq 0 ]; then
    echo "Removing %{{name}}..."
fi

%postun
# Post-uninstallation script
/sbin/ldconfig

%changelog
* {self._get_rpm_date()} Maintainer <maintainer@example.com> - {version}-{release}
- Initial package release
'''

        config_path = output_dir / f"{name}.spec"
        config_path.write_text(spec_content, encoding="utf-8")

        metadata = {
            "spec_path": str(config_path),
        }

        return str(config_path), metadata

    def _generate_pkg(
        self,
        output_dir: Path,
        package_info: Dict[str, Any],
    ) -> tuple[str, Dict[str, Any]]:
        """
        Generate pkgbuild scripts for macOS .pkg installer.

        AC#5: macOS Installer Configuration (pkg)
        - Component package definition
        - Distribution XML for customization
        - Post-installation scripts
        """
        name = package_info.get("name", "Package")
        version = package_info.get("version", "1.0.0")
        identifier = package_info.get("identifier", f"com.example.{name.lower()}")
        title = package_info.get("title", name)

        # Create scripts directory
        scripts_dir = output_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)

        # Generate distribution.xml
        distribution_content = f'''<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="1">
    <title>{title}</title>
    <organization>{identifier}</organization>
    <domains enable_localSystem="true"/>
    <options customize="never" require-scripts="true" rootVolumeOnly="true"/>

    <welcome file="welcome.html" mime-type="text/html"/>
    <license file="license.txt" mime-type="text/plain"/>
    <conclusion file="conclusion.html" mime-type="text/html"/>

    <pkg-ref id="{identifier}"/>

    <choices-outline>
        <line choice="default">
            <line choice="{identifier}"/>
        </line>
    </choices-outline>

    <choice id="default"/>
    <choice id="{identifier}" visible="false">
        <pkg-ref id="{identifier}"/>
    </choice>

    <pkg-ref id="{identifier}" version="{version}" onConclusion="none">{name}.pkg</pkg-ref>
</installer-gui-script>
'''

        distribution_path = output_dir / "distribution.xml"
        distribution_path.write_text(distribution_content, encoding="utf-8")

        # Generate postinstall script (BR-004: use bash)
        postinstall_content = f'''#!/bin/bash
# Post-installation script for {name}

set -e

# Set permissions
chmod -R 755 /Applications/{name}.app 2>/dev/null || true

# Register with Launch Services
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f /Applications/{name}.app 2>/dev/null || true

echo "{name} installation complete."

exit 0
'''

        postinstall_path = scripts_dir / "postinstall"
        postinstall_path.write_text(postinstall_content, encoding="utf-8")
        postinstall_path.chmod(postinstall_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        # Generate build script
        build_script_content = f'''#!/bin/bash
# Build script for {name} macOS installer

set -e

VERSION="{version}"
IDENTIFIER="{identifier}"
NAME="{name}"

# Build component package
pkgbuild --root ./root \\
         --identifier "$IDENTIFIER" \\
         --version "$VERSION" \\
         --scripts ./scripts \\
         --install-location /Applications \\
         "$NAME.pkg"

# Build product archive with distribution
productbuild --distribution distribution.xml \\
             --package-path . \\
             --version "$VERSION" \\
             "$NAME-$VERSION.pkg"

echo "Build complete: $NAME-$VERSION.pkg"
'''

        build_script_path = output_dir / "build.sh"
        build_script_path.write_text(build_script_content, encoding="utf-8")
        build_script_path.chmod(build_script_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        metadata = {
            "distribution_xml": str(distribution_path),
            "postinstall_path": str(postinstall_path),
            "build_script": str(build_script_path),
            "identifier": identifier,
        }

        return str(distribution_path), metadata

    @staticmethod
    def _get_rpm_date() -> str:
        """Get current date in RPM changelog format."""
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%a %b %d %Y")
