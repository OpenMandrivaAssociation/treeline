Summary:	Versatile Tree-Style Outliner for Defining Custom Data Schemas
Name:		treeline
Version:	1.4.1
Release:	1
Group:		Office
License:	GPLv2+
Url:		http://treeline.bellz.org/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-i18n-%{version}a.tar.gz
Source2:	httpload2.py.tar.gz
BuildArch:	noarch

BuildRequires:	python
Requires:	python-qt4
Requires(post,postun):	desktop-file-utils

%description
TreeLine is a versatile tool for working with all kinds of information
that fit into a tree-like structure.

It can be used to edit bookmark files, create mini-databases (for
example, for addresses, tasks, records, or CDs), outline documents, or
just collect ideas. It can also be used as a generic editor for XML
files.

The data schemas for any node in the data tree can be customized and
new types of nodes can be defined. The way data is presented on the
screen, exported to HTML, or printed can be defined with HTML-like
templates. Plug-ins can be written to load and save data from and to
custom file formats or external data sources and extend the
functionality of TreeLine.

TreeLine is written in Python and uses the PyQt bindings to the Qt
toolkit, which makes it very portable.

%prep
%setup -qn TreeLine -b1 -a2

%build

%install
for i in source/*.py; do
	sed -i "s|#!/usr/bin/env python|#!/usr/bin/python|g" $i
	chmod 755 $i
done

python install.py -x \
	-p %{_prefix} \
	-d %{_defaultdocdir}/%{name} \
	-i %{_datadir}/%{name}/icons \
	-b %{buildroot}

# httpload2 plugin
install -D -m 644 httpload2.py %{buildroot}%{_prefix}/lib/%{name}/plugins/httpload2.py

# Associate Files with MimeTypes (the KDE4/Gnome way)
mkdir -p %{buildroot}%{_datadir}/mime/packages
cat > %{buildroot}%{_datadir}/mime/packages/%{name}.xml << EOF
<?xml version="1.0"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/x-treeline">
    <comment>TreeLine File</comment>
    <glob pattern="*.trl"/>
    <glob pattern="*.TRL"/>
  </mime-type>
  <mime-type type="application/x-treeline-gz">
    <comment>Compressed TreeLine File</comment>
    <glob pattern="*.trl.gz"/>
    <glob pattern="*.TRL.GZ"/>
  </mime-type>
  <mime-type type="application/x-treepad">
    <comment>TreePad File</comment>
    <glob pattern="*.hjt"/>
    <glob pattern="*.HJT"/>
  </mime-type>
</mime-info>
EOF

# Menu entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Exec=%{name}
Icon=%{name}
Name=TreeLine
GenericName=Outliner
Categories=Office;X-MandrivaLinux-Office-TasksManagement;
MimeType=application/x-treeline;application/x-treeline-gz;application/x-treepad;text/xml;
StartupNotify=true
Terminal=false
EOF

# Icon
install -D -m 644 %{buildroot}%{_datadir}/%{name}/icons/tree/%{name}.png %{buildroot}%{_iconsdir}/%{name}.png

%files
%doc %{_defaultdocdir}/%{name}
%{_bindir}/%{name}
%{_usr}/lib/%{name}
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png

