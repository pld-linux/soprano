# TODO
# - missing deps:
#   * Sesame2 storage backend (java-based)
#   * Raptor RDF serializer
#
# Conditional build:
%bcond_without	serializer		# with raptor serializer. need to figure out proper BR
%bcond_without	sesame2			# with sesame2backend
%bcond_without	virtuoso		# with virtuosobackend

%define		qtbrver		4.6.0
%define		snap		svn1042011

Summary:	Soprano - Qt wrapper API to librdf
Summary(pl.UTF-8):	Soprano - wrapper Qt do librdf
Name:		soprano
Version:	2.3.70
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/sourceforge/soprano/%{name}-%{version}.tar.bz2
# Source0-md5:	de5cf230a95fc7218425aafdfb4a5e47
#Source0:	%{name}-%{version}-%{snap}.tar.gz
URL:		http://sourceforge.net/projects/soprano
BuildRequires:	QtCore-devel >= %{qtbrver}
BuildRequires:	QtDBus-devel >= %{qtbrver}
BuildRequires:	QtNetwork-devel >= %{qtbrver}
BuildRequires:	QtTest-devel >= %{qtbrver}
BuildRequires:	clucene-core-devel >= 0.9.16a-2
BuildRequires:	cmake >= 2.6.2
%{?with_sesame2:BuildRequires: libgcj-devel}
%{?with_serializer:BuildRequires:	libraptor-devel}
%{?with_virtuoso:BuildRequires:	libiodbc-devel}
BuildRequires:	qt4-build >= %{qtbrver}
BuildRequires:	qt4-qmake >= %{qtbrver}
BuildRequires:	rasqal-devel
BuildRequires:	redland-devel >= 1.0.6
BuildRequires:	rpmbuild(macros) >= 1.453
BuildConflicts:	java-sun
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Soprano (formally known as QRDF) is a library which provides a Qt
wrapper API to different RDF storage solutions. It features named
graphs (contexts) and has a modular plug-in structure which allows to
use different RDF storage implementations.

%description -l pl.UTF-8
Soprano (wcześniej znane jako QRDF) to biblioteka udostępniająca
API wrappera Qt do różnych rozwiązań przechowywania danych RDF.
Obsługuje nazwane grafy (konteksty) i ma strukturę modularnych
wtyczek, co pozwala na używanie różnych implementacji
przechowywania danych RDF.

%package devel
Summary:	Header files for soprano
Summary(pl.UTF-8):	Pliki nagłówkowe dla soprano
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for soprano.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla soprano.

%package plugin-virtuoso
Summary:	virtuoso plugin for soprano
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description plugin-virtuoso
Virtuoso plugin for soprano.

%prep
%setup -q
# Sesame2 backend doesn't really use the new JNI-1.6 feature -> GetObjectRefType.
#sed -i 's:JNI_VERSION_1_6:JNI_VERSION_1_4:g' CMakeLists.txt
# cleanup.
#sed -i 's:${JAVA_INCLUDE_PATH2}::' backends/sesame2/CMakeLists.txt

%build
install -d build
cd build
# add this to get verbose output
# -DCMAKE_VERBOSE_MAKEFILE=1
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DQT_QMAKE_EXECUTABLE=%{_bindir}/qmake-qt4 \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	-DJAVA_INCLUDE_PATH=%{_libdir}/gcc/%{_target_platform}/%{cc_version}/include \
	-DJAVA_INCLUDE_PATH2=%{_libdir}/gcc/%{_target_platform}/%{cc_version}/include \
%if "%{pld_release}" == "ti" 
	-DJAVA_JVM_LIBRARY=%{_libdir}/gcj-%{cc_version}-9/libjvm.so \
%else
	-DJAVA_JVM_LIBRARY=%{_libdir}/gcj-%{cc_version}-10/libjvm.so \
%endif
	../

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
%attr(755,root,root) %{_bindir}/onto2vocabularyclass
%attr(755,root,root) %{_libdir}/libsoprano.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsoprano.so.4
%attr(755,root,root) %{_libdir}/libsopranoclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsopranoclient.so.1
%attr(755,root,root) %{_libdir}/libsopranoserver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsopranoserver.so.1
%attr(755,root,root) %{_libdir}/libsopranoindex.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsopranoindex.so.1
%dir %{_libdir}/soprano
%attr(755,root,root) %{_libdir}/soprano/libsoprano_redlandbackend.so
%attr(755,root,root) %{_libdir}/soprano/libsoprano_nquadparser.so
%attr(755,root,root) %{_libdir}/soprano/libsoprano_nquadserializer.so
%attr(755,root,root) %{_libdir}/soprano/libsoprano_raptorparser.so
%{?with_sesame2:%attr(755,root,root) %{_libdir}/soprano/libsoprano_sesame2backend.so}
%{?with_serializer:%attr(755,root,root) %{_libdir}/soprano/libsoprano_raptorserializer.so}
%{_datadir}/soprano
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
%attr(755,root,root) %{_libdir}/libsopranoindex.so
%dir %{_includedir}/soprano
%{_includedir}/soprano/*.h
%{_includedir}/Soprano
%{_pkgconfigdir}/soprano.pc

%if %{with virtuoso}
%files plugin-virtuoso
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/soprano/libsoprano_virtuosobackend.so
%endif
