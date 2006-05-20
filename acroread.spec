#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
%define		base_name	acroread
Summary:	Acrobat Reader
Summary(pl):	Acrobat Reader - czytnik plików PDF
Summary(ru):	ðÒÏÇÒÁÍÍÁ ÄÌÑ ÞÔÅÎÉÑ ÄÏËÕÍÅÎÔÏ× × ÆÏÒÍÁÔÅ PDF ÏÔ Adobe
Summary(uk):	ðÒÏÇÒÁÍÁ ÄÌÑ ÞÉÔÁÎÎÑ ÄÏËÕÍÅÎÔ¦× Õ ÆÏÒÍÁÔ¦ PDF ×¦Ä Adobe
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
%define	_rel	4
Version:	7.0.5
Release:	%{_rel}%{?with_license_agreement:wla}
Epoch:		1
License:	distribution restricted (http://www.adobe.com/products/acrobat/distribute.html)
# in short:
# - not distributable on public sites (only linking to adobe.com permitted)
# - distribution on CD requires signing Distribution Agreement (see URL above)
Group:		X11/Applications/Graphics
%if %{with license_agreement}
Source0:	http://ardownload.adobe.com/pub/adobe/reader/unix/7x/7.0.5/enu/AdobeReader_enu-%{version}-1.i386.tar.gz
%else
Source0:	license-installer.sh
%endif
# please update @COPYSOURCES@ below if you add more Sources.
Source1:	%{base_name}.desktop
Source2:	%{base_name}.png
URL:		http://www.adobe.com/products/acrobat/
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.236
Requires:	openldap-libs >= 2.3
%else
Requires:	rpm-build-tools
%endif
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins

# TODO: galeon and skipstone, konqueror, opera.
# use macro, otherwise extra LF inserted along with the ifarch
%define	browsers mozilla, mozilla-firefox

%define		platform	intellinux
%define		tar0		ILINXR.TAR
%define		tar1		COMMON.TAR

%define		_noautostrip	.*\.api
%define		_noautoreq	'^lib.*\.so$' '^lib.*\(VERSION\)$'

%description
Adobe(R) Reader(R) is free software that lets you view and print PDF
files (Portable Document Format) on a variety of hardware and
operating system platforms.

%description -l pl
Adobe(R) Reader(R) jest darmowym oprogramowaniem umo¿liwiaj±cym
ogl±danie oraz drukowanie plików PDF (Portable Document Format) na
ró¿nych platformach sprzêtowych oraz ró¿nych systemach operacyjnych.

%description -l ru
ðÒÏÇÒÁÍÍÁ ÄÌÑ ÞÔÅÎÉÑ ÄÏËÕÍÅÎÔÏ× × ÆÏÒÍÁÔÅ Portable Document Format
(PDF), ÓÇÅÎÅÒÉÒÏ×ÁÎÎÙÈ Adobe Acrobat'ÏÍ.

%description -l uk
ðÒÏÇÒÁÍÁ ÄÌÑ ÞÉÔÁÎÎÑ ÄÏËÕÍÅÎÔ¦× Õ ÆÏÒÍÁÔ¦ Portable Document Format
(PDF), ÚÇÅÎÅÒÏ×ÁÎÉÈ Adobe Acrobat'ÏÍ.

%package plugin
Summary:	PDF plugin for Mozilla compatible browsers
Summary(pl):	Wtyczka PDF dla przegl±darek zgodnych Mozilla
Group:		X11/Applications
Requires:	%{base_name} = %{epoch}:%{version}-%{release}
Requires:	browser-plugins(%{_target_cpu})
Requires:	mozilla-embedded
Obsoletes:	mozilla-plugin-acroread

%description plugin
A Mozilla plugin for displaying PDF (Portable Document Format) files.

%description plugin -l pl
Wtyczka Mozilli do wy¶wietlania plików PDF (Portable Document Format).

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
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{base_name},%{_plugindir}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

cd AdobeReader
cp -a Reader Resource $RPM_BUILD_ROOT%{_libdir}/%{base_name}
awk -v INSTDIR=%{_libdir}/%{base_name}/Reader \
	'/^install_dir=/ {print "install_dir="INSTDIR; next} \
	{print}' \
	bin/%{base_name} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}
install Browser/%{platform}/* $RPM_BUILD_ROOT%{_plugindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/Patch

ln -sf /usr/lib/liblber-2.3.so.0 $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/%{platform}/lib/liblber.so
ln -sf /usr/lib/libldap-2.3.so.0 $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/%{platform}/lib/libldap.so
ln -sf /usr/share/ssl/ca-bundle.crt $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/Cert/curl-ca-bundle.crt

chmod a-x $RPM_BUILD_ROOT%{_libdir}/%{base_name}/Reader/%{platform}/lib/*.so.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
%post
%{_bindir}/%{base_name}.install

%else

%triggerin plugin -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins nppdf.so

%triggerun plugin -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins nppdf.so

%triggerin plugin -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins nppdf.so

%triggerun plugin -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins nppdf.so

# % triggerin plugin -- konqueror
# % nsplugin_install -d %{_libdir}/kde3/plugins/konqueror nppdf.so

# % triggerun plugin -- konqueror
# % nsplugin_uninstall -d %{_libdir}/kde3/plugins/konqueror nppdf.so

# % triggerin plugin -- opera
# % nsplugin_install -d %{_libdir}/opera/plugins nppdf.so

# % triggerun plugin -- opera
# % nsplugin_uninstall -d %{_libdir}/opera/plugins nppdf.so

# as rpm removes the old obsoleted package files after the triggers
# above are ran, add another trigger to make the links there.
%triggerpostun plugin -- mozilla-plugin-acroread
%nsplugin_install -f -d %{_libdir}/mozilla/plugins nppdf.so

%endif

%files
%defattr(644,root,root,755)
%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%doc AdobeReader/{LICREAD.TXT,ReadMe.htm}
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{base_name}
%{_libdir}/%{base_name}/Resource
%dir %{_libdir}/%{base_name}/Reader
%{_libdir}/%{base_name}/Reader/help
%{_libdir}/%{base_name}/Reader/AcroVersion
%{_libdir}/%{base_name}/Reader/Cert
%{_libdir}/%{base_name}/Reader/GlobalPrefs
%{_libdir}/%{base_name}/Reader/HowTo
%{_libdir}/%{base_name}/Reader/Legal
%{_libdir}/%{base_name}/Reader/JavaScripts
%{_libdir}/%{base_name}/Reader/Messages
%{_libdir}/%{base_name}/Reader/WebSearch
%dir %{_libdir}/%{base_name}/Reader/%{platform}
%dir %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/SPPlugins
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/bin
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/lib
%attr(755,root,root) %{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/*.api
%{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/AcroForm
%{_libdir}/%{base_name}/Reader/%{platform}/plug_ins/Annotations
%{_libdir}/%{base_name}/Reader/%{platform}/res
%{_desktopdir}/acroread.desktop
%{_pixmapsdir}/*

%files plugin
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/*
%endif
