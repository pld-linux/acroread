Summary:	Acrobat Reader
Summary(pl):	Acrobat Reader - czytnik plików PDF
Summary(ru):	ðÒÏÇÒÁÍÍÁ ÄÌÑ ÞÔÅÎÉÑ ÄÏËÕÍÅÎÔÏ× × ÆÏÒÍÁÔÅ PDF ÏÔ Adobe
Summary(uk):	ðÒÏÇÒÁÍÁ ÄÌÑ ÞÉÔÁÎÎÑ ÄÏËÕÍÅÎÔ¦× Õ ÆÏÒÍÁÔ¦ PDF ×¦Ä Adobe
Name:		acroread
Version:	405
Release:	3
License:	distributable
Group:		X11/Applications/Graphics
Group(cs):	X11/Aplikace/Grafika
Group(da):	X11/Programmer/Grafik
Group(de):	X11/Applikationen/Grafik
Group(es):	X11/Aplicaciones/Gráficos
Group(fr):	X11/Applications/Graphiques
Group(id):	X11/Aplikasi/Grafik
Group(is):	X11/Forrit/Myndvinnsla
Group(it):	X11/Applicazioni/Immagini
Group(ja):	X11/¥¢¥×¥ê¥±¡¼¥·¥ç¥ó/¥°¥é¥Õ¥£¥Ã¥¯¥¹
Group(no):	X11/Applikasjoner/Grafikk
Group(pl):	X11/Aplikacje/Grafika
Group(pt):	X11/Aplicações/Gráficos
Group(ru):	X11/ðÒÉÌÏÖÅÎÉÑ/çÒÁÆÉËÁ
Group(sl):	X11/Programi/Grafika
Group(sv):	X11/Tillämpningar/Grafik
Group(uk):	X11/ðÒÉËÌÁÄÎ¦ ðÒÏÇÒÁÍÉ/çÒÁÆ¦ËÁ
Source0:	ftp://ftp.adobe.com/pub/adobe/acrobatreader/unix/4.x/linux-ar-%{version}.tar.gz
Patch0:		%{name}-locale.patch
%define		platform		intellinux
%define		sourcedir		ILINXR.install
%define		tar0			ILINXR.TAR
%define		tar1			READ.TAR
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Adobe AcrobatReader - pdf browser.

%description -l pl
Oryginalny program firmy Adobe do przegl±dania plików .pdf.

%description -l ru
ðÒÏÇÒÁÍÍÁ ÄÌÑ ÞÔÅÎÉÑ ÄÏËÕÍÅÎÔÏ× × ÆÏÒÍÁÔÅ Portable Document Format
(PDF), ÓÇÅÎÅÒÉÒÏ×ÁÎÎÙÈ Adobe Acrobat'ÏÍ.

%description -l uk
ðÒÏÇÒÁÍÁ ÄÌÑ ÞÉÔÁÎÎÑ ÄÏËÕÍÅÎÔ¦× Õ ÆÏÒÍÁÔ¦ Portable Document Format
(PDF), ÚÇÅÎÅÒÏ×ÁÎÉÈ Adobe Acrobat'ÏÍ.

%prep
%setup -q -n %{sourcedir}
tar xfv %{tar0}
tar xfv %{tar1}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}

cp -a Browsers Reader Resource $RPM_BUILD_ROOT%{_libdir}/%{name}
awk -v INSTDIR=%{_libdir}/%{name}/Reader \
	'/^install_dir=/ {print "install_dir="INSTDIR ; next} \
	 {print}' \
	bin/%{name}.sh > $RPM_BUILD_ROOT%{_bindir}/%{name}

gzip -9nf LICREAD.TXT INSTGUID.TXT ReadMe

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICREAD.TXT.gz INSTGUID.TXT.gz ReadMe.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/Browsers
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
