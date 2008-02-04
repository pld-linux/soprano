# TODO
# - missing deps:
#   * Sesame2 storage backend (java-based)
#   * Raptor RDF serializer
#   * The CLucene-based full-text search index library
#
# Conditional build:
%bcond_without	serializer		# with raptor serializer. need to figure out proper BR

Summary:	Soprano - Qt wrapper API to librdf
Summary(pl.UTF-8):	Soprano - wrapper Qt do librdf
Name:		soprano
Version:	2.0.0
Release:	1
#Release:	0.%{_snap}.%{rel}
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/soprano/%{name}-%{version}.tar.bz2
# Source0-md5:	597d83ac793fff2ddbd628eb05d31624
URL:		http://sourceforge.net/projects/soprano
BuildRequires:	QtDBus-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtTest-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clucene-core-devel
BuildRequires:	cmake
BuildRequires:	libraptor-devel
BuildRequires:	qt4-build >= 4.3.3-3
BuildRequires:	qt4-qmake >= 4.3.3-3
BuildRequires:	rasqal-devel
BuildRequires:	redland-devel >= 1.0.6
BuildRequires:	rpmbuild(macros) >= 1.293
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Soprano (formally known as QRDF) is a library which provides a Qt
wrapper API to different RDF storage solutions. It features named
graphs (contexts) and has a modular plug-in structure which allows to
use different RDF storage implementations.

%description -l pl.UTF-8
Soprano (wcześniej znane jako QRDF) to biblioteka udostępniająca API
wrappera Qt do różnych rozwiązań przechowywania danych RDF. Obsługuje
nazwane grafy (konteksty) i ma strukturę modularnych wtyczek, co
pozwala na używanie różnych implementacji przechowywania danych RDF.

%package devel
Summary:	Header files for soprano
Summary(pl.UTF-8):	Pliki nagłówkowe dla soprano
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for soprano.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla soprano.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_VERBOSE_MAKEFILE=1 \
	-DQT_QMAKE_EXECUTABLE=%{_bindir}/qmake-qt4 \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sopranocmd
%attr(755,root,root) %{_bindir}/sopranod
%attr(755,root,root) %{_libdir}/libsoprano.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsoprano.so.4
%attr(755,root,root) %{_libdir}/libsopranoclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsopranoclient.so.1
%attr(755,root,root) %{_libdir}/libsopranoserver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsopranoserver.so.1
%dir %{_libdir}/soprano
%attr(755,root,root) %{_libdir}/soprano/libsoprano_redlandbackend.so
%attr(755,root,root) %{_libdir}/soprano/libsoprano_nquadparser.so
%attr(755,root,root) %{_libdir}/soprano/libsoprano_nquadserializer.so
%attr(755,root,root) %{_libdir}/soprano/libsoprano_raptorparser.so
%{?with_serializer:%attr(755,root,root) %{_libdir}/soprano/libsoprano_raptorserializer.so}
%{_datadir}/soprano
%dir %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/org.soprano.Model.xml
%{_datadir}/dbus-1/interfaces/org.soprano.NodeIterator.xml
%{_datadir}/dbus-1/interfaces/org.soprano.QueryResultIterator.xml
%{_datadir}/dbus-1/interfaces/org.soprano.Server.xml
%{_datadir}/dbus-1/interfaces/org.soprano.StatementIterator.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsoprano.so
%attr(755,root,root) %{_libdir}/libsopranoserver.so
%attr(755,root,root) %{_libdir}/libsopranoclient.so
%dir %{_includedir}/soprano
%{_includedir}/soprano/*.h
%{_includedir}/Soprano
%{_pkgconfigdir}/soprano.pc
