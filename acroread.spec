Summary:	Acrobat Reader
Summary(pl):	Acrobat Reader - czytnik plikСw PDF
Summary(ru):	Программа для чтения документов в формате PDF от Adobe
Summary(uk):	Програма для читання документ╕в у формат╕ PDF в╕д Adobe
Name:		acroread
Version:	507
Release:	1
License:	distributable
Group:		X11/Applications/Graphics
Source0:	ftp://ftp.adobe.com/pub/adobe/acrobatreader/unix/5.x/linux-%{version}.tar.gz
# Source0-md5:	25f0ab387ebed3bf63ca24962ffcf9fa
Source1:	%{name}.desktop
Patch0:		%{name}-locale.patch
URL:		http://www.adobe.com/products/acrobat/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozdir		%{_libdir}/mozilla/plugins

%define		platform	intellinux
%define		tar0		LINUXRDR.TAR
%define		tar1		COMMON.TAR

%description
Adobe Acrobat Reader - pdf browser.

%description -l pl
Oryginalny program firmy Adobe do przegl╠dania plikСw .pdf.

%description -l ru
Программа для чтения документов в формате Portable Document Format
(PDF), сгенерированных Adobe Acrobat'ом.

%description -l uk
Програма для читання документ╕в у формат╕ Portable Document Format
(PDF), згенерованих Adobe Acrobat'ом.

%package -n mozilla-plugin-%{name}
Summary:	Mozilla PDF plugin
Summary(pl):	Wtyczka PDF do Mozilli
Group:		X11/Applications
Requires:	%{name} = %{version}
Prereq:		mozilla-embedded

%description -n mozilla-plugin-%{name}
A Mozilla plugin for displaying Acrobat PDF files.

%description -n mozilla-plugin-%{name} -l pl
Wtyczka Mozilli dla wy╤wietlania plikСw Acrobat PDF.

%prep
%setup -q -c
tar xfv %{tar0}
tar xfv %{tar1}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{mozdir},%{_applnkdir}/Graphics/Viewers}

cp -a Reader Resource $RPM_BUILD_ROOT%{_libdir}/%{name}
awk -v INSTDIR=%{_libdir}/%{name}/Reader \
	'/^install_dir=/ {print "install_dir="INSTDIR; next} \
	{print}' \
	bin/%{name}.sh > $RPM_BUILD_ROOT%{_bindir}/%{name}
install Browsers/intellinux/* $RPM_BUILD_ROOT%{mozdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Graphics/Viewers

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
%{_applnkdir}/Graphics/Viewers/*.desktop

%files -n mozilla-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{mozdir}/*
