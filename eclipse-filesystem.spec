%{?scl:%scl_package eclipse-filesystem}
%{!?scl:%global pkg_name %{name}}

%global debug_package %{nil}

Name:           %{?scl_prefix}eclipse-filesystem
Version:        1.0
Release:        3.3%{?dist}
Summary:        Eclipse Platform Filesystem Layout
License:        EPL
URL:            http://www.eclipse.org/

# javapackages-tools defines %%{_javaconfdir} macro and owns that directory
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
Requires:       %{?scl_prefix_java_common}javapackages-tools

%{?scl:Requires: %scl_runtime}

%description
This package provides directories needed by the Eclipse platform and other
Eclipse plug-ins. This is abstracted out of the main Eclipse package due to
the need to build some Eclipse plug-ins before the Eclipse platform itself
without introducing circular dependencies.

%prep
%setup -q -c -T

%build
# Generate Eclipse configuration file
cat <<EOF >eclipse.conf
# Eclipse platform root directory
eclipse.root=%{_libdir}/eclipse
# Location of architecture-independant dropins
eclipse.dropins.noarch=%{_datadir}/eclipse/dropins
# Location of architecture-dependant dropins
eclipse.dropins.archful=%{_libdir}/eclipse/dropins
# Comma-separated list of directories searched for external bundles
eclipse.bundles=%{_javadir},%{_jnidir},%{_javadir}-1.8.0,%{_jnidir}-1.8.0,%{_javadir}-1.7.0,%{_jnidir}-1.7.0,%{_javadir}-1.6.0,%{_jnidir}-1.6.0,%{_javadir}-1.5.0,%{_jnidir}-1.5.0
# Software collection ID (empty if not SCL)
scl.namespace=%{?scl}
# Software collection root directory (empty if not SCL)
scl.root=%{?_scl_root}
EOF

# Generate Eclipse configuration file for the base
cat <<EOF >eclipse-base.conf
# Comma-separated list of directories searched for external bundles
eclipse.bundles=%{_root_datadir}/java
# Software collection ID (empty if not SCL)
scl.namespace=
# Software collection root directory (empty if not SCL)
scl.root=
EOF

%install
# Platform bundles
install -m 755 -d %{buildroot}%{_libdir}/eclipse/features
install -m 755 -d %{buildroot}%{_libdir}/eclipse/plugins
# Archful dropins
install -m 755 -d %{buildroot}%{_libdir}/eclipse/dropins
# Noarch dropins
install -m 755 -d %{buildroot}%{_datadir}/eclipse/dropins
# eclipse.conf
install -m 755 -d %{buildroot}%{_javaconfdir}
install -m 755 -d %{buildroot}%{_root_sysconfdir}/java
install -m 644 -p eclipse.conf %{buildroot}%{_javaconfdir}/
install -m 644 -p eclipse-base.conf %{buildroot}%{_root_sysconfdir}/java/eclipse.conf

%files
%dir %{_libdir}/eclipse
%dir %{_libdir}/eclipse/features
%dir %{_libdir}/eclipse/plugins
%dir %{_libdir}/eclipse/dropins
%dir %{_datadir}/eclipse
%dir %{_datadir}/eclipse/dropins
%config(noreplace) %{_javaconfdir}/eclipse.conf
%config(noreplace) %{_root_sysconfdir}/java/eclipse.conf

%changelog
* Mon Jan 12 2015 Mat Booth <mat.booth@redhat.com> - 1.0-3.3
- Related: rhbz#1175105 - rebuilt

* Sat Jan 10 2015 Roland Grunberg <rgrunber@redhat.com> - 1.0-3.2
- Provide eclipse.conf for the base.
- Related: rhbz#1175105

* Mon Jan 05 2015 Mat Booth <mat.booth@redhat.com> - 1.0-3.1
- Resolves: rhbz#1175105 - Initial import into DTS 3.1

* Fri Nov 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-3
- Generate and install eclipse.conf

* Mon Sep 08 2014 Mat Booth <mat.booth@redhat.com> - 1.0-2
- Suppress debuginfo package generation

* Tue Aug 26 2014 Mat Booth <mat.booth@redhat.com> - 1.0-1
- Initial package
