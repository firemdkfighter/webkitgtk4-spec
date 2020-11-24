Name:           webkitgtk4
Version:        2.30.2
Release:        1%{?dist}
Summary:        GTK+ Web content engine library

Group:          Development/Libraries
License:        LGPLv2+ and BSD
URL:            http://www.webkitgtk.org

Source0:        https://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz

BuildRequires: gobject-introspection-devel gtk3-devel mesa-libGL-devel
BuildRequires: ruby gperf bison flex cmake openjpeg2-devel ninja-build
BuildRequires: libwebp-devel libxml2-devel libXt-devel libsoup-devel
BuildRequires: libsecret-devel libxslt-devel geoclue2-devel perl-JSON-PP
BuildRequires: gstreamer1-plugins-base-devel rubygem-json clang libgcrypt-devel
BuildRequires: libtasn1-devel enchant-devel libnotify-devel libjpeg-turbo-devel

Requires:       enchant
Requires:       geoclue2
Requires:       gstreamer1-plugins-base
Requires:       gtk3
Requires:       harfbuzz-icu
Requires:       libgl
Requires:       libsecret
Requires:       libwebp
Requires:       libxslt
Requires:       libXt
Requires:       libnotify


%description
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

This package contains WebKitGTK+ for GTK+ 3.

%prep
%setup -qn "webkitgtk-%{version}"


%build
mkdir -vp build &&
cd        build &&

cmake -DCMAKE_BUILD_TYPE=Release  \
      -DCMAKE_INSTALL_PREFIX=%{buildroot} \
      -DCMAKE_SKIP_RPATH=ON       \
      -DPORT=GTK                  \
      -DLIB_INSTALL_DIR=%{buildroot}%{_libdir}  \
      -DUSE_LIBHYPHEN=OFF         \
      -DENABLE_MINIBROWSER=ON     \
      -DUSE_WOFF2=OFF             \
      -DUSE_WPE_RENDERER=OFF      \
      -DUSE_SYSTEMD=OFF           \
      -DENABLE_BUBBLEWRAP_SANDBOX=OFF \
      -Wno-dev -G Ninja ..
ninja

%install
ninja install

install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -m 755 Programs/GtkLauncher %{buildroot}%{_libexecdir}/%{name}

# Remove lib64 rpaths
chrpath --delete %{buildroot}%{_bindir}/jsc-4
chrpath --delete %{buildroot}%{_libdir}/libwebkitgtk-4.0.so
chrpath --delete %{buildroot}%{_libexecdir}/%{name}/GtkLauncher

# Remove .la files
find $RPM_BUILD_ROOT%{_libdir} -name "*.la" -delete

ln -s  %{buildroot}%{_libdir}/libwebkitgtk-4.0.so  %{buildroot}%{_libdir}/libwebkitgtk-3.0.so

## Finally, copy over and rename the various files for %%doc inclusion.
%add_to_doc_files Source/WebKit/LICENSE
%add_to_doc_files Source/WebKit/gtk/NEWS
%add_to_doc_files Source/WebCore/icu/LICENSE
%add_to_doc_files Source/WebCore/LICENSE-APPLE
%add_to_doc_files Source/WebCore/LICENSE-LGPL-2
%add_to_doc_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_doc_files Source/JavaScriptCore/COPYING.LIB
%add_to_doc_files Source/JavaScriptCore/THANKS
%add_to_doc_files Source/JavaScriptCore/AUTHORS
%add_to_doc_files Source/JavaScriptCore/icu/README
%add_to_doc_files Source/JavaScriptCore/icu/LICENSE

%files
%doc %{_pkgdocdir}/
%{_libdir}/libwebkitgtk-4.0.so.*
%{_libdir}/libjavascriptcoregtk-4.0.so.*
%{_libdir}/girepository-1.0/WebKit-4.0.typelib
%{_libdir}/girepository-1.0/JavaScriptCore-4.0.typelib
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/GtkLauncher
%{_datadir}/webkitgtk-4.0
%{_bindir}/jsc-3
%{_includedir}/webkitgtk-4.0
%{_libdir}/libwebkitgtk-4.0.so
%{_libdir}/libjavascriptcoregtk-4.0.so
%{_libdir}/pkgconfig/webkitgtk-4.0.pc
%{_libdir}/pkgconfig/javascriptcoregtk-4.0.pc
%{_datadir}/gir-1.0/WebKit-4.0.gir
%{_datadir}/gir-1.0/JavaScriptCore-4.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/webkitgtk
%{_datadir}/gtk-doc/html/webkitdomgtk
