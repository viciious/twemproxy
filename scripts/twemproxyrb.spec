Name: twemproxy
Version: 0.4.1.3rb
Release: 1%{?dist}
Summary: Fast and lightweight proxy for memcached and twemproxy protocols
Group: System Environment/Daemons
License: ASL 2.0
URL: https://github.com/viciious/twemproxy
Source0: https://github.com/viciious/twemproxy/archive/v%{version}.tar.gz
BuildRequires: autoconf, automake, libtool
BuildRequires: systemd-units
# FIXME : Uses bundled yaml-0.1.4 in contrib directory
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
twemproxy (pronounced "two-em-proxy"), aka nutcracker is a fast and
lightweight proxy for memcached and twemproxy protocol. It was built primarily
to reduce the number of connections to the caching servers on the backend.
This, together with protocol pipelining and sharding enables you to
horizontally scale your distributed caching architecture.


%define __logdir /var/log/%{name}/
%define __rundir /var/run/%{name}/

%prep
%setup -q

%build
autoreconf -fvi
%configure
make %{?_smp_mflags}


%install
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
echo "OPTIONS=-o /var/log/twemproxy/twemproxy.log -p /var/run/twemproxy/twemproxy.pid" > %{buildroot}%{_sysconfdir}/sysconfig/twemproxy
touch %{buildroot}%{_sysconfdir}/twemproxy.yml
mkdir -p %{buildroot}%{__logdir}
mkdir -p %{buildroot}%{__rundir}
install -p -D -m 0644 scripts/twemproxy.service %{buildroot}%{_unitdir}/twemproxy.service


%pre
getent group twemproxy &>/dev/null || \
groupadd -r twemproxy &>/dev/null
getent passwd twemproxy &>/dev/null || \
useradd -r -g twemproxy -d / -s /sbin/nologin \
  -c 'twemproxy' twemproxy &>/dev/null
exit 0

%post
%systemd_post twemproxy.service

%preun
%systemd_preun twemproxy.service

%postun
%systemd_postun_with_restart twemproxy.service


%files
%license LICENSE
%doc ChangeLog NOTICE README.md notes/
%ghost %config %{_sysconfdir}/twemproxy.yml
%config(noreplace) %{_sysconfdir}/sysconfig/twemproxy
%dir %attr(0755, twemproxy, twemproxy) %{__logdir}
%dir %attr(0755, twemproxy, twemproxy) %{__rundir}
%{_sbindir}/twemproxy
%{_mandir}/man8/twemproxy.8*
%{_unitdir}/twemproxy.service


%changelog
* Thu Jun 23 2016 Matthias Saou <matthias@saou.eu> 0.4.1-1
- Initial RPM release.

