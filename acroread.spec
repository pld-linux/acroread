Summary:	Acrobatreader
Summary(pl):	Acrobatreader
Name:		acroread
Version:	405
Release:	1
Copyright:	distributable
Group:          X11/Applications/Graphics
Group(pl):      X11/Aplikacje/Grafika
Source:		ftp://ftp.adobe.com/pub/adobe/acrobatreader/unix/4.x/linux-ar-%{version}.tar.gz
%define		platform		intellinux
%define		sourcedir		ILINXR.install
%define		tar0			ILINXR.TAR
%define		tar1			READ.TAR
Exclusivearch:  %{ix86}
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Adobe Acrobatreader - pdf browser

%description -l pl
Oryginalny program firmy Adobe do przegl±dania plików .pdf

%prep
%setup -q -n %{sourcedir}
tar xfv %{tar0}
tar xfv %{tar1}

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
