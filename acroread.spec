Summary:	Acrobat Reader
Summary(pl):	Acrobat Reader - czytnik plików PDF
Summary(ru):	ðÒÏÇÒÁÍÍÁ ÄÌÑ ÞÔÅÎÉÑ ÄÏËÕÍÅÎÔÏ× × ÆÏÒÍÁÔÅ PDF ÏÔ Adobe
Summary(uk):	ðÒÏÇÒÁÍÁ ÄÌÑ ÞÉÔÁÎÎÑ ÄÏËÕÍÅÎÔ¦× Õ ÆÏÒÍÁÔ¦ PDF ×¦Ä Adobe
Name:		acroread
Version:	509
Release:	1
License:	distribution restricted (http://www.adobe.com/products/acrobat/distribute.html)
# in short:
# - not distributable on public sites (only linking to adobe.com permitted)
# - distribution on CD requires signing Distribution Agreement (see URL above)
Group:		X11/Applications/Graphics
Source0:	ftp://ftp.adobe.com/pub/adobe/acrobatreader/unix/5.x/linux-%{version}.tar.gz
# NoSource0-md5:	53b7ca0fc83ab81214ba82050ce89c64
Source1:	%{name}.desktop
Source2:	%{name}.png
NoSource:	0
Patch0:		%{name}-locale.patch
URL:		http://www.adobe.com/products/acrobat/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozdir		%{_libdir}/mozilla/plugins

%define		platform	intellinux
%define		tar0		LINUXRDR.TAR
%define		tar1		COMMON.TAR

%define		_noautostrip	.*w.*\\.api

%description
Adobe(R) Reader(R) is free software that lets you view and print
PDF files (Portable Document Format) on a variety of hardware and
operating system platforms.

%description -l pl
Adobe(R) Reader(R) jest darmowym oprogramowaniem umo¿liwiaj±cym ogl±danie
oraz drukowanie plików PDF (Portable Document Format) na ró¿nych platformach
sprzêtowych oraz ró¿nych systemach operacyjnych.

%description -l ru
ðÒÏÇÒÁÍÍÁ ÄÌÑ ÞÔÅÎÉÑ ÄÏËÕÍÅÎÔÏ× × ÆÏÒÍÁÔÅ Portable Document Format
(PDF), ÓÇÅÎÅÒÉÒÏ×ÁÎÎÙÈ Adobe Acrobat'ÏÍ.

%description -l uk
ðÒÏÇÒÁÍÁ ÄÌÑ ÞÉÔÁÎÎÑ ÄÏËÕÍÅÎÔ¦× Õ ÆÏÒÍÁÔ¦ Portable Document Format
(PDF), ÚÇÅÎÅÒÏ×ÁÎÉÈ Adobe Acrobat'ÏÍ.

%package -n mozilla-plugin-%{name}
Summary:	Mozilla PDF plugin
Summary(pl):	Wtyczka PDF do Mozilli
Group:		X11/Applications
Prereq:		mozilla-embedded
Requires:	%{name} = %{version}

%description -n mozilla-plugin-%{name}
A Mozilla plugin for displaying PDF (Portable Document Format) files.

%description -n mozilla-plugin-%{name} -l pl
Wtyczka Mozilli do wy¶wietlania plików PDF (Portable Document Format).

%prep
%setup -q -c
tar xf %{tar0}
tar xf %{tar1}
#%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{mozdir}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

cp -a Reader Resource $RPM_BUILD_ROOT%{_libdir}/%{name}
awk -v INSTDIR=%{_libdir}/%{name}/Reader \
	'/^install_dir=/ {print "install_dir="INSTDIR; next} \
	{print}' \
	bin/%{name}.sh > $RPM_BUILD_ROOT%{_bindir}/%{name}
install Browsers/intellinux/* $RPM_BUILD_ROOT%{mozdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICREAD.TXT README
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/Resource

%dir %{_libdir}/%{name}/Reader
%{_libdir}/%{name}/Reader/help
%{_libdir}/%{name}/Reader/res
%{_libdir}/%{name}/Reader/AcroVersion
%{_libdir}/%{name}/Reader/*.pdf
%dir %{_libdir}/%{name}/Reader/%{platform}
%{_libdir}/%{name}/Reader/%{platform}/app-defaults
%{_libdir}/%{name}/Reader/%{platform}/fonts
%{_libdir}/%{name}/Reader/%{platform}/res
%attr(755,root,root) %{_libdir}/%{name}/Reader/%{platform}/plug_ins
%attr(755,root,root) %{_libdir}/%{name}/Reader/%{platform}/bin
%attr(755,root,root) %{_libdir}/%{name}/Reader/%{platform}/lib
%{_desktopdir}/acroread.desktop
%{_pixmapsdir}/*

%files -n mozilla-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{mozdir}/*
