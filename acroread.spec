#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
%define		base_name	acroread
%define		rel		1
Summary:	Adobe Acrobat Reader
Summary(pl.UTF-8):	Adobe Acrobat Reader - czytnik plików PDF
Summary(ru.UTF-8):	Программа для чтения документов в формате PDF от Adobe
Summary(uk.UTF-8):	Програма для читання документів у форматі PDF від Adobe
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	9.5.5
Release:	%{rel}%{?with_license_agreement:wla}
Epoch:		1
License:	distribution restricted (http://www.adobe.com/products/acrobat/distribute.html)
# in short:
# - not distributable on public sites (only linking to adobe.com permitted)
# - distribution on CD requires signing Distribution Agreement (see URL above)
Group:		X11/Applications/Graphics
%if %{with license_agreement}
Source0:	ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/%{version}/enu/AdbeRdr%{version}-1_i486linux_enu.tar.bz2
# NoSource0-md5:	664d546fbf0ad91f20dcf3753b0a2684
NoSource:	0
%else
Source1:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source1-md5:	329c25f457fea66ec502b7ef70cb9ede
%endif
# please update @COPYSOURCES@ below if you add more Sources or Patches.
Source2:	%{base_name}.desktop
Source3:	%{base_name}.png
URL:		http://www.adobe.com/products/acrobat/
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.357
# to force 32bit iconv
Requires:	%{_libdir}/gconv
Requires:	ca-certificates >= 20080809-4
Requires:	iconv
Requires:	openldap-libs < 2.5
Requires:	openldap-libs >= 2.4
%else
Requires:	rpm-build-tools >= 4.4.37
Requires:	rpmbuild(macros) >= 1.544
%endif
ExclusiveArch:	%{ix86}
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		platform	intellinux
%define		tar0		ILINXR.TAR
%define		tar1		COMMON.TAR

%define		_noautostrip	.*\.api
%define		_noautoprov	libcrypto\.so.* libssl\.so.* libcurl\.so.* libicu.* libstdc++\.so.* libgcc_s\.so.*
%if "%{_rpmversion}" >= "5.0"
%define		_noautoreq	%{_noautoprov} '^lib.*\.so$' '^lib.*\\(VERSION\\)$'
%else
%define		_noautoreq	%{_noautoprov} '^lib.*\.so$' '^lib.*\(VERSION\)$'
%endif
%define         no_install_post_check_so        1

%description
Adobe(R) Reader(R) is free software that lets you view and print PDF
files (Portable Document Format) on a variety of hardware and
operating system platforms.

%description -l pl.UTF-8
Adobe(R) Reader(R) jest darmowym oprogramowaniem umożliwiającym
oglądanie oraz drukowanie plików PDF (Portable Document Format) na
różnych platformach sprzętowych oraz różnych systemach operacyjnych.

%description -l ru.UTF-8
Программа для чтения документов в формате Portable Document Format
(PDF), сгенерированных Adobe Acrobat'ом.

%description -l uk.UTF-8
Програма для читання документів у форматі Portable Document Format
(PDF), згенерованих Adobe Acrobat'ом.

%package -n browser-plugin-%{name}
Summary:	PDF plugin for Mozilla compatible browsers
Summary(pl.UTF-8):	Wtyczka PDF dla przeglądarek zgodnych Mozilla
Group:		X11/Applications
Requires:	%{base_name} = %{epoch}:%{version}-%{release}
Requires:	browser-plugins >= 2.0
Obsoletes:	acroread-plugin
Obsoletes:	mozilla-plugin-acroread

%description -n browser-plugin-%{name}
A Mozilla plugin for displaying PDF (Portable Document Format) files.

%description -n browser-plugin-%{name} -l pl.UTF-8
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
%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@DATADIR@,%{_datadir}/%{base_name},g
	s/@COPYSOURCES@/%{base_name}{.desktop,.png}/g
' %{SOURCE1} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{base_name}/bin} \
	$RPM_BUILD_ROOT{%{_browserpluginsdir},%{_desktopdir},%{_pixmapsdir}}

cd AdobeReader/Adobe/Reader9
cp -a Browser Reader Resource $RPM_BUILD_ROOT%{_libdir}/%{base_name}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Browser/install_browser_plugin
awk -v INSTDIR=%{_libdir}/%{base_name}/Reader \
	'/^install_dir=/ {print "install_dir="INSTDIR; next} \
	{print}' \
	bin/%{base_name} > $RPM_BUILD_ROOT%{_libdir}/%{base_name}/bin/%{base_name}

# IMPORTANT NOTE: Here symlinks must be used instead of moving parts of tree
# for compatibility with other binary-only Adobe software (like AIR).
# This one is required to find Reader tree (relative to symlink target)...
ln -sf %{_libdir}/%{base_name}/bin/%{base_name} $RPM_BUILD_ROOT%{_bindir}/%{base_name}
# ...and nppdf plugin is expected in Browser subdir...
# ...so just symlink it to be used as browsers plugin.
ln -sf %{_libdir}/%{base_name}/Browser/%{platform}/nppdf.so $RPM_BUILD_ROOT%{_browserpluginsdir}/nppdf.so

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}

ln -sf /usr/lib/liblber-2.4.so.2 $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/%{platform}/lib/liblber.so
ln -sf /usr/lib/libldap-2.4.so.2 $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/%{platform}/lib/libldap.so
ln -sf /etc/certs/ca-certificates.crt $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/Cert/curl-ca-bundle.crt

# don't generate dependencies for internal libs
chmod a-x $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/%{platform}/lib/*.so.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
%post
%{_bindir}/%{base_name}.install
%endif

%if %{with license_agreement}
%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi
%endif

%files
%defattr(644,root,root,755)
%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%doc AdobeReader/ReadMe.htm
%attr(755,root,root) %{_bindir}/acroread
%dir %{_libdir}/%{base_name}
%dir %{_libdir}/%{base_name}/Browser
%dir %{_libdir}/%{base_name}/Browser/%{platform}
%attr(755,root,root) %{_libdir}/%{base_name}/Browser/%{platform}/nppdf.so
%{_libdir}/%{base_name}/Browser/HowTo
%dir %{_libdir}/%{base_name}/Reader
%{_libdir}/%{base_name}/Reader/help
%{_libdir}/%{base_name}/Reader/AcroVersion
%{_libdir}/%{base_name}/Reader/Cert
%{_libdir}/%{base_name}/Reader/GlobalPrefs
%{_libdir}/%{base_name}/Reader/IDTemplates
%{_libdir}/%{base_name}/Reader/JavaScripts
%{_libdir}/%{base_name}/Reader/Legal
%{_libdir}/%{base_name}/Reader/Tracker
%{_libdir}/%{base_name}/Reader/PDFSigQFormalRep.pdf
%{_libdir}/%{base_name}/Reader/pmd.cer
%{_libdir}/%{base_name}/Reader/%{platform}/mozilla
%dir %{_libdir}/%{base_name}/Reader/%{platform}
%dir %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins
%dir %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/Multimedia
%dir %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins3d
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/SPPlugins
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/bin
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/lib
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/*.api
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins3d/*.x3d
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/Multimedia/MPP
%{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/AcroForm
%{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/Annotations
%{_libdir}/%{base_name}/Reader/%{platform}/plug_ins3d/prc
%{_libdir}/%{base_name}/Resource
%dir %{_libdir}/%{base_name}/bin
%attr(755,root,root) %{_libdir}/%{base_name}/bin/acroread
%{_desktopdir}/acroread.desktop
%{_pixmapsdir}/acroread.png

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/nppdf.so
%endif
