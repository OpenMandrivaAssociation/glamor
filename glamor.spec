%define	major		0
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname -d %{name}

%define git			0
%define gitdate		20130313
%define	rel			1
%if %{git}
%define srctype		tar.gz
%define	release		0.git%{gitdate}.%{rel}
%else
%define srctype		tar.gz
%define release		1
%endif

# Otherwise it fails linking
%define	_disable_ld_no_undefined	1

Name:		glamor
Version:	0.5.1
Release:	%{release}
Summary:	Open-source X.org graphics common driver based on the GL library
License:	MIT
Group:		System/Libraries
Url:		http://www.freedesktop.org/wiki/Software/Glamor
%if %{git}
Source0:	%{name}-%{gitdate}.%{srctype}
%else
Source0:	%{name}-%{version}.%{srctype}
%endif
BuildRequires:	autoconf			>= 2.63
BuildRequires:	x11-util-macros		>= 1.17
BuildRequires:	x11-proto-devel		>= 7.6
BuildRequires:	pkgconfig(pixman-1)	>= 0.29.2
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(libdrm)	>= 2.4.42
BuildRequires:	pkgconfig(xorg-server)


%description
The %{name} module is an open-source 2D graphics common driver for the
X-Window System as implemented by X.org. It supports a variety of graphics
chipsets which have OpenGL/EGL/GBM supports.
It?s a GL-based rendering acceleration library for X server:
  * it uses GL functions and shader to complete the 2D graphics operations;
  * it uses normal texture to represent a drawable pixmap if possible;
  * it calls GL functions to render to the texture directly.
It?s somehow hardware independently and could be a building block of any X
server?s DDX driver; a such driver could leverage %{name}-egl package to create
an egl context without any native X system.
At the present the intel video driver use %{name} as one of its acceleration
options: when you build it with --enable-glamor, then it will use it as its
rendering engine. The %{name} package is also needed by the xf86-video-ati
driver to support newer video cards based on the Souhtern Island (SI)
chip-sets.

This package can be used on every platform which has both OpenGL support and
the libgbm and libdrm libraries installed.


%package -n %{libname}
Summary:	Open-source X.org graphics common driver based on the GL library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
The %{name} module is an open-source 2D graphics common driver for the
X-Window System as implemented by X.org. This package contains the main
library.


%package -n %{develname}
Summary:	Development files for %{libname}
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
The glamor module is an open-source 2D graphics common driver for the X
Window System as implemented by X.org. This package contains the
development files for %{libname}.


%prep
%if %{git}
%setup -qn %{name}-%{gitdate}
%else
%setup -qn %{name}-%{version}
%endif
autoreconf -vfi
#./autogen.sh


%build
# Other configure options
# --enable-glamor-gles2: build glamor over GLESv2 (default: no) - alternative to build over GL
# --enable-debug: build debug version of glamor (default: no)
# --enable-glx-tls: enable TLS support in GLX (default: no)
# --with-xorg-module-dir="%%{libdir}/xorg/modules"
%configure2_5x	--disable-static \
				--enable-glx-tls \
				--with-xorg-conf-dir="%{_sysconfdir}/X11/xorg.conf.d"

%make


%install
%makeinstall_std 
mv %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/glamor.conf %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/05-glamor.conf

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
cat <<EOF >%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_libdir}/xorg/modules
EOF

# Remove .la libraires
find %{buildroot} -name '*.la' -exec rm {} \;


%files
%doc COPYING
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/05-glamor.conf


%files -n %{libname}
%doc COPYING README ReleaseNote
%{_libdir}/libglamor.so.%{major}*
%{_libdir}/xorg/modules/libglamoregl.so


%files -n %{develname}
%doc COPYING
%{_libdir}/libglamor.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-egl.pc
%{_includedir}/xorg/glamor.h


