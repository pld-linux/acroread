#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
Summary:	Acrobat Reader
Summary(pl.UTF-8):   Acrobat Reader - czytnik plików PDF
Summary(ru.UTF-8):   Программа для чтения документов в формате PDF от Adobe
Summary(uk.UTF-8):   Програма для читання документів у форматі PDF від Adobe
%define		base_name	acroread
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	7.0
Release:	0.1%{?with_license_agreement:wla}
Epoch:		1
License:	distribution restricted (http://www.adobe.com/products/acrobat/distribute.html)
# in short:
# - not distributable on public sites (only linking to adobe.com permitted)
# - distribution on CD requires signing Distribution Agreement (see URL above)
#
# download it manually from: ftp://ftp.adobe.com/pub/adobe/reader/unix/7x/7.0/enu/
Group:		X11/Applications/Graphics
%if %{with license_agreement}
Source0:	AdbeRdr70_linux_enu.tar.gz
%endif
Source1:	%{base_name}.desktop
Source2:	%{base_name}.png
URL:		http://www.adobe.com/products/acrobat/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozdir		%{_libdir}/mozilla/plugins

%define		platform	intellinux
%define		tar0		ILINXR.TAR
%define		tar1		COMMON.TAR

%define		_noautostrip	'.*\.api'
%define		_noautoreq	'^lib.*\.so$' '^lib.*\(VERSION\)$'

%description
Adobe(R) Reader(R) is free software that lets you view and print
PDF files (Portable Document Format) on a variety of hardware and
operating system platforms.

%description -l pl.UTF-8
Adobe(R) Reader(R) jest darmowym oprogramowaniem umożliwiającym oglądanie
oraz drukowanie plików PDF (Portable Document Format) na różnych platformach
sprzętowych oraz różnych systemach operacyjnych.

%description -l ru.UTF-8
Программа для чтения документов в формате Portable Document Format
(PDF), сгенерированных Adobe Acrobat'ом.

%description -l uk.UTF-8
Програма для читання документів у форматі Portable Document Format
(PDF), згенерованих Adobe Acrobat'ом.

%package -n mozilla-plugin-%{base_name}
Summary:	Mozilla PDF plugin
Summary(pl.UTF-8):   Wtyczka PDF do Mozilli
Group:		X11/Applications
Prereq:		mozilla-embedded
Requires:	%{base_name} = %{epoch}:%{version}

%description -n mozilla-plugin-%{base_name}
A Mozilla plugin for displaying PDF (Portable Document Format) files.

%description -n mozilla-plugin-%{base_name} -l pl.UTF-8
Wtyczka Mozilli do wyświetlania plików PDF (Portable Document Format).

%prep
%if %{with license_agreement}
%setup -q -c
cd AdobeReader
tar xf %{tar0}
tar xf %{tar1}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if ! %{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/%{base_name}.install
#!/bin/sh
if [ "\$1" = "--with" -a "\$2" = "license_agreement" ]; then
	TMPDIR=\`rpm --eval "%%{tmpdir}"\`; export TMPDIR
	SPECDIR=\`rpm --eval "%%{_specdir}"\`; export SPECDIR
	SRPMDIR=\`rpm --eval "%%{_srcrpmdir}"\`; export SRPMDIR
	SOURCEDIR=\`rpm --eval "%%{_sourcedir}"\`; export SOURCEDIR
	BUILDDIR=\`rpm --eval "%%{_builddir}"\`; export BUILDDIR
	RPMDIR=\`rpm --eval "%%{_rpmdir}"\`; export RPMDIR
	BACKUP=0
	mkdir -p \$TMPDIR \$SPECDIR \$SRPMDIR \$RPMDIR \$SRPMDIR \$SOURCEDIR \$BUILDDIR
	if [ -f \$SPECDIR/%{base_name}.spec ]; then
		BACKUP=1
		mv -f \$SPECDIR/%{base_name}.spec \$SPECDIR/%{base_name}.spec.prev
	fi
	for i in %{base_name}.desktop %{base_name}.png %{base_name}-locale.patch; do
		if [ -f \$SOURCEDIR/\$i ]; then
			mv -f \$SOURCEDIR/\$i \$SOURCEDIR/\$i.prev
			BACKUP=1
		fi
	done
	if echo "\$3" | grep '\.src\.rpm$' >/dev/null; then
		( cd \$SRPMDIR
		if echo "\$3" | grep '://' >/dev/null; then
			wget --passive-ftp -t0 "\$3"
		else
			cp -f "\$3" .
		fi
		rpm2cpio \`basename "\$3"\` | ( cd \$TMPDIR; cpio -i %{base_name}.spec )
		for i in %{base_name}.desktop %{base_name}.png; do
			rpm2cpio \$i | ( cd \$TMPDIR; cpio -i \$i )
		done )
		cp -i \$TMPDIR/%{base_name}.spec \$SPECDIR/%{base_name}.spec \
			|| exit 1
		for i in %{base_name}.desktop %{base_name}.png; do
			cp -i \$TMPDIR/\$i \$SOURCEDIR/\$i || exit 1
		done
	else
		cp -i "\$3" \$SPECDIR || exit 1
		for i in %{base_name}.desktop %{base_name}.png; do
			cp -i %{_datadir}/%{base_name}/\$i \$SOURCEDIR/\$i || exit 1
		done
	fi
	( cd \$SPECDIR
	%{_bindir}/builder -nc -ncs --with license_agreement --opts --target=%{_target_cpu} %{base_name}.spec
	if [ "\$?" -ne 0 ]; then
		exit 2
	fi
	RPMNAME1=%{base_name}-%{version}-%{release}wla.%{_target_cpu}.rpm
	RPMNAME2=mozilla-plugin-%{base_name}-%{version}-%{release}wla.%{_target_cpu}.rpm
	echo "Installing \$RPMNAME1"
	RPMNAMES=\$RPMDIR/\$RPMNAME1
	if rpm -q --whatprovides mozilla-embedded >/dev/null 2>&1; then
		RPMNAMES="\$RPMNAMES \$RPMDIR/\$RPMNAME2"
		echo "Installing \$RPMNAME2"
	else
		echo "Not installing \$RPMNAME2"
	fi
	rpm -U \$RPMNAMES || \
		echo -e "Install manually the file(s):\n   \$RPMNAMES" )
	if [ "\$BACKUP" -eq 1 ]; then
		if [ -f \$SPECDIR/%{base_name}.spec.prev ]; then
			mv -f \$SPECDIR/%{base_name}.spec.prev \$SPECDIR/%{base_name}.spec
		fi
		for i in %{base_name}.desktop %{base_name}.png %{base_name}-locale.patch; do
			if [ -f \$SOURCEDIR/\$i.prev ]; then
				mv -f \$SOURCEDIR/\$i.prev \$SOURCEDIR/\$i
			fi
		done
	fi
else
	echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

\$0 --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
fi
EOF

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{base_name},%{mozdir}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

cd AdobeReader
cp -a Reader Resource $RPM_BUILD_ROOT%{_libdir}/%{base_name}
awk -v INSTDIR=%{_libdir}/%{base_name}/Reader \
	'/^install_dir=/ {print "install_dir="INSTDIR; next} \
	{print}' \
	bin/%{base_name} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}
install Browser/intellinux/* $RPM_BUILD_ROOT%{mozdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

chmod a-x $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/%{platform}/lib/*.so.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if ! %{with license_agreement}
%pre
echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%files
%defattr(644,root,root,755)
%if ! %{with license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%doc AdobeReader/{LICREAD.TXT,README}
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{base_name}
%{_libdir}/%{base_name}/Resource

%dir %{_libdir}/%{base_name}/Reader
%{_libdir}/%{base_name}/Reader/help
%{_libdir}/%{base_name}/Reader/AcroVersion
%{_libdir}/%{base_name}/Reader/HowTo
%{_libdir}/%{base_name}/Reader/Legal
%{_libdir}/%{base_name}/Reader/JavaScripts
%{_libdir}/%{base_name}/Reader/Messages
%{_libdir}/%{base_name}/Reader/WebSearch
%dir %{_libdir}/%{base_name}/Reader/%{platform}
#%{_libdir}/%{base_name}/Reader/%{platform}/fonts
%{_libdir}/%{base_name}/Reader/%{platform}/res
%{_libdir}/%{base_name}/Reader/%{platform}/SPPlugins
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/bin
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/lib
%{_desktopdir}/acroread.desktop
%{_pixmapsdir}/*

%files -n mozilla-plugin-%{base_name}
%defattr(644,root,root,755)
%attr(755,root,root) %{mozdir}/*
%endif
