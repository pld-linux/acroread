Summary:	Acrobat Reader
Summary(pl):	Acrobat Reader - czytnik plik�w PDF
Summary(ru):	��������� ��� ������ ���������� � ������� PDF �� Adobe
Summary(uk):	�������� ��� ������� �������Ԧ� � �����Ԧ PDF צ� Adobe
Name:		acroread
Version:	505
Release:	1
License:	distributable
Group:		X11/Applications/Graphics
Source0:	ftp://ftp.adobe.com/pub/adobe/acrobatreader/unix/5.x/linux-%{version}.tar.gz
Patch0:		%{name}-locale.patch
%define		platform		intellinux
%define		tar0			LINUXRDR.TAR
%define		tar1			COMMON.TAR

Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Adobe AcrobatReader - pdf browser.

%description -l pl
Oryginalny program firmy Adobe do przegl�dania plik�w .pdf.

%description -l ru
��������� ��� ������ ���������� � ������� Portable Document Format
(PDF), ��������������� Adobe Acrobat'��.

%description -l uk
�������� ��� ������� �������Ԧ� � �����Ԧ Portable Document Format
(PDF), ������������ Adobe Acrobat'��.

%package -n mozilla-plugin-%{name}
Summary:	Mozilla PDF plugin
Summary(pl):	Wtyczka PDF do Mozilli
Group:		X11/Applications
Requires:	%{name} = %{version}
Prereq:		mozilla-embedded

%description -n mozilla-plugin-%{name}
A Mozilla plugin for displaying Acrobat PDF files.

%description -n mozilla-plugin-%{name} -l pl
Wtyczka Mozilli dla wy�wietlania plik�w Acrobat PDF.

%prep
%setup -q -c
tar xfv %{tar0}
tar xfv %{tar1}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/{%{name},mozilla/plugins}

cp -a Reader Resource $RPM_BUILD_ROOT%{_libdir}/%{name}
awk -v INSTDIR=%{_libdir}/%{name}/Reader \
	'/^install_dir=/ {print "install_dir="INSTDIR ; next} \
	 {print}' \
	bin/%{name}.sh > $RPM_BUILD_ROOT%{_bindir}/%{name}
cp Browsers/intellinux/* $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins

gzip -9nf LICREAD.TXT README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
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

%files -n mozilla-plugin-%{name}
%defattr(644,root,root,755)
%{_libdir}/mozilla/plugins/*
